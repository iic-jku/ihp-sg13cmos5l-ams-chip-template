#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Builds the transistor-level reference netlist of the whole chip for KLayout LVS, from the powered gate netlists, the cell CDLs and the analog macros' LVS netlists. The netlist lists every change it makes against those files.
#
# usage: mk_ref.py --root <repo> --gds <layout> --gds-top <cell holding the placed cells> --top <name> -o <out.cdl>
import argparse
import collections
import os
import re
import sys

import klayout.db as db

PDK_ROOT = os.environ["PDK_ROOT"]
PDK = os.path.join(PDK_ROOT, os.environ["PDK"])

LIBS = [
    PDK + "/libs.ref/sg13cmos5l_io/cdl/sg13cmos5l_io.cdl",
    PDK + "/libs.ref/sg13cmos5l_stdcell/cdl/sg13cmos5l_stdcell.cdl",
    PDK + "/libs.ref/sg13cmos5l_stdcell_hv/cdl/sg13cmos5l_stdcell_hv.cdl",
    PDK_ROOT + "/ihp-sg13g2/libs.ref/ez130_8t/cdl/ez130_8t.cdl",
    "ip/sg13cmos5l_ip__rfpad_70x70/netlist/schematic/sg13cmos5l_ip__rfpad_70x70_klayout.cdl",
    "macros/inverter/netlist/schematic/inverter_top_klayout.cdl",
    "macros/amplifier/netlist/schematic/amplifier_klayout.cdl",
    "macros/ringosc/netlist/schematic/ringosc_klayout.cdl",
    "macros/vco/netlist/schematic/vco_top_klayout.cdl",
]
MODULES = [
    "macros/counter_lv_ihp/final/pnl/counter_lv_ihp_top.pnl.v",
    "macros/counter_lv_eth/final/pnl/counter_lv_eth_top.pnl.v",
    "macros/counter_hv_kvc/final/pnl/counter_hv_kvc_top.pnl.v",
    "netlist/pnl/chip_top.pnl.v",
]
TOP_MODULE = "chip_top"

# no devices and no reference netlist: metal, passivation and labels only
GEOM_ONLY = {"sg13cmos5l_ip__bondpad_70x70", "sealring", "sg13cmos5l_ip__jku", "sg13cmos5l_ip__jku_names",
             "FILLER1", "FILLER2", "FILLER4", "FILLER8", "FILLER16"}
# a port of the cell that is the same conductor as another one and is not in its CDL
PIN_ALIAS = {
    "sg13cmos5l_IOPadAnalog": {"padbare": "pad"},
    "sg13cmos5l_ip__rfpad_70x70": {"padbare": "pad"},
}
# the EZ130 library has well pins the powered Verilog leaves out, WELLTAP ties them in the layout
TIE = {"VNW": "VDD", "VPW": "VSS"}
TAPS = ("ptap1", "ntap1")
# cells whose layout splits a net into pieces only the parent joins, expanded into their callers
FLATTEN = ["sg13cmos5l_Clamp_N20N0D", "sg13cmos5l_Clamp_N43N43D4R", "sg13cmos5l_Clamp_N8N8D", "sg13cmos5l_Clamp_P20N0D",
           "sg13cmos5l_Clamp_P8N8D", "sg13cmos5l_DCNDiode", "sg13cmos5l_DCPDiode", "sg13cmos5l_RCClampResistor",
           "sg13cmos5l_SecondaryProtection"]
FLATTEN_MODULE = ["sg13cmos5l_IOPadAnalog", "sg13cmos5l_IOPadOut16mA", "sg13cmos5l_IOPadInOut16mA", "vco_top"]
JOIN = {"VSS": "IOVSS,VSS", "IOVSS": "IOVSS,VSS"}
GLOBAL_SUB = "sub!"

log = []


def say(msg):
    log.append(msg)
    print(msg, flush=True)


def die(msg):
    sys.exit("mk_ref: ERROR " + msg)


