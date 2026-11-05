# ihp-sg13cmos5l VCO

A 20 GHz LC voltage-controlled oscillator built from CMOS devices only, the RF macro of this template. It is the starting point for RF blocks: next to the analog flow of the [inverter](../inverter/README.md) it carries the RF layer, the EM simulation of the passives with AWS Palace, their lumped-element models from snp2le, and the periodic steady-state, small-signal and noise analyses of VACASK. The core follows a published design, the 27 GHz cross-coupled VCO of Jung and Park [[1]](#references), scaled to 20 GHz and to the devices of this PDK. It is the VCO of the ihp-sg13g2 template, ported to a process without TopMetal2, Metal5, MIM capacitors and an inductor PCell, see [Porting from ihp-sg13g2](#porting-from-ihp-sg13g2).

> [!NOTE]
> This macro is under construction on the branch `add-rf-macro`. The schematic, its simulations over corners, the layout of every cell (KLayout Python scripts, DRC and LVS clean), the EM model of the coil and a post-layout simulation are in place. The chip integration follows, see [Status](#status). The chip top-level does not build it yet.

> [!IMPORTANT]
> The VACASK testbenches need the IIC-OSIC-TOOLS container with tag `2026.10` or later: the oscillator PSS (`oscillator=1`), `pac` and `pnoise` arrived in VACASK after the `2026.09` image.


## Specification

| Parameter | Target | Simulated (TT, 27 C) |
| --- | --- | --- |
| Oscillation frequency | 20 GHz | 20.21 GHz post-layout at `vtune` = 0.75 V, 22.77 GHz in the schematic |
| Tuning range | about 2 GHz, with 20 GHz inside it at every corner | 1.94 GHz post-layout, 19.52 GHz to 21.46 GHz for `vtune` from 0 V to 1.5 V, 1.86 GHz to 2.04 GHz over the corners, 2.65 GHz in the schematic (21.78 GHz to 24.43 GHz) |
| Tuning gain | | 0.77 GHz/V to 2.28 GHz/V, 2.03 GHz/V at 0.75 V |
| Phase noise | not optimized, reported | -102.2 dBc/Hz at 1 MHz, see [Limitations](#limitations) |
| Output power | -10 dBm or more per output into 50 Ohm | -9.2 dBm in the schematic, -10.2 dBm post-layout from the peak-to-peak swing, which reads about 1 dB high |
| Supplies | `VDD` = 1.5 V, the chip core supply, and `vdd_core` = 0.78 V from its own pad | `VDD` 6.3 mA, `vdd_core` 4.8 mA, plus the 0.1 mA reference, post-layout 5.6 mA and 4.9 mA |
| Bias | 100 uA reference current into `ibias_100u` | |
| Power down | `di_en` low turns the buffer and bias currents off, `vdd_core` at 0 V the core | |
| Corners | starts and stays below 1.5 V on every node at SS, TT and FF, -40 C to 85 C | yes post-layout, 19.23 GHz to 21.63 GHz, highest node 1.43 V, see [Corners](#corners) |

The macro is centered on its post-layout simulation (see [Post-Layout Simulation](#post-layout-simulation)): 20 GHz at the middle of the tuning range, and `vdd_core` in the middle of the window in which every post-layout corner starts and no tank node passes 1.5 V. The schematic, without the resistance and the capacitance of the leads, oscillates 12 % higher and swings higher, so its tank peaks pass 1.5 V at FF, and they are reported but not checked. The other values are schematic-level unless they say post-layout, with the coil model fitted to the EM simulation of the coil's layout (see [EM Simulation of the Coil](#em-simulation-of-the-coil)).

This is a simple VCO to learn the RF flow on, not an optimized design. It goes through each step once, from the schematic over the coil's layout, EM simulation and lumped-element model to the oscillator analyses of VACASK and a post-layout simulation. [Limitations](#limitations) lists where it falls short and what a better design would change.


## Circuit

| Cell | Function |
| --- | --- |
| `vco_top` | the macro: bias, core, coil and buffer, and the pins |
| `vco_core` | negative resistance and tank capacitance: the cross-coupled NMOS pair `M1`/`M2`, the varactor array, and the decoupling capacitors `Cct1` and `Cct2` of `vdd_core` at the coil's center tap |
| `vco_ind` | the center-tapped tank coil: the inductor the LVS deck extracts (`vco_ind_lvs.sym`), and the lumped-element model `vco_ind_le` for simulation |
| `vco_var` | the varactor array: three `sg13_hv_svaricap` with `Nx=8` each, gates on the tank, wells on `vtune` |
| `vco_buf` | AC-coupled differential output buffer with 50 Ohm back-termination |
| `vco_bias` | the enable logic and the two bias voltages of the buffer, each behind an RC low-pass filter |

**Core.** The core is the voltage-biased cross-coupled pair of Jung and Park [[1]](#references): two NMOS (20 um / 0.13 um each) with their sources on `VSS`, and no current source at all. The center tap of the coil sits on its own supply `vdd_core`, 0.78 V from a pad, against 0.639 V in the paper. The tank's common mode is then `vdd_core`, and the pair draws whatever current its gate-source voltage `vdd_core` gives: 4.8 mA at TT, 3.6 mA to 5.7 mA over the post-layout corners. That common mode is what the varactor needs. `sg13_hv_svaricap` is an accumulation-mode MOS varactor whose capacitance changes most around 0 V gate-to-well voltage, so with the gates on the tank and the wells on `vtune`, a tune voltage from 0 V to `VDD` sweeps it across that transition. Each tank node swings from about 0.20 V to 1.33 V post-layout, from 0.11 V to 1.53 V in the schematic: the core works in the voltage-limited regime of Hajimiri and Lee [[2]](#references), where the supply and not a current sets the amplitude. `vdd_core` is therefore the amplitude knob, and 0.78 V sits in the middle of a post-layout window of 60 mV: from 0.75 V the slow corner starts, up to 0.81 V the highest node stays below the 1.5 V supply, see [Corners](#corners). `Cct1` and `Cct2` decouple `vdd_core` at the center tap, where the pair's current pulses at twice the oscillation frequency. They are six `cap_cmomf` units on Metal1 to Metal4, 3.8 pF by the model and 3.7 pF in the extraction.

The first version of this macro, in the ihp-sg13g2 template, fed the center tap from a PMOS current source and set the tank's common mode by the pair's gate-source voltage at that current. The bias noise of the source then moved the varactor's operating point, and the phase noise was -85.4 dBc/Hz at 1 MHz, 92 % of it from the bias chain. The voltage-biased core removes that path. What it gives up is a defined current: the core current follows the process and the temperature, and noise on `vdd_core` reaches the frequency, see [Limitations](#limitations).

**Coil.** The tank coil is a symmetric octagon of 2 turns in TopMetal1 with a center tap, 4 um width, 4 um spacing, 50 um inner and 74 um outer diameter, in a keep-out 10 um wide around it. This PDK has neither TopMetal2 nor an inductor PCell, so [`vco_ind.py`](scripts/layout/vco_ind.py) draws it, with its one crossing on Metal4 and Metal3 in parallel. Its EM simulation gives 380.5 pH differential with a Q of 11.8 at 20.25 GHz, see [EM Simulation of the Coil](#em-simulation-of-the-coil). Its diameter and the length of its leads set the post-layout frequency, see [Post-Layout Simulation](#post-layout-simulation). The PDK has no SPICE model for the coil, so `vco_ind` holds two views of it. The LVS view `vco_ind_lvs.sym` is what KLayout LVS extracts, and every simulation netlist skips it (`spice_ignore` is a `tcleval` of the LVS switch, `spectre_ignore=true`). The lumped-element model `vco_ind_le` is what simulation uses, and the LVS netlist skips it (`lvs_ignore=open`). It is fitted with `make snp2le` to the EM result. Its substrate network returns to the global ground node, so `VSS` has to be the ground of every testbench. The deck extracts the coil in the top cell of every LVS run, because its third terminal is the substrate, so the coil sits in `vco_top` beside the core, in the schematic as in the layout.

**Varactor.** One `sg13_hv_svaricap` with `Nx=8` measures 31 fF to 21 fF differential (63 fF to 41 fF per tank node) for a gate-to-well voltage from +0.75 V to -0.75 V, with a differential Q of 23 to 30 at 20 GHz. The model is that of ihp-sg13g2. The layout differs: this PDK's `SVaricap` PCell draws ThickGateOx where the ihp-sg13g2 one draws nBuLay, which this process does not have. The well resistance of the model is about 200 Ohm per varactor. It only carries common-mode current and does not load the differential tank, but its thermal noise reaches the frequency through the tuning gain like noise on `vtune` does.

**Buffer.** A differential pair (24 um / 0.13 um each, 6 mA tail in 30 fingers of 5 um) is AC-coupled to the tank through `cap_cmomf` capacitors (Metal2 to Metal4, 10 um by 18.6 um, 170 fF by the model and 153 fF in the extraction) and biased at `vbg_buf` (about 1.04 V) through 24 kOhm resistors. Each output has a 50 Ohm `rppd` resistor to `VDD`, so the buffer is back-terminated for a 50 Ohm measurement setup, and the load has to be AC-coupled. The pair is as wide as it is for the output power: in the ihp-sg13g2 macro, 16 um would raise the frequency by 270 MHz and cost 1 dB.

**Bias and enable.** The 100 uA reference current enters the diode-connected NMOS `MN0`, and `MBt` in the buffer mirrors it 60:1. `MN1` copies it into the diode-connected PMOS `MP1`, and `MP2` mirrors that into `Rg` and the diode `MN3`, which sets `vbg_buf` to a gate-source voltage plus 0.45 V. Both bias voltages pass an RC low-pass filter at about 170 kHz: `Rn` (95 kOhm) with `MCn1`/`MCn2` (9.4 pF) on `vbn_buf`, `Rf` (95 kOhm) with `MCg1`/`MCg2` (10 pF) on `vbg_buf`. They are there because the buffer's bias moves the frequency: the buffer's input capacitance depends on its currents and loads the tank through the coupling capacitors, by -38 MHz per mA of tail current in the ihp-sg13g2 macro. With the filters of the first version there (48 kOhm, 1.35 pF), that path set the phase noise once the core was quiet: -96.6 dBc/Hz at 1 MHz, with 77 % from `Rn` and `MN0`. The filter capacitors are NMOS gates (source, drain and bulk on `VSS`), 12 fF/um2 at these voltages against 1.29 fF/um2 for the densest `cap_cmomf` (Metal1 to Metal4), so 10 pF takes 800 um2. Their gate leakage drops 13 mV across `Rf`. `di_en` passes two inverters. Low, it pulls the NMOS gate lines to `VSS` and the PMOS gate line to `VDD`, so the buffer and bias currents are off. The core has no enable, as in the paper: with its own supply, it is off when `vdd_core` is at 0 V.


## Pins

| Pin | Direction | Function |
| --- | --- | --- |
| `VDD` | inout | supply of the buffer and the bias, 1.5 V |
| `vdd_core` | inout | supply of the core at the coil's center tap, 0.78 V from its own pad |
| `VSS` | inout | ground |
| `ibias_100u` | input | reference current, 100 uA into the macro |
| `di_en` | input | enable of the buffer and the bias, active high |
| `vtune` | input | tuning voltage, 0 V to `VDD` |
| `rf_out_p`, `rf_out_n` | inout | differential RF output, 50 Ohm back-terminated to `VDD`, the load has to be AC-coupled |

In the layout (143 um by 176.9 um), `di_en` and `ibias_100u` leave on Metal3 at the left edge. `vtune`, `rf_out_n`, `rf_out_p` and `vdd_core` leave on Metal3 at the bottom edge. `VSS` is a TopMetal1 strap and `VDD` a Metal4 strap along the bottom edge.


## Simulation Results

All results are from the testbenches in [`testbenches/xschem/`](testbenches/xschem/), plotted by `make sim-view-xschem` into [`testbenches/xschem/plot_simulations/figures/`](testbenches/xschem/plot_simulations/figures/).

| Testbench | Simulator | Analyses | Result |
| --- | --- | --- | --- |
| `vco_top_tb_tran` | ngspice | start-up transient, 2 ns | 22.72 GHz, tank 0.11 V to 1.53 V, 260 mVpp per output (-7.7 dBm), `VDD` 6.3 mA, `vdd_core` 4.8 mA |
| `vco_top_tb_pss_vacask` | VACASK | oscillator PSS, PNOISE, PAC | 22.77 GHz, -9.2 dBm per output at the fundamental, -102.2 dBc/Hz at 1 MHz, K_VCO 2.07 GHz/V at 10 MHz (PAC) |
| `vco_top_tb_tune_vacask` | VACASK | one 1.5 ns transient per tuning voltage | 21.78 GHz to 24.43 GHz for `vtune` from 0 V to 1.5 V |
| `vco_top_tb_tran_lpe` | ngspice | start-up transient of the post-layout netlist | 20.21 GHz, tank 0.20 V to 1.33 V, 4.9 mA, see [Post-Layout Simulation](#post-layout-simulation) |
| `vco_ind_tb_acsp_vacask` | VACASK | ACSP, S-parameters of the coil model from 0 Hz to 60 GHz | 386.5 pH and Q 11.7 at 20.25 GHz, against 380.5 pH and Q 11.8 from EM |

The ngspice transient and the VACASK PSS agree on the oscillation frequency within 0.2 % (the VACASK tuning transient within 0.1 %), and the tuning gain from PAC agrees with the slope of the tuning curve within about 2 %.

The phase noise at 1 MHz offset comes 50 % from the core (pair 29 %, varactors 12 %, coil 9 %) and 39 % from the buffer's tail bias (`Rn` 32 %, `MN0` 7 %), the rest from the buffer's devices. Below 1 MHz the tail bias takes over, with 78 % at 300 kHz: its noise passes the 170 kHz low-pass of the bias filters, so its share grows by 40 dB to 48 dB per decade towards lower offsets, against 20 dB for the core. With 3.7 mW in the core that is a figure of merit of -183.6 dBc/Hz.


### Corners

`make sim-corners` runs the start-up transient at the MOS corners SS, TT and FF (the LV and the HV models alike) and at -40 C, 27 C and 85 C, at both ends of the tuning range, `vdd_core` at 0.78 V. Every run oscillates. Post-layout, from `make sim-corners TB=vco_top_tb_tran_lpe` and [`vco_top_tb_tran_lpe_corners.csv`](testbenches/xschem/plot_simulations/figures/vco_top_tb_tran_lpe_corners.csv):

| Corner | Temperature | Frequency, `vtune` 0 V to 1.5 V | Tank nodes | Lowest output | Core current |
| --- | --- | --- | --- | --- | --- |
| TT | -40 C | 19.45 GHz to 21.43 GHz | 0.14 V to 1.39 V | -10.0 dBm | 4.8 mA to 5.0 mA |
| TT | 27 C | 19.52 GHz to 21.46 GHz | 0.16 V to 1.38 V | -10.6 dBm | 4.8 mA to 4.9 mA |
| TT | 85 C | 19.58 GHz to 21.48 GHz | 0.19 V to 1.35 V | -11.3 dBm | 4.7 mA to 4.8 mA |
| SS | -40 C | 19.64 GHz to 21.57 GHz | 0.17 V to 1.35 V | -11.2 dBm | 3.9 mA to 4.2 mA |
| SS | 27 C | 19.71 GHz to 21.60 GHz | 0.20 V to 1.32 V | -12.0 dBm | 3.8 mA to 4.1 mA |
| SS | 85 C | 19.77 GHz to 21.63 GHz | 0.24 V to 1.29 V | -13.2 dBm | 3.6 mA to 4.0 mA |
| FF | -40 C | 19.23 GHz to 21.27 GHz | 0.13 V to 1.43 V | -9.5 dBm | 5.3 mA to 5.7 mA |
| FF | 27 C | 19.30 GHz to 21.30 GHz | 0.15 V to 1.41 V | -10.1 dBm | 5.3 mA to 5.6 mA |
| FF | 85 C | 19.36 GHz to 21.33 GHz | 0.18 V to 1.38 V | -10.8 dBm | 5.2 mA to 5.5 mA |

The output columns are read from the peak-to-peak swing (see [Post-Layout Simulation](#post-layout-simulation)). The post-layout range covers 20 GHz at every corner, and no tank node passes 1.43 V. Schematic, from [`vco_top_tb_tran_corners.csv`](testbenches/xschem/plot_simulations/figures/vco_top_tb_tran_corners.csv):

| Corner | Temperature | Frequency, `vtune` 0 V to 1.5 V | Tank nodes | Lowest output | Core current |
| --- | --- | --- | --- | --- | --- |
| TT | -40 C | 21.66 GHz to 24.35 GHz | 0.08 V to 1.58 V | -7.4 dBm | 4.5 mA to 5.0 mA |
| TT | 27 C | 21.76 GHz to 24.40 GHz | 0.09 V to 1.56 V | -7.9 dBm | 4.5 mA to 4.9 mA |
| TT | 85 C | 21.82 GHz to 24.42 GHz | 0.10 V to 1.54 V | -8.4 dBm | 4.5 mA to 4.8 mA |
| SS | -40 C | 21.92 GHz to 24.54 GHz | 0.08 V to 1.55 V | -7.8 dBm | 4.1 mA to 4.5 mA |
| SS | 27 C | 22.01 GHz to 24.58 GHz | 0.10 V to 1.53 V | -8.3 dBm | 4.1 mA to 4.4 mA |
| SS | 85 C | 22.07 GHz to 24.60 GHz | 0.11 V to 1.50 V | -9.0 dBm | 4.0 mA to 4.3 mA |
| FF | -40 C | 21.39 GHz to 24.15 GHz | 0.07 V to 1.61 V | -7.3 dBm | 4.9 mA to 5.5 mA |
| FF | 27 C | 21.48 GHz to 24.20 GHz | 0.09 V to 1.59 V | -7.7 dBm | 4.9 mA to 5.4 mA |
| FF | 85 C | 21.54 GHz to 24.22 GHz | 0.10 V to 1.56 V | -8.2 dBm | 4.8 mA to 5.3 mA |

Without the leads, the schematic's tank swings higher, up to 1.61 V at FF and -40 C. The macro is centered on the post-layout corners, so `sim-corners` fails on a tank node above 1.5 V only on the post-layout testbench (`VPEAK_MAX`).

Post-layout, `vdd_core` has 30 mV of room either way, which `VCORE` shows. At 0.75 V the slow corner at `vtune` 0 V still starts (the tank swings 0.46 V to 1.02 V at -40 C), at 0.74 V it no longer does at any temperature. At 0.81 V the highest tank node is 1.498 V (FF, -40 C, `vtune` 1.5 V), at 0.82 V it passes 1.5 V at -40 C and 27 C. The frequency pushes by -1.4 GHz/V of `vdd_core` at `vtune` = 0.75 V post-layout, by -1.7 GHz/V in the schematic.


## Directory Structure

<details>
<summary>Show Directory Structure</summary>

```text
📁 vco/
├─ 📁 final/
│  ├─ 📁 gds/
│  ├─ 📁 lef/
│  ├─ 📁 lib/
│  └─ 📁 vh/
├─ 📁 layout/
│  ├─ vco_bias.gds
│  ├─ vco_buf.gds
│  ├─ vco_core.gds
│  ├─ vco_ind.gds
│  ├─ vco_top.gds
│  └─ vco_var.gds
├─ 📁 netlist/
│  ├─ 📁 layout/
│  ├─ 📁 pex/
│  │  └─ vco_top_leads_klayout_pex_3.spice
│  ├─ 📁 schematic/
│  ├─ 📁 spectre/
│  │  └─ vco_ind_le.inc
│  └─ 📁 spice/
│     └─ vco_ind_le.spice
├─ 📁 schematic/
│  └─ 📁 xschem/
│     ├─ vco_bias.sch
│     ├─ vco_bias.sym
│     ├─ vco_bias_pex.sym
│     ├─ vco_buf.sch
│     ├─ vco_buf.sym
│     ├─ vco_buf_pex.sym
│     ├─ vco_core.sch
│     ├─ vco_core.sym
│     ├─ vco_ind.sch
│     ├─ vco_ind.sym
│     ├─ vco_ind_le.sym
│     ├─ vco_ind_lvs.sym
│     ├─ vco_top.sch
│     ├─ vco_top.sym
│     ├─ vco_top_pex.sym
│     ├─ vco_var.sch
│     ├─ vco_var.sym
│     └─ xschemrc
├─ 📁 render/
│  └─ 📁 img/
├─ 📁 scripts/
│  ├─ 📁 layout/
│  │  ├─ vco_bias.py
│  │  ├─ vco_buf.py
│  │  ├─ vco_core.py
│  │  ├─ vco_ind.py
│  │  ├─ vco_layout.py
│  │  ├─ vco_top.py
│  │  └─ vco_var.py
│  ├─ check_boundary.py
│  ├─ check_coil_tap.py
│  ├─ check_mom.py
│  ├─ check_pex_ports.py
│  ├─ drop_subcells.py
│  ├─ momf_lpe.py
│  ├─ netgen_setup.tcl
│  ├─ pex_caps.py
│  └─ sim_corners.py
├─ 📁 testbenches/
│  └─ 📁 xschem/
│     ├─ 📁 models/
│     │  ├─ cornerMOShv.lib
│     │  ├─ sg13g2_svaricaphv_mod.lib
│     │  └─ sg13g2_svaricaphv_mod_mismatch.lib
│     ├─ 📁 plot_simulations/
│     │  ├─ 📁 data/
│     │  ├─ 📁 figures/
│     │  ├─ ngspice2python.py
│     │  ├─ plot_vco_ind.py
│     │  ├─ plot_vco_top.py
│     │  └─ vacask2data.py
│     ├─ vco_ind_tb_acsp_vacask.sch
│     ├─ vco_top_leads.sym
│     ├─ vco_top_lpe.sch
│     ├─ vco_top_lpe.sym
│     ├─ vco_top_tb_pss_vacask.sch
│     ├─ vco_top_tb_tran.sch
│     ├─ vco_top_tb_tran_lpe.sch
│     ├─ vco_top_tb_tune_vacask.sch
│     └─ xschemrc
├─ 📁 verification/
│  ├─ 📁 drc/
│  ├─ 📁 em/
│  │  ├─ 📁 layout/
│  │  │  └─ vco_ind.gds
│  │  ├─ 📁 palace_model/
│  │  │  └─ 📁 vco_ind_data/
│  │  ├─ 📁 s-parameter/
│  │  │  └─ vco_ind.s3p
│  │  └─ 📁 scripts/
│  │     ├─ momf_parasitics.py
│  │     ├─ palace_momf.py
│  │     └─ palace_vco_ind.py
│  └─ 📁 lvs/
├─ Makefile
└─ README.md
```

</details>

The exported views (`final/`) and the layout renders (`render/`) are those of the [inverter](../inverter/README.md#directory-structure). The difference is where a layout comes from: `layout/<cell>.gds` is written by `scripts/layout/<cell>.py`, not exported from a `.klay.gds` drawn by hand.


## Makefile Targets

### Show Available Targets

The default Make target is `help`, so running `make` prints usage and all available targets with short descriptions.

```sh
make
make help
```

All targets that operate on a specific cell accept an optional `CELL=<cellname>` parameter. The default is the top-level cell (`vco_top`).


### PDK Guard

Every target except `help` and `clean` needs the `ihp-sg13cmos5l` PDK and stops at parse time when `$PDK` differs, exactly as in the [inverter](../inverter/README.md#pdk-guard). Switch the PDK with `sak-pdk ihp-sg13cmos5l`.


### Open the Design Files

```sh
make open
make open OPEN_ARGS=--all
```

Opens the design files of this folder in the `sak-open.py` file browser, see [Open the Design Files](../inverter/README.md#open-the-design-files) in the inverter.


### Run Xschem Testbench Simulation

Runs a single Xschem testbench in batch mode: saves the schematic, exports the netlist to `testbenches/xschem/simulations/`, and runs the simulator. The testbench name selects the simulator:

- A name that contains `_vacask` is netlisted in the Spectre format (`xschem set netlist_type spectre`) and run with VACASK.
- Any other name is netlisted in the SPICE format and run with `ngspice -b`, as in the inverter.

```sh
make sim-xschem                              # run the default testbench (vco_top_tb_tran)
make sim-xschem TB=vco_top_tb_pss_vacask     # oscillator PSS, phase noise (PNOISE) and tuning gain (PAC)
make sim-xschem TB=vco_top_tb_tune_vacask    # tuning curve, one transient per tuning voltage
make sim-xschem TB=vco_top_tb_tran_lpe       # start-up transient of the post-layout netlist
make sim-xschem TB=vco_ind_tb_acsp_vacask    # S-parameters of the coil model (ACSP), to compare with the EM result
```

Both simulators write their results as text tables to `testbenches/xschem/plot_simulations/data/`. ngspice does it with `wrdata` at the end of the `.control` block. VACASK does it with its own postprocess hook: the last line of the control block runs [`vacask2data.py`](testbenches/xschem/plot_simulations/vacask2data.py), which turns the rawfile of every analysis into `data/<TB>_<analysis>.txt` with the column layout of `wrdata`, so the same `ngspice2python.loadngspicecol()` reads both. Since the hook is part of the testbench, the Simulate button of the schematic exports the data as well. The control block starts with `abort always`, so a failed analysis stops VACASK with a nonzero exit code instead of leaving old rawfiles behind for the export.

Things that are specific to these testbenches:

- **Two supplies**: `VDD` at 1.5 V and `vdd_core` at 0.78 V, each from its own source (`Vcore` reads `.param Vcore` in ngspice and `var vcore` in VACASK).
- **The coil model is included by every testbench**, `netlist/spice/vco_ind_le.spice` for ngspice and `netlist/spectre/vco_ind_le.inc` for VACASK, which also declares the `inductor` and `mutual` devices it needs. The ACSP testbench of the coil declares `capacitor` as well, because Xschem declares a device only when a symbol of the schematic uses it.
- **ACSP is VACASK's S-parameter analysis.** Each port is a voltage source and its series resistor, which sets the port impedance, and `ports` lists the pairs in port order.
- **The VACASK testbenches read a patched copy of the HV corner file** from `testbenches/xschem/models/`. The PDK's VACASK model of `sg13_hv_svaricap` (`sg13g2_svaricaphv_mod.lib`, which this PDK shares with ihp-sg13g2) keeps an ngspice voltage term `v(2,4)` in its well resistance, which VACASK cannot evaluate. All coefficients of that term are 0, so the copy replaces it by 0 and the model is unchanged. VACASK looks for an include next to the file that names it first, so the copied corner file picks up the patched model next to it and everything else from the PDK.
- **The oscillator PSS runs with `pss_minpts=4000` and `reltol=3e-5`.** At the default 1000 steps per period the shooting Newton cycles without converging. The tighter tolerance is for the bias filters: a node with a 1 us time constant barely changes over one 44 ps period, so the shooting Newton amplifies small integration errors on it into a drift, and at the default `reltol` it settled `vbn_buf` and `vbg_buf` about 70 mV off their DC values, with no error. At `reltol=1e-5` the operating point fails.
- **The PSS starts from `tper=43.9p`, `tstab=6n` and `stabstep=0.5p`.** `tper` sits at the transient's period, 1/22.8 GHz: from a guess 8 % off it, the shooting Newton diverged. `tstab` lets the oscillation build up from the kick of the initial condition. At the default stabilization step, `tper`/4000, the stabilization transient stops at t = 0 with "Timestep too small". `pss_debug=2` prints the Newton history of the shooting, which is how both showed up. The tuning curve uses transients rather than one PSS per tuning voltage, see [Limitations](#limitations).
- **`pnoise` and `pac` run with `tran_fbr=0.02`.** Both integrate one more period around the stored PSS, and VACASK before `7c38094` restarts that integration with a backward-Euler step at every sample of the linearization. The sampled period is then only first-order accurate, and the phase noise and the tuning gain read low below a few MHz: without the option, the phase noise at 1 MHz read 2.7 dB low and the tuning gain from PAC fell from 2.06 GHz/V at 10 MHz to 1.51 GHz/V at 1 MHz. A smaller `tran_fbr` shortens those first-order steps, at about nine times the `pnoise` run time. The option is global, so the `options` line before `pnoise` restates the others. VACASK fixed the cause in `7c38094`, see the discussion of [PR 165](https://codeberg.org/arpadbuermen/VACASK/pulls/165), and the line can go once the image carries it.
- **The ngspice transient sets `rshunt=1e12`.** The varactor model has a node without a DC path, and without the 1 TOhm shunts the operating point takes more than a minute of gmin stepping.
- **Every testbench kicks the oscillation** with an initial condition on the two tank nodes, since the operating point is the symmetric, unstable solution.


### Plot Xschem Simulation Results

```sh
make sim-view-xschem                       # run the default plotting script (plot_vco_top)
make sim-view-xschem SCRIPT=plot_vco_top
make sim-view-xschem SCRIPT=plot_vco_ind      # the coil, same as make view-em-sim
```

[`plot_vco_top.py`](testbenches/xschem/plot_simulations/plot_vco_top.py) plots whatever the testbenches of `vco_top` have written to `data/`: the start-up transients of the schematic and the post-layout netlist, the PSS waveform and output spectrum, the phase noise and the tuning gain from PNOISE and PAC, and the tuning curve, whose frequencies it takes from the zero crossings of the last 0.5 ns of each transient. It also checks the PSS against the tuning transient at the PSS bench's tuning voltage and warns when the two frequencies differ by more than 0.3 %, the symptom of a PSS that settled a slow state wrongly. [`plot_vco_ind.py`](testbenches/xschem/plot_simulations/plot_vco_ind.py) plots the differential inductance and Q and the S-parameters of the coil from the EM result, and from the ACSP testbench next to it once that has run. Both write the figures and CSV files to `testbenches/xschem/plot_simulations/figures/` and open the plot windows when a display is available.


### Simulate All

```sh
make sim-all
```

Runs `vco_top_tb_tran`, `vco_top_tb_pss_vacask`, `vco_top_tb_tune_vacask` and `vco_top_tb_tran_lpe` in sequence. `sim-view-xschem` is not part of it, because it blocks until the plot windows are closed.


### Simulate Over Corners

```sh
make sim-corners                                    # SS, TT, FF at -40 C, 27 C, 85 C, vtune 0 V and 1.5 V
make sim-corners TB=vco_top_tb_tran_lpe             # the same with the post-layout netlist
make sim-corners TB=vco_top_tb_tran_lpe VCORE="0.75 0.81"   # the edges of the vdd_core window
make sim-corners CORNERS=mos_ss TEMPS=-40 VTUNE=0   # one case
```

Netlists the transient testbench `TB` (default `vco_top_tb_tran`) and runs [`sim_corners.py`](scripts/sim_corners.py), which writes one copy of the netlist per MOS corner, temperature, `vdd_core` and `vtune` value into `testbenches/xschem/simulations/corners/`, runs ngspice on four of them at a time, and writes the table `<TB>_corners.csv` to `plot_simulations/figures/`. It fails when a run does not oscillate (a tank swing below 0.5 V) or a tank node passes `VPEAK_MAX`: 1.5 V on the post-layout testbench, which the macro is centered on, and no limit on the schematic one, whose peaks the table still records. The 18 default runs take about 20 seconds, two minutes post-layout.


### Generate the Layouts with KLayout Python Scripts

```sh
make klayout-script CELL=vco_bias     # one cell
make klayout-script-all               # every cell, subcells before the cells that place them
```

Every layout of this macro is written by a KLayout Python script in [`scripts/layout/`](scripts/layout/), run in batch mode, which writes `layout/<CELL>.gds`. Nothing is drawn by hand: to change a layout, change its script, rerun it, and rerun DRC and LVS.

| Script | Cell | Floorplan |
| --- | --- | --- |
| [`vco_ind.py`](scripts/layout/vco_ind.py) | the coil | drawn without a PCell: two octagonal turns of TopMetal1, the crossing on Metal4 and Metal3 with via arrays at both ends, the leads and the center tap down to the lower edge of the keep-out 10 um below the outer turn, the `IND` box with its pins and labels and the no-fill markers, and a `ptap1` for the substrate terminal |
| [`vco_var.py`](scripts/layout/vco_var.py) | the varactor array | three `SVaricap` stacked in a column, each one's bottom gate strip on a Metal2 stub to the `rf_p` bus on the left, its top strip on an equal stub to the `rf_n` bus on the right, both buses on Metal3 8 um off the axis where the core's tank lines run, `vtune` on Metal3 over the well contacts, a substrate tap on three sides |
| [`vco_bias.py`](scripts/layout/vco_bias.py) | bias and enable | the four NMOS gate capacitors on top as two mirrored row pairs that share their tap band, below them an NMOS row (gates up, VSS taps down) and a PMOS row (gates down, VDD taps up) facing a channel of Metal3 tracks, one net each, which the gates and drains reach on Metal2 stubs. `Rg` lies in the channel, the two long filter resistors under the VSS rail, reaching their tracks on Metal4 |
| [`vco_buf.py`](scripts/layout/vco_buf.py) | the output buffer | mirror-symmetric: the tail (30 fingers) at the bottom, its taps also biasing the pair's substrate, the pair above it, the 50 Ohm loads at the sides, the coupling caps on top, each with its plate B fed from above as the input and its plate A facing inward to the gate line, the gate bias resistors outside them |
| [`vco_core.py`](scripts/layout/vco_core.py) | the core | the varactor array as a subcell, a column under the coil's feeds: `rf_p` and `rf_n` as Metal3 lines 2.5 um wide down its whole height, doubled on Metal4 except where the pair's `VSS` bar crosses them, from 6 x 6 via stacks at the feeds, the pair right below the feeds with its cross-coupling on Metal2 (`rf_n`) and Metal3 (`rf_p`) from via rows along its gate pads, the array below it with its buses on the same lines. The center tap's TopMetal1 spine turns right into the middle collector of `Cct1`, which fills the space right of the column, `Cct2` the space right of the buffer. In each array the columns are mirrored in pairs, so the plates on `vdd_core` share one collector in the middle, under a TopMetal1 strap, and the plates on `VSS` face outward. The pair's source bar returns to `VSS` on TopMetal1, down the channel between the column and `Cct1` |
| [`vco_top.py`](scripts/layout/vco_top.py) | the macro | as wide as the coil's keep-out: the coil at the core's origin, the core's column on the axis, the buffer centered under it, the bias on the left, a VSS strap (TopMetal1, 4 um) over a VDD strap (Metal4) along the bottom, `vdd_core` on a TopMetal1 tab with 16 Via3 cuts down to its Metal3 pin, nothing that closes a loop around the coil, the PR boundary with the origin at its lower-left corner |

The macro measures 143 um by 176.9 um, 35 % of it the coil's keep-out, and every region outside it is filled: the bias's capacitor rows beside the core's column, `Cct1` and `Cct2` on the other side. The scripts share [`vco_layout.py`](scripts/layout/vco_layout.py):

- `mos()` builds a transistor with its wiring: a poly strap with contacts joining the gate fingers below the active area and a Metal1 pad reaching 1 um past the device's left edge, the sources up to a Metal1 rail, the drains joined by a Metal2 strap through the middle, and a substrate or well tap under the source rail or apart from it. With `cap=True` it builds a MOS capacitor, every stripe on the rail. The cell scripts place it mirrored or rotated.
- `stub()` and `track()` join a port to a horizontal track, the routing scheme of the bias cell. The bias script checks its stubs for two nets that would touch before it writes anything.
- `comb_feed()` connects one plate of a `cap_cmomf`, see below.
- Every coordinate snaps to the 5 nm grid. A cell is written flat except for the subcells it places (the core keeps the varactor array, the macro keeps bias, core, coil and buffer), so LVS compares the hierarchy of the schematic and cells read from several files cannot clash by name. Each metal is merged into one polygon per connected piece, so no internal outline reads as broken metal.
- Pins are a pin shape (datatype 2) with its label (datatype 25), as in the inverter.

What the scripts had to learn:

- **A KLayout batch script that ends in `SystemExit` exits with code 0 and prints nothing**, so a failed check would leave the old GDS in place. The scripts raise `RuntimeError`, which KLayout reports and `make` stops on.
- **PDK PCells write their terminal names as texts**: `SVaricap` writes `G1`, `G2` and `W` on TEXT, and `ntap1` writes `well` on the NWell layer. KLayout LVS names a net after each of them, and a net with a second name fails its strict port check, while Magic, and so KPEX, turns the NWell text into a dangling port. The cells drop the texts once they are flat (`write(drop_texts=...)`).
- **The resistor PCells compute a dimension from R by default** (`Calculate`), so the scripts pass `Calculate="R"` to keep the drawn width and length.
- **The buffer's tail is drawn as one device with 30 fingers.** KLayout LVS does not combine parallel devices (`m`) with a multi-finger device, so the schematic says `w=150u ng=30`.
- **Two `ptap1` taps that abut put their contact rows 0.1 um apart**, which fails `Cnt.b`. The capacitor rows' taps keep 0.3 um between them, and one Metal1 band covers both.
- **The pair's ground path is part of the circuit.** On Metal4 alone, the path from the pair's source bar around `Cct1` and `Cct2` to the `VSS` pin was 16 Ohm in the post-layout netlist, which put the sources 64 mV above `VSS` at 4 mA. A TopMetal1 return down the free channel beside the column, along under `Cct1` and down `Cct2`'s outer collector, and a TopMetal1 strap of 4 um along the macro's bottom edge brought it to 1.7 Ohm from the pin to the sources.
- **At 20 GHz the leads are part of the tank.** The coil's own series resistance is 2.05 Ohm per side, and with every resistance extracted (see [Parasitic Extraction (PEX)](#parasitic-extraction-pex)) the first layout had 41 Ohm and 23 Ohm in the pair's gate lines, one via of 9 Ohm per level, 3.5 Ohm from the coil's feed to the varactors over 1 um of Metal3, and 3.8 Ohm in the supply path of `vdd_core` through four Via3 cuts. That VCO did not start at the slow corner. Via rows along the gate pads, the tank lines at 2.5 um and doubled on Metal4, 6 x 6 via stacks at the feeds and 16 cuts under `vdd_core` brought these to 4.4 Ohm, 1.4 Ohm and 1.7 Ohm, the pair's drains to 1.6 Ohm.

Four details of `cap_cmomf`, the only capacitor of this PDK besides the MOS gate:

- **Its plates are combs on every metal from `mmin` to `mmax`, and a wide conductor may not merge onto them.** Merged onto a comb, a wide feed turns the PCell's own 0.21 um gaps into a wide-metal spacing violation. `comb_feed()` feeds a plate through the edge band it owns, with bridges 0.35 um wide (under the 0.39 um wide-metal threshold) from a collector 0.3 um outside the cap. Plate A owns the west face and the south spine, plate B the east face and the north spine, so the face chooses the plate.
- **KLayout LVS orders its two terminals by the x position of their pins**, so a unit mirrored in x has its terminals swapped against one placed as drawn, and the deck does not combine the two. The schematic splits every array by orientation (`Cct1a` as drawn, `Cct1b` mirrored) so that each group combines on its own.
- **The deck compares neither `w` nor `l`, and `mmin` and `mmax` never reach the LVS netlist**, so a schematic at the wrong size or stack still matches, while the model's density runs from 0.61 fF/um2 to 1.29 fF/um2 over the stacks. [`check_mom.py`](scripts/check_mom.py) closes the gap: it compares the extent and the metals of every `cap_cmomf` marker of a cell with the instances of its schematic, and `make check-mom CELL=<cell>` runs it on the buffer and the core.
- **Magic draws it but extracts no device for it**, so Magic LVS of the buffer reruns Netgen with [`netgen_setup.tcl`](scripts/netgen_setup.tcl), the PDK setup plus `ignore class "-circuit2 cap_cmomf"`. The `sak-lvs.sh` run before it reports LVS errors for that reason and does not stop `make` for the cells in `MOM_CELLS`.

Three details of the coil:

- `d` is the inner diameter: 50 um gives the 74 um outer diameter. The `IND` box, the coil's keep-out, keeps 10 um around the outer turn, 94 um by 94 um, and the leads and the tap cross it to its lower edge: `LA` and `LB` at x = -8 um and 8 um, `LC` at x = 0, all on TopMetal1, their pins and labels 1 um below the box. The `inductor3` PCell of ihp-sg13g2 keeps 30 um, which made the leads 31 um long here, 24 pH of the coil's differential inductance and 40 um of the macro's height, and kept the pair and the varactors that far from the windings. The deck has no rule on the margin. The box also carries the no-fill markers `NoMetFiller` (160/0), `Activ.nofill` and `GatPoly.nofill`: a fill tile in the coil's field is a shorted turn, and the metal filler reads only the first of them.
- **KLayout LVS extracts the coil from its `IND` box as an `inductor` from `LA` to `LB`** with the substrate as third terminal, and with `w`, `s`, `d` and `nr_r` read from the drawn geometry, which [`vco_ind_lvs.sym`](schematic/xschem/vco_ind_lvs.sym) repeats. It puts the device into the top cell of the run, whatever cell holds the coil: with the coil inside the core, the core's own run found it there, but the macro's run moved it out of the core, so no one schematic hierarchy matched both. So `vco_top` places the coil beside the core, and the `ptap1` ties the substrate terminal to `VSS`.
- **No LVS sees the center tap.** Inside the `IND` box Metal3, Metal4 and TopMetal1 are device core and not conductors, so the tap ends at the box edge in every extracted netlist. [`check_coil_tap.py`](scripts/check_coil_tap.py) proves it on the GDS with plain connectivity: the winding is one net, the tap that crosses the box edge between the leads is on it, the substrate tap is not, a cut at x = 0 splits the coil into two halves with one half of the tap each, and the halves are mirror images in projection. `--self-test` plants a tap that is open, off center and on two shorted turns, and fails unless each is caught. `make check-coil-tap` runs it on `vco_ind` and with `--feed vdd_core` on `vco_top`, where `vdd_core` has to reach the coil through the tap and only through it.


### EM Simulation of the Coil

```sh
make sim-em                 # EM layout, Palace model, solve, Touchstone files
make copy-sparam            # copy the result to verification/em/s-parameter/vco_ind.s3p
make view-em-sim            # plot L, Q and the S-parameters, against the model once the ACSP testbench has run
make em-model               # sim-em, copy-sparam, snp2le and the ACSP testbench in one go
make sim-em NP=8            # more MPI processes
```

`sim-em` runs [`palace_vco_ind.py`](verification/em/scripts/palace_vco_ind.py), which builds two things from `layout/vco_ind.gds` with gds2palace:

- **The EM layout** `verification/em/layout/vco_ind.gds`: the coil metals (Metal3, Via3, Metal4, TopVia1, TopMetal1) and a Metal1 ground as in the inductor synthesis example of the PDK's Palace flow, a 20 um wide frame half a coil diameter away from the windings and a tongue from the frame up under the three feeds. The ports are 50 Ohm lumped ports, vertical sheets from the tongue up to TopMetal1 at the lower end of each feed pin: port 1 at `LA`, port 2 at `LB`, port 3 at the center tap `LC`, the port order of snp2le's `inductor-ct`. The script reads the coil's diameter and pins from the layout, so it follows a change of the coil.
- **The Palace model** in `verification/em/palace_model/vco_ind_data/`: the stackup `SG13CMOS5L_200um.xml` with its 200 um lossy substrate, a sweep from 0 Hz to 60 GHz in 0.75 GHz steps to cover the third harmonic (gds2palace replaces 0 Hz by 10 MHz and 20 MHz), Palace's adaptive frequency sweep, third-order elements, 3 um cells along the conductors and 2 um cells inside the coil metals. This PDK has no Palace flow of its own: the stackup and the scripts come from `libs.tech/palace` of ihp-sg13g2, which carries the SG13CMOS5L stackup, so the `Makefile` reads them from `$PDK_ROOT/ihp-sg13g2` (`PALACE_SCRIPTS`) and the script names the stackup's PDK (`STACKUP_PDK`).

Palace solves the model, and `combine_extend_snp.py` of the PDK writes `vco_ind.s3p` and three variants of it to `output/vco_ind/`: `_dc` with an extrapolated DC point, and `_deembedded` with the inductance of the vertical ports subtracted. `copy-sparam` takes the raw file, because the vertical port stands for the via stack down to the transistors, which the coil sees in the circuit as well.

**The metals are volumes.** gds2palace models a metal either as a hollow shell with a surface impedance (`surface`, its default) or as a solid with the bulk conductivity of the stackup (`volume`). The coil's traces are 4 um wide and 2 um thick, the case where the surface model is least accurate: it applies the surface impedance to the side walls as well and so counts them as extra cross-section. The study of the ihp-sg13g2 macro on its first coil showed it at 10 MHz: the surface model gave 1.65 Ohm, less than the 1.72 Ohm of the traces alone, and the volume model 2.93 Ohm. Two more settings came out of it:

- `fill_factor_correction`: gds2palace merges each via array into one block to keep the mesh small. Without the correction a block has the resistance of a solid via of its size, much less than that of its vias.
- Third-order elements, with 2 um cells inside the coil metals (Metal3, Metal4 and TopMetal1). Second-order elements with 1 um cells read the coil's Q 2.0 % lower at 20.25 GHz (0.7 % at 10 GHz, 3.4 % at 60 GHz) and its L 0.4 % lower, while halving those cells to 0.5 um moved Q by 1.6 % in that study: the element order, not the cell, limited the second-order result. The skin depth of TopMetal1 at 20 GHz is 0.68 um. Third order with 1 um cells did not fit into 15 GB of memory.

The committed coil gives 380.5 pH, 4.10 Ohm and Q 11.8 at 20.25 GHz, 2.56 Ohm at 10 MHz. The sweep took 2.9 hours with `NP=6` and 7.2 GB of memory, 20 minutes at second order. The EM layout, the Palace configuration, its outputs and the Touchstone file are committed. The mesh `vco_ind.msh` is not, `sim-em` rebuilds it in a few seconds.


### Lumped-Element Model of the Coil

Fits a lumped-element model to the S-parameters of a passive with [snp2le](https://github.com/iic-jku/snp2le) and writes it for both simulators, `netlist/spice/<EM>_le.spice` (ngspice) and `netlist/spectre/<EM>_le.inc` (VACASK). The `.SUBCKT` name is the file stem, which is also the name of the symbol that instantiates it (`vco_ind_le.sym`).

```sh
make snp2le                                   # fit verification/em/s-parameter/vco_ind.s3p
make snp2le SNP=<file.sNp>                    # fit another Touchstone file
make snp2le EM=<structure> SNP=<file.sNp> LE_MODEL=universal ORDER=8
```

- `EM` names the structure and the output files (default: `vco_ind`).
- `SNP` is the Touchstone file (default: `verification/em/s-parameter/<EM>.s3p`, written by `make copy-sparam`).
- `LE_MODEL` is an snp2le structure, `inductor-ct` for a center-tapped coil (default), `inductor-wideband` or `inductor-pi` for a two-port coil, or `universal` for a vector fit of order `ORDER` (default: 6).

The committed model is fitted with the defaults to the EM result of the drawn coil: two coil segments per half, peak differential Q 15.9 at 48.8 GHz against 16.4 at 51.0 GHz in the data. `make sim-xschem TB=vco_ind_tb_acsp_vacask` and `make view-em-sim` compare it with the EM data. From 1.5 GHz to 40 GHz the model is within 2.3 % of the EM inductance and within 4.3 % of its Q. At 20.25 GHz it is 1.6 % high in inductance (386.5 pH against 380.5 pH), which lowers the oscillation frequency by about 0.8 %, and 4.1 % low at 60 GHz.


### EM Simulation of the MoM Caps

```sh
make sim-em-momf            # EM fixtures, Palace models and solves of the caps in LEADS_CUT_GEOS, then the parasitics table
make sim-em-momf NP=32      # more MPI processes, on a compute host
```

The `cap_cmomf` model is a capacitance only. The target simulates the geometries in `LEADS_CUT_GEOS`: the buffer's coupling caps, 10 um by 18.6 um on Metal2 to Metal4, which the tank sees. The decoupling caps `Cct1` and `Cct2` need no EM, since no spec depends on their parasitics. [`palace_momf.py`](verification/em/scripts/palace_momf.py) cuts the first cap of a geometry out of `layout/vco_top.gds`, with the two feeds that drive its plates, and joins the feeds with two Metal4 leads at an in-plane port. Three fixtures per geometry de-embed the leads and the feeds (open-short): the cap as drawn (`dut`), the feeds alone (`open`), and the comb replaced by solid metal on every level of its stack (`short`). The models use third-order elements, volume metals and 0.3 um cells along the conductors, about the finger pitch, and solve 10 GHz and 20 GHz. [`momf_parasitics.py`](verification/em/scripts/momf_parasitics.py) takes the series resistance from the real part of the de-embedded impedance at 20 GHz, the series inductance and the capacitance from its imaginary part at both frequencies, and the capacitance of each plate to the substrate from a C-coupled Magic extraction of the cap and its feeds alone, from the area and fringe terms, which magic#557 does not touch. It writes `verification/em/cap_cmomf_parasitics.json`, which `klayout-pex-leads` reads (see [Parasitic Extraction (PEX)](#parasitic-extraction-pex)).

The combs make the meshes large: 288 thousand tetrahedra for the buffer's cap, about 40 GB of memory at third order by the scaling from a unit of `Cct2`, whose 978 thousand and 18 million unknowns took 139 GB within minutes. So the target runs on a compute host. Each fixture and its mesh build in a few minutes.


### Layout, Verification and Build

The verification and build targets are those of the [inverter](../inverter/README.md): `klayout-drc`, `magic-drc`, `klayout-lvs`, `magic-lvs`, their `*-lvs-netlist` exporters, `symbol-pex`, `klayout-pex`, `magic-pex`, `klayout-verify`, `magic-verify`, `check-boundary`, `lef`, `lib`, `verilog`, `copy-gds`, `render-gds` and `build-top`, plus `check-mom`, `check-coil-tap` and `klayout-pex-leads`. As in the inverter, `klayout-verify` runs DRC and LVS and `magic-verify` DRC, LVS and PEX. What runs on which cell:

| Cell | KLayout | Magic |
| --- | --- | --- |
| `vco_bias` | DRC, LVS | DRC, LVS, PEX |
| `vco_buf` | DRC, LVS, `check-mom` | DRC, LVS without the `cap_cmomf`, PEX |
| `vco_var` | DRC, LVS | DRC |
| `vco_ind` | DRC, LVS, `check-coil-tap` | DRC |
| `vco_core` | DRC, LVS, `check-mom` | DRC |
| `vco_top` | DRC, LVS, `check-coil-tap` of the `vdd_core` feed, PEX without the coil and the varactor array (`klayout-pex-leads`) | DRC, PEX for the pin list of the Verilog stub |

`klayout-verify-all` and `magic-verify-all` run exactly that. The gaps have three reasons:

- **Magic extracts `sg13_hv_svaricap` as two two-terminal halves** and extracts no device for the coil or for `cap_cmomf`, so Netgen cannot compare a cell that holds the varactor or the coil, and compares the buffer without its coupling caps.
- **KPEX cannot read Magic's extraction of the varactor.** Magic writes it as a `veriloga` device, and KPEX's parser of the `.ext` file stops on `'veriloga' is not a valid DeviceType`. Every cell above the array inherits it.
- **A parasitic extraction of a cell that contains the coil is not its RF model.** RC extraction misses the coil's inductance and its coupling, and Magic's view of the coil's metal shorts `rf_p`, `rf_n` and `vdd_core`. The coil's model is its EM simulation.

`make build-top` checks the PR boundary and writes the LEF, the Liberty stub, the Verilog stub (from the Magic PEX netlist of `vco_top`), the GDS in `final/` and the renders.


### Parasitic Extraction (PEX)

`magic-pex` and `klayout-pex` are those of the inverter, see [Parasitic Extraction (PEX)](../inverter/README.md#parasitic-extraction-pex), with the same `EXT_MODE` and the same three full-RC parameters. Two things differ.

**The full-RC parameters are ten times finer**: `THRESHOLD=1000` (1 Ohm), `MINRES=100` (0.1 Ohm) and `MINDELAY=0`, so that `THRESHOLD` also gates the extracted resistance. At Magic's defaults, the inverter's 10 Ohm, 1 Ohm and 1 ps, every net of the VCO except `VSS` came out without resistance, the tank leads, the gate lines of the pair and the supply path of `vdd_core` among them. At 20 GHz the coil's own series resistance is 2.05 Ohm per side, so a lead of 1 Ohm is a part of the tank. `klayout-pex` and `klayout-pex-leads` pass the same three values to KPEX (`--magic_thresh`, `--magic_minres`, `--magic_mindel`).

**The post-layout netlist is one extraction of the whole macro**, without the two parts that have models of their own:

```sh
make klayout-pex-leads                                   # netlist/pex/vco_top_leads_klayout_pex_3.spice
make klayout-pex-leads THRESHOLD=10000 MINRES=1000 MINDELAY=1   # Magic's defaults, to compare
```

- [`drop_subcells.py`](scripts/drop_subcells.py) writes `vco_top` without the coil and the varactor array, with a port where each of their pins lands on the metal that remains: `vco_ind_LA`, `vco_ind_LB` and `vco_ind_LC` at the coil's feeds, `vco_var_rf_p` and `vco_var_rf_n` at the middle of the array's buses, `vco_var_VSS` at its substrate tap. Magic keeps such a label as a port of its own, joined to the net's other ports by the extracted resistance, so the coil model and the array attach where they really connect, and the extraction keeps everything between them and the macro's pins. The array's `vtune`, which carries no current, and the coil's substrate tap, for which its model has no terminal, get no port (`LEADS_SKIP`).
- **A net without a resistor network keeps one of its ports.** Magic builds no network on a net without a device that carries current, at any threshold, and then keeps one of its ports and leaves the others unconnected. Here that would be `vdd_core` if the combs of `Cct1` and `Cct2` were cut out (see below). `drop_subcells.py` records which pins share a net in the layout (`--ties`), and [`pex_caps.py`](scripts/pex_caps.py) joins such a port to its net through 1 mOhm. [`check_pex_ports.py`](scripts/check_pex_ports.py) fails on any port that is still unconnected.
- **The capacitances come from a C-coupled run of the same layout.** Magic's `extresist` counts the coupling capacitance of a net that gets a resistor network a second time, as capacitance to the substrate on the network's nodes (magic#557). In this macro, that is the 153 fF coupling caps of the buffer on the tank nets: the full-RC run has 4.78 pF in all, the C-coupled run of the same layout 4.43 pF, and the 0.35 pF more sit mostly between the tank nodes and `VSS`, where the C-coupled run has 17 fF and 23 fF. `klayout-pex-leads` runs KPEX twice, and [`pex_caps.py`](scripts/pex_caps.py) keeps the resistors and devices of the full-RC netlist and scales its capacitors per net pair to the C-coupled totals. A full-RC and a C-coupled run of the core alone, without the buffer's coupling caps, agree within 0.2 %.
- **The extraction runs in KPEX, not in `sak-pex.sh`.** `sak-pex.sh` hits the same double count in full RC, and its C-coupled run leaves out the substrate capacitance of the tank nets altogether (0 fF from `rf_p` to `VSS` where KPEX finds 17 fF), so it cannot serve as the reference either. The cell netlists of `magic-pex` (bias and buffer) are verification outputs that no testbench reads.
- **The buffer's coupling caps can go back in as PDK devices.** Magic extracts no `cap_cmomf` device and reads its comb as plain metal (magic#552), so the capacitance of the combs in the netlist is Magic's estimate of the metal, not the PDK model: 152.6 fF for each coupling cap of the buffer against 170.2 fF by the model, and 3.69 pF for `Cct1` and `Cct2` against 3.79 pF. The tank sees the coupling caps, so with `LEADS_CUT` set to `99/40 momf`, `drop_subcells.py` cuts their combs (`LEADS_CUT_GEOS`) out of the `Recog.momf` markers and leaves a port on each of the two feeds, and [`momf_lpe.py`](scripts/momf_lpe.py) puts the PDK `cap_cmomf` back between them at the drawn size, with the series resistance and inductance of the comb and the capacitance of each plate to `VSS` from the table of [EM Simulation of the MoM Caps](#em-simulation-of-the-mom-caps) (`LEADS_PARASITICS`). The ports become internal nodes, so the pins of `vco_top_leads.sym` stay as they are. That table needs an EM run on a compute host, so `LEADS_CUT` is empty until it exists. The combs of `Cct1` and `Cct2` stay metal: 3 % off the model does not matter for decoupling, and cut out they would leave `vdd_core` without a device in the extraction, so without a resistor network, its routing from the pin to the center tap one node as in the ihp-sg13g2 macro.
- The pins of the netlist are reordered to [`vco_top_leads.sym`](testbenches/xschem/vco_top_leads.sym), the symbol [`vco_top_lpe`](testbenches/xschem/vco_top_lpe.sch) places, see [Post-Layout Simulation](#post-layout-simulation).


### Post-Layout Simulation

`vco_top_tb_tran_lpe` is `vco_top_tb_tran` around [`vco_top_lpe`](testbenches/xschem/vco_top_lpe.sch): the extraction of the whole macro without the coil and the varactor array (`make klayout-pex-leads`, see [Parasitic Extraction (PEX)](#parasitic-extraction-pex)), the coil's EM model at the coil's feeds, and the array's schematic at the middle of its buses. What the extraction misses is the routing inside the varactor array. And Magic puts the coupling capacitance of a net on one node of its resistor network, here the coupling caps of the buffer at the coil's feeds, so the resistance of the lines down to the buffer is not in series with them.

| TT, 27 C, `vtune` = 0.75 V | Schematic | Post-layout |
| --- | --- | --- |
| Frequency | 22.72 GHz | 20.21 GHz |
| Tuning range, `vtune` 0 V to 1.5 V | 21.76 GHz to 24.40 GHz | 19.52 GHz to 21.46 GHz |
| Tank nodes | 0.11 V to 1.53 V | 0.20 V to 1.33 V |
| Output, from the peak-to-peak swing | -7.7 dBm | -10.2 dBm |
| `vdd_core` current | 4.79 mA | 4.89 mA |
| `VDD` current | 6.31 mA | 5.62 mA |

Both columns are the same ngspice transient, so the output here is read from the peak-to-peak swing, which counts the harmonics and reads about 1 dB above the fundamental of the PSS.

- **The frequency falls by 11 %**, through the capacitance of the buffer's inputs, which the tank sees through the coupling capacitors, and of the leads: 17 fF from `rf_p` and 23 fF from `rf_n` to `VSS`. The 5.5 fF that `rf_n` has more come from the `VSS` return beside its line, 2 % of the capacitance of a tank node.
- **The swing is smaller** because the resistance of the leads adds to the coil's own 2.05 Ohm per side: from the coil's feed 1.4 Ohm to the varactors, 1.6 Ohm to the pair's drains and 4.4 Ohm to its gates, 1.7 Ohm from the `VSS` pin to the pair's sources and 1.7 Ohm from the `vdd_core` pin to the center tap. The varactors carry the largest share of the tank current, most at `vtune` 0 V, so the slow corner there is the one that starts last.
- **The macro is centered on this simulation.** The coil's diameter and the length of its leads put the post-layout frequency at 20 GHz in the middle of the tuning range, and `vdd_core` sits in the middle of the post-layout window, see [Corners](#corners).

The first post-layout simulation of this macro extracted the leads at Magic's default thresholds, which left every net but `VSS` without resistance: it showed 19.82 GHz and the tank at 0.12 V to 1.31 V with a coil of 415 pH and `vdd_core` at 0.72 V. With every resistance in, that layout did not start at the slow corner. The leads were redrawn (see [What the scripts had to learn](#generate-the-layouts-with-klayout-python-scripts)), the coil got 10 um of keep-out instead of 30 um and an inner diameter of 50 um instead of 52 um, 380 pH, and `vdd_core` moved to the middle of its post-layout window, 0.78 V.


### Verify, Build and Simulate All

```sh
make all
```

Runs `klayout-script-all`, `klayout-verify-all`, `magic-verify-all`, `build-top` and `sim-all`: the inverter's chain, which first writes the layouts from their scripts. It takes about 6 minutes. The EM simulation of the coil and the corners are not part of it, see [EM Simulation of the Coil](#em-simulation-of-the-coil) and [Simulate Over Corners](#simulate-over-corners).


### Clean

`make clean` deletes the generated files: `final/`, `netlist/schematic/`, `netlist/layout/`, `netlist/pex/`, `render/img/`, the DRC and LVS reports, the Xschem `simulations/` folders and the `plot_simulations/` outputs. The EM results in `verification/em/` and the lumped-element models in `netlist/spice/` and `netlist/spectre/` stay, because an EM run of the coil takes hours.

> [!WARNING]
> Most of these outputs are committed in this repository, so `make clean` leaves a deletion set in `git status`. Run `git restore .` to get them back if you did not mean to remove them.


## Limitations

This VCO is kept simple on purpose. These are the places where it falls short, and what a better design would change:

- **Phase noise** is -102.2 dBc/Hz at 1 MHz. Published 130 nm CMOS LC VCOs from 20 GHz to 27 GHz measure -102 dBc/Hz to -113 dBc/Hz [[1]](#references)[[3]](#references)[[4]](#references)[[5]](#references), Jung and Park -113 dBc/Hz at 26.9 GHz with a resonator Q of 19 [[1]](#references). The tank sets the limit here: the coil's Q is 11.8, against the microstrip resonator of the paper, and the paper's own comparison shows a symmetric spiral as good as its microstrip only up to 22.4 GHz. Wider traces and fewer turns raise the coil's Q, and in this process the only thick metal is the 2 um TopMetal1. After the tank, the buffer's tail bias is the largest contributor (39 %), and below 1 MHz the largest of all, which a larger filter capacitor or a bias of the buffer that does not change its input capacitance would remove. The phase noise is simulated on the schematic only, see the last point.
- **`vdd_core` is a noise input.** The tank's common mode is `vdd_core`, which is also the varactor's operating point, so noise on `vdd_core` moves the frequency by -1.4 GHz/V at `vtune` = 0.75 V post-layout, close to the tuning gain. The pad supply has to be as quiet as `vtune`. The paper measured with a laboratory supply. An on-chip regulator would bring its own noise into the same path.
- **The core current is not defined.** With no current source, it follows the process and the temperature (3.6 mA to 5.7 mA at 0.78 V over the post-layout corners), and `vdd_core` has only 30 mV of room either way between no start at SS and an overstressed tank at FF, see [Corners](#corners). A per-die trim of `vdd_core` is the way a voltage-biased oscillator is usually set up.
- **The `cap_cmomf` model is a capacitance only**: an area density, no series resistance of its fingers and no substrate capacitance. The schematic sees neither. The post-layout simulation sees both through Magic's extraction of the combs, which also sets their capacitance, 10 % below the model on the buffer's caps, until the EM of the buffer's caps has run and `LEADS_CUT` puts the PDK device in there, see [Parasitic Extraction (PEX)](#parasitic-extraction-pex). KLayout LVS checks the caps' connections but not their size, which `check-mom` does.
- **The oscillator PSS is fragile.** It needs `pss_minpts=4000`, `reltol=3e-5` and a period guess at the transient's (see the testbench notes), it converges at the nominal tuning voltage but not at every one, which is why the tuning curve uses transients, and a slow state can settle wrong without an error, which the plot script's check against the transient catches.
- **PNOISE and PAC need care at low offsets.** With `tran_fbr=0.02` (see the testbench notes) the tuning gain from PAC is flat within 2 % from 100 MHz down to 180 kHz (2.07 GHz/V), and the phase noise follows its sources: 20 dB per decade above 3 MHz, steeper below, where the filtered bias noise takes over. Below about 100 kHz the tuning gain falls again (0.56 GHz/V at 10 kHz) and the phase noise flattens, a limit that moves down with a finer time step of the period. So read the phase noise from about 100 kHz up, and check it against a transient-noise simulation. With `oscillator=1`, `pnoise` computes the noise as for a driven circuit, so it is the total noise, phase and amplitude, which close to the carrier is the phase noise.
- **The post-layout simulation is a transient.** VACASK does not read the SPICE netlists of the extraction without a translation, so the post-layout phase noise is not simulated, and the varactor array's own routing is not extracted.


## Status

The macro is built in steps, each one reviewed before the next:

- [x] Folder structure, `Makefile` and `README.md`
- [x] Schematics of all cells, LVS netlists exported for KLayout and Magic
- [x] Testbenches: start-up transient (ngspice), oscillator PSS with PNOISE and PAC, and the tuning curve (VACASK)
- [x] Layout of the coil, drawn by a KLayout Python script in TopMetal1, DRC and LVS clean, its center tap checked on the GDS
- [x] EM simulation of the drawn coil with Palace (gds2palace, volume metals) and its snp2le model, checked with ACSP
- [x] Layout of every cell as a KLayout Python script, DRC and LVS clean with KLayout, the cells Magic can compare clean with Magic, PEX of the bias and the buffer, the `cap_cmomf` sizes checked against the schematics
- [x] Core after Jung and Park [[1]](#references): voltage-biased pair on its own supply `vdd_core`, buffer bias filters, compact layout
- [x] Post-layout simulation of the whole macro: KPEX with every resistance above 1 Ohm, ports where the coil and the varactor array connect, the capacitances from a C-coupled run (magic#557), the EM model of the coil
- [x] Tank leads redrawn for the extracted resistance, and the macro centered on the post-layout simulation: coil keep-out and diameter, `vdd_core` at 0.78 V
- [x] Corners (SS, TT, FF, -40 C to 85 C, both ends of the tuning range, the `vdd_core` trim range)
- [ ] The buffer's coupling caps as PDK devices with their EM parasitics in the post-layout netlist: the tooling is in place (`drop_subcells.py --cut`, `momf_lpe.py`, `make sim-em-momf`), the EM runs on a compute host
- [x] Port from ihp-sg13g2, see [Porting from ihp-sg13g2](#porting-from-ihp-sg13g2)
- [ ] Enable and power-up transient
- [ ] More RF analyses: transient noise as the cross-check of PNOISE, the post-layout phase noise, HB, HBAC and HBNOISE on the buffer, ACSP of the buffer
- [ ] Layouts by other methods for the tutorial: hand-drawn in KLayout, generated with GDSFactory
- [ ] Chip integration: an analog pad for `vdd_core`, the 20 GHz output needs RF pads or a divider to an existing pad, and the coil occupies TopMetal1, the top layer of the chip power grid
- [x] Tutorial chapter after the analog macro


## Porting from ihp-sg13g2

The circuit, the device sizes, the testbenches and the flow are those of the VCO of the ihp-sg13g2 template. The MOS, varactor and resistor models of this PDK are those of ihp-sg13g2. What had to change is what SG13CMOS5L does not have:

| ihp-sg13g2 | ihp-sg13cmos5l | Where |
| --- | --- | --- |
| `inductor3` PCell, windings in TopMetal2 (3 um), underpass in TopMetal1, 52 um inner diameter, keep-out 30 um | an octagon drawn by a script, windings in TopMetal1 (2 um), crossing on Metal4 and Metal3, 50 um inner diameter, keep-out 10 um | [`vco_ind.py`](scripts/layout/vco_ind.py) |
| `inductor3` device in `vco_core` for LVS, its center tap a pin | `inductor` device beside the core in `vco_top`, the center tap checked on the GDS | [`vco_ind_lvs.sym`](schematic/xschem/vco_ind_lvs.sym), [`check_coil_tap.py`](scripts/check_coil_tap.py) |
| MIM coupling caps of 150 fF | `cap_cmomf` on Metal2 to Metal4, 10 um by 18.6 um, 153 fF extracted | `vco_buf` |
| `Cct1` and `Cct2`, 4.9 pF of MIM | six `cap_cmomf` units on Metal1 to Metal4, 3.8 pF | `vco_core` |
| `VSS` on Metal5 bars and a Metal5 strap under a TopMetal2 strap | Metal4 bars, a TopMetal1 return from the pair and a TopMetal1 strap | `vco_core`, `vco_top` |
| `SVaricap` with nBuLay, `Nx=7` | `SVaricap` with ThickGateOx, the same model, `Nx=8` | `vco_var` |
| Palace stackup `SG13G2_200um.xml` | `SG13CMOS5L_200um.xml` from the ihp-sg13g2 tree | [`palace_vco_ind.py`](verification/em/scripts/palace_vco_ind.py), `Makefile` |
| PSS from `tper=44.3p` | `tper=43.9p` | `vco_top_tb_pss_vacask` |
| Magic LVS of the buffer with Netgen's PDK setup | a Netgen rerun without `cap_cmomf` | [`netgen_setup.tcl`](scripts/netgen_setup.tcl), `Makefile` |

Both macros are centered on their post-layout simulation, each with its own means. The coil drawn here has 380.5 pH and a Q of 11.8 at 20.25 GHz, its short leads and smaller diameter take 9 % off the 417 pH and Q 10.6 of the TopMetal2 coil of ihp-sg13g2 (still at second order there, see its README). That `inductor3` keeps its 30 um keep-out and draws no clean octagon below 51 um at this width and spacing, so ihp-sg13g2 is centered with smaller varactors instead (`Nx=7`, 12 % less tuning gain). Post-layout, this macro oscillates at 20.21 GHz with `vdd_core` at 0.78 V, the one of ihp-sg13g2 at 20.06 GHz with 0.79 V, and both start at every corner. The decoupling of `vdd_core` is a quarter smaller here, and the macro is 143 um by 176.9 um, 38.6 um shorter than the one of ihp-sg13g2.


## Start a New RF Macro from This One

`make macro FROM=vco NAME=<name>` in [`macros/`](../) copies and renames this macro as for the other two, see [Start a New Macro from an Existing One](../README.md#start-a-new-macro-from-an-existing-one).


## References

1. D. Y. Jung and C. S. Park, "Power efficient Ka-band low phase noise VCO in 0.13 um CMOS", Electronics Letters, vol. 44, no. 10, May 2008, [doi:10.1049/el:20080527](https://doi.org/10.1049/el:20080527).
2. A. Hajimiri and T. H. Lee, "Design issues in CMOS differential LC oscillators", IEEE Journal of Solid-State Circuits, vol. 34, no. 5, pp. 717-724, May 1999, [doi:10.1109/4.760369](https://doi.org/10.1109/4.760369).
3. M. Hossain and A. Chan Carusone, "20 GHz low power QVCO and de-skew techniques in 0.13 um digital CMOS", IEEE Custom Integrated Circuits Conference, pp. 447-450, 2008, [doi:10.1109/CICC.2008.4672117](https://doi.org/10.1109/CICC.2008.4672117).
4. J.-H. Song, B.-S. Kim and S. Nam, "A 24 GHz transformer coupled CMOS VCO for a wide linear tuning range", IEICE Transactions on Electronics, vol. E96-C, no. 10, pp. 1348-1350, 2013, [doi:10.1587/transele.E96.C.1348](https://doi.org/10.1587/transele.E96.C.1348).
5. M. Toermaenen and H. Sjoeland, "A 24 GHz VCO with 20 % tuning range in 130-nm CMOS using SOP technology", IEEE Radio Frequency Integrated Circuits Symposium, pp. 423-426, 2009.
