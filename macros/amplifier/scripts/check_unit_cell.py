# SPDX-FileCopyrightText: 2026 The HeiChips Contributors, Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Check that a layout holds a unit cell and everything below it exactly as a reference layout does.

import argparse
import sys


def subtree(layout, cell):
    """Return the cell and every cell below it by name."""
    indexes = [cell.cell_index()] + list(cell.called_cells())
    return {layout.cell(index).name: layout.cell(index) for index in indexes}


def geometry(kdb, layout, cell):
    """Return the merged flat geometry of a cell per GDS layer."""
    regions = {}
    for index in layout.layer_indexes():
        info = layout.get_info(index)
        region = kdb.Region(cell.begin_shapes_rec(index)).merged()
        if not region.is_empty():
            regions[(info.layer, info.datatype)] = region
    return regions


def main():
    parser = argparse.ArgumentParser(
        description="Check that a layout holds a unit cell and everything below it exactly as a reference layout does."
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

    trees = []
    for path in (args.layout, args.reference):
        layout = kdb.Layout()
        layout.read(path)
        cell = layout.cell(args.cell)
        if cell is None:
            print(f"[ERROR] {path}: no cell '{args.cell}' found.", file=sys.stderr)
            return 1
        trees.append((layout, subtree(layout, cell)))
    (layout, cells), (ref_layout, ref_cells) = trees

    print(f"[INFO] Checking {args.cell} in {args.layout} against {args.reference} ...", flush=True)
    # Cells of one name merge at the chip top-level, so the names have to match as well as the geometry
    errors = [f"cell '{name}' is only in {path}" for names, others, path in
              ((cells, ref_cells, args.layout), (ref_cells, cells, args.reference))
              for name in sorted(set(names) - set(others))]
    dbu = layout.dbu
    for name in sorted(set(cells) & set(ref_cells)):
        regions = geometry(kdb, layout, cells[name])
        ref_regions = geometry(kdb, ref_layout, ref_cells[name])
        for key in sorted(set(regions) | set(ref_regions)):
            xor = regions.get(key, kdb.Region()) ^ ref_regions.get(key, kdb.Region())
            if not xor.is_empty():
                errors.append(f"cell '{name}' differs on layer {key[0]}/{key[1]} by {xor.area() * dbu * dbu:.3f} um2")

    if errors:
        for error in errors:
            print(f"[ERROR] {error}", file=sys.stderr)
        print(f"[ERROR] {args.layout} does not hold {args.cell} as {args.reference} does. "
              f"Re-create the instance from the library and re-export the GDS.", file=sys.stderr)
        return 1
    print(f"[INFO] {len(cells)} cells match. Unit cell check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
