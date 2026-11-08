# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1

"""Cocotb testbench for chip_top.

The chip exposes the generic-named padframe ports defined in rtl/chip_top.sv:
  - clk_PAD                    : main clock                 (single)
  - rst_n_PAD                  : active-low reset           (single)
  - input_PAD[NUM_INPUT_PADS]  : digital inputs (3 bits: sel[1:0], di_en)
  - output_PAD[NUM_OUTPUT_PADS]: digital outputs (8 bits)
  - bidir_PAD[NUM_BIDIR_PADS]  : bidir pads (1 bit)
  - analog_PAD[NUM_ANALOG_PADS]: analog pads (6 bits)
  - rf_PAD[NUM_RF_PADS]        : RF pads (2 bits)
  - vdd_rf_PAD, vdd_ro_PAD, vdd_hv_PAD: supplies of the VCO, ring oscillator and IHP HV counter

input_PAD bit assignment (read by rtl/chip_core.sv):
  - [1:0]   sel: 00 none, 01 IHP LV counter, 10 IHP HV counter, 11 ETH LV counter
  - [2]     di_en (VCO enable)

output_PAD bit assignment (driven by rtl/chip_core.sv):
  - [6:0]   count[6:0] of the selected counter, 0 for sel = 00
  - [7]     inverter.vout4 (digital channel, inverts count[7])

bidir_PAD bit assignment:
  - [0]     count[7], always driven, read back into inverter.vin4

analog_PAD bit assignment:
  - [0]     vco.vtune        (via padres)
  - [1]     amplifier.vin    (via padres)
  - [2]     amplifier.vout   (via padbare)
  - [3]     inverter.vin1    (via padres)
  - [4]     inverter.vout1   (via padbare)
  - [5]     ringosc.vout     (via padbare)

rf_PAD bit assignment:
  - [0]     vco.rf_out_n     (via padbare)
  - [1]     vco.rf_out_p     (via padbare)

The analog and RF macros are functional blackboxes in this simulation, so any signal that passes through them
resolves to X or Z. The tests therefore only assert on the counter, select and bidir signal paths.
"""

import os
import logging
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles
from cocotb_tools.runner import get_runner

sim      = os.getenv("SIM", "icarus")
pdk_root = os.getenv("PDK_ROOT", Path("~/.ciel").expanduser())
pdk      = os.getenv("PDK", "ihp-sg13cmos5l")
scl      = os.getenv("SCL", "sg13cmos5l_stdcell")
scl_hv   = os.getenv("SCL_HV", "sg13cmos5l_stdcell_hv")
# The image installs the ETH library ez130_8t only in the ihp-sg13g2 tree
pdk_eth  = "ihp-sg13g2"
scl_eth  = os.getenv("SCL_ETH", "ez130_8t")
# GL=1 selects the gate-level netlist; anything else (unset, "0", "") stays in RTL mode.
gl       = os.getenv("GL", "0").strip().lower() in ("1", "true", "yes", "on")

hdl_toplevel = "chip_top"

# Main clock frequency. Matches CLOCK_PERIOD = 20 ns in flow/librelane/config.yaml.
CPU_CLK_FREQ_MHZ = 50

# Counters wrap from 255 -> 0 (8-bit, default CTR_MAX).
CTR_MAX = 255

# Counter select values on input_PAD[1:0]
SEL_NONE   = 0b00
SEL_LV_IHP = 0b01
SEL_HV_IHP = 0b10
SEL_LV_ETH = 0b11
SEL_NAMES  = {SEL_LV_IHP: "IHP LV", SEL_HV_IHP: "IHP HV", SEL_LV_ETH: "ETH LV"}


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
async def enable_power(dut):
    """Drive supplies for gate-level simulation (USE_POWER_PINS)."""
    dut.VDD.value   = 1
    dut.VSS.value   = 0
    dut.IOVDD.value = 1
    dut.IOVSS.value = 0


async def start_clock(clock, freq_mhz=CPU_CLK_FREQ_MHZ):
    """Start the chip clock at `freq_mhz` MHz."""
    period_ns = round(1 / freq_mhz * 1000, 4)
    cocotb.start_soon(Clock(clock, period_ns, "ns").start())


