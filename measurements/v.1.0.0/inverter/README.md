# Inverter

The quad inverter [`inverter_top`][macro] of `ef8524f` on `VDD`. Channel 1 is analog on two pads of its own, channel 4 is digital and reads `count[7]` back from its bidir pad. Channels 2 and 3 are not bonded out.


## Connections

| Pin | Signal | Path | Connect to |
| --- | --- | --- | --- |
| 19 | `inv_vin`, channel 1 input | `padres`, through the secondary ESD resistor of the pad | source meter or signal generator |
| 20 | `inv_vout`, channel 1 output | `padbare` | voltmeter or high-impedance probe |
| 21 | `inv_dout`, channel 4 output | 16 mA output pad | logic analyzer |
| 25 | `count[7]`, channel 4 input | bidir pad, driven by the selected counter | logic analyzer |
| 7 | `VDD` | | source meter |


## Channel 1, Analog

Stop `clk` for the DC sweeps, so that the `VDD` current changes with the inverter alone. The simulated values are of the schematic at `tt` with `VDD` at 1.5 V and 10 pF on `vout`. The bandwidth depends on that load, so record the load of the setup (pad, package, board and probe) with the result.

| Parameter | Condition | Simulated | Source | Measured |
| --- | --- | --- | --- | --- |
| Switching point, `inv_vout` = `inv_vin` | `VDD` 1.5 V, `inv_vin` from 0 V to 1.5 V in 1 mV steps | 0.745 V | [DC bench][dc] | TBD |
| Largest gain, slope of the transfer curve | as above | 48.1 V/V (33.6 dB) at 0.744 V | [DC bench][dc] | TBD |
| Switching point and largest gain | `VDD` 1.2 V | not simulated | | TBD |
| Supply current at the switching point | `VDD` 1.5 V and 1.2 V | no value in the repository | | TBD |
| Small-signal gain at low frequency | `VDD` 1.5 V, `inv_vin` biased at the switching point | 31.3 dB at 0.75 V | [AC bench][ac] | TBD |
| -3 dB frequency | as above | 2.9 MHz | [AC bench][ac] | TBD |

The CACE runs of the macro check the gain at 10 Hz against at least 3 dB and the -3 dB frequency against at least 1 MHz, over mismatch, Monte Carlo and five MOS corners at 1.35 V to 1.65 V ([plots][cace]).


## Channel 4, Digital

Run a counter as in [`counters/`](../counters/README.md), so that `count[7]` toggles.

| Parameter | Condition | Simulated | Source | Measured |
| --- | --- | --- | --- | --- |
| `inv_dout` is the inverse of `count[7]` | `VDD` 1.2 V, any counter selected | static case only: `count[7]` stays at 0 in the chip bench and `inv_dout` at 3.3 V. The cocotb benches do not check it | [chip bench][chip-bench] | TBD |
| Delay from pin 25 to pin 21 | `VDD` 1.2 V | not simulated | | TBD |


## Setup

| Item | Value |
| --- | --- |
| Samples | TBD |
| Source meters | TBD |
| Signal generator and scope | TBD |
| Load on `inv_vout` | TBD |
| Temperature | TBD |

[macro]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/inverter/README.md
[dc]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/inverter/testbenches/xschem/plot_simulations/figures/inverter_tb_dc_vout.csv
[ac]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/inverter/testbenches/xschem/plot_simulations/figures/inverter_tb_ac_ol.csv
[cace]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/tree/ef8524f81b8355548f01540cfba7907767346396/macros/inverter/verification/cace/results/inverter
[chip-bench]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/testbenches/xschem/plot_simulations/figures/chip_top_tb_tran_digital.svg
