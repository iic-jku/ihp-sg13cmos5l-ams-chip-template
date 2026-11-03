# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: KLayout batch script that writes the VCO core layout/vco_core.gds: coil, pair, varactors, Cct1 and Cct2.
# ============================================
#
# Usage: klayout -b -r scripts/layout/vco_core.py [-rd out=<file.gds>], or make klayout-script CELL=vco_core
# Needs layout/vco_ind.gds and layout/vco_var.gds. The array stays a subcell, so LVS compares the hierarchy of the
# schematic. The coil is read for its pins only: vco_top places it at this cell's origin, beside the core, because the
# ihp-sg13cmos5l deck extracts it in the top cell of a run (its third terminal is the substrate).
#
# A column under the coil's feeds (the coil cell's origin, feed ends at y = -1), symmetric about x = 0 where the circuit
# is: the feeds LA and LB drop to Metal3 lines at x = -8 and 8, which run down the whole column as rf_p and rf_n. The pair
# sits right below the feeds with its cross-coupling on Metal2 (rf_n) and Metal4 (rf_p), the varactor array below it with
# its buses on the same lines. The center tap LC goes to vdd_core on a TopMetal1 spine, which turns right to Cct1.
# Cct1 (2 x 2 cap_cmomf units) fills the space right of the column, Cct2 (two units) the space right of the buffer below
# it. The columns of each array are mirrored in pairs, so the plates facing each other share one collector: vdd_core in
# the middle (Metal4 under a TopMetal1 strap down to the pin), VSS on the outer faces (Metal4), joined by Metal4 bars
# along the top and the bottom and along the right edge. A Metal1 spine at x = -12 collects the coil's, the pair's and
# the array's taps, a Metal4 bar along the pair's source bar takes them to Cct1's VSS collector. The pair's current
# returns on TopMetal1 from there: down the channel between the column and Cct1, along under Cct1, and down Cct2's west
# collector to the pin.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pya  # noqa: E402
import vco_layout as vl  # noqa: E402

XF = 8.0  # x of the feeds LA (-XF) and LB (XF), the rf_p and rf_n lines
Y_FV = -6.0  # y of the feed via stacks down to Metal3
Y_PAIR = -11.0  # top of the pair's active areas
GAP = 5.0  # half the gap between the pair's active areas
Y_XN, Y_XP = -9.0, -8.0  # cross-coupling lines: rf_n on Metal2, rf_p on Metal4
Y_SP = -11.0  # y of the vdd_core bar from the spine over to the arrays' middle collector, 3 um wide on TopMetal1
Y_VAR = -16.0  # top edge of the varactor array cell
Y_BOT = -44.0  # bottom edge of the column, where rf_p, rf_n and vtune leave for the buffer
Y_VT = -42.0  # y of vtune's Metal4 jog from the array's line onto the axis
XS = -12.0  # x of the VSS spine
Y_VSS = -43.0  # y of the foot of the VSS spine
# cap_cmomf arrays on Metal1 to Metal4: x of the columns' outer edges, unit length (PCell l, along x) and height (w)
CCT1 = dict(x0=14.5, x1=69.5, y0=-43.0, y1=-4.0, l=26.0, w=19.0, rows=2)  # right of the column
CCT2 = dict(x0=28.5, x1=69.5, y0=-72.5, y1=-47.0, l=19.0, w=25.5, rows=1)  # right of the buffer
ROW_GAP = 1.0  # between the rows of Cct1, plate A's south spine above plate B's north spine
Y_VSS_TOP = (-3.5, -2.5)  # Metal4 VSS bar along the top of Cct1, under the coil's keep-out
Y_VSS_BOT = (-74.5, -73.5)  # Metal4 VSS bar along the bottom of Cct2
X_VSS_E = (69.8, 70.8)  # Metal4 VSS collector along the right edge, both arrays' east faces
Y_CELL_BOT = -75.0  # bottom edge of the cell, where vdd_core and VSS leave
# VSS return on TopMetal1: the channel right of the rf_n line, the band under Cct1, above the buffer's top edge at
# -45.1 in vco_top, and Cct2's west collector, widened to the gap beside the buffer (its right edge at 24.7)
X_CH = (10.0, 14.2)
Y_CH = (-45.0, -43.3)
X_C2W = (25.2, 28.2)

ly = vl.new_layout()
top = vl.Block(ly, "vco_core")

# Coil, and its feeds extended below its keep-out. The extensions end on the lead ends at y = -1 and stay off the
# coil's IND pin boxes: overlapping them made LVS extract the inductor in this cell instead of in vco_ind.
ind = vl.read_cell(ly, "vco_ind", __file__)
ipins = vl.cell_pins(ly, ind, pya.DCplxTrans())
for x in (-XF, XF):
    top.rect("TopMetal1", x - 2.0, Y_FV - 1.5, x + 2.0, -1.0)
    top.via(x, Y_FV, "Metal3", "TopMetal1", cols=4, rows=4, tcols=3, trows=3)

