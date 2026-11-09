# Chip Specifications

This document describes this chip from a designer's point of view: what it contains, how it behaves, and where each subsystem is configured. The numbers below are read from the actual design files. If you change them in the source, please mirror them here.

Related documents:
- Pinout: [pinout.md](pinout.md)
- Floorplan: [floorplan.md](floorplan.md)

## Where things live

| Topic                    | File                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------- |
| Padframe generation      | [rtl/chip_top.sv](../rtl/chip_top.sv)                                               |
| Top-level assembly       | [rtl/chip_core.sv](../rtl/chip_core.sv)                                             |
| Padframe / pin lists     | [flow/librelane/config.yaml](../flow/librelane/config.yaml) (`PAD_*` arrays)        |
| RF pad placement         | [flow/librelane/pad_cfg.tcl](../flow/librelane/pad_cfg.tcl)                         |
| Macro placement          | [flow/librelane/config.yaml](../flow/librelane/config.yaml) (`MACROS`)              |
| Power-distribution rules, drawn straps | [flow/librelane/pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl)           |
| Timing constraints       | [flow/librelane/chip_top.sdc](../flow/librelane/chip_top.sdc)                       |
| Cocotb testbench         | [testbenches/cocotb/chip_top_tb.py](../testbenches/cocotb/chip_top_tb.py)           |
| Build automation         | [Makefile](../Makefile) (see `make help`)                                           |

## Overview

| Parameter           | Value                                                                                                            |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Technology          | IHP SG13CMOS5L (130 nm CMOS, Open-PDK)                                                                           |
| Metal stack         | Metal1 to Metal4 plus TopMetal1 (no Metal5, no TopMetal2)                                                        |
| Die area            | 1.6 mm × 1.6 mm (2.56 mm²): `DIE_AREA: [0, 0, 1600, 1600]`                                                       |
| Core area           | 0.87 mm × 0.87 mm: `CORE_AREA: [365, 365, 1235, 1235]`                                                           |
| Clock frequency     | 50 MHz (`CLOCK_PERIOD: 20` ns in [config.yaml](../flow/librelane/config.yaml))                                   |
| Core supply         | 1.2 V                                                                                                            |
| I/O supply          | 3.3 V                                                                                                            |
| Macro supplies      | `vdd_rf` 1.5 V (VCO), `vdd_ro` (ring oscillator), `vdd_hv` 1.2 V to 1.65 V (IHP HV counter)                      |
| Total bondpads      | 32 (8 per side, 100 µm pitch), see [pinout.md](pinout.md)                                                        |
| Packaging           | QFN-32 (`PACKAGE_NAME: OP_QFN32_A4_FIT` in [packaging/config.yaml](../packaging/config.yaml))                    |
| Temperature range   | -40 °C to +125 °C                                                                                                |
| STA corners         | nom_fast_1p32V_m40C · nom_fast_1p65V_m40C · nom_slow_1p08V_125C · nom_slow_1p35V_125C · nom_typ_1p20V_25C · nom_typ_1p50V_25C |
| Default STA corner  | `nom_typ_1p20V_25C`                                                                                              |

The six corner names are the same as on the SG13G2 sibling of this template, and they resolve to `sg13cmos5l_stdcell` Liberty files plus the IO Liberty files from [ip/sg13cmos5l_io_custom/lib/](../ip/sg13cmos5l_io_custom/lib/).


## Padframe layout (8 × 8 = 32 pads)

The padframe uses the generic top-level port names defined in [chip_top.sv](../rtl/chip_top.sv). The mapping of bit indices to roles is in [chip_core.sv](../rtl/chip_core.sv).

| Side  | Pads (bottom→top / left→right)                                                                                                     |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------- |
| West  | VSS, VDD, IOVSS, IOVDD, `input_PAD[1:0]` (`sel[1:0]`), `rst_n_PAD`, `clk_PAD`                                                      |
| North | `output_PAD[6:0]` (`count[6:0]`), `bidir_PAD` (`count[7]`)                                                                         |
| South | `input_PAD[2]` (`di_en`), `analog_PAD[0]` (`vtune`), VSS, `rf_PAD[1:0]`, VSS, `vdd_rf_PAD`, VSS                                    |
| East  | `analog_PAD[1:4]` (amplifier and inverter), `output_PAD[7]` (`inv_dout`), `vdd_ro_PAD`, `analog_PAD[5]` (`ro_vout`), `vdd_hv_PAD`  |

Full per-pad breakdown including pad-cell instance names is in [pinout.md](pinout.md).


## On-die macros

| Macro           | Cell name            | Location            | Role                                                                     |
| --------------- | -------------------- | ------------------- | ------------------------------------------------------------------------ |
| IHP LV counter  | `counter_lv_ihp_top` | Top row, left       | 8-bit synchronous up-counter on the IHP LV standard cells                |
| ETH LV counter  | `counter_lv_eth_top` | Top row, center     | The same counter on the ETH LV standard cells                            |
| IHP HV counter  | `counter_hv_kvc_top` | Top row, right      | The same counter on the IHP HV standard cells, on `vdd_hv`               |
| Inverter        | `inverter_top`       | Right side          | Quad inverter: channel 1 analog, channel 4 digital, channels 2 and 3 unused |
| Amplifier       | `amplifier`          | Right side, low     | Self-biased single-ended inverter amplifier                              |
| Ring oscillator | `ringosc`            | Right side, high    | Ring oscillator on `vdd_ro`                                              |
| VCO             | `vco_top`            | Bottom center       | 20 GHz LC VCO on `vdd_rf`                                                |

Exact coordinates, the floorplan diagram and overlap rules are in [floorplan.md](floorplan.md).


## Functional behaviour

### Counter select

