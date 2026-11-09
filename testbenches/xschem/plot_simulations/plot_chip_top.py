# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Author: Simon Dorrer
# Description: Transient plots for the chip top-level testbench based on ngspice exports.
# Created: 12.05.2026
# Last Modified: 08.11.2026
# ============================================

# Imports
import numpy as np
import matplotlib.pyplot as plt
import ngspice2python as ng
from pathlib import Path
# ============================================

# Plotting Configuration
# ============================================
# Interactive mode stays off: the plt.show() at the end of main() then blocks in the GUI
# event loop, which is what draws the windows in the first place. With plt.ion() the call
# returns immediately and nothing pumps that loop afterwards, so no window ever appears.
plt.close("all")

# Matplotlib Settings
# %matplotlib qt
# %matplotlib inline

# Pure Matplotlib text rendering (no external LaTeX dependency)
plt.rcParams.update({
    "text.usetex": False,
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.size": 12,
})
# =========================================================================

def plot_digital(fig_title, signals, data_time, figures_dir, filename, fig_height=9):
    """Stack digital signals in separate subplots sharing the time axis."""
    y_ticks = [0.0, 1.0, 2.0, 3.0, 4.0]
    fig, axs = plt.subplots(len(signals), sharex=True)
    if len(signals) == 1:
        axs = [axs]
    fig.set_figwidth(16)
    fig.set_figheight(fig_height)
    fig.suptitle(fig_title)

    for ax, (name, values, color) in zip(axs, signals):
        ax.plot(data_time, values, color=color, linewidth=1.3)
        ax.set_ylabel(f'{name} (V)', fontsize=11)
        ax.set_ylim(-0.2, 4.2)
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(["0", "1.0", "2.0", "3.0", "4.0"], fontsize=8)
        ax.tick_params(axis='x', labelsize=8)
        ax.grid(True, alpha=0.4)

    axs[-1].set_xlabel(r'$t$ ($\mu$s)')
    fig.tight_layout(rect=[0, 0, 1, 0.98], pad=0.5, w_pad=0.1, h_pad=0.1)
    fig.savefig(str(figures_dir / f"{filename}.svg"), bbox_inches='tight')
    fig.savefig(str(figures_dir / f"{filename}.pdf"), bbox_inches='tight')
    return fig
# =========================================================================

def moving_average(time_us, values, window_us):
    """Average over window_us after resampling on a uniform grid, ngspice writes a non-uniform time axis."""
    grid = np.arange(time_us[0], time_us[-1], window_us / 200.0)
    uniform = np.interp(grid, time_us, values)
    return grid, np.convolve(uniform, np.ones(200) / 200.0, mode="same")
# =========================================================================