# rf_p and rf_n: Metal3 lines from the feed via stacks down the whole column
for name, x in (("rf_p", -XF), ("rf_n", XF)):
    line = top.rect("Metal3", x - 0.5, Y_BOT, x + 0.5, Y_FV + 0.5)
    top.pin("Metal3", name, pya.DBox(line.left, line.bottom, line.right, line.bottom + 1.0))

# Cross-coupled pair, gates on top: M1 (drain rf_p) left, M2 (drain rf_n) its image in x
pair = vl.mos(ly, "Mpair", "nmos", 20.0, 0.13, 10, tap="merge")
paw = pair.ports["ACT"][1].width()
m1 = top.place(pair, -GAP - paw, Y_PAIR, mirror=True)
m2 = top.place(pair, GAP + paw, Y_PAIR, rot=180)
for x, p in ((-XF, m1), (XF, m2)):
    top.via(x, p["D"][1].center().y, "Metal2", "Metal3", cols=2, rows=3)
# M1's gate is rf_n: up to a Metal2 line over to the rf_n line
g1 = m1["G"][1]
x1 = g1.right - 0.4
top.via(x1, g1.center().y, "Metal1", "Metal2")
top.rect("Metal2", x1 - 0.2, g1.center().y, x1 + 0.2, Y_XN + 0.2)
top.rect("Metal2", x1 - 0.2, Y_XN - 0.2, XF + 0.3, Y_XN + 0.2)
top.via(XF, Y_XN, "Metal2", "Metal3")
# M2's gate is rf_p: up on Metal4 to a line over to the rf_p line
g2 = m2["G"][1]
x2 = g2.left + 0.4
top.via(x2, g2.center().y, "Metal1", "Metal4")
top.rect("Metal4", x2 - 0.2, g2.center().y, x2 + 0.2, Y_XP + 0.2)
top.rect("Metal4", -XF - 0.3, Y_XP - 0.2, x2 + 0.2, Y_XP + 0.2)
top.via(-XF, Y_XP, "Metal3", "Metal4")

# Varactor array, its axis on x = 0, so its rf_p and rf_n buses lie on the column's lines
var = vl.read_cell(ly, "vco_var", __file__)
vb = var.dbbox()
tv = top.add(var, -4.925, Y_VAR - vb.top)
vpins = vl.cell_pins(ly, var, tv)

# vtune: the array's line down, a Metal4 jog onto the axis, down to the bottom edge
vt = vpins["vtune"][1]
xv = vt.center().x
top.rect("Metal3", vt.left, Y_VT - 0.5, vt.right, vt.bottom + 0.5)
top.via(xv, Y_VT, "Metal3", "Metal4", cols=1, rows=2)
top.rect("Metal4", xv - 0.3, Y_VT - 0.3, 0.3, Y_VT + 0.3)
vline = top.rect("Metal4", -0.3, Y_BOT, 0.3, Y_VT + 0.3)
top.pin("Metal4", "vtune", pya.DBox(vline.left, vline.bottom, vline.right, vline.bottom + 1.0))

# Cct1 and Cct2: per array a column pair, the left one as drawn (plate A west, plate B east), the right one mirrored in x,
# so both plates B face the middle gap and share the vdd_core collector there. Plates A face outward, onto VSS.
mid = {}
for name, a in (("Cct1", CCT1), ("Cct2", CCT2)):
    unit = top.pcell("cap_cmomf", w=vl.um(a["w"]), l=vl.um(a["l"]), mmin=1, mmax=4)
    xm0, xm1 = a["x0"] + a["l"], a["x1"] - a["l"]  # the middle gap
    cols_b, cols_a = [], []
    for r in range(a["rows"]):
        y = a["y0"] + r * (a["w"] + ROW_GAP)
        top.add(unit, a["x0"], y)
        top.add(unit, a["x1"], y, rot=180, mirror=True)
        left = pya.DBox(a["x0"], y, xm0, y + a["w"])
        right = pya.DBox(xm1, y, a["x1"], y + a["w"])
        cols_b += [vl.comb_feed(top, left, "E", col_w=xm1 - xm0 - 0.6), vl.comb_feed(top, right, "W", col_w=0.1)]
        cols_a += [vl.comb_feed(top, left, "W"), vl.comb_feed(top, right, "E")]
    # vdd_core collector: the middle gap on Metal4 for the whole array height, TopMetal1 over it, TopVia1 between
    xc = (xm0 + xm1) / 2
    top.rect("Metal4", xm0 + 0.3, a["y0"] + 0.5, xm1 - 0.3, a["y1"] - 0.5)
    for y in range(int(a["y0"] + 2), int(a["y1"] - 1), 3):
        top.via(xc, y, "Metal4", "TopMetal1", tcols=2, trows=2)
    mid[name] = (xm0 + 0.3, xm1 - 0.3)
    # VSS collectors on the outer faces, the west one over the array's full height
    top.rect("Metal4", a["x0"] - 1.3, a["y0"] + 0.5, a["x0"] - 0.3, a["y1"] - 0.5)

