# Chip Specifications

This document describes the AMS template chip from a designer's point of view: what it contains, how it behaves, and where each subsystem is configured. The numbers below are read from the actual design files. If you change them in the source, please mirror them here.

Related documents:
- Pinout: [pinout.md](pinout.md)
- Floorplan: [floorplan.md](floorplan.md)

## Where things live

| Topic                    | File                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------- |
| Padframe generation      | [rtl/chip_top.sv](../rtl/chip_top.sv)                                               |
| Top-level assembly       | [rtl/chip_core.sv](../rtl/chip_core.sv)                                             |
| Padframe / pin lists     | [flow/librelane/config.yaml](../flow/librelane/config.yaml) (`PAD_*` arrays)        |
| Macro placement          | [flow/librelane/config.yaml](../flow/librelane/config.yaml) (`MACROS`)              |
| Power-distribution rules | [flow/librelane/pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl)                         |
| Timing constraints       | [flow/librelane/chip_top.sdc](../flow/librelane/chip_top.sdc)                       |
| Cocotb testbench         | [testbenches/cocotb/chip_top_tb.py](../testbenches/cocotb/chip_top_tb.py)           |
| Xschem mixed-signal TB   | [testbenches/xschem/chip_top_tb_tran.sch](../testbenches/xschem/chip_top_tb_tran.sch) |
| Build automation         | [Makefile](../Makefile) (see `make help`)                                           |

## Overview

| Parameter           | Value                                                                                                            |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Technology          | IHP SG13CMOS5L (130 nm CMOS, Open-PDK)                                                                           |
| Metal stack         | Metal1 to Metal4 plus TopMetal1 (no Metal5, no TopMetal2)                                                        |
| Die area            | 1.6 mm × 1.6 mm (2.56 mm²): `DIE_AREA: [0, 0, 1600, 1600]`                                                       |
| Core area           | 0.87 mm × 0.87 mm: `CORE_AREA: [365, 365, 1235, 1235]`                                                           |
| Clock frequency     | 50 MHz (`CLOCK_PERIOD: 20` ns in [config.yaml](../flow/librelane/config.yaml))                                   |
| Core supply         | 1.5 V                                                                                                            |
| I/O supply          | 3.3 V                                                                                                            |
| Total bondpads      | 32 (8 per side), see [pinout.md](pinout.md)                                                                     |
| Packaging           | QFN-32 (`PACKAGE_NAME: OP_QFN32_A4_FIT` in [packaging/config.yaml](../packaging/config.yaml))                    |
| Temperature range   | -40 °C to +125 °C                                                                                                |
| STA corners         | nom_fast_1p32V_m40C · nom_fast_1p65V_m40C · nom_slow_1p08V_125C · nom_slow_1p35V_125C · nom_typ_1p20V_25C · nom_typ_1p50V_25C |
| Default STA corner  | `nom_typ_1p50V_25C`                                                                                              |

The six corner names are the same as on the SG13G2 sibling of this template, and they resolve to `sg13cmos5l_stdcell` Liberty files plus the IO Liberty files from [ip/sg13cmos5l_io_custom/lib/](../ip/sg13cmos5l_io_custom/lib/).


## Padframe layout (8 × 8 = 32 pads)

The padframe uses the generic top-level port names defined in [chip_top.sv](../rtl/chip_top.sv). The mapping of bit indices to roles is in [chip_core.sv](../rtl/chip_core.sv).

| Side  | Pads (bottom→top / left→right)                                                                                                       |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------ |
| West  | `output_PAD[16]` (SRAM out), VSS, VDD, IOVSS, IOVDD, `input_PAD[0]` (enable), `rst_n_PAD`, `clk_PAD`                                 |
| North | `output_PAD[3:0]` (counter1[3:0]), `bidir_PAD[3:0]` (counter1[7:4] / inverter1.vin1..vin4)                                           |
| South | `output_PAD[11:4]` (counter2[7:0])                                                                                                   |
| East  | `analog_PAD[3:0]` (inverter2: vin1, vin2, vout1, vout2), `output_PAD[15:12]` (inverter1.vout1..vout4)                                |

Full per-pad breakdown including pad-cell instance names is in [pinout.md](pinout.md).


