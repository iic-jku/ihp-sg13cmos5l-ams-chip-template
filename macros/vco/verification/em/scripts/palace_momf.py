# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Builds the EM fixtures of the MoM caps and their AWS Palace models with gds2palace.
# ============================================
#
# Usage: python3 verification/em/scripts/palace_momf.py <geometry> <kind>, or make sim-em-momf, which runs every
#        geometry and kind, Palace, and momf_parasitics.py.
#        python3 verification/em/scripts/palace_momf.py --list prints the geometries of the macro.
#
# Input:  layout/vco_top.gds, the caps as drawn with their feeds.
# Output: verification/em/layout/momf_<geometry>_<kind>.gds and the Palace model in
#         verification/em/palace_model/momf_<geometry>_<kind>_data/.
#
# cap_cmomf is a capacitance only, so momf_lpe.py adds the series resistance and inductance of the comb from these
# solves. Per cap geometry (w, l and metal stack) the first cap of the macro is cut out of the layout with the two
# feeds that drive its plates, and two Metal4 leads join the feeds at an in-plane port. Three structures de-embed the
# leads and the feeds (open-short): dut is the cap as drawn, open the feeds without the comb, short the comb replaced
# by solid metal on every level of its stack. One structure per call: gmsh keeps state between structures.

import json
import os
import sys

import klayout.db as kdb

HERE = os.path.dirname(os.path.abspath(__file__))
MACRO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(MACRO, "scripts"))
from drop_subcells import COMB, METALS, VIAS, cut_combs  # noqa: E402

TOP = "vco_top"
MARKER = (99, 40)  # Recog.momf
STACKUP = "SG13CMOS5L_200um.xml"
STACKUP_PDK = "ihp-sg13g2"  # ihp-sg13cmos5l ships no Palace workflow
KINDS = ("dut", "open", "short")
FREQS = [10, 20]  # GHz, point solves: two frequencies separate the series inductance from the capacitance

# Mesh. The KB of this flow: order 3 for MoM caps, whose 0.2 um fingers and 0.21 um gaps need it, and volume metal,
# because a surface impedance on every face of a strip as thick as it is wide counts its sidewalls as width.
ORDER = 3
REFINED_CELLSIZE = 0.3  # um, along the conductors: about the finger pitch
METALS_MODEL = "volume"

FEED = 1.5  # um outside the marker that the fixture keeps of each feed, its bridges and collector
LEAD_W, LEAD_OUT, SLOT = 2.0, 3.0, 1.0  # um, lead width, distance of the leads from the marker, port gap
PORT_LAYER = 201


def geometries(ly, top):
    """{geometry name: marker} for the first cap of each (w, l, mmin, mmax), from a cut copy, with its two feeds: the
    metal that touches the marker, as far as FEED outside it."""
    cut = kdb.Layout()
    cut.assign(ly)
    ctop = cut.cell(top.name)
    found = {}
    for mk in cut_combs(cut, ctop, MARKER, "momf"):
        box = mk["poly"].bbox().to_dtype(ly.dbu)
        mmin, mmax = COMB.index(mk["stack"][0]) + 1, COMB.index(mk["stack"][-1]) + 1
        name = f"w{box.height():g}_l{box.width():g}_m{mmin}{mmax}".replace(".", "p")
        if name in found:
            continue
        reg = kdb.Region(mk["poly"])
        near, touch = reg.sized(round(FEED / ly.dbu)), reg.sized(round(0.005 / ly.dbu))
        feeds = []
        for metal, patch in mk["pieces"]:
            full = kdb.Region(ctop.begin_shapes_rec(cut.find_layer(METALS[metal], 0))).merged().interacting(kdb.Region(patch))
            # only what touches the marker: a line of the same net passing within FEED, but joined outside it, stays out
            feeds.append((metal, (full & near).merged().interacting(touch)))
        found[name] = dict(mk, feeds=feeds, w=round(box.height(), 3), l=round(box.width(), 3), mmin=mmin, mmax=mmax)
    return found


def face(marker, feed):
    """Side of the marker box a feed lies on, W, E, S or N, and the part of the feed beside that side: a feed can run on
    past the cap's corner into a line of its net."""
    m = marker.bbox()
    f = round(FEED / 0.001)
    bands = {"W": kdb.Box(m.left - f, m.bottom, m.left, m.top), "E": kdb.Box(m.right, m.bottom, m.right + f, m.top),
             "S": kdb.Box(m.left, m.bottom - f, m.right, m.bottom), "N": kdb.Box(m.left, m.top, m.right, m.top + f)}
    touch = (feed & marker.sized(5)).bbox()
    side = min(bands, key=lambda s: bands[s].center().distance(touch.center()))
    beside = feed & kdb.Region(bands[side])
    if beside.is_empty():
        sys.exit(f"palace_momf.py: a feed of the cap at {m} lies on no side of its marker")
    return side, beside.bbox()