# vdd_core: the center tap's TopMetal1 spine down to a bar over to Cct1's middle collector, a strap down its gap, a jog
# between the arrays over to Cct2's gap and on down to the pin at the bottom edge
(m1x0, m1x1), (m2x0, m2x1) = mid["Cct1"], mid["Cct2"]
top.rect("TopMetal1", -2.0, Y_SP - 1.5, 2.0, -1.0)
top.rect("TopMetal1", -2.0, Y_SP - 1.5, m1x1, Y_SP + 1.5)
top.rect("TopMetal1", m1x0, CCT1["y0"] - 3.5, m1x1, CCT1["y1"] - 0.5)
y_jog = (CCT1["y0"] + CCT2["y1"]) / 2
top.rect("TopMetal1", min(m1x0, m2x0), y_jog - 1.0, max(m1x1, m2x1), y_jog + 1.0)
vdc = top.rect("TopMetal1", m2x0, Y_CELL_BOT, m2x1, y_jog + 1.0)
top.pin("TopMetal1", "vdd_core", pya.DBox(vdc.left, vdc.bottom, vdc.right, vdc.bottom + 1.0))

# VSS: the coil's tap over to a Metal1 spine, the pair's and the array's taps onto it. The pair's sources carry the whole
# core current and its 2 f0 pulses: via stacks all along the source bar, clear of the rf lines, up to a Metal4 bar that
# runs straight into Cct1's west VSS collector. Metal4 bars along the top of Cct1 and the bottom of Cct2 and a collector
# along the right edge join every VSS face. On Metal4 alone, that path to the pin was 16 Ohm in the post-layout netlist,
# 64 mV off the pair's gate-source voltage, so the current returns on TopMetal1 (X_CH, Y_CH, X_C2W), 0.34 Ohm.
tap = ipins["VSS"][1]
top.rect("Metal1", XS - 0.5, Y_VSS - 0.5, XS + 0.5, tap.top)
top.rect("Metal1", tap.left, tap.bottom, XS + 0.5, tap.top)
s1, s2 = m1["S"][1], m2["S"][1]
sbar = top.rect("Metal1", XS - 0.5, s1.bottom, s2.right, s1.top)
for x in (-11.5, -6.0, -3.0, 0.0, 3.0, 6.0, 10.0):
    top.via(x, sbar.center().y, "Metal1", "Metal4", cols=2, rows=2)
top.rect("Metal4", XS - 0.5, sbar.bottom - 1.2, CCT1["x0"] - 0.3, sbar.top)
# TopMetal1 return, its top 1.7 um under the vdd_core bar at Y_SP. TopVia1 rows every 3 um onto the Metal4 below it.
top.rect("Metal4", X_CH[0], Y_CH[1], X_CH[1], sbar.top)
top.rect("TopMetal1", X_CH[0], Y_CH[0], X_CH[1], Y_SP - 3.2)
for y in range(-16, int(Y_CH[1]), -3):
    top.via((X_CH[0] + X_CH[1]) / 2, y + 0.5, "Metal4", "TopMetal1", tcols=4, trows=2)
top.rect("TopMetal1", X_CH[0], Y_CH[0], X_C2W[1], Y_CH[1])
top.rect("Metal4", X_C2W[0], Y_VSS_BOT[0], X_C2W[1], CCT2["y1"] - 0.5)
vss = top.rect("TopMetal1", X_C2W[0], Y_CELL_BOT, X_C2W[1], Y_CH[1])
for y in range(int(CCT2["y1"]) - 2, int(Y_VSS_BOT[0]), -3):
    top.via((X_C2W[0] + X_C2W[1]) / 2, y, "Metal4", "TopMetal1", tcols=3, trows=2)
vss_var = vpins["VSS"][1]
top.rect("Metal1", XS - 0.5, vss_var.bottom, vss_var.left + 0.1, vss_var.top)
top.rect("Metal4", CCT1["x0"] - 1.3, Y_VSS_TOP[0], X_VSS_E[1], Y_VSS_TOP[1])
top.rect("Metal4", CCT1["x0"] - 1.3, CCT1["y0"] + 0.5, CCT1["x0"] - 0.3, Y_VSS_TOP[1])
top.rect("Metal4", X_VSS_E[0], Y_VSS_BOT[0], X_VSS_E[1], Y_VSS_TOP[1])
top.rect("Metal4", CCT2["x0"] - 1.3, Y_VSS_BOT[0], X_VSS_E[1], Y_VSS_BOT[1])
top.rect("Metal4", CCT2["x0"] - 1.3, Y_VSS_BOT[0], CCT2["x0"] - 0.3, CCT2["y1"] - 0.5)
top.pin("TopMetal1", "VSS", pya.DBox(vss.left, vss.bottom, vss.right, vss.bottom + 1.0))

vl.write(top, vl.out_path("vco_core", __file__), keep=("vco_var",))
# ==============================================================================
