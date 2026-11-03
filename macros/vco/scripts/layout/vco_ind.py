# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: KLayout batch script that draws the center-tapped tank coil layout/vco_ind.gds in TopMetal1.
# ============================================
#
# Usage: klayout -b -r scripts/layout/vco_ind.py [-rd out=<file.gds>], or make klayout-script CELL=vco_ind
#
# ihp-sg13cmos5l has no inductor PCell and no TopMetal2, so the coil is drawn here: a symmetric octagonal coil of two
# turns wound in TopMetal1, its one crossing in Metal4 and Metal3 in parallel. The leads LA and LB leave the outer turn
# at the bottom, the center tap LC leaves the inner turn between them. Rings, leads and tap match the 52 um inductor3
# of the ihp-sg13g2 macro. LVS extracts the coil as inductor2 from LA and LB. No LVS sees the center tap.

import os

import pya

# Coil geometry in um: trace width, spacing, inner diameter, two turns
W, S, D_INNER = 4, 4, 52
A_IN = D_INNER / 2 + W / 2  # center-line apothem of the inner turn
A_OUT = A_IN + W + S  # center-line apothem of the outer turn
YC = 68  # coil center, the feeds end at y = -1 like the PCell's
XG = 8  # half width of the gap at the crossing
X_LEAD = 8  # lead and tap center lines: LA at -X_LEAD, LB at +X_LEAD, LC at 0
Y_FEED = -1
LAND = 4  # length of the via landing where the crossing runs under a turn

# IND recognition box (the coil's keep-out), as for the PCell: 136 um square
IND_HALF = 68

# Substrate tap left of the feeds, below the keep-out
TAP_W, TAP_L = 4, 1
TAP_X, TAP_Y = -30, -3

GRID = 0.005
L_TM1, L_TV1, L_M4, L_V3, L_M3, L_M1 = (126, 0), (125, 0), (50, 0), (49, 0), (30, 0), (8, 0)
L_IND, L_IND_PIN, L_IND_TXT, L_TXT = (27, 0), (27, 2), (27, 25), (63, 0)
L_TM1_PIN, L_TM1_TXT, L_M1_TXT = (126, 2), (126, 25), (8, 25)

CELL = "vco_ind"
here = os.path.dirname(os.path.abspath(__file__))
out_file = globals().get("out") or os.path.join(here, "..", "..", "layout", f"{CELL}.gds")


def snap(v):
    return round(v / GRID) * GRID


def octagon(a):
    # Axis sides at distance a, diagonal sides on x + y = b with b on the grid, so every vertex lies on the grid
    b = snap(a * 2**0.5)
    pts = [(a, -(b - a)), (a, b - a), (b - a, a), (-(b - a), a), (-a, b - a), (-a, -(b - a)), (-(b - a), -a), (b - a, -a)]
    return pya.Region(pya.DPolygon([pya.DPoint(x, y + YC) for x, y in pts]).to_itype(0.001))


def ring(a):
    return octagon(a + W / 2) - octagon(a - W / 2)


def box(x1, y1, x2, y2):
    return pya.Region(pya.DBox(x1, y1, x2, y2).to_itype(0.001))


def crossing(sign, land):
    # One connector of the crossing, a 45 degree jog of width W between horizontal stubs, from the outer turn at
    # x = -sign * XG to the inner turn at x = +sign * XG. land extends both stubs under the turns.
    d = snap(W / 2 * 2**0.5)
    c = (A_OUT + A_IN) / 2  # x + y of the jog's center line relative to YC: it crosses the axis between the turns
    hi, lo = c + d, c - d
    to, bo, ti, bi = A_OUT + W / 2, A_OUT - W / 2, A_IN + W / 2, A_IN - W / 2
    pts = [(-XG - land, to), (hi - to, to), (hi - ti, ti), (XG + land, ti), (XG + land, bi), (lo - bi, bi), (lo - bo, bo), (-XG - land, bo)]
    return pya.Region(pya.DPolygon([pya.DPoint(sign * x, y + YC) for x, y in pts]).to_itype(0.001))


