# Chip Pinout

This document lists every bondpad of the chip together with the top-level `chip_top` port it is attached to and the role it plays inside the core. The padframe layout is **8 pads per side, 32 bondpads total**.

Order convention:
- `PAD_WEST` / `PAD_EAST`: **bottom → top**
- `PAD_NORTH` / `PAD_SOUTH`: **left → right**

Same convention as the four `PAD_*` lists in [config.yaml](../flow/librelane/config.yaml).

Related documents:
- Floorplan: [floorplan.md](floorplan.md)
- Specifications: [specifications.md](specifications.md)
- Package pin assignment and bond report: [packaging/result.md](../packaging/result.md)


## Top-level ports

Defined in [chip_top.sv](../rtl/chip_top.sv):

| Top-level port    | Direction | Width                 | Role                                            |
| ----------------- | --------- | --------------------- | ----------------------------------------------- |
| `IOVDD`           | inout     | 1                     | I/O supply (3.3 V), under `USE_POWER_PINS`      |
| `IOVSS`           | inout     | 1                     | I/O ground, under `USE_POWER_PINS`              |
| `VDD`             | inout     | 1                     | Core supply (1.2 V), under `USE_POWER_PINS`     |
| `VSS`             | inout     | 1                     | Core ground, under `USE_POWER_PINS`             |
| `clk_PAD`         | inout     | 1                     | main clock                                      |
| `rst_n_PAD`       | inout     | 1                     | active-low reset                                |
| `input_PAD[2:0]`  | inout     | `NUM_INPUT_PADS=3`    | `sel[1:0]` counter select, `di_en` VCO enable   |
| `output_PAD[7:0]` | inout     | `NUM_OUTPUT_PADS=8`   | `count[6:0]`, digital inverter channel          |
| `bidir_PAD`       | inout     | `NUM_BIDIR_PADS=1`    | `count[7]`, read back into the inverter         |
| `analog_PAD[5:0]` | inout     | `NUM_ANALOG_PADS=6`   | `vtune`, amplifier, inverter, ring oscillator   |
| `rf_PAD[1:0]`     | inout     | `NUM_RF_PADS=2`       | VCO RF outputs                                  |
| `vdd_rf_PAD`      | inout     | 1                     | VCO supply                                      |
| `vdd_ro_PAD`      | inout     | 1                     | ring oscillator supply                          |
| `vdd_hv_PAD`      | inout     | 1                     | IHP HV counter supply                           |

The bit-to-role mapping is fixed inside [chip_core.sv](../rtl/chip_core.sv):

| Port bit          | Signal                                                     |
| ----------------- | ---------------------------------------------------------- |
| `input_PAD[1:0]`  | `sel[1:0]`                                                 |
| `input_PAD[2]`    | `di_en`                                                    |
| `output_PAD[6:0]` | `count[6:0]` of the selected counter                       |
| `output_PAD[7]`   | `inv_dout`, `inverter.vout4` (digital channel)             |
| `bidir_PAD`       | `count[7]` of the selected counter, also `inverter.vin4`   |
| `analog_PAD[0]`   | `vtune` (via `padres`)                                     |
| `analog_PAD[1]`   | `amp_vin` (via `padres`)                                   |
| `analog_PAD[2]`   | `amp_vout` (via `padbare`)                                 |
| `analog_PAD[3]`   | `inv_vin`, `inverter.vin1` (via `padres`)                  |
| `analog_PAD[4]`   | `inv_vout`, `inverter.vout1` (via `padbare`)               |
| `analog_PAD[5]`   | `ro_vout` (via `padbare`)                                  |
| `rf_PAD[0]`       | `rf_out_n` (via `padbare`)                                 |
| `rf_PAD[1]`       | `rf_out_p` (via `padbare`)                                 |


## Pad-count overview

