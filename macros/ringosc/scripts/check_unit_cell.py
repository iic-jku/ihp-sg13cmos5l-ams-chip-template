# SPDX-FileCopyrightText: 2026 The HeiChips Contributors, Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Check that a layout holds a unit cell as the layout of its macro does, and that no cell name the two share has two contents.

import argparse
import sys


def contents(kdb, layout, cell):
    """Return the merged flat geometry and the texts of a cell per GDS layer."""
    found = {}
    for index in layout.layer_indexes():
        info = layout.get_info(index)
        region = kdb.Region(cell.begin_shapes_rec(index)).merged()
        texts = sorted((text.string, text.x, text.y) for text in kdb.Texts(cell.begin_shapes_rec(index)).each())
        if not region.is_empty() or texts:
            found[(info.layer, info.datatype)] = (region, texts)
    return found


def main():
    parser = argparse.ArgumentParser(
        description="Check that a layout holds a unit cell as the layout of its macro does, and that no cell name the two share has two contents."
    )
    parser.add_argument("layout", help="layout file to check (GDS or OASIS)")
    parser.add_argument("reference", help="layout file of the macro the unit cell comes from")
    parser.add_argument("cell", help="name of the unit cell")
    args = parser.parse_args()

    try:
        import klayout.db as kdb
    except ImportError:
        print("[ERROR] The klayout Python module is not available. Run this inside the "
              "IIC-OSIC-TOOLS container.", file=sys.stderr)
        return 2

    layouts = []
    for path in (args.layout, args.reference):
        layout = kdb.Layout()
        layout.read(path)
        if layout.cell(args.cell) is None:
            print(f"[ERROR] {path}: no cell '{args.cell}' found.", file=sys.stderr)
            return 1
        layouts.append(layout)
    layout, reference = layouts

    print(f"[INFO] Checking {args.cell} in {args.layout} against {args.reference} ...", flush=True)
    # Cells of one name merge at the chip top-level. The numbers in via_stack$3 are per layout, so the two lists of names may differ.
    names = sorted({cell.name for cell in layout.each_cell()} & {cell.name for cell in reference.each_cell()})
    dbu = layout.dbu
    empty = (kdb.Region(), [])
    errors = []
    for name in names:
        ours = contents(kdb, layout, layout.cell(name))
        theirs = contents(kdb, reference, reference.cell(name))
        for key in sorted(set(ours) | set(theirs)):
            region, texts = ours.get(key, empty)
            ref_region, ref_texts = theirs.get(key, empty)
            xor = region ^ ref_region
            if not xor.is_empty():
                errors.append(f"cell '{name}' differs on layer {key[0]}/{key[1]} by {xor.area() * dbu * dbu:.3f} um2")
            if texts != ref_texts:
                errors.append(f"cell '{name}' has other texts on layer {key[0]}/{key[1]}")

    if errors:
        for error in errors:
            print(f"[ERROR] {error}", file=sys.stderr)
        print(f"[ERROR] {args.layout} and {args.reference} hold different cells of one name, which merge at the chip top-level. "
              f"Export both layouts with the same PCell revision, see the layout section of README.md.", file=sys.stderr)
        return 1
    print(f"[INFO] {len(names)} shared cell names match. Unit cell check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
