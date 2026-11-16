# Measurements of v.1.0.0, the TO Chip of 2026-11

| | |
| --- | --- |
| Chip | the template chip of branch [`IHP-TO-2026-11`][to-branch], 1.6 mm × 1.6 mm on SG13CMOS5L |
| Design source | commit [`ef8524f`][to-commit], from which release v.1.0.0 is built |
| Submission | [`SoC1693`][soc1693] in the IHP open MPW of November 2026, [issue 80][issue-80] of `IHP-GmbH/Open-Silicon-MPW` |
| GDS | `release/v.1.0.0/gds/chip_top_logo_fill.gds.gz` of `ef8524f`, SHA-256 `55acb3891aa4089f86c2497768746602b4807c198c65cfbe2c4d6f77c4b0ab7a`. IHP received it with the top cell renamed, as `SoC1693.gds.gz`, SHA-256 `74304160c8ee35d0cf98c567a8412c2110a7ff2b753dcf5ff24fe3bbd8e92978` |
| Package | QFN32 `OP_QFN32_A4_FIT`, pin numbers as in [`packaging/result.md`][bondplan] |
| Status | not measured |

The chip and its pads are described in [`doc/specifications.md`][spec] and [`doc/pinout.md`][pinout] of `ef8524f`. Each folder below is a placeholder: its tables list what to measure, the conditions and the simulated value to compare with, and its column `Measured` reads `TBD` until a result replaces it.


## Blocks

| Folder | Block | Package pins | Setup | Status |
| --- | --- | --- | --- | --- |
| [`chip/`](chip/) | die photo, pad check, quiescent supply currents | all | bare die, packaged | not measured |
| [`counters/`](counters/) | the three 8-bit counters behind `sel[1:0]` | 1 to 4, 7, 24 to 32 | packaged | not measured |
| [`inverter/`](inverter/) | quad inverter, channels 1 and 4 | 19 to 21, 25 | packaged | not measured |
| [`amplifier/`](amplifier/) | self-biased inverter amplifier | 17, 18 | packaged | not measured |
| [`ringosc/`](ringosc/) | three-stage ring oscillator | 22, 23 | packaged | not measured |
| [`vco/`](vco/) | 20 GHz LC VCO | 9 to 16 | on-wafer | not measured |


## Setups

- **Packaged:** the QFN32 on a PCB, for every block but the VCO's RF output. The digital pads switch at the `IOVDD` levels, 3.3 V.
- **On-wafer:** the VCO's 20 GHz output, because the bond wires of the package are 1.3 mm to 1.7 mm long. A GSSG probe of 100 µm pitch lands on the pads of pins 11 to 14. The die also needs `IOVDD`, `IOVSS`, `VDD` and `VSS` on the west side (pins 5 to 8) and `di_en`, `vtune` and `vdd_rf` on the south side (pins 9, 10 and 15).


## Operating Rules

From [`doc/specifications.md`][spec] of `ef8524f`:

- Bring up `IOVDD` first and `VDD` no later than `vdd_rf`: the pad diodes of `vdd_rf`, `vdd_ro`, `vdd_hv` and the RF pads conduct into an unpowered rail.
- Keep `vdd_hv` at or below 1.65 V, because the outputs of the IHP HV counter drive LV gates in the select multiplexer.
- Change `sel[1:0]` only with `rst_n` low or `clk` stopped.
- Measure the VCO with `VDD` and `vdd_rf` both at 1.5 V, so that `di_en` reaches 1.5 V. The ETH LV library is characterized up to 1.32 V only, so leave its counter deselected then.
- The ring oscillator has no enable, 0 V on `vdd_ro` turns it off.

[to-branch]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/tree/IHP-TO-2026-11
[to-commit]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/tree/ef8524f81b8355548f01540cfba7907767346396
[soc1693]: https://github.com/simi1505/IHP__SoC1693
[issue-80]: https://github.com/IHP-GmbH/Open-Silicon-MPW/issues/80
[bondplan]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/packaging/result.md
[spec]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/doc/specifications.md
[pinout]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/doc/pinout.md
