# sg13cmos5l_ip__bondpad_70x70

A 70 µm × 70 µm square bondpad for the IHP SG13CMOS5L 130 nm CMOS process, generated using the KLayout PCell engine and the `SG13_dev` library. The same script also draws the [RF pad](#rf-pad) `sg13cmos5l_ip__rfpad_70x70`, an 80 µm × 250 µm pad cell for RF signals.

## Directory Structure

<details>
<summary>Show Directory Structure</summary>

```text
📁 sg13cmos5l_ip__bondpad_70x70/
├─ Makefile                             # Build automation
├─ 📁 script/
│  └─ bondpad.py                        # KLayout generator of the bondpad and the RF pad
├─ 📁 schematic/
│  └─ 📁 xschem/                        # RF pad schematic and symbol, the LVS reference
├─ 📁 netlist/
│  ├─ 📁 schematic/                     # RF pad CDL netlist from Xschem
│  └─ 📁 layout/                        # RF pad netlist extracted by KLayout LVS
├─ 📁 final/
│  ├─ 📁 gds/
│  │  ├─ sg13cmos5l_ip__bondpad_70x70.gds   # Generated GDSII layout
│  │  └─ sg13cmos5l_ip__rfpad_70x70.gds
│  ├─ 📁 lef/
│  │  ├─ sg13cmos5l_ip__bondpad_70x70.lef   # LEF macro for place-and-route
│  │  └─ sg13cmos5l_ip__rfpad_70x70.lef
│  ├─ 📁 lib/
│  │  └─ sg13cmos5l_ip__rfpad_70x70.lib     # Liberty view of the RF pad
│  └─ 📁 vh/
│     ├─ sg13cmos5l_ip__bondpad_70x70.vh    # Verilog blackbox stub
│     └─ sg13cmos5l_ip__rfpad_70x70.vh
└─ 📁 verification/
   ├─ 📁 drc/                           # DRC reports
   └─ 📁 lvs/                           # RF pad LVS report
```

</details>


## Usage

The default Make target is `help`, so running `make` prints usage and all available targets with short descriptions.

```bash
make
make help
```

Build everything (clean, generate bondpad and RF pad, generate Verilog, run DRC on both, run LVS on the RF pad):

```bash
make all
```

### PDK Guard

Every target except `help` and `clean` needs the `ihp-sg13cmos5l` PDK. The container starts with `ihp-sg13g2` selected, so the wrong PDK is the default state here, and it breaks this IP in both directions: the `bondpad` target reads the KLayout technology from `$PDK_ROOT/$PDK` and asks for `sg13cmos5l` by name, which another PDK does not provide, and `sak-drc.sh` runs the DRC against the rule deck of whatever `$PDK` says. The Makefile therefore compares `$PDK` against `REQUIRED_PDK` once when it is parsed, before any target runs:

```bash
$ make all
Makefile:21: *** PDK is "ihp-sg13g2", but this IP needs "ihp-sg13cmos5l". Run `sak-pdk ihp-sg13cmos5l` in this shell and retry, or pass REQUIRED_PDK= to skip this check.  Stop.
```

The check is a parse-time conditional at the top of the Makefile, not a prerequisite of each target. Switch the PDK with `sak-pdk ihp-sg13cmos5l`, pass `REQUIRED_PDK=` to skip the check, or `REQUIRED_PDK=<pdk>` to require a different PDK.


### Individual Targets

| Target        | Description                                                                                                          |
| ------------- | -------------------------------------------------------------------------------------------------------------------- |
| `bondpad`     | Generate GDS and LEF via `bondpad.py` (usage: `make bondpad [DIAMETER=<um>] [SHAPE=<square\|octagon\|circle>] [BOTTOM_METAL=<1-4>]`) |
| `rfpad`       | Generate GDS, LEF and Liberty of the RF pad via `bondpad.py`, which stops on a broken geometry or connectivity |
| `verilog`     | Generate the Verilog blackbox stubs of both cells                                                                    |
| `klayout-drc` | Run KLayout DRC using `sak-drc.sh` (usage: `make klayout-drc [CELL=<cellname>] [DRC_LEVEL=<precheck\|macro\|regular>] [DRC_JOBS=<n>]`) |
| `magic-drc`   | Run Magic DRC using `sak-drc.sh` (usage: `make magic-drc [CELL=<cellname>]`)                                         |
| `gdscheck-drc` | Run gdscheck DRC using `sak-drc.sh` (usage: `make gdscheck-drc [CELL=<cellname>] [DRC_LEVEL=<precheck\|macro\|regular>] [GDSCHECK_SUITE=<suite>\|GDSCHECK_DECKS=<decks>] [DRC_JOBS=<n>]`) |
| `rfpad-klayout-drc` | Run KLayout DRC of the RF pad at `macro` level, passes only with exactly the 7 waived `Pad.fR_M1` markers (usage: `make rfpad-klayout-drc [DRC_JOBS=<n>]`) |
| `rfpad-lvs-netlist` | Export the CDL netlist of the RF pad from Xschem |
| `rfpad-lvs`   | Run KLayout LVS of the RF pad against its schematic |
| `open`        | Browse this folder with `sak-open.py` and open each file in its tool                                |
| `clean`       | Remove all generated output directories                                                                              |

### Parameters

The following Makefile variables can be overridden:

| Variable       | Default  | Description                                                                                |
| -------------- | -------- | ------------------------------------------------------------------------------------------ |
| `DIAMETER`     | `70.0`   | Bondpad diameter/side length in µm                                                         |
| `SHAPE`        | `square` | Bondpad shape (`square`/`octagon`/`circle`)                                                |
| `BOTTOM_METAL` | `3`      | Lowest metal in the pad stack (`1`=Metal1 .. `4`=Metal4). Top is fixed to TopMetal1. |

Example: generate an octagonal 70 µm bondpad starting at Metal2:

```bash
make bondpad DIAMETER=70.0 SHAPE=octagon BOTTOM_METAL=2
```

> **Note:** The SG13_dev `bondpad` PCell expects its bottom-metal parameter as the string choice `'1'..'4'`, its top metal is fixed to TopMetal1. `bondpad.py` maps the integer `BOTTOM_METAL` (1..4) to that choice automatically, and also writes the matching `OBS` range into the LEF so the GDS and LEF stay consistent.


## Bondpad Generator Script

The `script/bondpad.py` script runs in KLayout batch mode. It:

1. Instantiates the `bondpad` PCell from the `SG13_dev` library
2. Flattens the PCell and redraws its Metal4 ring and TopVia1 to meet `Pad.gR`
3. Exports the layout as GDSII, with the pad in the child cell `bondpad`
4. Generates a matching LEF file (with `pad` pin on TopMetal1 and metal obstruction layers)
5. Stops if a TopVia1 fails `Pad.gR`, if the LEF pin lies outside the drawn metal on any layer, or if it covers under 90 % of the pad

The metal stack used for the bondpad covers `Metal3` through `TopMetal1` by default (`BOTTOM_METAL=3`, matching the SG13CMOS5L PDK default). Override `BOTTOM_METAL` to start the stack at a different layer.

**The `pad` pin is on TopMetal1 only.** TopMetal1 is the only plate the PCell draws. Every metal below it down to `BOTTOM_METAL` is a ring at the pad edge, so a lower pin plate would claim metal that is not there. `place_bondpad` makes the chip's terminal on TopMetal1. The `OBS` stays a full-size rectangle on every layer, because an obstruction that stops short leaves the conductor exposed.

**`Pad.gR` asks for 1.40 µm of Metal4 around every TopVia1 inside `dfpad`.** The PCell's ring is 1.53 µm wide with its cuts 0.555 µm from either edge, which gives 648 `Pad.gR` markers per 70 µm square pad in gdscheck's `recommended` suite, and KLayout's deck does not run the rule. `pad_gr` redraws the ring 3.45 µm wide from the same outer edge, with the cuts on its centre line and outside the passivation opening. The price is at the chip top level: the wider ring reaches under the passivation opening, so `Pad.fR_M4` starts to apply to the 3 µm `pad` strip of the IO cell, one recommended marker per pad in a KLayout run with recommended rules, next to the `Pad.fR_TM1` that strip already causes.

**The pad stays in a child cell.** Magic's `Slt.c` flags a solid plate drawn in the top cell, 6 markers on the 70 µm square pad, while KLayout and gdscheck exempt metal under `dfpad`. In a child cell, where the PCell instance always was, `make magic-drc` is clean.

**`SHAPE=circle` keeps the PCell's rings.** A circle has no 0/45/90 outline to redraw, so it does not meet `Pad.gR`, and its Metal3 and Metal4 rings fail the 45° angle rule in KLayout and gdscheck, 129 markers per layer at `BOTTOM_METAL=3`.


## RF Pad

`make rfpad` runs `script/bondpad.py` with `-rd pad_type=rf` and draws `sg13cmos5l_ip__rfpad_70x70`. It takes the slot of `sg13cmos5l_IOPadAnalog` plus its bondpad at one place of the pad ring, for a signal that needs about half the load of that cell (197 fF against about 395 fF) and a defined return path under the pad. It is one fixed cell, so `DIAMETER`, `SHAPE` and `BOTTOM_METAL` do not apply.

| y (µm, 0 is the die edge) | Content |
| --- | --- |
| 0 to 70 | The `bondpad` PCell: octagon, 70 µm, `bottomMetal` `3`, with its Metal4 ring and TopVia1 redrawn to meet `Pad.gR`, over a solid Metal1 shield on `vss` with a 3 µm collar |
| 70 to 250 | The rail bands of `sg13cmos5l_IOPadAnalog` shifted by 70 µm, read from the LEF in `ip/sg13cmos5l_io_custom`, the ESD pair, the supply clamp and the RF line |

**Ports.** `vss`, `vdd`, `iovss`, `iovdd`, `pad` and `padbare`. `pad` is the plate and `padbare` the inner end of the same TopMetal1 conductor, with no series resistor between them. There is no `padres`. `padbare` is 1.64 µm wide on TopMetal1 at y 240 to 250. It is a LEF and Verilog alias, the schematic has no such node.

**RF line.** The plate leaves through a teardrop, 14.92 µm wide for the 7 µm that `Pad.fR` asks for, then a 45° taper onto 4.92 µm up to the ESD tap at y 210, then 1.64 µm. It runs through a corridor cut in the TopMetal1 and Metal4 rails, 5 µm from the rails on either side. `iovss` and `iovdd` cross it on Metal3 and on the Metal2 strips under it.

**ESD.** `diodevss_2kv` and `diodevdd_2kv` connect the pad to the core rails `vss` and `vdd`, not to `iovss` and `iovdd`. An RC-triggered clamp between `vdd` and `vss` takes the strike from there, because IHP's pad ring clamps `vdd` only to `iovss`. It is the circuit of `sg13cmos5l_IOPadVdd` with its source on `vss` and a 1512 µm / 0.6 µm `sg13_hv_nmos`. What the pad survives also depends on the circuit behind it and the chip's rails, so simulate HBM on the chip.

**A pad above `vdd`.** The pad clamps at `vdd` plus one diode. With `vdd` at 1.2 V, `diodevdd_2kv` and `diodevss_2kv` together draw this DC current (ngspice, `dio_tt`):

| Pad voltage | 27 °C | 125 °C |
| --- | --- | --- |
| 1.35 V | 3.1 pA | 0.6 nA |
| 1.55 V | 0.14 nA | 31 nA |
| 1.75 V | 18 nA | 6.6 µA |

A circuit on its own, higher supply can therefore drive this pad, but `vdd` has to come up no later than that supply, or the diode conducts into the unpowered rail.

**Capacitance on the pad node.** 197 fF at 0.6 V and 27 °C, and the Liberty view carries that value with no timing arc. Its junctions grow to 57 fF at a pad voltage of 1.35 V with `vdd` at 1.2 V, and to 63 fF at 125 °C.

| Part | fF | Source |
| --- | --- | --- |
| Plate and rings to the shield | 60.7 | Palace, order 3, 2.44 GHz, a separate EM solve whose setup is not in this repo, against 66.6 fF from Magic |
| All other metal on the node | 84.3 | Magic, `sak-pex.sh -m 2`, 150.95 fF in total less Magic's plate term |
| `diodevss_2kv` at 0.6 V | 27.2 | PDK model card |
| `diodevdd_2kv` at 0.6 V to `vdd` | 24.7 | PDK model card |

The schematic carries the metal as four `Cm_*` capacitors, one per chip net, with `lvs_ignore=open`, so a simulation charges them and LVS never sees them. None of this is an EM solve at 20 GHz, where the 180 µm line is no longer a lumped capacitor.

**Checks.** DRC and LVS both miss a pad shorted to a rail, because the rails carry no device and two touching shapes are one polygon. So `bondpad.py` checks the cell before it writes any view, and stops if one of these fails:

- The cell outline, the pad stack areas, the `Pad.gR` enclosure of every TopVia1 in the pad, and that the pad pin is one centred rectangle.
- The 3 µm shield collar, the widths of the RF line, and that the TopMetal1 rails keep exactly 5 µm from it with Metal4 cut in the same place.
- That no pad net metal reaches a cell edge, that each of `vss`, `vdd`, `iovss` and `iovdd` is its own net, and that every `iovss` and `iovdd` band is one conductor across Metal3, Metal4 and TopMetal1.
- That the shield reaches `vss`, that each ESD terminal is on its rail, and that the clamp's stripes, rings, gate buses and RC node are on their nets.

**Verification results**, image `ghcr.io/iic-jku/iic-osic-tools:nightly` (`8ea7cab3bd18`), PDK `ac438346`:

| Check | Result |
| --- | --- |
| `make rfpad-lvs` (KLayout LVS) | match |
| `make gdscheck-drc CELL=sg13cmos5l_ip__rfpad_70x70` (`core`) | clean, the `recommended` suite too |
| `make rfpad-klayout-drc` (`macro`) | exactly 7 `Pad.fR_M1`, waived |
| `make klayout-drc DRC_LEVEL=regular CELL=sg13cmos5l_ip__rfpad_70x70` | the 7 `Pad.fR_M1` plus `AFil.g` and `GFil.g`, density rules that a single cell cannot meet |
| `make magic-drc CELL=sg13cmos5l_ip__rfpad_70x70` | 2 `Slt.c` on the Metal1 shield, Magic does not exempt the plate under `dfpad` as KLayout does |

`Pad.fR_M1` asks for 7 µm of Metal1 past `dfpad`. The Metal1 crossing `dfpad` is the shield's 3 µm collar, a ground plane that exits nowhere, and the 80 µm cell leaves 5 µm a side. Without the collar the rim field of the pad lands on the substrate, so the markers are waived by their exact count: one more or one less fails `make rfpad-klayout-drc`.

### Using the RF Pad on a Chip

A chip instantiates it like `sg13cmos5l_IOPadAnalog`, with `.pad` and `.padbare` and without `.padres`, and needs these entries in `flow/librelane/config.yaml`:

| Variable | Entry |
| --- | --- |
| `PAD_LEFS` | `final/lef/sg13cmos5l_ip__rfpad_70x70.lef`, next to the IO library's LEF |
| `PAD_VERILOG_MODELS` | `final/vh/sg13cmos5l_ip__rfpad_70x70.vh`, next to the IO library's Verilog |
| `EXTRA_GDS` | `final/gds/sg13cmos5l_ip__rfpad_70x70.gds` |
| `LIB` | `final/lib/sg13cmos5l_ip__rfpad_70x70.lib`, in every corner. `EXTRA_LIBS` does not work, Yosys then replaces the Verilog blackbox and the power ports are gone |
| `PAD_PLACE_IO_TERMINALS` | `sg13cmos5l_ip__rfpad_70x70/pad`. `place_bondpad` is what creates a pad's top-level terminal, and this cell gets no bondpad |
| `PAD_CFG` | A copy of LibreLane's `scripts/openroad/common/pad_cfg.tcl` that moves every pad whose master matches no `PAD_BONDPAD_OFFSETS` regex outward by the bondpad depth, 70 µm, before `connect_by_abutment`. `place_pad` leaves the instance `FIRM`, so the script sets it to `PLACED` for the move and restores it |

The cell is 70 µm taller than the IO library's pads and its rail bands are drawn 70 µm further in, so its rails abut its neighbours only when its outer edge sits where the bondpads' outer edges are. `OpenROAD.PadRing` places every pad at the row, which leaves this cell 70 µm too far in with an open supply ring and no report. `PAD_BONDPAD_OFFSETS` already skips it, because its name does not match `sg13cmos5l_IOPad*`. The width of 80 µm is that of the IO library's pads, so the pad pitch does not change.


## Design Rule Check (DRC)

Runs DRC on the GDS layout in `final/gds/`. All three flows use `sak-drc.sh` and write their reports into per-cell run folders: `verification/drc/<CELL>.magic.drc/` (Magic), `verification/drc/<CELL>.klayout.drc/` (KLayout, `.lyrdb`) and `verification/drc/<CELL>.gdscheck.drc/` (gdscheck, `.lyrdb`).

**KLayout DRC** uses `sak-drc.sh` at the selected `DRC_LEVEL` (`precheck`, `macro` [default], or `regular`), with at most `DRC_JOBS` processes (default: 4, or the CPU count if lower):

```sh
make klayout-drc
make klayout-drc CELL=sg13cmos5l_ip__bondpad_70x70
make klayout-drc DRC_LEVEL=regular
```

**Magic DRC** uses `sak-drc.sh`. `make all` leaves it out until the foundry cells of the chip are clean in Magic:

```sh
make magic-drc
make magic-drc CELL=sg13cmos5l_ip__bondpad_70x70
```

**gdscheck DRC** runs the standalone [gdscheck](https://github.com/aesc-silicon/gdscheck) engine (`sak-drc.sh -g`). `DRC_LEVEL` selects its suite (`precheck`, `core` for the default `macro`, or `main` for `regular`) and `GDSCHECK_SUITE` replaces it, or `GDSCHECK_DECKS` runs single rule decks instead, see the [top-level README](../../README.md#design-rule-check-drc). `make all` runs it:

```sh
make gdscheck-drc
make gdscheck-drc CELL=sg13cmos5l_ip__bondpad_70x70
```