class Block:
    def __init__(self, name, ports, cards, src):
        self.name, self.ports, self.cards, self.src = name, list(ports), cards, src
        self.orig_ports = list(ports)
        self.sub_net = None
        self.mapped = {}


def parse_x(t):
    """(nodes, cell, params) of an X card in tokens."""
    if "/" in t:
        k = t.index("/")
        return t[1:k], t[k + 1], t[k + 2:]
    plain = [i for i, x in enumerate(t) if "=" not in x]
    last = plain[-1]
    return t[1:last], t[last], t[last + 1:]


def node_slots(t):
    """Indices of the node tokens of a card."""
    k = t[0][0].upper()
    if k == "X":
        last = [i for i, x in enumerate(t) if "=" not in x][-1]
        return list(range(1, last))
    if k == "M":
        return list(range(1, 5))
    if k == "D":
        last = [i for i, x in enumerate(t) if "=" not in x][-1]
        return list(range(1, last))
    if k in "RC":
        return [1, 2]
    if k == "L":
        return [1, 2, 3]
    die("unknown card " + " ".join(t))


def read_cdl(path, lib):
    lines = []
    for raw in open(path, encoding="utf-8", errors="replace"):
        s = raw.strip()
        if s.startswith("+") and lines:
            lines[-1] += " " + s[1:].strip()
        else:
            lines.append(s)
    cur = None
    for s in lines:
        if not s or s[0] == "*" or s[0] == "$":
            continue
        low = s.lower()
        if low.startswith(".subckt"):
            t = s.split()
            ports = [p for p in t[2:] if "=" not in p]
            cur = Block(t[1], ports, [], path)
            continue
        if low.startswith(".ends"):
            if cur is None:
                continue
            old = lib.get(cur.name)
            if old is not None and [" ".join(c) for c in old.cards] != [" ".join(c) for c in cur.cards]:
                die("%s defined twice, differently, in %s and %s" % (cur.name, old.src, path))
            lib[cur.name] = cur
            cur = None
            continue
        if cur is None or s[0] == ".":
            continue
        t = ["$[rppd]" if x == "$[res_rppd]" else x for x in s.split()]
        if "$[rppd]" in t:
            t = [x for x in t if not x.lower().startswith("ps=")]
        if t[0][0].upper() == "X":
            nodes, cell, params = parse_x(t)
            t = [t[0]] + nodes + [cell] + params
        cur.cards.append(t)


def tap_merge(b):
    """Removes ptap1/ntap1 cards and merges their terminals, the reference-side twin of --disable_tap_extraction."""
    parent = {}

    def find(x):
        while parent.get(x, x) != x:
            x = parent[x]
        return x

    keep, n = [], 0
    for t in b.cards:
        if any(m in t for m in TAPS):
            n += 1
            ra, rb = find(t[1]), find(t[2])
            if ra != rb:
                if rb in b.ports and ra not in b.ports:
                    ra, rb = rb, ra
                parent[rb] = ra
            continue
        keep.append(t)
    if not n:
        return
    b.sub_net = find(GLOBAL_SUB) if any(GLOBAL_SUB in c for c in b.cards) else None
    cards = []
    for t in keep:
        t = list(t)
        for i in node_slots(t):
            t[i] = find(t[i])
        t = [x[:5] + find(x[5:]) if x.upper().startswith("$SUB=") else x for x in t]
        cards.append(t)
    b.cards = cards
    b.ports = [find(p) for p in b.orig_ports]
    uniq = []
    for p in b.ports:
        if p not in uniq:
            uniq.append(p)
    b.mapped = dict(zip(b.orig_ports, b.ports))
    b.ports = uniq
    say("tap merge: %s, %d cards, ports %s" % (b.name, n, " ".join(b.ports)))


def has_devices(b, lib):
    for t in b.cards:
        k = t[0][0].upper()
        if k in "MDRCLQ":
            return True
        if k == "X":
            _, cell, _ = parse_x(t)
            if cell in GEOM_ONLY:
                continue
            if cell not in lib or has_devices(lib[cell], lib):
                return True
    return False


