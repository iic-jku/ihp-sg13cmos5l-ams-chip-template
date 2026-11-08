#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: KLayout LVS of the whole chip at transistor level, with planted defects as negative controls.
#
# Builds the reference with mk_ref.py, runs the PDK's run_lvs.py and judges the run from its .lvsdb: run_lvs.py exits 0 on a mismatch too.
# usage: run.py --gds <layout> --top <top cell> --gds-top <cell holding the placed cells> --work <dir> [--strict] [--negative] [--jobs <n>]
import argparse
import collections
import concurrent.futures
import glob
import os
import re
import shutil
import subprocess
import sys

import klayout.db as db

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RUN_LVS = os.path.join(os.environ["PDK_ROOT"], os.environ["PDK"], "libs.tech/klayout/tech/lvs/run_lvs.py")

# tag, how to plant the defect in the reference, the circuit that has to stop matching (None: the top cell)
CONTROLS = [
    ("top_mux", ("swap", None, "sg13cmos5l_mux2_1", "A0", "A1"), None),
    ("lv_macro", ("swap", "counter_lv_ihp_top", "sg13cmos5l_dfrbpq_1$1", "D", "CLK"), "counter_lv_ihp_top"),
    ("eth_macro", ("swap", "counter_lv_eth_top", "DFFQX1", "D", "CK"), "counter_lv_eth_top"),
    ("hv_macro", ("swap", "counter_hv_kvc_top", "sg13g2_hv_dfrbpq_1", "D", "CLK"), "counter_hv_kvc_top"),
    ("pad", ("swap", None, "sg13cmos5l_IOPadIn", "p2c", "pad"), None),
    ("analog", ("swap", None, "amplifier", "vin", "vout"), None),
    ("coil", ("param", None, "L", "nr_r=2", "nr_r=3"), None),
]


def lvs(gds, cdl, top, run_dir, strict):
    """Runs the PDK runner, returns True when it reports that the netlists match."""
    shutil.rmtree(run_dir, ignore_errors=True)
    os.makedirs(run_dir)
    cmd = [sys.executable, RUN_LVS, "--layout=" + gds, "--netlist=" + cdl, "--topcell=" + top, "--run_dir=" + run_dir, "--run_mode=deep", "--combine_devices", "--disable_tap_extraction"]
    if not strict:
        # a GDS whose pad labels sit one level below its top cell has no top-level pins to compare
        cmd.append("--ignore_top_ports_mismatch")
    log = run_dir + ".log"
    with open(log, "w", encoding="utf-8") as fh:
        subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, check=False)
    text = open(log, encoding="utf-8", errors="replace").read()
    return "PASS (netlists match)" in text


def lvsdb(run_dir):
    found = glob.glob(os.path.join(run_dir, "*.lvsdb"))
    if len(found) != 1:
        sys.exit("run: want one .lvsdb in %s, found %d" % (run_dir, len(found)))
    data = db.LayoutVsSchematic()
    data.read(found[0])
    return data


def circuits(data):
    """Status name to count, and the layout names of the circuits that do not match."""
    status = db.NetlistCrossReference
    names = {status.Match: "Match", status.MatchWithWarning: "MatchWithWarning", status.Mismatch: "Mismatch", status.NoMatch: "NoMatch", status.Skipped: "Skipped"}
    count, bad = collections.Counter(), []
    for pair in data.xref().each_circuit_pair():
        name = names.get(pair.status(), str(pair.status()))
        count[name] += 1
        if name not in ("Match", "MatchWithWarning"):
            first, second = pair.first(), pair.second()
            bad.append((name, first.name if first else "-", second.name if second else "-"))
    return count, bad


