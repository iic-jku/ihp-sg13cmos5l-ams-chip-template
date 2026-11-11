# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Turns the EM solves of the MoM cap fixtures into the parasitics table that momf_lpe.py reads.
# ============================================
#
# Usage: python3 verification/em/scripts/momf_parasitics.py <geometry> ..., after the Palace runs of make sim-em-momf.
#
# Input:  verification/em/palace_model/momf_<geometry>_<kind>_data/output/*/port-S.csv of palace_momf.py.
# Output: verification/em/cap_cmomf_parasitics.json, one entry per cap geometry.
#
# Open-short de-embedding removes the leads and the feeds: Zc = 1/(1/Zdut - 1/Zopen) - 1/(1/Zshort - 1/Zopen), which
# leaves out the small resistance of the short's solid metal. rs is Re(Zc) at the higher frequency, ls and C follow from
# Im(Zc) = w ls - 1/(w C) at the two frequencies. C is reported to compare with the model, not used. The capacitance
# of each plate to the substrate, cs, comes from C-coupled Magic extractions of the cap with its feeds less the feeds
# alone, whose metal the post-layout extraction keeps. These are the area and fringe terms, which Magic gets right (the
# sidewall term between the fingers is the one it got wrong).

import csv
import glob
import json
import math
import os
import subprocess
import sys

import klayout.db as kdb

HERE = os.path.dirname(os.path.abspath(__file__))
MACRO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import palace_momf as pm  # noqa: E402

Z0 = 50.0
OUT = os.path.join(MACRO, "verification", "em", "cap_cmomf_parasitics.json")


def s11(name):
    """{frequency in GHz: S11} from Palace's port-S.csv of one structure."""
    hits = glob.glob(os.path.join(MACRO, "verification", "em", "palace_model", f"{name}_data", "output", "*", "port-S.csv"))
    if len(hits) != 1:
        sys.exit(f"momf_parasitics.py: {len(hits)} port-S.csv for {name}, run make sim-em-momf")
    out = {}
    with open(hits[0], encoding="utf-8") as f:
        rows = list(csv.reader(f))
    for r in rows[1:]:
        f_ghz, mag_db, ang = float(r[0]), float(r[1]), float(r[2])
        out[round(f_ghz, 6)] = 10 ** (mag_db / 20) * complex(math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    return out


def plate_caps(ly, top, mk, work):
    """Capacitance of each plate to the substrate: the cap with its feeds less the feeds alone."""
    full = extract_caps(ly, top, mk, os.path.join(work, "full"), True)
    feeds = extract_caps(ly, top, mk, os.path.join(work, "feeds"), False)
    return {side: full[side] - feeds[side] for side in full}


def extract_caps(ly, top, mk, work, comb):
    """Capacitance of each feed to the rest, from a C-coupled Magic run (KPEX), with or without the comb."""
    em = kdb.Layout()
    em.dbu = ly.dbu
    cell = em.create_cell("momf_cs")
    marker = kdb.Region(mk["poly"])
    idx = [pm.COMB.index(s) for s in mk["stack"]]
    for name in mk["stack"] + [f"Via{i + 1}" for i in idx[:-1]]:
        lay = pm.METALS.get(name, pm.VIAS.get(name))
        reg = kdb.Region(top.begin_shapes_rec(ly.find_layer(lay, 0))) & marker if comb else kdb.Region()
        for metal, f in mk["feeds"]:
            if metal == name:
                reg += f
        cell.shapes(em.layer(lay, 0)).insert(reg.merged())
    for side, (metal, f) in zip("AB", mk["feeds"]):
        box = max(f.each(), key=lambda p: p.area()).decompose_trapezoids()
        box = max(box, key=lambda q: q.area()).bbox()
        cell.shapes(em.layer(pm.METALS[metal], 2)).insert(box)
        cell.shapes(em.layer(pm.METALS[metal], 25)).insert(kdb.Text(side, kdb.Trans(box.center())))
    os.makedirs(work, exist_ok=True)
    gds = os.path.join(work, "momf_cs.gds")
    em.write(gds)
    spice = os.path.join(work, "momf_cs.spice")
    subprocess.run(["kpex", "--pdk", os.environ["PDK"], "--cell", "momf_cs", "--gds", gds, "--magic", "--magic_mode", "CC",
                    "--out_dir", work, "--out_spice", spice], check=True, capture_output=True)
    caps = {"A": 0.0, "B": 0.0}
    mult = {"a": 1e-18, "f": 1e-15, "p": 1e-12}
    for line in open(spice, encoding="utf-8"):
        t = line.split()
        if t and t[0][0] in "Cc" and len(t) >= 4:
            v = t[3].lower()
            v = float(v[:-1]) * mult[v[-1]] if v[-1] in mult else float(v)
            a, b = t[1], t[2]
            for side in "AB":
                other = "B" if side == "A" else "A"
                if side in (a, b) and other not in (a, b):
                    caps[side] += v
    return caps


def main():
    ly = kdb.Layout()
    ly.read(os.path.join(MACRO, "layout", f"{pm.TOP}.gds"))
    top = ly.cell(pm.TOP)
    top.flatten(True)
    table = []
    geos = pm.geometries(ly, top)
    if not sys.argv[1:] or not set(sys.argv[1:]) <= set(geos):
        sys.exit(f"usage: momf_parasitics.py <geometry> ..., the layout has {sorted(geos)}")
    for geo in sys.argv[1:]:
        mk = geos[geo]
        s = {k: s11(f"momf_{geo}_{k}") for k in pm.KINDS}
        z = {k: {f: Z0 * (1 + v) / (1 - v) for f, v in s[k].items()} for k in pm.KINDS}
        zc = {f: 1 / (1 / z["dut"][f] - 1 / z["open"][f]) - 1 / (1 / z["short"][f] - 1 / z["open"][f]) for f in z["dut"]}
        (f1, z1), (f2, z2) = sorted(zc.items())
        w1, w2 = 2 * math.pi * f1 * 1e9, 2 * math.pi * f2 * 1e9
        ls = (z2.imag * w2 - z1.imag * w1) / (w2 ** 2 - w1 ** 2)
        c = 1 / (w1 ** 2 * ls - z1.imag * w1)
        cs = plate_caps(ly, top, mk, os.path.join("/tmp", f"momf_cs_{geo}"))
        entry = {"w": mk["w"], "l": mk["l"], "mmin": mk["mmin"], "mmax": mk["mmax"],
                 "rs": round(z2.real, 4), "ls": float(f"{ls:.4g}"), "cs": float(f"{(cs['A'] + cs['B']) / 2:.4g}"),
                 "rs_at_f1": round(z1.real, 4), "c_em": float(f"{c:.4g}"), "cs_plates": [float(f"{cs['A']:.4g}"), float(f"{cs['B']:.4g}")],
                 "source": f"Palace order {pm.ORDER} {pm.METALS_MODEL} metal, open-short at {f1:g} and {f2:g} GHz, cs from Magic C-coupled"}
        table.append(entry)
        print(f"momf_parasitics.py: {geo}: rs {entry['rs']} Ohm ({entry['rs_at_f1']} at {f1:g} GHz), ls {ls * 1e12:.2f} pH, "
              f"C {c * 1e15:.1f} fF (EM), cs {cs['A'] * 1e15:.2f} / {cs['B'] * 1e15:.2f} fF")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(table, f, indent=1)
    print(f"momf_parasitics.py: wrote {OUT}")


if __name__ == "__main__":
    main()
