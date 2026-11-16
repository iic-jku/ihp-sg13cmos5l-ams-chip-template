# Ring Oscillator

The three-stage ring oscillator [`ringosc`][macro] of `ef8524f`, with an output buffer, on its own supply `vdd_ro`. It has no enable: 0 V on `vdd_ro` turns it off.


## Connections

| Pin | Signal | Path | Connect to |
| --- | --- | --- | --- |
| 22 | `vdd_ro` | `padbare` | source meter |
| 23 | `ro_vout` | `padbare` | spectrum analyzer, frequency counter or scope |


## Results

The simulated values are CACE runs of the schematic with 100 fF on `vout`: the typical point at `tt` and 1.5 V, then the spread over 200 Monte Carlo iterations at 1.5 V and over five MOS corners at 1.35 V to 1.65 V. The output buffer runs from `vdd_ro` as well, so the measured current includes the buffer charging the pad, the package, the board and the probe. Record that load and whether `ro_vout` sees a high-impedance probe or 50 Ohm.

| Parameter | Condition | Simulated | Source | Measured |
| --- | --- | --- | --- | --- |
| Oscillation frequency, `fosc` | `vdd_ro` 1.5 V | 290.7 MHz, Monte Carlo 274.8 MHz to 309.0 MHz, corners 248.5 MHz to 325.5 MHz | [CACE][cace] | TBD |
| Supply current, `Idd` | `vdd_ro` 1.5 V | 2.96 mA, Monte Carlo 2.72 mA to 3.33 mA, corners 2.04 mA to 4.07 mA | [CACE][cace] | TBD |
| `fosc` and `Idd` against the supply | `vdd_ro` from 1.2 V to 1.65 V | CACE covers 1.35 V to 1.65 V ([plots][cace-plots]) | [CACE][cace] | TBD |
| Oscillation frequency in the chip | `vdd_ro` 1.2 V | 234 MHz in the chip bench with 1 pF on `ro_vout`, the median period of its waveform | [chip bench data][chip-bench] | TBD |
| Output swing at `ro_vout` | `vdd_ro` 1.2 V and 1.5 V | -0.05 V to 1.27 V in the chip bench at 1.2 V with 1 pF | [chip bench data][chip-bench] | TBD |


## Setup

| Item | Value |
| --- | --- |
| Samples | TBD |
| Source meter | TBD |
| Spectrum analyzer, frequency counter or scope | TBD |
| Load on `ro_vout` | TBD |
| Temperature | TBD |

[macro]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/ringosc/README.md
[cace]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/ringosc/README.md#cace-simulations
[cace-plots]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/tree/ef8524f81b8355548f01540cfba7907767346396/macros/ringosc/verification/cace/results/ringosc
[chip-bench]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/testbenches/xschem/plot_simulations/data/chip_top_tb_tran.txt