## On-die macros

| Macro     | Cell name                            | Count | Location                       | Role                                                                                                           |
| --------- | ------------------------------------ | ----- | ------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Counter   | `counter_top`                        | 2     | Mid-right core (counter1 above counter2) | `counter1` drives north pads (LSB + bidir MSB), `counter2` drives all south pads. 8-bit synchronous up-counter. |
| Inverter  | `inverter_top`                       | 2     | Right side, stacked vertically | `inverter1` used as 4-channel CMOS digital inverter, `inverter2` as 2-channel analog inverter.                 |
| SRAM      | `RM_IHPSG13_1P_1024x32_c2_bm_bist`   | 1     | Left-lower region of the core  | 1024 × 32-bit single-port SRAM (with bit-mask + BIST). Read-only sweep clocked from the main clock.            |

Exact coordinates, the floorplan diagram and overlap rules are in [floorplan.md](floorplan.md).


## Functional behaviour

### Global enable

`input_PAD[0]` (also named `enable` inside [chip_core.sv](../rtl/chip_core.sv)) is the chip global enable signal. It gates:

- the counters' `enable_i` input,
- all four bidirectional pad output enables (`bidir_oe[3:0]`).

| `enable` | Counters         | `bidir_PAD[3:0]` direction                       |
| -------- | ---------------- | ------------------------------------------------ |
| `0`      | hold their value | input (high-Z driver, external stimuli reach `inverter1.vin1..vin4`) |
| `1`      | increment        | output (`counter1_value[7:4]` is driven onto the pads) |

### Counters

`counter1` and `counter2` are two instances of the `counter_top` macro (8-bit, default `CTR_MAX = 255`). They share `clk_PAD`, `rst_n_PAD` and `input_PAD[0]`:

- `rst_n = 0`: both counters reset synchronously to 0.
- `enable = 0`: both counters hold their current value.
- `enable = 1`: both counters increment by one on every rising clock edge.
- On reaching `CTR_MAX`, the next clock edge wraps the counter back to 0.

`counter1_value[3:0]` drives `output_PAD[3:0]` (north LSB nibble).
`counter1_value[7:4]` drives `bidir_PAD[3:0]` (north MSB nibble, in output mode). `counter2_value[7:0]` drives `output_PAD[11:4]` (full south side).

The counter is hardened by LibreLane on `sg13cmos5l_stdcell`. The PDK default routing window is Metal2 to TopMetal1, and [macros/counter/flow/librelane/config.yaml](../macros/counter/flow/librelane/config.yaml) carries a commented-out `RT_MAX_LAYER: Metal4` to cap the macro below the chip's TopMetal1 PDN if a future floorplan ever needs it.

### Inverter 1

`inverter1` (instance of `inverter_top`) is used as a 4-channel CMOS digital inverter:

- `vin1..vin4` come from `bidir_in[3:0]` (i.e. `counter1_value[7:4]` when `enable = 1`, or external stimuli when `enable = 0`).
- `vout1..vout4` drive `output_PAD[15:12]` on the east side.

Two test modes are therefore possible:

1. **Coupled to counter1** (`enable = 1`): observe `~counter1_value[7:4]` on `output_PAD[15:12]` while `counter1_value[7:4]` itself is observable on `bidir_PAD[3:0]`.
2. **Standalone** (`enable = 0`): drive `bidir_PAD[3:0]` externally and observe the inverted response on `output_PAD[15:12]`.

### Inverter 2

`inverter2` (instance of `inverter_top`) is used as an analog block. Two of its four channels are exposed via four east-side analog pads:

| Pad            | Signal                                   |
| -------------- | ---------------------------------------- |
| `analog_PAD[0]`| `inverter2.vin1`  (channel 1 input,  via `padres`)  |
| `analog_PAD[1]`| `inverter2.vin2`  (channel 2 input,  via `padres`)  |
| `analog_PAD[2]`| `inverter2.vout1` (channel 1 output, via `padbare`) |
| `analog_PAD[3]`| `inverter2.vout2` (channel 2 output, via `padbare`) |

