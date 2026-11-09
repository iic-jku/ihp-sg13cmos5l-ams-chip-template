# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1

"""Adds rectangles on one layer to the top cell of a GDS file.

Expected KLayout -rd parameters:
    gds_file: path to the GDS file (read and written in-place)
    layer:    GDS layer as layer_number/datatype (e.g. "31/0")
    boxes:    rectangles in um, "x0,y0,x1,y1" separated by spaces
"""

import pya

layout = pya.Layout()
layout.read(gds_file)

top = layout.top_cell()
layer_num, datatype = (int(v) for v in layer.split("/"))
layer_idx = layout.layer(layer_num, datatype)

for box in boxes.split():
    x0, y0, x1, y1 = (float(v) for v in box.split(","))
    top.shapes(layer_idx).insert(pya.DBox(x0, y0, x1, y1))
layout.write(gds_file)
