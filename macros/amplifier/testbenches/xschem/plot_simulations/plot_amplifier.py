# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2026 The HeiChips Contributors
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Author: Simon Dorrer
# Description: AC, DC and transient plots for the amplifier macro based on ngspice exports.
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

def main():
    # Resolve data and output paths relative to this script
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / "data"
    figures_dir = script_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    def missing(path):
        # Every testbench can be run on its own, so simply skip the plots of a
        # testbench that has not been simulated yet instead of failing.
        if path.is_file():
            return False
        print(f"Skipping {path.name}: run 'make sim-xschem TB={path.stem}' first.")
        return True

    # ------------------------------------------------------------------
    # 1. Load ngspice open-loop AC simulation data
    # ------------------------------------------------------------------
    ngspice_file = data_dir / "amplifier_tb_ac_ol.txt"

    if not missing(ngspice_file):
        # ngspice writes the complex ac vectors interleaved, so every second entry
        # is taken (same convention as in plot_inverter.py).
        frequency = ng.loadngspicecol(str(ngspice_file), "frequency")[0::2]
        mag_dB = ng.loadngspicecol(str(ngspice_file), "v(Aol_dB)")[0::2]
        phase_deg = ng.loadngspicecol(str(ngspice_file), "v(Aol_arg)")[0::2]

        # --------------------------------------------------------------
        # 2. Bode Plot (AC)
        # --------------------------------------------------------------
        ac_color_mag = '#0c5da5'
        ac_color_phase = '#ff6b35'

        fig1, axs = plt.subplots(2)
        fig1.set_figwidth(10)
        fig1.set_figheight(7)
        fig1.suptitle('Amplifier - AC Open-Loop Response')

        # Magnitude
        axs[0].set_xscale('log')
        axs[0].plot(frequency, mag_dB, color=ac_color_mag, linewidth=2.4)
        axs[0].set_xlabel('$f$ (Hz)')
        axs[0].set_ylabel(r'$|A_\mathrm{ol}(f)|$ (dB)')
        axs[0].set_xlim(1, 1e9)
        axs[0].grid(visible=True, which='both', linestyle='--', alpha=0.5)

        # Phase
        axs[1].set_xscale('log')
        axs[1].plot(frequency, phase_deg, color=ac_color_phase, linewidth=2.4)
        axs[1].set_xlabel('$f$ (Hz)')
        axs[1].set_ylabel(r'$\angle A_\mathrm{ol}(f)$ ($^\circ$)')
        axs[1].set_xlim(1, 1e9)
        axs[1].grid(visible=True, which='both', linestyle='--', alpha=0.5)

        # Characteristic Bode-plot values: DC gain, -3 dB cutoff, transit frequency.
        # Magnitude is monotonically decreasing in frequency, so reverse the
        # arrays to feed np.interp (which requires ascending xp).
        mag_dB_asc = mag_dB[::-1]
        freq_desc = frequency[::-1]
        phase_desc = phase_deg[::-1]

        Aol_dB = float(mag_dB[0])
        Aol_VV = 10.0 ** (Aol_dB / 20.0)
        f_cu = float(np.interp(Aol_dB - 3.0, mag_dB_asc, freq_desc))
        phase_cu = float(np.interp(Aol_dB - 3.0, mag_dB_asc, phase_desc))
        f_T = float(np.interp(0.0, mag_dB_asc, freq_desc))
        phase_T = float(np.interp(0.0, mag_dB_asc, phase_desc))

        def _fmt_hz(f):
            for prefix, scale in (('G', 1e9), ('M', 1e6), ('k', 1e3)):
                if f >= scale:
                    return rf"{f/scale:.2f}\,\mathrm{{{prefix}Hz}}"
            return rf"{f:.2f}\,\mathrm{{Hz}}"

        marker_color = '#444444'
        line_kw = dict(color=marker_color, linestyle=':', linewidth=1.2, alpha=0.85)
        point_kw = dict(marker='o', color=marker_color, linestyle='None',
                        markersize=6, zorder=5)
        box_kw = dict(boxstyle='round,pad=0.4', fc='white',
                      ec=marker_color, alpha=0.9)

        # Magnitude markers (lines + dots)
        axs[0].axhline(Aol_dB, **line_kw)
        axs[0].axvline(f_cu, **line_kw)
        axs[0].axvline(f_T, **line_kw)
        axs[0].plot([frequency[0]], [Aol_dB], **point_kw)
        axs[0].plot([f_cu], [Aol_dB - 3.0], **point_kw)
        axs[0].plot([f_T], [0.0], **point_kw)

        # Magnitude info box (lower-left corner)
        mag_text = '\n'.join((
            rf'$A_\mathrm{{ol}} = {Aol_dB:.1f}\,\mathrm{{dB}}\;({Aol_VV:.1f}\,\mathrm{{V/V}})$',
            rf'$f_\mathrm{{cu}} = {_fmt_hz(f_cu)}$',
            rf'$f_\mathrm{{T}} = {_fmt_hz(f_T)}$',
        ))
        axs[0].text(0.02, 0.05, mag_text, transform=axs[0].transAxes,
                    ha='left', va='bottom', color=marker_color, bbox=box_kw,
                    zorder=6)

        # Phase markers (lines + dots)
        axs[1].axvline(f_cu, **line_kw)
        axs[1].axvline(f_T, **line_kw)
        axs[1].plot([f_cu], [phase_cu], **point_kw)
        axs[1].plot([f_T], [phase_T], **point_kw)

        phase_text = '\n'.join((
            rf'$\angle A_\mathrm{{ol}}(f_\mathrm{{cu}}) = {phase_cu:.1f}^\circ$',
            rf'$\angle A_\mathrm{{ol}}(f_\mathrm{{T}}) = {phase_T:.1f}^\circ$',
        ))
        axs[1].text(0.02, 0.05, phase_text, transform=axs[1].transAxes,
                    ha='left', va='bottom', color=marker_color, bbox=box_kw,
                    zorder=6)

        plt.tight_layout()

        # --------------------------------------------------------------
        # 3. Export AC figures and CSV
        # --------------------------------------------------------------
        fig1.savefig(str(figures_dir / "amplifier_tb_ac_ol.svg"), bbox_inches='tight')
        fig1.savefig(str(figures_dir / "amplifier_tb_ac_ol.pdf"), bbox_inches='tight')
        np.savetxt(str(figures_dir / "amplifier_tb_ac_ol.csv"),
                   np.column_stack((frequency, mag_dB, phase_deg)), comments="",
                   header="frequency,Aol_dB,Aol_arg", delimiter=",")

    # ------------------------------------------------------------------
    # 4. Load ngspice DC simulation data
    # ------------------------------------------------------------------
    ngspice_file_dc = data_dir / "amplifier_tb_dc_vout.txt"

    if not missing(ngspice_file_dc):
        vin = ng.loadngspicecol(str(ngspice_file_dc), "v(vin)")
        vout = ng.loadngspicecol(str(ngspice_file_dc), "v(vout)")

        # Local slope dVout/dVin (numerical derivative)
        gain = np.gradient(vout, vin)

        # --------------------------------------------------------------
        # 5. Transfer Plot (DC)
        # --------------------------------------------------------------
        dc_color = '#0c5da5'
        gain_color = '#ff6b35'
        vin_color = '#2f855a'

        fig2, ax1 = plt.subplots(figsize=(10, 6.2))
        ax2 = ax1.twinx()
        fig2.suptitle('Amplifier - DC Transfer Characteristic')

        ax1.plot(vin, vout, color=dc_color, linewidth=2.6, label=r'$V_\mathrm{out}(V_\mathrm{in})$')
        ax1.plot(vin, vin, color=vin_color, linewidth=1.5, linestyle='-.', label=r'$V_\mathrm{out}=V_\mathrm{in}$')
        ax2.plot(vin, gain, color=gain_color, linewidth=1.8, linestyle='--', label=r'$\mathrm{d}V_\mathrm{out}/\mathrm{d}V_\mathrm{in}$')

        ax1.set_xlabel(r'$V_\mathrm{in}$ (V)')
        ax1.set_xlim(0, 1.5)
        ax1.set_ylabel(r'$V_\mathrm{out}$ (V)')
        ax1.set_ylim(0, 1.5)
        ax1.set_yticks(np.arange(0, 1.5, 0.25))
        ax1.grid(visible=True, which='major', linestyle='--', alpha=0.45)

        ax2.set_ylabel(r'$\mathrm{d}V_\mathrm{out}/\mathrm{d}V_\mathrm{in}$')

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1 + h2, l1 + l2, loc='center left')
        plt.tight_layout()

        # --------------------------------------------------------------
        # 6. Export DC figures and CSV
        # --------------------------------------------------------------
        fig2.savefig(str(figures_dir / "amplifier_tb_dc_vout.svg"), bbox_inches='tight')
        fig2.savefig(str(figures_dir / "amplifier_tb_dc_vout.pdf"), bbox_inches='tight')
        np.savetxt(str(figures_dir / "amplifier_tb_dc_vout.csv"),
                   np.column_stack((vin, vout, gain)), comments="",
                   header="vin,vout,dvout_dvin", delimiter=",")

    # ------------------------------------------------------------------
    # 7. Load ngspice transient simulation data
    # ------------------------------------------------------------------
    ngspice_file_tran = data_dir / "amplifier_tb_tran.txt"

    if not missing(ngspice_file_tran):
        time = ng.loadngspicecol(str(ngspice_file_tran), "time")
        vin_t = ng.loadngspicecol(str(ngspice_file_tran), "v(vin)")
        vout_t = ng.loadngspicecol(str(ngspice_file_tran), "v(vout)")

        time_ms = time * 1e3

        # Small-signal gain from the peak-to-peak values of the steady-state part.
        # The first 10% of the run is dropped so that the initial settling does
        # not distort the peak-to-peak measurement.
        settled = time >= (time[0] + 0.1 * (time[-1] - time[0]))
        vin_pp = float(np.ptp(vin_t[settled]))
        vout_pp = float(np.ptp(vout_t[settled]))
        gain_VV = vout_pp / vin_pp if vin_pp > 0 else float('nan')
        gain_dB = 20.0 * np.log10(gain_VV) if gain_VV > 0 else float('nan')

        # --------------------------------------------------------------
        # 8. Transient Plot
        # --------------------------------------------------------------
        vin_color_t = '#2f855a'
        vout_color_t = '#0c5da5'
        marker_color = '#444444'
        box_kw = dict(boxstyle='round,pad=0.4', fc='white', ec=marker_color, alpha=0.9)

        fig3, axs3 = plt.subplots(2, sharex=True)
        fig3.set_figwidth(10)
        fig3.set_figheight(7)
        fig3.suptitle('Amplifier - Transient Response')

        axs3[0].plot(time_ms, vin_t, color=vin_color_t, linewidth=2.0)
        axs3[0].set_ylabel(r'$V_\mathrm{in}$ (V)')
        axs3[0].grid(visible=True, which='both', linestyle='--', alpha=0.5)

        axs3[1].plot(time_ms, vout_t, color=vout_color_t, linewidth=2.0)
        axs3[1].set_xlabel(r'$t$ (ms)')
        axs3[1].set_ylabel(r'$V_\mathrm{out}$ (V)')
        axs3[1].grid(visible=True, which='both', linestyle='--', alpha=0.5)

        tran_text = '\n'.join((
            rf'$V_\mathrm{{in,pp}} = {vin_pp*1e3:.2f}\,\mathrm{{mV}}$',
            rf'$V_\mathrm{{out,pp}} = {vout_pp*1e3:.2f}\,\mathrm{{mV}}$',
            rf'$A_\mathrm{{v}} = {gain_VV:.1f}\,\mathrm{{V/V}}\;({gain_dB:.1f}\,\mathrm{{dB}})$',
        ))
        axs3[1].text(0.02, 0.05, tran_text, transform=axs3[1].transAxes,
                     ha='left', va='bottom', color=marker_color, bbox=box_kw,
                     zorder=6)

        plt.tight_layout()

        # --------------------------------------------------------------
        # 9. Export transient figures and CSV
        # --------------------------------------------------------------
        fig3.savefig(str(figures_dir / "amplifier_tb_tran.svg"), bbox_inches='tight')
        fig3.savefig(str(figures_dir / "amplifier_tb_tran.pdf"), bbox_inches='tight')
        np.savetxt(str(figures_dir / "amplifier_tb_tran.csv"),
                   np.column_stack((time, vin_t, vout_t)), comments="",
                   header="time,vin,vout", delimiter=",")

    # ------------------------------------------------------------------
    # 10. Open the plot windows (blocks until they are closed)
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
