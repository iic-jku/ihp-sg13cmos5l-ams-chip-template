# SPDX-FileCopyrightText: 2026 Harald Pretl, Johannes Kepler University, 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Check on the GDS that the coil's center tap lands on its electrical center, which no LVS can see.
"""The center tap of the tank coil, checked on the GDS.

The ihp-sg13cmos5l deck extracts the coil as a two-terminal inductor from LA to LB. Inside the IND box, Metal3,
Metal4 and TopMetal1 are device core and not conductors, so the tap that feeds vdd_core into the coil ends at the IND
edge in every extracted netlist. This script proves the tap with plain connectivity from Metal1 to TopMetal1 and no
IND exclusion, every probe read from the GDS (IND box, IND:text labels, the tap at the IND edge, the VSS label):

  1. coil      LA and LB are one net (the winding is continuous)
  2. tap       the TopMetal1 tap that crosses the IND bottom edge between the leads is on that net
  3. isolated  the substrate tap (VSS) is not on that net
  4. centre    cutting TopMetal1 along x = 0 over the tap and the turn it lands on splits the coil into two halves,
               LA with one half of the tap and LB with the other. So the tap sits where the path from LA meets the
               path from LB.
  5. symmetry  the two halves are mirror images about x = 0 in projection (all layers), to at most --tol of a half's
               area. Layer by layer they cannot be: the coil has one crossing, where one half dives to Metal4 and
               Metal3 and the other does not.

--self-test plants three defects (tap open, two turns shorted, tap off center) and fails unless each is caught.
--feed NET checks a parent instead: the net labeled NET is on the coil's net as drawn and off it once the tap is cut at
the IND edge, so NET reaches the coil through the tap and only through it.

    python3 scripts/check_coil_tap.py layout/vco_ind.gds [--tol 0] [--self-test]
    python3 scripts/check_coil_tap.py layout/vco_top.gds --feed vdd_core

Exit 0 when everything holds, 1 otherwise.
"""

import sys

import klayout.db as db

# Connectivity stack, bottom to top: (name, layer, datatype)
STACK = [("m1", 8, 0), ("v1", 19, 0), ("m2", 10, 0), ("v2", 29, 0), ("m3", 30, 0), ("v3", 49, 0), ("m4", 50, 0),
         ("tv1", 125, 0), ("tm1", 126, 0)]
NAMES = [nm for nm, _, _ in STACK]
L_IND, L_IND_TEXT, L_M1_TEXT = (27, 0), (27, 25), (8, 25)
CUT = 0.1  # um, width of the cut along x = 0
LAND_MARGIN = 1.5  # um, how far the cut reaches past the turn the tap lands on

_LAYOUTS = []  # regions built from a shape iterator refer to their layout, which has to outlive them


class Abort(Exception):
    pass


def read(gds):
    """The top cell as flat regions per stack layer, plus IND, its labels and the VSS label."""
    ly = db.Layout()
    ly.read(gds)
    _LAYOUTS.append(ly)
    top = ly.top_cell()

    def region(ld):
        li = ly.find_layer(*ld)
        return db.Region(top.begin_shapes_rec(li)) if li is not None else db.Region()

    def texts(ld):
        out = {}
        li = ly.find_layer(*ld)
        if li is not None:
            it = top.begin_shapes_rec(li)
            while not it.at_end():
                if it.shape().is_text():
                    t = it.shape().text.transformed(it.trans())
                    out[t.string] = db.Point(t.x, t.y)
                it.next()
        return out

    regs = {nm: region((lay, dt)).merged() for nm, lay, dt in STACK}
    return ly.dbu, regs, region(L_IND), texts(L_IND_TEXT), texts(L_M1_TEXT), top.bbox()


def nets(dbu, regs):
    """A probe function over the connectivity of the given regions."""
    fl = db.Layout()
    _LAYOUTS.append(fl)
    fl.dbu = dbu
    fc = fl.create_cell("flat")
    for nm, lay, dt in STACK:
        fc.shapes(fl.layer(lay, dt)).insert(regs[nm])
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(fl, fc, []))
    lr = {nm: l2n.make_layer(fl.layer(lay, dt), nm) for nm, lay, dt in STACK}
    for nm in NAMES:
        l2n.connect(lr[nm])
    for a, b in zip(NAMES, NAMES[1:]):
        l2n.connect(lr[a], lr[b])
    l2n.extract_netlist()

    def probe(layer, pt):
        n = l2n.probe_net(lr[layer], pt)
        return n.cluster_id if n else None

    return probe