# --- Verilog -------------------------------------------------------------------------------------------------------
TOK = re.compile(r"\\\S+|[A-Za-z_][\w$]*|\d+'[bBhHdD][0-9a-fA-FxXzZ_]+|\d+|[()\[\]{},;.:#=]")


class Module:
    def __init__(self, name):
        self.name, self.header, self.widths, self.insts, self.assigns = name, [], {}, [], []


def read_verilog(path):
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//[^\n]*", "", text)
    tk = [t[1:] if t[0] == "\\" else t for t in TOK.findall(text)]
    i, mods = 0, {}

    def expr():
        nonlocal i
        if tk[i] == "{":
            i += 1
            out = []
            while tk[i] != "}":
                out += expr()
                if tk[i] == ",":
                    i += 1
            i += 1
            return out
        name = tk[i]
        i += 1
        if re.match(r"\d+'", name):
            die("constant %s on a pin in %s" % (name, path))
        if tk[i] == "[":
            msb = tk[i + 1]
            if tk[i + 2] == ":":
                lsb = tk[i + 3]
                i += 5
                step = 1 if int(lsb) >= int(msb) else -1
                return ["%s[%d]" % (name, b) for b in range(int(msb), int(lsb) + step, step)]
            i += 3
            return ["%s[%s]" % (name, msb)]
        return [name]

    while i < len(tk):
        if tk[i] != "module":
            i += 1
            continue
        m = Module(tk[i + 1])
        i += 2
        if tk[i] == "(":
            i += 1
            while tk[i] != ")":
                if tk[i] != ",":
                    m.header.append(tk[i])
                i += 1
            i += 1
        i += 1  # ;
        while tk[i] != "endmodule":
            word = tk[i]
            if word in ("input", "output", "inout", "wire"):
                i += 1
                rng = None
                if tk[i] == "[":
                    rng = (int(tk[i + 1]), int(tk[i + 3]))
                    i += 5
                while tk[i] != ";":
                    if tk[i] != "," and word != "wire":
                        m.widths[tk[i]] = rng
                    i += 1
                i += 1
            elif word == "assign":
                i += 1
                a = expr()
                i += 1  # =
                b = expr()
                i += 1  # ;
                m.assigns += list(zip(a, b))
            else:
                cell, inst = tk[i], tk[i + 1]
                i += 2
                if tk[i] != "(":
                    die("no port list at %s %s" % (cell, inst))
                i += 1
                con = {}
                while tk[i] != ")":
                    if tk[i] == ",":
                        i += 1
                        continue
                    pin = tk[i + 1]
                    i += 3  # . pin (
                    con[pin] = [] if tk[i] == ")" else expr()
                    i += 1  # )
                i += 2  # ) ;
                m.insts.append((cell, inst, con))
        mods[m.name] = m
        i += 1
    return mods


def bits(name, rng):
    if rng is None:
        return [name]
    a, b = rng
    step = 1 if b >= a else -1
    return ["%s[%d]" % (name, x) for x in range(a, b + step, step)]


