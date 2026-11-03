# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: KLayout batch script that writes the output buffer layout/vco_buf.gds.
# ============================================
#
# Usage: klayout -b -r scripts/layout/vco_buf.py [-rd out=<file.gds>], or make klayout-script CELL=vco_buf
#
# Mirror-symmetric about x = 0, bottom to top: the VSS rail, the tail MBt (30 fingers, gate on top, its taps also bias
# the pair's substrate), the pair MB1/MB2 (gates on top), the 50 Ohm loads at the outer sides, the VDD rail, the gate
# bias line, the coupling caps with the gate bias resistors outside them, the vbg_buf track above them.
# The coupling caps are cap_cmomf on Metal2 to Metal4. Nothing crosses under them and Metal1 below them stays empty.
# Their plate A (west face) is the gate node, fed from the inner face, the left cap mirrored in x so that its plate A
# faces inward too. Plate B (north spine) is the input rf_p/rf_n, fed from above. A wide conductor may not merge onto
# a comb, so the feeds are rows of 0.35 um bridges from collectors 0.3 um outside the cap.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pya  # noqa: E402
import vco_layout as vl  # noqa: E402

Y1 = 4.5  # top of the pair's active areas
GAP = 1.5  # half the gap between the pair's active areas
XO = 12.0  # x of the output nodes, outside the pair
RL_Y = 6.5  # bottom of the load resistor bodies
VDD_Y = 9.1  # bottom of the VDD rail
Y_GB = 10.25  # y of the gate bias lines from the resistors to the gate lines, below the caps
CC_X, CC_Y, CC_W, CC_L = 4.5, 11.5, 10.0, 18.6  # inner edge, bottom, height (PCell w) and length (PCell l) of the caps
XG = 2.5  # x of the gate lines from the caps' collectors down to the pair
XIN = 8.0  # x of the inputs, under the core's rf_p and rf_n lines
RB_X = 24.25  # x of the gate bias resistors
TOP_Y = 22.5  # y of the vbg_buf track over the caps
Y_TOP = 23.5  # top edge, the inputs end there
X_EDGE = 26.0  # pins on the left edge sit at -X_EDGE

ly = vl.new_layout()
top = vl.Block(ly, "vco_buf")

# Tail, mirrored so its gate pad faces the pair
mbt = vl.mos(ly, "MBt", "nmos", 150.0, 0.5, 30, tap="merge")
aw = mbt.ports["ACT"][1].width()
pt = top.place(mbt, -aw / 2, 0.0, mirror=True)
vss_s = pt["S"][1]
vss = top.rect("Metal1", vss_s.left, vss_s.bottom - 1.2, vss_s.right, vss_s.bottom - 0.4)
top.rect("Metal1", vss_s.left, vss.top - 0.1, vss_s.right, vss_s.bottom + 0.1)
top.pin("Metal1", "VSS", pya.DBox(vss.left, vss.bottom, vss.left + 2.0, vss.top))
y_bot = vss.bottom  # the outputs end on the bottom edge, level with the VSS rail

# vbn_buf: the tail's gate pad to the left edge on Metal3
g = pt["G"][1]
top.via(g.left + 0.4, g.center().y, "Metal1", "Metal3")
vbn = top.rect("Metal3", -X_EDGE, g.center().y - 0.2, g.left + 0.6, g.center().y + 0.2)
top.pin("Metal3", "vbn_buf", pya.DBox(vbn.left, vbn.bottom, vbn.left + 1.0, vbn.top))