def half(regs, seed_pt):
    """Every shape connected to seed_pt on TopMetal1, per layer."""
    seed = db.Region(db.Box(seed_pt, seed_pt).enlarged(1, 1))
    grown = {nm: db.Region() for nm in NAMES}
    grown["tm1"] = regs["tm1"].interacting(seed)
    while True:
        before = sum(r.area() for r in grown.values())
        for i, nm in enumerate(NAMES):
            for j in (i - 1, i + 1):
                if 0 <= j < len(NAMES):
                    grown[nm] = (grown[nm] + regs[nm].interacting(grown[NAMES[j]])).merged()
        if sum(r.area() for r in grown.values()) == before:
            return grown


def find_tap(dbu, regs, ind, labels):
    """The TopMetal1 piece that crosses the IND bottom edge between the LA and LB labels."""
    um = lambda v: int(round(v / dbu))
    ib = ind.bbox()
    xa, xb = sorted((labels["LA"].x, labels["LB"].x))
    band = db.Region(db.Box(ib.left, ib.bottom - um(0.5), ib.right, ib.bottom + um(0.5)))
    taps = [p.bbox() for p in (regs["tm1"] & band).merged().each()
            if xa < p.bbox().center().x < xb and not p.bbox().left <= xa <= p.bbox().right
            and not p.bbox().left <= xb <= p.bbox().right]
    if len(taps) != 1:
        raise Abort("want one TopMetal1 tap across the IND bottom edge between LA and LB, found %d" % len(taps))
    return taps[0]


def check(dbu, regs, ind, labels, m1_labels, cbox, tol, say=print):
    um = lambda v: int(round(v / dbu))
    if ind.count() != 1:
        raise Abort("want one IND box, found %d" % ind.count())
    for lab in ("LA", "LB"):
        if lab not in labels:
            raise Abort("no IND:text %s" % lab)
    ib = ind.bbox()
    tb = find_tap(dbu, regs, ind, labels)
    p_tap = db.Point(tb.center().x, ib.bottom - um(0.25))
    res = {}

    def report(name, cond, detail):
        res[name] = bool(cond)
        say("check_coil_tap: %-9s %s  %s" % (name, "ok  " if cond else "FAIL", detail))

    # 1 to 3 on the layout as drawn
    probe = nets(dbu, regs)
    n_la, n_lb, n_tap = probe("tm1", labels["LA"]), probe("tm1", labels["LB"]), probe("tm1", p_tap)
    report("coil", n_la is not None and n_la == n_lb, "LA and LB one net")
    report("tap", n_tap is not None and n_tap == n_la, "TopMetal1 tap at the IND edge on the coil net")
    if "VSS" in m1_labels:
        n_vss = probe("m1", m1_labels["VSS"])
        report("isolated", n_vss is not None and n_vss != n_la, "substrate tap VSS not on the coil net")

    # 4: cut TopMetal1 along x = 0 from below the tap up past the turn it lands on, which leaves the crossing at the
    # top whole. On the axis, the tap and that turn are one TopMetal1 piece reaching up from the IND edge.
    axis = (regs["tm1"] & db.Region(db.Box(-um(CUT), cbox.bottom, um(CUT), cbox.top))).merged()
    lands = [p.bbox().top for p in axis.each() if p.bbox().bottom <= ib.bottom]
    if not lands:
        report("centre", False, "no TopMetal1 on the axis at the IND edge")
        report("symmetry", False, "skipped, no tap landing")
        return res
    y_land = min(lands)
    cut_box = db.Box(-um(CUT / 2), cbox.bottom, um(CUT / 2), y_land + um(LAND_MARGIN))
    cut = dict(regs)
    cut["tm1"] = regs["tm1"] - db.Region(cut_box)
    probe = nets(dbu, cut)
    c_la, c_lb = probe("tm1", labels["LA"]), probe("tm1", labels["LB"])
    c_tl = probe("tm1", db.Point(-um(CUT), p_tap.y))
    c_tr = probe("tm1", db.Point(um(CUT), p_tap.y))
    split = c_la is not None and c_lb is not None and c_la != c_lb and {c_tl, c_tr} == {c_la, c_lb}
    report("centre", split, "cut at x = 0 up to y %.3f: LA and LB apart, each with one half of the tap"
           % ((y_land + um(LAND_MARGIN)) * dbu))

    # 5: the halves in projection
    if not split:
        report("symmetry", False, "skipped, the cut did not split the coil")
        return res
    ha, hb = half(cut, labels["LA"]), half(cut, labels["LB"])
    proj = lambda h: sum((h[nm] & ind for nm in NAMES), db.Region()).merged()
    pa, pb = proj(ha), proj(hb)
    x = (pa.transformed(db.Trans(db.Trans.M90)) ^ pb).area()
    ref = max(pa.area(), pb.area())
    report("symmetry", ref > 0 and x <= tol * ref,
           "halves mirrored in projection, XOR %.3f um2 of %.1f um2 (limit %g %%)" % (x * dbu ** 2, ref * dbu ** 2, 100.0 * tol))
    return res


