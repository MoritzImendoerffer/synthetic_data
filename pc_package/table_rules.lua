--[[
table_rules.lua: the rules of the plain pipe tables (title block, approvals, revision history,
abbreviations, related documents, registers, df.to_markdown() tables) in a variant rendering pass.

The default pass never loads this filter. render_variant.py (make corpus-variant RULES=...) passes
it with --metadata-file table_rules.yml, which runs it after Quarto's own filters (post-render),
when a captioned table already carries its caption and its label. It reads the rules from the
environment variable PC_TABLE_RULES, the one switch of the pass (see ctable.py):

  rows   pandoc's booktabs rules stay, and a thin rule (\hline) runs under every row;
  grid   every cell ruled: | between and around the columns, \hline above, below and between
         every row (booktabs rules leave gaps in vertical rules, so they become \hline too).

Anything else leaves every table as it is. Only LaTeX output is touched; the DOCX takes its rules
from the reference document of the pass. A table is written by pandoc's own LaTeX writer and only
its rules are changed, so its cells, caption and label are what the default pass prints, and the
grounding text (read from the DOCX) cannot change. A table this filter cannot read with certainty
(a merged cell, or row ends it cannot count) is left as the default pass sets it, with a warning.
]]

local RULES = (os.getenv("PC_TABLE_RULES") or ""):lower()

local function warn(msg)
  io.stderr:write("table_rules.lua: " .. msg .. "\n")
end

-- a merged cell: a rule after every row would run through it, so such a table is left alone
local function has_spans(tbl)
  local function any_span(rows)
    for _, row in ipairs(rows) do
      for _, cell in ipairs(row.cells) do
        if cell.row_span > 1 or cell.col_span > 1 then return true end
      end
    end
    return false
  end
  if any_span(tbl.head.rows) or any_span(tbl.foot.rows) then return true end
  for _, body in ipairs(tbl.bodies) do
    if any_span(body.head) or any_span(body.body) then return true end
  end
  return false
end

local function body_row_count(tbl)
  local n = 0
  for _, body in ipairs(tbl.bodies) do n = n + #body.head + #body.body end
  return n
end

-- lines that end a table row ("... \\"); the caption line ends in \tabularnewline instead
local function is_row_end(line)
  return line:match("\\\\%s*$") ~= nil
end

-- a line after which no row rule belongs: a rule of its own, a head/foot marker, the end
local STOP = { "\\toprule", "\\midrule", "\\bottomrule", "\\hline", "\\cline", "\\cmidrule",
               "\\endhead", "\\endfirsthead", "\\endfoot", "\\endlastfoot", "\\end{longtable}" }
local function stops(line)
  if line == nil then return true end
  local s = line:match("^%s*(.-)%s*$")
  for _, p in ipairs(STOP) do
    if s:sub(1, #p) == p then return true end
  end
  return false
end

-- insert `rule` after every row that another row follows directly (header rows and body rows);
-- returns the new text and the number of row ends seen after \endlastfoot (the body rows)
local function rule_rows(tex, rule)
  local lines = {}
  for line in (tex .. "\n"):gmatch("(.-)\n") do lines[#lines + 1] = line end
  local out, in_body, body_rows = {}, false, 0
  for i, line in ipairs(lines) do
    out[#out + 1] = line
    if line:match("^%s*\\endlastfoot") then in_body = true end
    if is_row_end(line) then
      if in_body then body_rows = body_rows + 1 end
      local j = i + 1
      while lines[j] ~= nil and lines[j]:match("^%s*$") do j = j + 1 end
      if not stops(lines[j]) then out[#out + 1] = rule end
    end
  end
  -- (tex .. "\n") added one line break, and gmatch kept every line: join without the extra one
  return table.concat(out, "\n"), body_rows
end

-- the column spec for the grid: "|" between and around the columns, and the widths pandoc gave
-- for n columns between @{} reduced by the two outer paddings and the n + 1 rules, so the table
-- stays as wide as the line
local function grid_spec(spec, ncols)
  local s = spec:gsub("^%s*@{}", ""):gsub("@{}%s*$", "")
  local cols, i = {}, 1
  while i <= #s do
    local c = s:sub(i, i)
    if c:match("%s") then
      i = i + 1
    elseif c == ">" then
      local a, b = s:find("^>%b{}%s*[pmb]%b{}", i)
      if not a then return nil end
      cols[#cols + 1] = s:sub(a, b)
      i = b + 1
    elseif c:match("[pmb]") then
      local a, b = s:find("^[pmb]%b{}", i)
      if not a then return nil end
      cols[#cols + 1] = s:sub(a, b)
      i = b + 1
    elseif c:match("[lcr]") then
      cols[#cols + 1] = c
      i = i + 1
    else
      return nil
    end
  end
  if #cols ~= ncols then return nil end
  local reduce = "\\linewidth - " .. (2 * ncols) .. "\\tabcolsep - " .. (ncols + 1) .. "\\arrayrulewidth"
  for k, col in ipairs(cols) do
    local new, n = col:gsub("\\linewidth %- %d+\\tabcolsep", reduce)
    if n == 0 then new = col:gsub("\\linewidth", "(" .. reduce .. ")") end
    cols[k] = new
  end
  return "|" .. table.concat(cols, "|") .. "|"
end

local function grid(tex, ncols)
  local a, b, spec = tex:find("\\begin{longtable}%[%]%s*(%b{})")
  if not a then return nil, "no longtable column spec" end
  local new = grid_spec(spec:sub(2, -2), ncols)
  if not new then return nil, "column spec not understood: " .. spec end
  tex = tex:sub(1, a - 1) .. "\\begin{longtable}[]{" .. new .. "}" .. tex:sub(b + 1)
  -- booktabs rules leave gaps in vertical rules: \hline instead (pandoc writes "\toprule\noalign{}")
  for _, r in ipairs({ "toprule", "midrule", "bottomrule" }) do
    tex = tex:gsub("\\" .. r .. "\\noalign{}", "\\hline"):gsub("\\" .. r .. "%f[^%a]", "\\hline")
  end
  return tex
end

function Table(tbl)
  if RULES ~= "rows" and RULES ~= "grid" then return nil end
  if not FORMAT:match("latex") then return nil end
  local id = tbl.attr.identifier ~= "" and tbl.attr.identifier or "(no label)"
  if has_spans(tbl) then
    warn("table " .. id .. " has a merged cell; left with the default rules")
    return nil
  end
  local tex = pandoc.write(pandoc.Pandoc({ tbl }), "latex")
  if not tex:match("\\begin{longtable}") then
    warn("table " .. id .. " is not a longtable; left with the default rules")
    return nil
  end
  local err
  if RULES == "grid" then
    tex, err = grid(tex, #tbl.colspecs)
    if not tex then
      warn("table " .. id .. ": " .. err .. "; left with the default rules")
      return nil
    end
  end
  local ruled, n = rule_rows(tex, "\\hline")
  if n ~= body_row_count(tbl) then
    warn("table " .. id .. ": " .. n .. " row ends for " .. body_row_count(tbl)
         .. " body rows; left with the default rules")
    return nil
  end
  -- the table number of an uncaptioned table given back without an empty last row (table_rules.tex)
  local k = ruled:find("\\end{longtable}", 1, true)
  ruled = ruled:sub(1, k - 1) .. "\\ifdefined\\PCLTgiveback\\PCLTgiveback\\fi\n" .. ruled:sub(k)
  return pandoc.RawBlock("latex", ruled)
end
