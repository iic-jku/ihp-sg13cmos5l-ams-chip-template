# Amplifier

The self-biased single-ended inverter amplifier [`amplifier`][macro] of `ef8524f` on `VDD`: the `inverter` unit cell with an `rhigh` feedback resistor from `vout` back to `vin`, which sets the DC point.


## Connections

| Pin | Signal | Path | Connect to |
| --- | --- | --- | --- |
| 17 | `amp_vin` | `padres`, through the secondary ESD resistor of the pad | signal generator, AC-coupled |
| 18 | `amp_vout` | `padbare` | scope or network analyzer, high impedance |
| 7 | `VDD` | | source meter |


## Results

The gain is `amp_vout` over `amp_vin`, both measured at the pins, as CACE defines it. Then it does not depend on what drives `amp_vin`. The simulated values are CACE runs of the schematic with 10 pF on `vout`: the typical point at `tt` and 1.5 V, then the spread over 200 Monte Carlo iterations at 1.5 V and over five MOS corners at 1.35 V to 1.65 V. The bandwidth depends on the load, so record the load of the setup (pad, package, board and probe) with the result.

| Parameter | Condition | Simulated | Source | Measured |
| --- | --- | --- | --- | --- |
| DC level of `amp_vin` and `amp_vout` | `VDD` 1.5 V and 1.2 V, no signal | no value in the repository | | TBD |
| Gain at 10 Hz, `Av_dB` | `VDD` 1.5 V | 32.70 dB, Monte Carlo 31.54 dB to 33.24 dB, corners 31.84 dB to 33.32 dB | [CACE][cace] | TBD |
| -3 dB frequency, `fcu` | `VDD` 1.5 V | 2.50 MHz, Monte Carlo 2.15 MHz to 3.21 MHz, corners 1.70 MHz to 3.50 MHz | [CACE][cace] | TBD |
| Gain and -3 dB frequency | `VDD` 1.2 V | not simulated, CACE covers 1.35 V to 1.65 V | | TBD |


## Setup

| Item | Value |
| --- | --- |
| Samples | TBD |
| Signal generator and coupling capacitor | TBD |
| Scope or network analyzer | TBD |
| Load on `amp_vout` | TBD |
| Temperature | TBD |

[macro]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/amplifier/README.md
[cace]: https://github.com/iic-jku/ihp-sg13cmos5l-ams-chip-template/blob/ef8524f81b8355548f01540cfba7907767346396/macros/amplifier/README.md#cace-simulations