| Category                | Count | Pads                                                                 |
| ----------------------- | ----- | -------------------------------------------------------------------- |
| Clock                   | 1     | `clk_PAD`                                                            |
| Reset (active-low)      | 1     | `rst_n_PAD`                                                          |
| Digital inputs          | 3     | `sel[1:0]`, `di_en`                                                  |
| I/O supply              | 1     | `IOVDD`                                                              |
| I/O ground              | 1     | `IOVSS`                                                              |
| Core supply             | 1     | `VDD`                                                                |
| Core ground             | 4     | `VSS` on the west side and three times on the south side, around the RF pair |
| Digital outputs         | 8     | `count[6:0]`, `inv_dout`                                             |
| Digital bidir           | 1     | `count[7]`                                                           |
| Analog                  | 6     | `vtune`, `amp_vin`, `amp_vout`, `inv_vin`, `inv_vout`, `ro_vout`     |
| RF                      | 2     | `rf_out_n`, `rf_out_p`                                               |
| Macro supplies          | 3     | `vdd_rf`, `vdd_ro`, `vdd_hv`                                         |
| **Total**               | **32**|                                                                      |


## Location overview

| Side  | Pad count | Function                                                                    |
| ----- | --------- | --------------------------------------------------------------------------- |
| West  | 8         | supplies, `sel[1:0]`, `rst_n`, `clk`                                        |
| North | 8         | `count[7:0]` of the selected counter                                        |
| South | 8         | VCO: `di_en`, `vtune`, RF pair in GSSG, `vdd_rf`                            |
| East  | 8         | amplifier, inverter, ring oscillator, `vdd_hv`                              |


## West (bottom → top)

| # | Top-level port  | Pad-cell instance           | Type    | Direction | Domain | Role                          |
| - | --------------- | --------------------------- | ------- | --------- | ------ | ----------------------------- |
| 1 | `VSS`           | `g_vss_pads[0].vss_pad`     | power   | inout     | gnd    | core ground (VSS)             |
| 2 | `VDD`           | `g_vdd_pads[0].vdd_pad`     | power   | inout     | 1.2 V  | core supply (VDD)             |
| 3 | `IOVSS`         | `g_iovss_pads[0].iovss_pad` | power   | inout     | gnd    | I/O ground (IOVSS / IOGND)    |
| 4 | `IOVDD`         | `g_iovdd_pads[0].iovdd_pad` | power   | inout     | 3.3 V  | I/O supply (IOVDD)            |
| 5 | `input_PAD[0]`  | `g_inputs[0].input_pad`     | digital | in        | 1.2 V  | `sel[0]`                      |
| 6 | `input_PAD[1]`  | `g_inputs[1].input_pad`     | digital | in        | 1.2 V  | `sel[1]`                      |
| 7 | `rst_n_PAD`     | `rst_n_pad`                 | digital | in        | 1.2 V  | active-low synchronous reset  |
| 8 | `clk_PAD`       | `clk_pad`                   | digital | in        | 1.2 V  | main clock (50 MHz)           |


## North (left → right)

| # | Top-level port  | Pad-cell instance         | Type    | Direction | Role                                     |
| - | --------------- | ------------------------- | ------- | --------- | ---------------------------------------- |
| 1 | `output_PAD[0]` | `g_outputs[0].output_pad` | digital | out       | `count[0]` (LSB)                         |
| 2 | `output_PAD[1]` | `g_outputs[1].output_pad` | digital | out       | `count[1]`                               |
| 3 | `output_PAD[2]` | `g_outputs[2].output_pad` | digital | out       | `count[2]`                               |
| 4 | `output_PAD[3]` | `g_outputs[3].output_pad` | digital | out       | `count[3]`                               |
| 5 | `output_PAD[4]` | `g_outputs[4].output_pad` | digital | out       | `count[4]`                               |
| 6 | `output_PAD[5]` | `g_outputs[5].output_pad` | digital | out       | `count[5]`                               |
| 7 | `output_PAD[6]` | `g_outputs[6].output_pad` | digital | out       | `count[6]`                               |
| 8 | `bidir_PAD`     | `g_bidirs[0].bidir_pad`   | digital | bidir     | `count[7]` (MSB), always driven, read back into `inverter.vin4` |

The output and bidir pads are the 16 mA cells. `bidir_oe` is tied high, so the pad cannot float and `count[7]` also drives the digital inverter channel.


## South (left → right)

