#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Post-layout timing of the macro at the 1.2 V to 1.65 V of the chip, below the 3.0 V of its Liberty files.
#
# One ngspice run per case. q0 to q7 are sampled at 0.9 T after each rising clock edge and compared with the expected count, through the wrap from 255 to 0.
# usage: counter_hv_kvc_top_tb_low_vdd.py [--jobs <n>]
import argparse
import concurrent.futures
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PEX = os.path.join(HERE, "..", "..", "netlist", "pex", "counter_hv_kvc_top_magic_pex_3.spice")
DATA = os.path.join(HERE, "data")
RUNS = os.path.join(HERE, "simulations")
SUMMARY = os.path.join(DATA, "counter_hv_kvc_top_tb_low_vdd.rpt")
CYCLES = 264
RST_CYCLES = 4.1

# mos corner, temperature, supply, level of the inputs, clock in MHz
CASES = [
    ("ss", 125, 1.2, 1.2, 50),
    ("tt", 27, 1.2, 1.2, 50),
    ("ff", -40, 1.2, 1.2, 50),
    ("ss", 125, 1.2, 1.2, 25),
    ("ss", 125, 1.2, 1.2, 12.5),
    ("tt", 27, 1.5, 1.2, 50),
    ("ff", -40, 1.65, 1.2, 50),
]

DECK = """* post-layout HV counter, {c} corner, {t} C, supply {v} V, inputs {vin} V, {f} MHz
.include {pex}
.lib cornerMOSlv.lib mos_{c}
.lib cornerMOShv.lib mos_{c}
.lib cornerRES.lib res_typ
.lib cornerDIO.lib dio_tt
.param fclk={f}e6
.temp {t}
.options klu method=gear reltol=1e-3 abstol=1e-12 gmin=1e-12 rshunt=1e14
Vvdd vdd 0 {v}
Vclk clk 0 pulse(0 {vin} 0 100p 100p {{0.5/fclk}} {{1/fclk}})
Vrst rst 0 pwl(0 0 {{{rst}/fclk}} 0 {{{rst}/fclk+100p}} {vin})
Ven en 0 {vin}
xdut vdd 0 clk rst en q0 q1 q2 q3 q4 q5 q6 q7 counter_hv_kvc_top_pex
.control
set num_threads=8
save clk rst q0 q1 q2 q3 q4 q5 q6 q7
tran 1n {tstop}
set wr_vecnames
set wr_singlescale
wrdata {data} v(clk) v(rst) v(q0) v(q1) v(q2) v(q3) v(q4) v(q5) v(q6) v(q7)
.endc
.end
"""


def simulate(case):
    """Runs one case, returns the path of its data file."""
    c, t, v, vin, f = case
    tag = "%s_%d_%sv_%smhz" % (c, t, v, f)
    deck = os.path.join(RUNS, tag + ".spice")
    data = os.path.join(DATA, tag + ".txt")
    with open(deck, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(DECK.format(c=c, t=t, v=v, vin=vin, f=f, pex=os.path.abspath(PEX), rst=RST_CYCLES, tstop="%g" % (CYCLES / f / 1e6), data=data))
    with open(os.path.join(RUNS, tag + ".log"), "w", encoding="utf-8") as log:
        subprocess.run(["ngspice", "-b", deck], stdout=log, stderr=subprocess.STDOUT, cwd=RUNS, check=True)
    return data


def judge(case, path):
    """Returns one verdict line and whether the case passed."""
    c, temp, vdd, _, f_mhz = case
    T = 1e-6 / f_mhz
    with open(path, encoding="utf-8") as fh:
        names = fh.readline().split()
    d = np.loadtxt(path, skiprows=1)
    t = d[:, names.index("time")]
    q = np.array([d[:, names.index("v(q%d)" % i)] for i in range(8)])
    n_edges = int(t[-1] / T)
    vth = vdd / 2.0

    def value(ts):
        return sum(int(np.interp(ts, t, q[i]) > vth) << i for i in range(8))

    # rst is released at 4.1 T, so the edge at 5 T is the first one that counts
    wrong, first, seq = 0, None, []
    for k in range(5, n_edges):
        got, want = value((k + 0.9) * T), (k - 4) % 256
        seq.append(got)
        if got != want:
            wrong += 1
            first = first or (k, got, want)
    # latest output crossing after a clock edge, as a fraction of the period
    worst = 0.0
    for i in range(8):
        s = q[i] > vth
        for idx in np.nonzero(s[1:] != s[:-1])[0]:
            if t[idx] >= 5 * T:
                worst = max(worst, (t[idx] % T) / T)
    wrap = any(a == 255 and b == 0 for a, b in zip(seq, seq[1:]))
    good = wrong == 0 and wrap
    line = "%s %-3s %4d C VDD %.2f V %5.1f MHz, edges %d, wrong %d, wrap 255->0 %s, last output crossing %.2f T" % ("PASS" if good else "FAIL", c, temp, vdd, f_mhz, n_edges - 5, wrong, wrap, worst)
    if first:
        line += ", first wrong at edge %d: got %d, want %d" % first
    return line, good


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=len(CASES), help="parallel ngspice runs, 8 threads each")
    args = ap.parse_args()
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(RUNS, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        paths = list(pool.map(simulate, CASES))
    done = [judge(case, path) for case, path in zip(CASES, paths)]
    with open(SUMMARY, "w", encoding="utf-8", newline="\n") as fh:
        for line, _ in done:
            print(line)
            fh.write(line + "\n")
    sys.exit(0 if all(ok for _, ok in done) else 1)


if __name__ == "__main__":
    main()
