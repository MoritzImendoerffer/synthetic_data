"""Version 2.0 annex builders, one module per document (``pcp_007.py`` builds ``PCP-007``).

``build_ground_truth.BUILDERS`` uses a module here in place of the builder in
``build_ground_truth.py`` as soon as the module exists. Each module defines ``build()``, which
returns the document's ``schema_ext.GroundTruthAnnex``, and imports the shared helpers from
``build_ground_truth`` (``ref``, ``row_quotes``, ``ctable_rows``, ``rev2_layer``, ...). One module
per document lets several documents be annexed in parallel without editing one shared file.
"""