`sel[1:0]` on `input_PAD[1:0]` selects one of the three counters. Only the selected counter gets a clock and an enable, and its value appears on `count[7:0]`:

| `sel[1:0]` | On `count[7:0]`  | Clocked counter |
| ---------- | ---------------- | --------------- |
| `00`       | held at 0        | none            |
| `01`       | IHP LV counter   | IHP LV only     |
| `10`       | IHP HV counter   | IHP HV only     |
| `11`       | ETH LV counter   | ETH LV only     |

The clock gates are plain AND gates on a static select, so `sel` must only change with `rst_n` low or `clk` stopped. With one counter clocked, the change in the `VDD` current gives the power of the LV and ETH counters, and the HV counter reads on `vdd_hv`.

### Counters

The three counters are 8-bit (`CTR_MAX = 255`) and share `clk_PAD` through their clock gates and `rst_n_PAD`:

- `rst_n = 0` with the counter selected and `clk` running: the counter resets synchronously to 0. A counter that is not selected gets no clock, so it holds its state through a reset. Select it while `rst_n` is low to reset it.
- Selected: the counter increments on every rising clock edge.
- Not selected: the counter holds its value.
- On reaching `CTR_MAX`, the next clock edge wraps the counter back to 0.

`count[6:0]` drives `output_PAD[6:0]` and `count[7]` drives `bidir_PAD`, whose output enable is tied high.

Chip STA covers the LV counter with its own Liberty in all six corners. The ETH library has Liberty up to 1.32 V only, so its 1.35 V to 1.65 V corners reuse the nearest one. The HV library has Liberty at 3.0 V and above only, so chip STA cannot judge the HV counter at 1.2 V to 1.65 V. Its post-layout netlist in ngspice counted 259 clock edges through the wrap without an error at 50 MHz in seven cases from ss 125 °C at 1.2 V to ff -40 °C at 1.65 V, with the inputs at 1.2 V, see [macros/counter_hv_kvc/README.md](../macros/counter_hv_kvc/README.md).

### Inverter

`inverter` (instance of `inverter_top`) has four channels:

| Channel | Input                                   | Output                                  |
| ------- | --------------------------------------- | --------------------------------------- |
| 1       | `inv_vin` on `analog_PAD[3]`, via `padres` | `inv_vout` on `analog_PAD[4]`, via `padbare` |
| 2, 3    | tied to `VSS`                           | open                                    |
| 4       | `count[7]`, read back from `bidir_PAD`  | `inv_dout` on `output_PAD[7]`           |

An inverter with a low input drives its output high, so the outputs of the unused channels stay open. `Checker.DisconnectedPins` accepts this because the `lef` target of the macro writes pin directions into its LEF.

The `padres` path goes through the IO pad's secondary ESD resistor. The `padbare` path bypasses it. The corresponding nets are listed in `RSZ_DONT_TOUCH_LIST` in [config.yaml](../flow/librelane/config.yaml) so that the resizer leaves them alone.

See [macros/inverter/README.md](../macros/inverter/README.md) for its own build and sign-off flow.

### Amplifier

`amplifier` has its input `amp_vin` on `analog_PAD[1]` via `padres` and its output `amp_vout` on `analog_PAD[2]` via `padbare`. See [macros/amplifier/README.md](../macros/amplifier/README.md).

### Ring oscillator

`ringosc` runs from `vdd_ro` and has no enable, so 0 V on `vdd_ro` turns it off. Its output `ro_vout` is on `analog_PAD[5]` via `padbare`. See [macros/ringosc/README.md](../macros/ringosc/README.md).

### VCO

`vco_top` runs from `vdd_rf` at 1.5 V. `di_en` on `input_PAD[2]` enables it at the level of `VDD`, so run `VDD` at 1.5 V too to measure the VCO. `vtune` on `analog_PAD[0]` tunes it through `padres`, and its differential output `rf_out_n` and `rf_out_p` reaches the two RF pads through `padbare`. The pads are arranged ground, signal, signal, ground. See [macros/vco/README.md](../macros/vco/README.md).

20 GHz is for on-wafer measurement: the bond wires of the package are 1.3 mm to 1.7 mm long.


## Power and reset

- One IOVDD/IOVSS pair powers the I/O ring. Filler pads in the padframe distribute the supply around the four sides.
- One VDD pad and four VSS pads power the core. The chip's PDN ring sits on Metal4 (vertical) and TopMetal1 (horizontal), 15 µm wide, with 5 µm spacing. Both PDN layers are below the 30 µm width above which the layout rules require slotting.
- `vdd_rf`, `vdd_ro` and `vdd_hv` are analog pads whose `padbare` feeds one macro each, so the ring keeps a single `VDD` and `IOVDD`. They have no RC clamp of their own to `VSS`.
- Bring up `IOVDD` first and the ring `VDD` no later than `vdd_rf`, because the pad diodes of these pads and of the RF pads conduct into an unpowered rail.
- Keep `vdd_hv` at or below 1.65 V: its counter outputs drive LV gates in the select multiplexer.
- Current density was checked by hand on the pad-to-macro paths against the process specification limits for 11 years at 105 °C. At nominal current the tightest sections are the ring oscillator `VSS` at the macro pin (92 %), the `vdd_ro` via stack at the pin (82 %) and the VCO `VSS` return on three 1 µm Metal4 stripes (about 65 %). At the worst corner the first two reach 126 % and 113 %.
- The `inverter_top` macro has its own internal power ring, 2.2 µm wide, with the horizontal segments on Metal3 and the vertical ones on Metal4. The chip's TopMetal1 stripes cross it and feed it through the macro grid in [pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl).
- Active-low reset on `rst_n_PAD`. The counter macros convert polarity internally and feed a synchronous active-high reset to their FFs.
