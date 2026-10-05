# MeasureBatch — native feasibility gate

This is an early, original synthetic test harness, not a finished app.

The proposed utility fills numeric slots in an anonymous Seamly `.smis` 0.3.4 template from explicitly mapped CSV columns while retaining formulas and all other template bytes. Native acceptance is a go/no-go gate before UI development.

CI fetches a checksum-pinned official Seamly release for testing only. No Seamly code, binary, schema, measurement database, illustration, or sample pattern is distributed here. The anonymous measurement and rectangular pattern fixtures are authored for this project.

The gate requires all three measurement files to open in SeamlyME, an invalid formula to fail, and an original rectangle consuming preserved formulas to export from Seamly2D at 22×25, 24.5×30, and 27.4×30.48 cm. XML acceptance alone is not success.

## Scope and provenance

- [Current CSV workflow friction](https://forum.seamly.io/t/excel-csv-import-for-custom-seamlyme-measurement-tables/17425)
- [Native schema reference](https://github.com/FashionFreedom/Seamly2D/blob/v2026.10.5.154/src/libs/ifc/schema/individual_size_measurements/v0.3.4.xsd)
- [Pinned test-only consumer](https://github.com/FashionFreedom/Seamly2D/releases/tag/v2026.10.5.154)

No fit, grading, body-inference or first-ever CSV-import claim is made. Valentina Tape already imports CSV, Seamly MCP already edits and validates measurement XML, and 3D Measure Up offers experimental VIT export. The intended difference is template-preserving batch fill, explicit mapping, protected formulas and exact conversion receipts.

All rights reserved. No open-source license has been granted for this original project. Upstream Seamly retains its own GPL licensing; it is neither bundled nor modified.
