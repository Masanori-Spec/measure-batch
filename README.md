# MeasureBatch — native feasibility gate

**NO-GO under the original acceptance criteria. This is a closed feasibility investigation and synthetic test harness, not a finished app. No product UI or CSV-conversion engine was built.**

The proposed utility would fill existing numeric slots in an anonymous Seamly `.smis` 0.3.4 template from explicit CSV mappings, while preserving formulas and every other template byte. Native verification was required before UI development.

## Verified outcome

[Hosted native run](https://github.com/Masanori-Spec/measure-batch/actions/runs/37300717757) tested commit `6243c058494653e944acfb6e19901ab3486a0565` with official Seamly `v2026.10.5.154`, checksum-pinned and run in an isolated Ubuntu 24.04 Xvfb display.

- All three synthetic measurement files opened successfully in SeamlyME `--test`
- Seamly2D exported the original rectangular pattern using the preserved formulas
- Measured unscaled SVG sides: A 220.0000665 × 250.0001956 mm; B 245.0001831 × 300.0003751 mm; C 273.9999374 × 304.8004163 mm
- Each geometry matched its handwritten expected dimensions within 0.08 mm
- **The mandatory negative failed:** a formula containing `@missing_dependency` also returned exit code 0 from SeamlyME `--test`

The overall workflow remains failed. A successful file-load exit code cannot be treated as proof that measurement formulas are valid. Positive geometry evidence does not override the failed negative control. Product development stopped at this gate; no fit or grading capability is claimed.

[Machine-readable evidence](native-report.json) contains the individual results and expected dimensions. The diagnostic harness records every geometry result before failing overall. It does not suppress or weaken the negative.

## Reproduce

Run the GitHub Actions workflow. It fetches the official AppImage for testing only, verifies SHA-256, checks runtime linkage, and invokes the native tools inside isolated Xvfb. The pinned CLI uses `--mfile` and `--exportOnlyDetails`; SVG format is discovered from native help. SeamlyME's version probe includes `--test` to avoid its first-run welcome dialog.

No Seamly source, binary, schema, measurement database, illustration, font, or sample pattern is distributed here. The anonymous measurement and rectangular pattern fixtures are original synthetic inputs. Row A expects 22 × 25 cm, B 24.5 × 30 cm, and C 27.4 × 30.48 cm after formula recomputation.

## Scope and provenance

- [Current CSV workflow friction](https://forum.seamly.io/t/excel-csv-import-for-custom-seamlyme-measurement-tables/17425)
- [Pinned native schema](https://github.com/FashionFreedom/Seamly2D/blob/v2026.10.5.154/src/libs/ifc/schema/individual_size_measurements/v0.3.4.xsd)
- [Pinned official release](https://github.com/FashionFreedom/Seamly2D/releases/tag/v2026.10.5.154)
- [Native formula evaluator](https://github.com/FashionFreedom/Seamly2D/blob/v2026.10.5.154/src/libs/vformat/measurements.cpp)

Valentina Tape already imports CSV, Seamly MCP already edits and validates measurement XML, and 3D Measure Up offers experimental VIT export. No first-ever-import claim is made. The proposed difference was template-preserving batch fill with explicit mapping, protected formulas and exact conversion receipts; those application features are not implemented in this feasibility repository.

All rights reserved. No open-source license has been granted for this original project. Upstream Seamly retains its own GPL licensing; it is neither bundled nor modified.
