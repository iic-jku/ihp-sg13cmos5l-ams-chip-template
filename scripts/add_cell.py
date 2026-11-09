# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1

"""Places the top cell of one GDS file into the top cell of another.

Expected KLayout -rd parameters:
    gds_file: path to the GDS file (read and written in-place)
    cell_gds: path to the GDS file holding the cell to place
    x, y:     lower-left corner of the placed cell in um
"""

import pya

layout = pya.Layout()
layout.read(gds_file)
top = layout.top_cell()
known = {cell.cell_index() for cell in layout.each_cell()}

layout.read(cell_gds)
new_tops = [cell for cell in layout.top_cells() if cell.cell_index() not in known]
if len(new_tops) != 1:
    raise RuntimeError(f"add_cell: want one new top cell from {cell_gds}, found {len(new_tops)}")

top.insert(pya.DCellInstArray(new_tops[0].cell_index(), pya.DTrans(float(x), float(y))))
layout.write(gds_file)