def leads(ly, marker, feeds):
    """Metal4 leads from the two feeds to an in-plane port, in dbu: (lead region, port box, port direction). Each lead
    starts 0.2 um inside the outer edge of its feed's collector, clear of the bridges between collector and comb."""
    u = lambda v: round(v / ly.dbu)
    m = marker.bbox()
    ends = []
    for _, f in feeds:
        s, pb = face(marker, f)
        c = pb.center()
        edge = {"W": m.left - u(LEAD_OUT), "E": m.right + u(LEAD_OUT), "S": m.bottom - u(LEAD_OUT), "N": m.top + u(LEAD_OUT)}[s]
        ends.append((s, kdb.Point(edge, c.y) if s in "WE" else kdb.Point(c.x, edge), pb))
    w2, ov = u(LEAD_W / 2), u(0.2)
    reg = kdb.Region()
    for s, e, pb in ends:  # stub from the collector's outer edge out to the lead's corner point
        reg.insert({"W": kdb.Box(e.x, e.y - w2, pb.left + ov, e.y + w2), "E": kdb.Box(pb.right - ov, e.y - w2, e.x, e.y + w2),
                    "S": kdb.Box(e.x - w2, e.y, e.x + w2, pb.bottom + ov), "N": kdb.Box(e.x - w2, pb.top - ov, e.x + w2, e.y)}[s])
    (sa, ea, _), (sb, eb, _) = ends
    g = u(SLOT / 2)
    if {sa, sb} in ({"W", "E"}, {"S", "N"}):  # opposite sides: a U over the north (or east) side, the port in its middle
        if sa in "WE":
            y = m.top + u(LEAD_OUT)
            xm = (ea.x + eb.x) // 2
            for e in (ea, eb):
                reg.insert(kdb.Box(e.x - w2, min(e.y, y), e.x + w2, y + w2))
                reg.insert(kdb.Box(min(e.x, xm), y - w2, max(e.x, xm), y + w2))
            reg = reg.merged() - kdb.Region(kdb.Box(xm - g, y - w2 - 1, xm + g, y + w2 + 1))
            return reg, kdb.Box(xm - g, y - w2, xm + g, y + w2), "x"
        x = m.right + u(LEAD_OUT)
        ym = (ea.y + eb.y) // 2
        for e in (ea, eb):
            reg.insert(kdb.Box(min(e.x, x), e.y - w2, x + w2, e.y + w2))
            reg.insert(kdb.Box(x - w2, min(e.y, ym), x + w2, max(e.y, ym)))
        reg = reg.merged() - kdb.Region(kdb.Box(x - w2 - 1, ym - g, x + w2 + 1, ym + g))
        return reg, kdb.Box(x - w2, ym - g, x + w2, ym + g), "y"
    # adjacent sides: an L to the corner the two corner points span, the port on the leg of the second feed
    (sh, eh), (sv, ev) = ((sa, ea), (sb, eb)) if sa in "WE" else ((sb, eb), (sa, ea))
    corner = kdb.Point(eh.x, ev.y)
    reg.insert(kdb.Box(eh.x - w2, min(eh.y, corner.y) - w2, eh.x + w2, max(eh.y, corner.y) + w2))
    reg.insert(kdb.Box(min(ev.x, corner.x) - w2, ev.y - w2, max(ev.x, corner.x) + w2, ev.y + w2))
    xm = (ev.x + corner.x) // 2
    reg = reg.merged() - kdb.Region(kdb.Box(xm - g, ev.y - w2 - 1, xm + g, ev.y + w2 + 1))
    return reg, kdb.Box(xm - g, ev.y - w2, xm + g, ev.y + w2), "x"