def via_array(region_box, size, space, enc):
    # Square cuts on a regular grid, centered in the box with at least enc to its edges
    x1, y1, x2, y2 = region_box
    out = pya.Region()
    n_x = int((x2 - x1 - 2 * enc + space) // (size + space))
    n_y = int((y2 - y1 - 2 * enc + space) // (size + space))
    span_x, span_y = n_x * size + (n_x - 1) * space, n_y * size + (n_y - 1) * space
    x0, y0 = snap((x1 + x2 - span_x) / 2), snap((y1 + y2 - span_y) / 2)
    for i in range(n_x):
        for j in range(n_y):
            x, y = x0 + i * (size + space), y0 + j * (size + space)
            out.insert(pya.DBox(x, y, x + size, y + size).to_itype(0.001))
    return out


ly = pya.Layout()
ly.dbu = 0.001
ly.technology_name = "sg13cmos5l"
top = ly.create_cell(CELL)

# Turns, cut at the top for the crossing and the outer turn at the bottom for the feeds
gap_top = box(-XG, YC + A_IN - W, XG, YC + A_OUT + W)
gap_bottom = box(-X_LEAD + W / 2, YC - A_OUT - W, X_LEAD - W / 2, YC - A_OUT + W)
tm1 = (ring(A_IN) + ring(A_OUT)) - gap_top - gap_bottom
# Crossing: outer left to inner right in TopMetal1, inner left to outer right in Metal4 and Metal3
tm1 += crossing(+1, 0)
under = crossing(-1, LAND)
# Leads from the outer turn and the tap from the inner turn down to the feed line
tm1 += box(-X_LEAD - W / 2, Y_FEED, -X_LEAD + W / 2, YC - A_OUT)
tm1 += box(X_LEAD - W / 2, Y_FEED, X_LEAD + W / 2, YC - A_OUT)
tm1 += box(-W / 2, Y_FEED, W / 2, YC - A_IN)
tm1.merge()

# Via landings where the crossing runs under the turns: TopVia1 to TopMetal1, Via3 between Metal4 and Metal3
lands = [(XG, YC + A_OUT - W / 2, XG + LAND, YC + A_OUT + W / 2), (-XG - LAND, YC + A_IN - W / 2, -XG, YC + A_IN + W / 2)]
tv1, v3 = pya.Region(), pya.Region()
for b in lands:
    tv1 += via_array(b, 0.42, 0.42, 0.42)
    v3 += via_array(b, 0.19, 0.29, 0.05)

for layer, region in ((L_TM1, tm1), (L_M4, under), (L_M3, under), (L_TV1, tv1), (L_V3, v3)):
    top.shapes(ly.layer(*layer)).insert(region)

# Recognition: IND box, one IND pin per lead across the box edge, the lead names, and the device name the deck needs
top.shapes(ly.layer(*L_IND)).insert(pya.DBox(-IND_HALF, YC - IND_HALF, IND_HALF, YC + IND_HALF))
for name, x in (("LA", -X_LEAD), ("LB", X_LEAD)):
    top.shapes(ly.layer(*L_IND_PIN)).insert(pya.DBox(x - W / 2, Y_FEED, x + W / 2, Y_FEED + 2))
    top.shapes(ly.layer(*L_IND_TXT)).insert(pya.DText(name, x, 0))
top.shapes(ly.layer(*L_TXT)).insert(pya.DText("inductor2", 0, YC))

# Pins on TopMetal1 for the macro and the EM ports, on the feed ends below the IND box: inside it TopMetal1 is device
# core and not a conductor, so a label there names no net. LC is a port only through that 1 um of tap outside the box.
for name, x in (("LA", -X_LEAD), ("LB", X_LEAD), ("LC", 0)):
    top.shapes(ly.layer(*L_TM1_PIN)).insert(pya.DBox(x - W / 2, Y_FEED, x + W / 2, Y_FEED + 1))
    top.shapes(ly.layer(*L_TM1_TXT)).insert(pya.DText(name, x, Y_FEED + 0.5))

# Substrate tap from the PDK PCell
lib = pya.Library.library_by_name("SG13_dev", "sg13cmos5l")
if lib is None:
    import importlib
    import sys

    kl = os.path.join(os.environ["PDK_ROOT"], os.environ["PDK"], "libs.tech", "klayout", "python")
    for d in (kl, os.path.join(kl, "pycell4klayout-api", "source", "python")):
        if d not in sys.path:
            sys.path.append(d)
    importlib.import_module("sg13cmos5l_pycell_lib")
tap = ly.create_cell("ptap1", "SG13_dev", {"w": f"{TAP_W}u", "l": f"{TAP_L}u"})
if tap is None:
    raise RuntimeError("vco_ind.py: PCell ptap1 not found in library SG13_dev")
tap_box = tap.dbbox()
top.insert(pya.DCellInstArray(tap.cell_index(), pya.DTrans(TAP_X - tap_box.center().x, TAP_Y - tap_box.center().y)))
top.flatten(-1, True)
top.shapes(ly.layer(*L_M1_TXT)).insert(pya.DText("VSS", TAP_X, TAP_Y))

opt = pya.SaveLayoutOptions()
opt.write_context_info = False
opt.gds2_write_timestamps = False
ly.write(out_file, opt)
print(f"vco_ind.py: wrote {os.path.normpath(out_file)}, cell {CELL}, bbox {top.dbbox()}")
# ==============================================================================