async def reset(dut, sel, cycles=4):
    """Pulse the active-low reset for `cycles` clock cycles. sel changes only while rst_n is low, as the chip requires."""
    cocotb.log.info("Reset asserted, sel = %s...", format(sel, "02b"))
    dut.rst_n_PAD.value = 0
    dut.input_PAD.value = sel
    await ClockCycles(dut.clk_PAD, cycles)
    dut.rst_n_PAD.value = 1
    await RisingEdge(dut.clk_PAD)
    cocotb.log.info("Reset deasserted.")


async def start_up(dut, sel=SEL_NONE):
    """Power up, start the clock, drive a reset pulse with the counter select `sel`."""
    if gl:
        await enable_power(dut)

    # Initialise inputs to known levels before clocking.
    dut.rst_n_PAD.value = 0
    dut.input_PAD.value = sel

    await start_clock(dut.clk_PAD, CPU_CLK_FREQ_MHZ)
    await reset(dut, sel)


def _count(dut) -> int:
    """count[7:0] of the selected counter: count[6:0] on output_PAD[6:0], count[7] on bidir_PAD[0]."""
    # A one-bit port reads as a single value in RTL and can read as an array in the netlist, the last character is the bit
    return (int(str(dut.bidir_PAD.value)[-1]) << 7) | int(dut.output_PAD.value[6:0])


async def _count_after_edge(dut) -> int:
    await RisingEdge(dut.clk_PAD)
    await Timer(1, "ns")
    return _count(dut)


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
@cocotb.test()
async def test_none_selected_holds_zero(dut):
    """With sel = 00 no counter is clocked and count[7:0] stays 0."""
    logger = logging.getLogger("chip_top_tb")
    await start_up(dut, SEL_NONE)
    for _ in range(32):
        assert await _count_after_edge(dut) == 0, "count is not 0 with sel = 00"
    logger.info("Done!")


async def _check_counts(dut, sel):
    """After reset the selected counter starts at 0 and increments once per clock."""
    logger = logging.getLogger("chip_top_tb")
    await start_up(dut, sel)
    # The rising edge after rst_n rises already clocks the counter once.
    await Timer(1, "ns")
    first = _count(dut)
    assert first == 1, f"{SEL_NAMES[sel]}: count after reset is {first}"
    for step in range(1, 17):
        cur = await _count_after_edge(dut)
        assert cur == first + step, f"{SEL_NAMES[sel]}: expected {first + step}, got {cur}"
    logger.info("Done!")


@cocotb.test()
async def test_lv_ihp_counts(dut):
    """sel = 01 puts the IHP LV counter on count[7:0]."""
    await _check_counts(dut, SEL_LV_IHP)


@cocotb.test()
async def test_hv_ihp_counts(dut):
    """sel = 10 puts the IHP HV counter on count[7:0]."""
    await _check_counts(dut, SEL_HV_IHP)


@cocotb.test()
async def test_lv_eth_counts(dut):
    """sel = 11 puts the ETH LV counter on count[7:0]."""
    await _check_counts(dut, SEL_LV_ETH)


@cocotb.test()
async def test_counter_wraps(dut):
    """The IHP LV counter wraps from CTR_MAX back to 0, which also toggles count[7] on the bidir pad."""
    await start_up(dut, SEL_LV_IHP)
    saw_max  = False
    saw_wrap = False
    prev     = _count(dut)
    for _ in range(2 * (CTR_MAX + 1) + 4):
        cur = await _count_after_edge(dut)
        if cur == CTR_MAX:
            saw_max = True
        if saw_max and prev == CTR_MAX and cur == 0:
            saw_wrap = True
            break
        prev = cur
    assert saw_max,  "count never reached CTR_MAX"
    assert saw_wrap, "count did not wrap from CTR_MAX to 0"


@cocotb.test()
async def test_unselected_counter_holds(dut):
    """An unselected counter gets no clock and holds its value, through a reset of another counter as well.
    The reset is synchronous, so a counter only resets while it is selected.
    sel changes while clk is low, so the AND gates of the clock pass no partial pulse."""
    await start_up(dut, SEL_HV_IHP)
    await Timer(1, "ns")
    hv_value = _count(dut)

    # Reset the LV counter with it selected, then let it count.
    await reset(dut, SEL_LV_IHP)
    for _ in range(9):
        await _count_after_edge(dut)
    lv_value = _count(dut)

    # Switch to the HV counter: it has not been clocked since.
    await FallingEdge(dut.clk_PAD)
    dut.input_PAD.value = SEL_HV_IHP
    await Timer(1, "ns")
    assert _count(dut) == hv_value, f"HV counter did not hold {hv_value} (got {_count(dut)})"
    for step in range(1, 5):
        assert await _count_after_edge(dut) == hv_value + step, "HV counter does not count after selecting it"

    # Back to the LV counter: it held its value while unselected.
    await FallingEdge(dut.clk_PAD)
    dut.input_PAD.value = SEL_LV_IHP
    await Timer(1, "ns")
    assert _count(dut) == lv_value, f"LV counter did not hold {lv_value} (got {_count(dut)})"
    assert await _count_after_edge(dut) == lv_value + 1, "LV counter does not resume"