def self_test(dbu, regs, ind, labels, m1_labels, cbox, tol):
    """Plant one defect at a time, each must fail the check it targets."""
    um = lambda v: int(round(v / dbu))
    ib = ind.bbox()
    tb = find_tap(dbu, regs, ind, labels)
    above = db.Box(tb.left, ib.bottom + um(1.0), tb.right, ib.bottom + um(2.0))
    # a TopMetal1 strap from the inner turn to the outer one on the east side, halfway up the coil
    yc = (ib.bottom + ib.top) // 2
    inner = [p.bbox() for p in (regs["tm1"] & db.Region(db.Box(0, yc - um(1), ib.right, yc + um(1)))).each()]
    inner.sort(key=lambda b: b.left)
    strap = db.Box(inner[0].left, yc - um(1), inner[-1].right, yc + um(1)) if len(inner) >= 2 else None
    # the tap moved 3 um east: its TopMetal1 replaced by a copy shifted east
    tap_run = regs["tm1"] & db.Region(db.Box(tb.left, ib.bottom - um(2), tb.right, ib.bottom + um(1)))
    shifted = tap_run.moved(um(3.0), 0)
    cases = [
        ("tap open", "tap", dict(regs, tm1=(regs["tm1"] - db.Region(above)).merged())),
        ("tap off centre", "centre", dict(regs, tm1=(regs["tm1"] - tap_run + shifted).merged())),
    ]
    if strap:
        cases.append(("turns shorted", "centre", dict(regs, tm1=(regs["tm1"] + db.Region(strap)).merged())))
    ok = True
    for name, target, r in cases:
        try:
            res = check(dbu, r, ind, labels, m1_labels, cbox, tol, say=lambda s: None)
            caught = not res.get(target, True)
            failed = sorted(k for k, v in res.items() if not v)
        except Abort as e:
            caught, failed = True, ["abort: %s" % e]
        ok &= caught
        print("check_coil_tap: self-test %-16s %s  (%s fails: %s)" % (name, "caught" if caught else "MISSED", target,
                                                                       ", ".join(failed) or "none"))
    return ok


def feed(gds, net):
    """In a parent: the net labeled net reaches the coil through the tap and only through it."""
    dbu, regs, ind, labels, _, cbox = read(gds)
    ly = _LAYOUTS[-1]
    top = ly.top_cell()
    um = lambda v: int(round(v / dbu))
    by_layer = {(lay, dt): nm for nm, lay, dt in STACK}
    pts = []
    for li in ly.layer_indexes():
        info = ly.get_info(li)
        for s in top.shapes(li).each():
            if s.is_text() and s.text_string == net and (info.layer, 0) in by_layer:
                pts.append((by_layer[(info.layer, 0)], db.Point(s.text.x, s.text.y)))
    if not pts:
        raise Abort("no %s label on a stack metal in %s" % (net, top.name))
    if ind.count() != 1 or "LA" not in labels:
        raise Abort("want one coil (IND box, IND:text LA) in %s" % top.name)
    ib = ind.bbox()
    tb = find_tap(dbu, regs, ind, labels)
    cut = dict(regs)
    cut["tm1"] = regs["tm1"] - db.Region(db.Box(tb.left - um(0.1), ib.bottom - um(0.5), tb.right + um(0.1), ib.bottom + um(0.5)))
    ok = True
    for name, r, want in (("as drawn", regs, True), ("tap cut at the IND edge", cut, False)):
        probe = nets(dbu, r)
        coil = probe("tm1", labels["LA"])
        on = [probe(layer, pt) == coil for layer, pt in pts]
        good = all(on) if want else not any(on)
        ok &= good
        print("check_coil_tap: feed      %s  %s: %s %s the coil net" % ("ok  " if good else "FAIL", name, net,
                                                                      "on" if any(on) else "off"))
    return ok


def main(argv):
    opts, args, i = {}, [], 0
    while i < len(argv):
        if argv[i] in ("--tol", "--feed") and i + 1 < len(argv):
            opts[argv[i]] = argv[i + 1]
            i += 2
        elif argv[i] == "--self-test":
            opts["--self-test"] = True
            i += 1
        else:
            args.append(argv[i])
            i += 1
    if len(args) != 1:
        print(__doc__)
        return 1
    try:
        if "--feed" in opts:
            ok = feed(args[0], opts["--feed"])
        else:
            data = read(args[0])
            res = check(*data, float(opts.get("--tol", 0.0)))
            ok = all(res.values()) and len(res) >= 4
            if opts.get("--self-test"):
                ok &= self_test(*data, float(opts.get("--tol", 0.0)))
    except Abort as e:
        print("check_coil_tap: FAIL: %s" % e)
        return 1
    print("check_coil_tap: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