def module_block(m, lib, mods):
    parent = {}

    def find(x):
        while parent.get(x, x) != x:
            x = parent[x]
        return x

    portbits = [bb for p in m.header for bb in bits(p, m.widths.get(p))]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            if rb in portbits and ra not in portbits:
                ra, rb = rb, ra
            parent[rb] = ra

    for a, b in m.assigns:
        union(a, b)
    rows = []
    skipped = collections.Counter()
    for cell, inst, con in m.insts:
        if cell in GEOM_ONLY:
            skipped[cell] += 1
            continue
        if cell in mods:
            mod = mods[cell]
            pins = [p for p in mod.header]
            ports = [bb for p in pins for bb in bits(p, mod.widths.get(p))]
            flat = {}
            for p in pins:
                nets = con.get(p, [])
                names = bits(p, mod.widths.get(p))
                if nets and len(nets) != len(names):
                    die("%s.%s has %d nets for %d bits" % (inst, p, len(nets), len(names)))
                for k, n in enumerate(names):
                    flat[n] = nets[k] if nets else None
            rows.append((cell, inst, ports, flat))
            continue
        if cell not in lib:
            die("cell %s (instance %s of %s) is in no library" % (cell, inst, m.name))
        b = lib[cell]
        for alias, target in PIN_ALIAS.get(cell, {}).items():
            if alias in con:
                if con[alias] and con.get(target):
                    union(con[target][0], con[alias][0])
                del con[alias]
        flat = {}
        for p, nets in con.items():
            if len(nets) > 1:
                die("bus pin %s on library cell %s" % (p, cell))
            if nets:
                flat[p] = nets[0]
            if p not in b.orig_ports:
                die("pin %s of instance %s is not a port of %s (%s)" % (p, inst, cell, " ".join(b.orig_ports)))
        for p, target in TIE.items():
            if p in b.orig_ports and p not in flat:
                flat[p] = flat[target]
        rows.append((cell, inst, b.orig_ports, flat))
    if skipped:
        say("%s: geometry-only cells left out: %s" % (m.name, dict(skipped)))
    cards = []
    for cell, inst, ports, flat in rows:
        nodes = []
        for p in ports:
            n = flat.get(p)
            nodes.append(find(n) if n is not None else "_nc_%s_%s" % (inst, p))
        cards.append(["X" + inst] + nodes + [cell])
    ports = []
    for p in portbits:
        r = find(p)
        if r not in ports:
            ports.append(r)
    return Block(m.name, ports, cards, "verilog")


# --- flatten -------------------------------------------------------------------------------------------------------
def port_map(child, nodes, clashes=None):
    pm = {}
    for p, n in zip(child.orig_ports, nodes):
        key = child.mapped.get(p, p)
        if key in pm and pm[key] != n:
            if clashes is None:
                die("%s: merged port %s gets two nets, %s and %s" % (child.name, key, pm[key], n))
            clashes.append((n, pm[key]))
            continue
        pm[key] = n
    return pm


def merge_net(b, a, keep):
    """Renames net a to keep in block b, ports included."""
    if a == keep:
        return
    if a in b.ports and keep not in b.ports:
        a, keep = keep, a
    for t in b.cards:
        for i in node_slots(t):
            if t[i] == a:
                t[i] = keep
        for i, x in enumerate(t):
            if x.upper() == "$SUB=" + a.upper() and x[5:] == a:
                t[i] = x[:5] + keep
    for orig in b.orig_ports:
        if b.mapped.get(orig, orig) == a:
            b.mapped[orig] = keep
    b.ports = list(dict.fromkeys(keep if p == a else p for p in b.ports))
    if b.sub_net == a:
        b.sub_net = keep
    say("substrate: %s joins %s and %s" % (b.name, a, keep))


def expand(parent, names, lib):
    """Expands every call of the named cells in parent, deepest first."""
    again = True
    joins = []
    while again:
        again = False
        out = []
        for t in parent.cards:
            if t[0][0].upper() == "X":
                nodes, cell, params = parse_x(t)
                if cell in names and cell in lib:
                    again = True
                    child = lib[cell]
                    pm = port_map(child, nodes, joins)
                    if child.sub_net in pm and parent.sub_net:
                        joins.append((pm[child.sub_net], parent.sub_net))
                    inst = t[0][1:]
                    sub = parent.sub_net or GLOBAL_SUB

                    def ren(n):
                        if n in pm:
                            return pm[n]
                        if n == GLOBAL_SUB:
                            return sub
                        return "%s.%s" % (inst, n)

                    for c in child.cards:
                        c = list(c)
                        for i in node_slots(c):
                            c[i] = ren(c[i])
                        c = [x[:5] + ren(x[5:]) if x.upper().startswith("$SUB=") else x for x in c]
                        c[0] = c[0][0] + inst + "." + c[0][1:]
                        out.append(c)
                    continue
            out.append(t)
        parent.cards = out
    for a, keep in joins:
        merge_net(parent, a, keep)