# ----------------------------------------------------------------------
# Runner
# ----------------------------------------------------------------------
def chip_top_runner():

    proj_path = Path(__file__).resolve().parent
    root_path = proj_path.parent.parent

    sources  = []
    defines  = {}
    includes = [root_path / "rtl"]

    counters = ["counter_lv_ihp", "counter_hv_kvc", "counter_lv_eth"]

    if gl:
        # Standard-cell models for gate-level simulation: IHP LV, IHP HV and ETH LV
        sources.append(Path(pdk_root) / pdk / "libs.ref" / scl / "verilog" / f"{scl}.v")
        sources.append(Path(pdk_root) / pdk / "libs.ref" / scl_hv / "verilog" / f"{scl_hv}.v")
        sources.append(Path(pdk_root) / pdk / "libs.ref" / scl / "verilog" / "sg13cmos5l_udp.v")
        sources.append(Path(pdk_root) / pdk_eth / "libs.ref" / scl_eth / "verilog" / f"{scl_eth}.v")
        sources.append(root_path / "macros/counter_lv_eth/testbenches/cocotb/ez130_8t_physical_cells.v")
        # Unpowered top-level netlist
        sources.append(root_path / f"netlist/nl/{hdl_toplevel}.nl.v")
        # Macro netlists referenced by the top-level netlist
        for m in counters:
            sources.append(root_path / f"macros/{m}/final/nl/{m}_top.nl.v")
    else:
        # RTL sources
        sources.append(root_path / "rtl/chip_top.sv")
        sources.append(root_path / "rtl/chip_core.sv")
        # Counter macro RTL
        for m in counters:
            sources.append(root_path / f"macros/{m}/rtl/constants.sv")
            sources.append(root_path / f"macros/{m}/rtl/{m}.sv")
            sources.append(root_path / f"macros/{m}/rtl/{m}_top.sv")

    sources += [
        # Analog and RF macro stubs (blackboxes)
        root_path / "macros/inverter/final/vh/inverter_top.vh",
        root_path / "macros/amplifier/final/vh/amplifier.vh",
        root_path / "macros/ringosc/final/vh/ringosc.vh",
        root_path / "macros/vco/final/vh/vco_top.vh",
        # Bondpad and RF pad stubs
        root_path / "ip/sg13cmos5l_ip__bondpad_70x70/final/vh/sg13cmos5l_ip__bondpad_70x70.vh",
        root_path / "ip/sg13cmos5l_ip__rfpad_70x70/final/vh/sg13cmos5l_ip__rfpad_70x70.vh",
        # Custom IO pad models
        root_path / "ip/sg13cmos5l_io_custom/verilog/sg13cmos5l_io.v",
        # Logo IPs
        root_path / "ip/sg13cmos5l_ip__jku/final/vh/sg13cmos5l_ip__jku.vh",
        root_path / "ip/sg13cmos5l_ip__jku_names/final/vh/sg13cmos5l_ip__jku_names.vh",
    ]

    build_args = []

    if sim == "icarus":
        # -gno-specify: skip specify blocks; the SCL Verilog uses `ifnone`
        # with edge-sensitive paths, which iverilog cannot parse.
        build_args = ["-DSIM", "-gno-specify"]

    if sim == "verilator":
        build_args = ["--timing", "--trace", "--trace-fst", "--trace-structs"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=hdl_toplevel,
        defines=defines,
        always=True,
        includes=includes,
        build_args=build_args,
        waves=True,
        timescale=("1ns", "1fs")
    )

    plusargs = []

    runner.test(
        hdl_toplevel=hdl_toplevel,
        test_module="chip_top_tb",
        plusargs=plusargs,
        waves=True,
    )


if __name__ == "__main__":
    chip_top_runner()