def flat_devices(netlist):
    """Flat device count per class, top circuit down."""
    order = list(netlist.each_circuit_top_down())
    mult = {order[0].name: 1}
    for circuit in order:
        k = mult.get(circuit.name, 0)
        for sub in circuit.each_subcircuit():
            mult[sub.circuit_ref().name] = mult.get(sub.circuit_ref().name, 0) + k
    count = collections.Counter()
    for circuit in order:
        k = mult.get(circuit.name, 0)
        for device in circuit.each_device():
            count[device.device_class().name.upper()] += k
    return count


def plant(cdl, out, how, top):
    """Writes a copy of the reference with one defect in it."""
    kind, sub, cell, a, b = how
    sub = sub or top
    lines = open(cdl, encoding="utf-8").read().split("\n")
    ports = {ln.split()[1]: ln.split()[2:] for ln in lines if ln.startswith(".SUBCKT ")}
    inside = False
    for i, ln in enumerate(lines):
        if ln.startswith(".SUBCKT "):
            inside = ln.split()[1] == sub
            continue
        t = ln.split()
        if not inside or not t:
            continue
        if kind == "swap" and t[0][0] in "Xx":
            if [x for x in t if "=" not in x][-1] != cell:
                continue
            pa, pb = 1 + ports[cell].index(a), 1 + ports[cell].index(b)
            if t[pa] == t[pb]:
                continue
            t[pa], t[pb] = t[pb], t[pa]
        elif kind == "param" and t[0].startswith(cell) and a in t:
            t[t.index(a)] = b
        else:
            continue
        lines[i] = " ".join(t)
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines))
        return
    sys.exit("run: no card found for control %s" % (how,))


def control(args, tag, how, want):
    cdl = os.path.join(args.work, "control_%s.cdl" % tag)
    plant(args.cdl, cdl, how, args.top)
    run_dir = os.path.join(args.work, "control_" + tag)
    passed = lvs(args.gds, cdl, args.top, run_dir, args.strict)
    _, bad = circuits(lvsdb(run_dir))
    hit = [b[1] for b in bad]
    ok = not passed and hit == [want or args.top]
    return "control %-10s %s, does not match: %s" % (tag, "caught" if ok else "NOT CAUGHT", " ".join(hit) or "-"), ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gds", required=True)
    ap.add_argument("--top", required=True, help="top cell of the GDS, also the top subcircuit of the reference")
    ap.add_argument("--gds-top", default="chip_top", help="the cell of the GDS that holds the placed cells")
    ap.add_argument("--work", required=True)
    ap.add_argument("--cdl", help="where to write the reference, default <work>/<top>.cdl")
    ap.add_argument("--strict", action="store_true", help="also compare the top-level pin names, for a GDS that has its pad labels in the top cell")
    ap.add_argument("--negative", action="store_true", help="also run the planted defects, each has to fail in its own circuit")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    os.makedirs(args.work, exist_ok=True)
    args.cdl = args.cdl or os.path.join(args.work, args.top + ".cdl")
    subprocess.run([sys.executable, os.path.join(HERE, "mk_ref.py"), "--root", ROOT, "--gds", args.gds, "--gds-top", args.gds_top, "--top", args.top, "-o", args.cdl], check=True, stdout=subprocess.DEVNULL)

    run_dir = os.path.join(args.work, "lvs")
    passed = lvs(args.gds, args.cdl, args.top, run_dir, args.strict)
    data = lvsdb(run_dir)
    count, bad = circuits(data)
    layout, schematic = flat_devices(data.netlist()), flat_devices(data.reference)
    good = passed and not bad and layout == schematic
    print("verdict %s, circuit pairs %s, flat devices %d layout, %d schematic" % ("PASS" if good else "FAIL", dict(count), sum(layout.values()), sum(schematic.values())))
    for row in bad:
        print("  %s: layout %s, schematic %s" % row)
    if args.negative:
        with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
            done = list(pool.map(lambda c: control(args, *c), CONTROLS))
        for line, _ in done:
            print(line)
        good = good and all(ok for _, ok in done)
    sys.exit(0 if good else 1)


if __name__ == "__main__":
    main()