def build_fixture(ly, top, mk, kind, dst):
    """Writes the fixture of one cap: its comb (dut), nothing (open) or solid metal (short) inside the marker, the
    two feeds and the leads, on the comb's metals and the vias between them."""
    marker = kdb.Region(mk["poly"])
    stack = mk["stack"]
    idx = [COMB.index(s) for s in stack]
    vias = [f"Via{i + 1}" for i in idx[:-1]]
    em = kdb.Layout()
    em.dbu = ly.dbu
    cell = em.create_cell(f"momf_{kind}")
    lead, port, _ = leads(ly, marker, mk["feeds"])
    for name in stack + vias:
        lay = METALS.get(name, VIAS.get(name))
        reg = kdb.Region()
        if kind == "dut":
            reg = kdb.Region(top.begin_shapes_rec(ly.find_layer(lay, 0))) & marker
        elif kind == "short":
            reg = marker.dup()
        if name in stack:
            for metal, f in mk["feeds"]:
                if metal == name:
                    reg += f
            if name == "Metal4":
                reg += lead
        # Convex pieces: the feeds, their bridges and the comb's edge band enclose holes, which KLayout writes as cut
        # lines and gds2palace then repairs as malformed polygons, for hours.
        cell.shapes(em.layer(lay, 0)).insert(reg.merged().decompose_convex_to_region())
    cell.shapes(em.layer(PORT_LAYER, 0)).insert(port)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    em.write(dst)


def build_palace_model(gds_file, palace_dir, name, direction):
    from gds2palace import gds_reader, simulation_setup, stackup_reader, utilities

    base = os.path.join(os.environ["PDK_ROOT"], STACKUP_PDK, "libs.tech", "palace")
    stackup = next((os.path.join(base, sub, STACKUP) for sub in ("XML_stackup/legacy", "workflow")
                    if os.path.isfile(os.path.join(base, sub, STACKUP))), None)
    if stackup is None:
        sys.exit(f"palace_momf.py: stackup {STACKUP} not found in {base}")
    settings = {
        "unit": 1e-6, "margin": 20, "fstart": FREQS[0] * 1e9, "fstop": FREQS[-1] * 1e9, "fstep": 1e9,
        "refined_cellsize": REFINED_CELLSIZE, "cells_per_wavelength": 10, "meshsize_max": 20,
        "adaptive_mesh_iterations": 0, "order": ORDER, "no_gui": True, "no_preview": True,
        "filled_metals": METALS_MODEL == "volume", "fill_factor_correction": True,
    }
    ports = simulation_setup.all_simulation_ports()
    ports.add_port(simulation_setup.simulation_port(portnumber=1, voltage=1, port_Z0=50, source_layernum=PORT_LAYER,
                                                    target_layername="Metal4", direction=direction))
    materials, dielectrics, metals = stackup_reader.read_substrate(stackup)
    layers = metals.getlayernumbers()
    layers.extend(ports.portlayers)
    # merge_polygon_size joins each via row of the comb into one block, whose conductivity fill_factor_correction scales
    polygons = gds_reader.read_gds(gds_file, layers, purposelist=[0], metals_list=metals, merge_polygon_size=0.5)
    sim_path = utilities.create_sim_path(palace_dir, name, dirname="")
    settings.update({"simulation_ports": ports, "materials_list": materials, "dielectrics_list": dielectrics,
                     "metals_list": metals, "layernumbers": layers, "allpolygons": polygons, "sim_path": sim_path,
                     "model_basename": name})
    config, _ = simulation_setup.create_palace(ports.all_active_excitations(), settings)
    # point solves instead of a sweep
    cfg = json.load(open(config))
    cfg["Solver"]["Driven"] = {"Samples": [{"Type": "Point", "Freq": FREQS, "SaveStep": 0}], "AdaptiveTol": 0.0}
    json.dump(cfg, open(config, "w"), indent=2)
    print(f"palace_momf.py: wrote {os.path.normpath(config)}")


def main():
    ly = kdb.Layout()
    ly.read(os.path.join(MACRO, "layout", f"{TOP}.gds"))
    top = ly.cell(TOP)
    top.flatten(True)
    geos = geometries(ly, top)
    if sys.argv[1:] == ["--list"]:
        print(json.dumps({k: {f: v[f] for f in ("w", "l", "mmin", "mmax")} for k, v in geos.items()}))
        return
    if len(sys.argv) != 3 or sys.argv[1] not in geos or sys.argv[2] not in KINDS:
        sys.exit(f"usage: palace_momf.py <{'|'.join(geos)}> <{'|'.join(KINDS)}>, or --list")
    geo, kind = sys.argv[1:]
    name = f"momf_{geo}_{kind}"
    gds = os.path.join(MACRO, "verification", "em", "layout", f"{name}.gds")
    build_fixture(ly, top, geos[geo], kind, gds)
    _, _, direction = leads(ly, kdb.Region(geos[geo]["poly"]), geos[geo]["feeds"])
    build_palace_model(gds, os.path.join(MACRO, "verification", "em", "palace_model"), name, direction)


if __name__ == "__main__":
    main()