def main():
    # Resolve data and output paths relative to this script
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / "data"
    figures_dir = script_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Load ngspice transient simulation data
    # ------------------------------------------------------------------
    ngspice_file = str(data_dir / "chip_top_tb_tran.txt")

    time     = ng.loadngspicecol(ngspice_file, "time")
    rst_n    = ng.loadngspicecol(ngspice_file, "v(rst_n)")
    sel1     = ng.loadngspicecol(ngspice_file, "v(sel1)")
    sel0     = ng.loadngspicecol(ngspice_file, "v(sel0)")
    count    = [ng.loadngspicecol(ngspice_file, f"v(count{i})") for i in range(8)]
    inv_dout = ng.loadngspicecol(ngspice_file, "v(inv_dout)")
    inv_vin  = ng.loadngspicecol(ngspice_file, "v(inv_vin)")
    inv_vout = ng.loadngspicecol(ngspice_file, "v(inv_vout)")
    amp_vin  = ng.loadngspicecol(ngspice_file, "v(amp_vin)")
    amp_vout = ng.loadngspicecol(ngspice_file, "v(amp_vout)")
    ro_vout  = ng.loadngspicecol(ngspice_file, "v(ro_vout)")
    i_vdd    = ng.loadngspicecol(ngspice_file, "i(vvdd)")
    i_hv     = ng.loadngspicecol(ngspice_file, "i(vhv)")

    # Display-friendly axis scale
    time_us = time * 1e6

    # ------------------------------------------------------------------
    # 2. Plot 1 (digital): reset, counter select and the chip outputs
    # ------------------------------------------------------------------
    colors = ["#ff6b35", "#845ec2", "#2c73d2", "#008f7a", "#c34a36", "#4d8076", "#7b2cbf", "#b39f00"]
    signals = [
        ("RST_n", rst_n, "#00b945"),
        ("SEL1",  sel1,  "#0c5da5"),
        ("SEL0",  sel0,  "#ff9500"),
    ]
    signals += [(f"COUNT{i}", count[i], colors[i]) for i in range(8)]
    signals += [("INV_DOUT", inv_dout, "#e63946")]
    plot_digital(
        "Chip Top: Counter Select and Digital Outputs",
        signals, time_us, figures_dir,
        "chip_top_tb_tran_digital",
        fig_height=13,
    )

    # ------------------------------------------------------------------
    # 3. Plot 2 (analog): inverter, amplifier and ring oscillator
    # ------------------------------------------------------------------
    fig2, (ax1, ax2, ax3) = plt.subplots(3)
    fig2.set_figwidth(14)
    fig2.set_figheight(10)
    fig2.suptitle("Chip Top: Analog Macros")

    ax1.plot(time_us, inv_vin,  color="#0c5da5", linewidth=1.5, label=r'$V_\mathrm{in}$')
    ax1.plot(time_us, inv_vout, color="#ff6b35", linewidth=1.5, label=r'$V_\mathrm{out}$')
    ax1.set_ylabel(r'$V$ (V)')
    ax1.set_xlabel(r'$t$ ($\mu$s)')
    ax1.set_title("Inverter, Analog Channel (200 kHz)")
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.4)

    ax2.plot(time_us, amp_vin,  color="#2c73d2", linewidth=1.5, label=r'$V_\mathrm{in}$')
    ax2.plot(time_us, amp_vout, color="#c34a36", linewidth=1.5, label=r'$V_\mathrm{out}$')
    ax2.set_ylabel(r'$V$ (V)')
    ax2.set_xlabel(r'$t$ ($\mu$s)')
    ax2.set_title("Amplifier (1 MHz)")
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(True, alpha=0.4)

    # A few periods at the end of the run, when the ring oscillator has settled
    zoom = time_us > time_us[-1] - 0.02
    ax3.plot(time_us[zoom], ro_vout[zoom], color="#008f7a", linewidth=1.5)
    ax3.set_ylabel(r'$V_\mathrm{out}$ (V)')
    ax3.set_xlabel(r'$t$ ($\mu$s)')
    ax3.set_title("Ring Oscillator")
    ax3.grid(True, alpha=0.4)

    fig2.tight_layout(rect=[0, 0, 1, 0.98])
    fig2.savefig(str(figures_dir / "chip_top_tb_tran_analog.svg"), bbox_inches='tight')
    fig2.savefig(str(figures_dir / "chip_top_tb_tran_analog.pdf"), bbox_inches='tight')

    # ------------------------------------------------------------------
    # 4. Plot 3 (supply): average current of the core and the IHP HV counter
    # ------------------------------------------------------------------
    fig3, ax = plt.subplots()
    fig3.set_figwidth(14)
    fig3.set_figheight(5)
    fig3.suptitle("Chip Top: Supply Current, Averaged over 100 ns")

    # A source sinks the supply current into its positive terminal, so the sign is flipped
    for values, color, label in ((i_vdd, "#0c5da5", "VDD (core)"), (i_hv, "#ff6b35", "vdd_hv (IHP HV counter)")):
        grid, avg = moving_average(time_us, -values, 0.1)
        ax.plot(grid, avg * 1e3, color=color, linewidth=1.5, label=label)
    ax.set_ylabel(r'$I$ (mA)')
    ax.set_xlabel(r'$t$ ($\mu$s)')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.4)

    fig3.tight_layout(rect=[0, 0, 1, 0.98])
    fig3.savefig(str(figures_dir / "chip_top_tb_tran_supply.svg"), bbox_inches='tight')
    fig3.savefig(str(figures_dir / "chip_top_tb_tran_supply.pdf"), bbox_inches='tight')

    # ------------------------------------------------------------------
    # 5. Open the plot windows (blocks until they are closed)
    # ------------------------------------------------------------------
    plt.show()
    # ============================================

# Main Execution
if __name__ == '__main__':
    main()
# =========================================================================
