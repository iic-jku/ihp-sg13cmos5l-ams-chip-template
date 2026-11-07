# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2026 The HeiChips Contributors
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Author: Simon Dorrer
# Description: Transient plot for the ring oscillator macro based on ngspice exports.
# Created: 05.08.2026
# Last Modified: 05.08.2026
# ============================================

# Imports
import os
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

# Pure Matplotlib text rendering (no external LaTeX dependency)
plt.rcParams.update({
    "text.usetex": False,
    "mathtext.fontset": "cm",
    "font.family": "serif",
    "font.size": 14,
})
# =========================================================================

def rising_crossings(time, signal, level):
    '''
    Return the interpolated time points where the signal crosses the given
    level with a positive slope. Linear interpolation between the two
    neighbouring samples is used, so the result is not limited by the time step.
    '''
    below = signal[:-1] < level
    above = signal[1:] >= level
    idx = np.nonzero(below & above)[0]

    crossings = []
    for i in idx:
        y0, y1 = signal[i], signal[i + 1]
        if y1 == y0:
            continue
        t0, t1 = time[i], time[i + 1]
        crossings.append(t0 + (level - y0) * (t1 - t0) / (y1 - y0))
    return np.array(crossings)
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
    ngspice_file = data_dir / "ringosc_tb_tran.txt"

    if not ngspice_file.is_file():
        print(f"Skipping {ngspice_file.name}: run 'make sim-xschem' first.")
        return

    time = ng.loadngspicecol(str(ngspice_file), "time")
    vout = ng.loadngspicecol(str(ngspice_file), "v(vout)")

    time_ns = time * 1e9

    # ------------------------------------------------------------------
    # 2. Oscillation frequency from the rising threshold crossings
    # ------------------------------------------------------------------
    # The threshold is placed in the middle of the swing instead of at a fixed
    # VDD/2, so the measurement also works when the output does not reach the
    # rails (for example in a post-layout run with heavy parasitic loading).
    v_min, v_max = float(np.min(vout)), float(np.max(vout))
    v_pp = v_max - v_min
    v_mid = 0.5 * (v_max + v_min)

    crossings = rising_crossings(time, vout, v_mid)

    if crossings.size >= 2:
        periods = np.diff(crossings)
        T_osc = float(np.mean(periods))
        f_osc = 1.0 / T_osc
        # A ring oscillator with N stages has a stage delay of T/(2*N).
        N_stages = 3
        t_delay = T_osc / (2 * N_stages)
    else:
        T_osc = f_osc = t_delay = float('nan')
        print("Fewer than two rising crossings found, cannot measure the "
              "oscillation frequency. Simulate a longer time window.")

    def _fmt_hz(f):
        for prefix, scale in (('G', 1e9), ('M', 1e6), ('k', 1e3)):
            if f >= scale:
                return rf"{f/scale:.2f}\,\mathrm{{{prefix}Hz}}"
        return rf"{f:.2f}\,\mathrm{{Hz}}"

    # ------------------------------------------------------------------
    # 3. Transient Plot
    # ------------------------------------------------------------------
    vout_color = '#0c5da5'
    marker_color = '#444444'
    line_kw = dict(color=marker_color, linestyle=':', linewidth=1.2, alpha=0.85)
    point_kw = dict(marker='o', color=marker_color, linestyle='None',
                    markersize=6, zorder=5)
    box_kw = dict(boxstyle='round,pad=0.4', fc='white', ec=marker_color, alpha=0.9)

    fig1, ax = plt.subplots(figsize=(10, 6.2))
    fig1.suptitle('Ring Oscillator - Transient Response')

    ax.plot(time_ns, vout, color=vout_color, linewidth=2.4,
            label=r'$V_\mathrm{out}(t)$')
    ax.set_xlabel(r'$t$ (ns)')
    ax.set_ylabel(r'$V_\mathrm{out}$ (V)')
    ax.set_xlim(time_ns[0], time_ns[-1])
    ax.grid(visible=True, which='both', linestyle='--', alpha=0.5)

    # Mark the mid-level and the rising crossings that define the period
    ax.axhline(v_mid, **line_kw)
    if crossings.size:
        ax.plot(crossings * 1e9, np.full(crossings.size, v_mid), **point_kw)

    info_text = '\n'.join((
        rf'$f_\mathrm{{osc}} = {_fmt_hz(f_osc)}$',
        rf'$T_\mathrm{{osc}} = {T_osc*1e9:.3f}\,\mathrm{{ns}}$',
        rf'$t_\mathrm{{d}} = T_\mathrm{{osc}}/(2 \cdot 3) = {t_delay*1e12:.1f}\,\mathrm{{ps}}$',
        rf'$V_\mathrm{{out,pp}} = {v_pp*1e3:.1f}\,\mathrm{{mV}}$',
    ))
    ax.text(0.02, 0.05, info_text, transform=ax.transAxes,
            ha='left', va='bottom', color=marker_color, bbox=box_kw, zorder=6)

    ax.legend(loc='upper right')
    plt.tight_layout()

    # ------------------------------------------------------------------
    # 4. Export figures and CSV
    # ------------------------------------------------------------------
    fig1.savefig(str(figures_dir / "ringosc_tb_tran.svg"), bbox_inches='tight')
    fig1.savefig(str(figures_dir / "ringosc_tb_tran.pdf"), bbox_inches='tight')
    np.savetxt(str(figures_dir / "ringosc_tb_tran.csv"),
               np.column_stack((time, vout)), comments="",
               header="time,vout", delimiter=",")

    # ------------------------------------------------------------------
    # 5. Open the plot window (blocks until it is closed)
    # ------------------------------------------------------------------
    # Only open the interactive window when requested (sim-view-xschem sets
    # SHOW_PLOTS=1); batch/headless runs just save the figures and exit.
    if os.environ.get("SHOW_PLOTS"):
        plt.show()
    # =========================================================================

# Main Execution
if __name__ == '__main__':
    main()
# =========================================================================