# The pair: MB1 on the left (mirrored), MB2 its image in x (rotated by 180 degrees)
mb = vl.mos(ly, "MB", "nmos", 24.0, 0.13, 12)
paw = mb.ports["ACT"][1].width()
pairs = {
    "left": top.place(mb, -GAP - paw, Y1, mirror=True),
    "right": top.place(mb, GAP + paw, Y1, rot=180),
}
td = pt["D"][1]
for side, sgn in (("left", -1), ("right", 1)):
    p = pairs[side]
    s, d = p["S"][1], p["D"][1]
    # Tail: three Metal2 stubs from the tail's drain strap up to the pair's source rail
    for f in (0.15, 0.5, 0.85):
        x = s.left + f * s.width()
        top.rect("Metal2", x - 0.3, td.center().y, x + 0.3, s.center().y + 0.15)
        top.via(x, s.center().y, "Metal1", "Metal2", cols=1, rows=1)
    # Output node: the drain strap out to x = sgn * XO, up to the load's bottom head, down to the bottom edge on Metal3
    xo = sgn * XO
    top.rect("Metal2", min(xo - 0.3, d.left), d.center().y - 0.3, max(xo + 0.3, d.right), d.center().y + 0.3)
    rl = top.pcell("rppd", Calculate="R", w=vl.um(10.0), l=vl.um(1.65), b=0)
    trl = top.add(rl, xo - 9.0 if sgn < 0 else xo - 1.0, RL_Y)
    bot_head, top_head = sorted(top.shapes(rl, trl, "Metal1"), key=lambda b: b.bottom)
    top.rect("Metal2", bot_head.left + 0.2, bot_head.bottom, bot_head.right - 0.2, bot_head.top)
    top.via(bot_head.center().x, bot_head.center().y, "Metal1", "Metal2", cols=20, rows=1)
    top.rect("Metal2", xo - 0.3, d.center().y, xo + 0.3, bot_head.top)
    top.via(xo, d.center().y, "Metal2", "Metal3", cols=1, rows=2)
    oline = top.rect("Metal3", xo - 0.3, y_bot, xo + 0.3, d.center().y + 0.3)
    top.pin("Metal3", "rf_out_n" if sgn < 0 else "rf_out_p", pya.DBox(oline.left, oline.bottom, oline.right, oline.bottom + 1.0))
    top.rect("Metal1", top_head.left, top_head.bottom, top_head.right, VDD_Y + 0.1)

    # Coupling cap: the right one as drawn, the left one mirrored in x, so plate A (west face) faces the axis
    cc = top.pcell("cap_cmomf", w=vl.um(CC_W), l=vl.um(CC_L), mmin=2, mmax=4)
    x_in = sgn * CC_X  # the cap's inner face
    top.add(cc, x_in, CC_Y, rot=180 if sgn < 0 else 0, mirror=sgn < 0)
    cap = pya.DBox(min(x_in, sgn * (CC_X + CC_L)), CC_Y, max(x_in, sgn * (CC_X + CC_L)), CC_Y + CC_W)
    # Plate A, the gate node: fed from the inner face, a bar from its collector over to the gate line
    col = vl.comb_feed(top, cap, "W" if sgn > 0 else "E")
    xg = sgn * XG
    yg = cap.center().y
    top.rect("Metal4", xg - 0.5 * sgn, yg - 0.5, col.center().x, yg + 0.5)
    top.via(xg, yg, "Metal2", "Metal4", cols=2, rows=2)
    gpad = p["G"][1]
    top.rect("Metal2", xg - 0.3, gpad.center().y, xg + 0.3, yg)
    top.via(xg, gpad.center().y, "Metal1", "Metal2", cols=1, rows=1)
    # Plate B, the input: fed from the north spine, a tab up from its collector
    colb = vl.comb_feed(top, cap, "N")
    xi = sgn * XIN
    tab = top.rect("Metal4", xi - 0.5, colb.top - 0.1, xi + 0.5, Y_TOP)
    top.pin("Metal4", "rf_p" if sgn < 0 else "rf_n", pya.DBox(tab.left, Y_TOP - 0.5, tab.right, Y_TOP))

    # Gate bias resistor outside the cap: bottom head onto the gate bias line under the cap, top head up to vbg_buf
    rb = top.pcell("rhigh", Calculate="R", w=vl.um(0.5), l=vl.um(8.0), b=0)
    trb = top.add(rb, sgn * RB_X - 0.25, Y_GB + 0.28)
    rb_bot, rb_top = sorted(top.shapes(rb, trb, "Metal1"), key=lambda b: b.bottom)
    top.via(rb_bot.center().x, rb_bot.center().y, "Metal1", "Metal2")
    top.rect("Metal2", min(rb_bot.center().x, xg) - 0.3, Y_GB - 0.25, max(rb_bot.center().x, xg) + 0.3, Y_GB + 0.25)
    top.via(rb_top.center().x, rb_top.center().y, "Metal1", "Metal2")
    top.rect("Metal2", rb_top.center().x - 0.3, rb_top.center().y, rb_top.center().x + 0.3, TOP_Y)

vbg = top.rect("Metal2", -X_EDGE + 0.5, TOP_Y - 0.3, RB_X + 0.3, TOP_Y + 0.3)
top.via(-X_EDGE + 0.8, TOP_Y, "Metal2", "Metal3")
vbg3 = top.rect("Metal3", -X_EDGE, TOP_Y - 0.3, -X_EDGE + 1.1, TOP_Y + 0.3)
top.pin("Metal3", "vbg_buf", pya.DBox(vbg3.left, vbg3.bottom, vbg3.left + 1.0, vbg3.top))
vdd = top.rect("Metal1", -XO - 10.0, VDD_Y, XO + 10.0, VDD_Y + 0.8)
top.pin("Metal1", "VDD", pya.DBox(vdd.left, vdd.bottom, vdd.left + 2.0, vdd.top))

vl.write(top, vl.out_path("vco_buf", __file__))
# ==============================================================================