Channels 3 and 4 (`vin3`, `vout3`, `vin4`, `vout4`) are tied to `VSS` inside [chip_core.sv](../rtl/chip_core.sv) and are not bonded out.

The `padres` path goes through the IO pad's secondary ESD resistor. The `padbare` path bypasses it (lower parasitics, used for the output signals). The corresponding nets are listed in `RSZ_DONT_TOUCH_LIST` in [config.yaml](../flow/librelane/config.yaml) so the resizer leaves them alone, and the `DRT_ASSIGN_NDR` regex applies the wider `NDR_analog` non-default rule to them during detailed routing. `NDR_analog` covers Metal1 to Metal4 and the double-cut vias `Via1_DC1B`, `Via2_DC1B` and `Via3_DC1B`. The SG13G2 version of the same rule has a Metal5 entry and a fourth via, neither of which exists on this stack.

The `inverter_top` macro is a hand-drawn layout, redrawn for the SG13CMOS5L design rules at the same 54.18 × 81.92 µm footprint as its SG13G2 counterpart. See [macros/inverter/README.md](../macros/inverter/README.md) for its own build and sign-off flow, including the note that KPEX has no SG13CMOS5L support yet and Magic is the extraction path here.

### SRAM

The `RM_IHPSG13_1P_1024x32_c2_bm_bist` macro is wired up for a simple read-only demonstration in [chip_core.sv](../rtl/chip_core.sv):

| Port              | Value / connection                                                  |
| ----------------- | ------------------------------------------------------------------- |
| `A_CLK`           | `clk` (main clock)                                                  |
| `A_MEN`           | constant `1`                                                        |
| `A_REN`           | constant `1`                                                        |
| `A_WEN`           | constant `0` (writes disabled)                                      |
| `A_ADDR[9:0]`     | constant `0` (always reads address 0)                               |
| `A_DIN[31:0]`     | constant `0`                                                        |
| `A_BM[31:0]`      | constant `0`                                                        |
| `A_DLY`           | constant `1`                                                        |
| `A_DOUT[31:0]`    | XOR-reduced to one bit and routed to `output_PAD[16]`               |
| `A_BIST_*`        | tied to `0` (BIST disabled)                                         |

The behavioural model has no `USE_POWER_PINS` block, so the Verilog instantiation only connects the functional/BIST ports. Physical supply hookup is handled at the PDN level via `PDN_MACRO_CONNECTIONS` in [config.yaml](../flow/librelane/config.yaml), which binds both the macro's `VDD!/VSS!` and its secondary `VDDARRAY!/VSS!` to the chip's `VDD`/`VSS`.

The IHP SRAM macros are not characterised for every corner of this template, in particular not above 1.32 V. The `lib` block of the macro in [config.yaml](../flow/librelane/config.yaml) therefore reuses `RM_IHPSG13_1P_1024x32_c2_bm_bist_fast_1p32V_m55C.lib` for the three corners that have no matching Liberty (`nom_fast_1p65V_m40C`, `nom_slow_1p35V_125C`, `nom_typ_1p50V_25C`). That is a deliberate substitution, and `nom_typ_1p50V_25C` is the default corner, so any SRAM timing number the flow reports at the default corner is read from a 1.32 V / -55 °C model.


## Power and reset

- One IOVDD/IOVSS pair powers the I/O ring. Filler pads in the padframe distribute the supply around the four sides.
- One VDD/VSS pair powers the core. The chip's PDN ring sits on Metal4 (vertical) and TopMetal1 (horizontal), 15 µm wide, with 5 µm spacing. Both PDN layers are below the 30 µm width above which the layout rules require slotting.
- Each `inverter_top` instance has its own internal power ring, 2.2 µm wide, with the horizontal segments on Metal3 and the vertical ones on Metal4. The chip's TopMetal1 stripes cross it and feed it through the macro grid in [pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl).
- The SRAM's supply pins are vertical Metal4 stripes, which is the chip's own vertical PDN layer, so its grid (`sram` in [pdn_cfg.tcl](../flow/librelane/pdn_cfg.tcl)) is a plain Metal4 to TopMetal1 connect with no extra stripes.
- Active-low reset on `rst_n_PAD`. The counter macro converts polarity internally and feeds a synchronous active-high reset to its FFs.