# --- output --------------------------------------------------------------------------------------------------------
def gds_table(path):
    ly = db.Layout()
    ly.read(path)
    table = {}
    for c in ly.each_cell():
        table[c.name] = {ly.cell(i.cell_index).name for i in c.each_inst()}
    return table


def base(name):
    return re.sub(r"(\$\d+)+$", "", name)


def emit(top_out, top_name, top_gds, lib, table):
    out, done, renames = [], set(), collections.Counter()

    def write(name, gname, label):
        if label in done:
            return
        done.add(label)
        b = lib[name]
        kids = table.get(gname, set())
        body = []
        for t in b.cards:
            if t[0][0].upper() != "X":
                body.append(" ".join(t))
                continue
            nodes, cell, params = parse_x(t)
            if cell in GEOM_ONLY:
                continue
            if cell not in lib:
                body.append(" ".join(t))
                continue
            child = lib[cell]
            if not has_devices(child, lib):
                continue
            gchild = cell
            if cell not in kids:
                cands = sorted(k for k in kids if base(k) == base(cell))
                if len(cands) == 1:
                    gchild = cands[0]
                    renames[(gname, cell, gchild)] += 1
                elif len(cands) > 1:
                    die("%s in %s has several copies %s" % (cell, gname, cands))
            pm = port_map(child, nodes)
            write(cell, gchild if gchild in table else cell, gchild)
            ordered = [pm[p] for p in child.ports]
            body.append(" ".join([t[0]] + ordered + [gchild] + params))
        out.append(".SUBCKT %s %s" % (label, " ".join(b.ports)))
        out.extend(body)
        out.append(".ENDS")
        out.append("")

    write(top_name, top_gds, top_out)
    for (g, c, gc), n in sorted(renames.items()):
        say("copy under the GDS name: in %s, %d x %s called as %s" % (g, n, c, gc))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--gds", required=True)
    ap.add_argument("--gds-top", default="chip_top")
    ap.add_argument("--top", required=True)
    ap.add_argument("-o", required=True)
    args = ap.parse_args()
    lib = {}
    for f in LIBS:
        read_cdl(f if f.startswith("/") else os.path.join(args.root, f), lib)
    for b in lib.values():
        tap_merge(b)
    mods = {}
    for f in MODULES:
        mods.update(read_verilog(os.path.join(args.root, f)))
    for m in mods:
        lib[m] = None
    # macros first, so that the chip top can read their ports
    for m in MODULES:
        name = os.path.basename(m).split(".")[0]
        lib[name] = module_block(mods[name], {k: v for k, v in lib.items() if v is not None}, mods)
    top = lib[TOP_MODULE]
    for t in top.cards:
        if t[0][0].upper() == "X":
            for i in node_slots(t):
                t[i] = JOIN.get(t[i], t[i])
    top.ports = [JOIN.get(p, p) for p in top.ports]
    top.ports = list(dict.fromkeys(top.ports))
    top.sub_net = "IOVSS,VSS"
    say("joined: VSS and IOVSS as IOVSS,VSS, one substrate node in the layout")
    for b in lib.values():
        expand(b, set(FLATTEN), lib)
    expand(top, set(FLATTEN_MODULE), lib)
    changed = True
    while changed:
        changed = False
        for b in lib.values():
            for t in b.cards:
                if t[0][0].upper() != "X":
                    continue
                nodes, cell, _ = parse_x(t)
                if cell in lib:
                    clashes = []
                    port_map(lib[cell], nodes, clashes)
                    for a, keep in clashes:
                        merge_net(b, a, keep)
                        changed = True
    lines = emit(args.top, TOP_MODULE, args.gds_top, lib, gds_table(args.gds))
    with open(args.o, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("* Transistor-level reference netlist of %s for KLayout LVS\n" % args.top)
        for m in log:
            fh.write("* " + m + "\n")
        fh.write("\n".join(lines) + "\n")
    print("written", args.o, "lines", len(lines))


if __name__ == "__main__":
    main()