| # | Top-level port  | Pad-cell instance           | Type    | Direction | Role                                   |
| - | --------------- | --------------------------- | ------- | --------- | -------------------------------------- |
| 1 | `input_PAD[2]`  | `g_inputs[2].input_pad`     | digital | in        | `di_en`, VCO enable (active high)      |
| 2 | `analog_PAD[0]` | `g_analogs[0].analog_pad`   | analog  | inout     | `vtune` (via `padres`)                 |
| 3 | `VSS`           | `g_vss_pads[1].vss_pad`     | power   | inout     | ground of the RF pair                  |
| 4 | `rf_PAD[0]`     | `g_rf_pads[0].rf_pad`       | RF      | inout     | `rf_out_n` (via `padbare`)             |
| 5 | `rf_PAD[1]`     | `g_rf_pads[1].rf_pad`       | RF      | inout     | `rf_out_p` (via `padbare`)             |
| 6 | `VSS`           | `g_vss_pads[2].vss_pad`     | power   | inout     | ground of the RF pair                  |
| 7 | `vdd_rf_PAD`    | `vdd_rf_pad`                | analog  | inout     | VCO supply, 1.5 V (via `padbare`)      |
| 8 | `VSS`           | `g_vss_pads[3].vss_pad`     | power   | inout     | core ground                            |


## East (bottom → top)

| # | Top-level port  | Pad-cell instance         | Type    | Direction | Role                                       |
| - | --------------- | ------------------------- | ------- | --------- | ------------------------------------------ |
| 1 | `analog_PAD[1]` | `g_analogs[1].analog_pad` | analog  | inout     | `amp_vin` (via `padres`)                   |
| 2 | `analog_PAD[2]` | `g_analogs[2].analog_pad` | analog  | inout     | `amp_vout` (via `padbare`)                 |
| 3 | `analog_PAD[3]` | `g_analogs[3].analog_pad` | analog  | inout     | `inv_vin`, `inverter.vin1` (via `padres`)  |
| 4 | `analog_PAD[4]` | `g_analogs[4].analog_pad` | analog  | inout     | `inv_vout`, `inverter.vout1` (via `padbare`) |
| 5 | `output_PAD[7]` | `g_outputs[7].output_pad` | digital | out       | `inv_dout`, `inverter.vout4`               |
| 6 | `vdd_ro_PAD`    | `vdd_ro_pad`              | analog  | inout     | ring oscillator supply (via `padbare`)     |
| 7 | `analog_PAD[5]` | `g_analogs[5].analog_pad` | analog  | inout     | `ro_vout` (via `padbare`)                  |
| 8 | `vdd_hv_PAD`    | `vdd_hv_pad`              | analog  | inout     | IHP HV counter supply, 1.2 V to 1.65 V (via `padbare`) |

`inverter` has four channels. Channel 1 is analog on its own two pads. Channel 4 is digital: `vin4` reads `count[7]` back from its bidir pad and `vout4` drives `inv_dout`. Channels 2 and 3 are not bonded out: `vin2` and `vin3` are tied to `VSS` and `vout2` and `vout3` stay open inside [chip_core.sv](../rtl/chip_core.sv), because an inverter with a low input drives its output high.

The `sg13cmos5l_IOPadAnalog` cell exposes two internal nodes per pad:

| Net      | Path through pad cell                          | Use case                                                  |
| -------- | ---------------------------------------------- | --------------------------------------------------------- |
| `padres` | Via the pad's **secondary** ESD resistor       | Input signals: the series resistor limits ESD current and protects sensitive gate oxides |
| `padbare` | **Direct** connection to the pad metal (only primary ESD diodes present) | Output signals and supplies: no series resistor |

Two details of the pad cell are specific to this PDK instance:

- `padbare` is not part of the IHP `sg13cmos5l_io` release. It is added by the repo's own copy of the library in [ip/sg13cmos5l_io_custom/](../ip/sg13cmos5l_io_custom/): a LEF pin, a Verilog port and a Liberty pin block.
- `padres` and `padbare` are exposed on **Metal3 only**, at the top edge of the 80 × 180 µm pad cell. The `pad` pin itself is drawn on Metal2, Metal3, Metal4 and TopMetal1.

The analog nets are protected on the way from the pad to the macro: they are listed in `RSZ_DONT_TOUCH_LIST` so the resizer leaves them alone, and `DRT_ASSIGN_NDR` applies the `NDR_analog` non-default rule (0.5 µm width and spacing on Metal1 to Metal4) during detailed routing.

The two RF lines and the three macro supplies are not router wires. [pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl) draws them, see [floorplan.md](floorplan.md).
