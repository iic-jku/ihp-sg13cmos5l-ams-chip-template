# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Check the size and metal stack of every cap_cmomf of a cell against its schematic, which LVS does not.
"""The KLayout LVS deck of ihp-sg13cmos5l compares neither w nor l of a MoM capacitor, and mmin and mmax never reach
the LVS netlist at all, so a schematic at the wrong size or stack still matches, while the model's density runs from
0.61 to 1.29 fF/um2 over the stacks. This check closes both gaps after an LVS pass.

Layout: every cap_cmomf recognition marker (99/40) of the cell, its extent (l along x, w along y, as the PCell draws
them) and the metals drawn inside it (mmin to mmax). Schematic: every cap_cmomf instance of the cell's .sch, a vector
instance such as Cct1a[1..2] counted by its width. The two lists have to be equal.

    python3 scripts/check_mom.py layout/vco_buf.gds schematic/xschem/vco_buf.sch [--self-test]

Exit 0 when they are, 1 otherwise.
"""

import re
import sys
from collections import Counter

import klayout.db as db

L_MARKER = (99, 40)
METALS = {1: (8, 0), 2: (10, 0), 3: (30, 0), 4: (50, 0)}


def layout_caps(gds):
    ly = db.Layout()
    ly.read(gds)
    top = ly.top_cell()
    li = ly.find_layer(*L_MARKER)
    caps = []
    if li is None:
        return caps
    metal = {n: db.Region(top.begin_shapes_rec(ly.find_layer(*ld))) if ly.find_layer(*ld) is not None else db.Region()
             for n, ld in METALS.items()}
    for p in db.Region(top.begin_shapes_rec(li)).merged().each():
        b = p.bbox()
        inner = db.Region(b.enlarged(-10, -10))  # 10 nm inside, so a neighbour touching the edge does not count
        stack = [n for n, r in metal.items() if not (r & inner).is_empty()]
        caps.append((round(b.height() * ly.dbu, 3), round(b.width() * ly.dbu, 3), min(stack), max(stack)))
    return caps


def schematic_caps(sch):
    text = open(sch, encoding="utf-8").read()
    caps = []
    for m in re.finditer(r"^C \{[^}]*cap_cmomf\.sym\} [^{]*\{(.*?)\}\s*$", text, re.S | re.M):
        attrs = dict(re.findall(r"(\w+)=(\S+)", m.group(1)))
        count = 1
        bus = re.search(r"\[(\d+)(?:\.\.|:)(\d+)\]", attrs.get("name", ""))
        if bus:
            count = abs(int(bus.group(1)) - int(bus.group(2))) + 1
        count *= int(attrs.get("m", "1"))
        cap = (round(float(attrs["w"]) * 1e6, 3), round(float(attrs["l"]) * 1e6, 3), int(attrs["mmin"]), int(attrs["mmax"]))
        caps += [cap] * count
    return caps


def compare(lay, sch, say=print):
    lc, sc = Counter(lay), Counter(sch)
    ok = lc == sc
    for cap in sorted(set(lc) | set(sc)):
        say("check_mom: w %6.2f um, l %6.2f um, Metal%d..Metal%d: layout %d, schematic %d%s"
            % (cap + (lc[cap], sc[cap], "" if lc[cap] == sc[cap] else "  MISMATCH")))
    return ok


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 1
    lay, sch = layout_caps(args[0]), schematic_caps(args[1])
    ok = compare(lay, sch)
    if "--self-test" in argv and sch:
        w, l, mn, mx = sch[0]
        for name, wrong in (("wrong w", [(w + 1.0, l, mn, mx)] + sch[1:]), ("wrong stack", [(w, l, mn % 4 + 1, mx)] + sch[1:])):
            caught = not compare(lay, wrong, say=lambda s: None)
            ok &= caught
            print("check_mom: self-test %-11s %s" % (name, "caught" if caught else "MISSED"))
    print("check_mom: %s (%d caps)" % ("PASS" if ok else "FAIL", len(lay)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
