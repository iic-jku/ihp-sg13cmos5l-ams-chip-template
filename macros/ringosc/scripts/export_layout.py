# SPDX-FileCopyrightText: 2026 The HeiChips Contributors, Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Description: Export a hierarchical layout for tapeout in batch, with the same write as File > Export Layout For Tapeout.
#
# Run it without the PDK. The PCells then stay frozen as the source saved them, while a GUI session re-evaluates them against the installed PDK.
#
#     klayout -b -r export_layout.py -rd layout=<TOP>.klay.gds -rd out=<TOP>.gds

import json
import os

import pya

klib = layout[: -len(".gds")] + ".klib"
with open(klib, encoding="utf-8") as f:
    statements = json.load(f)["statements"]
for statement in statements:
    library = pya.Library()
    library.layout().read(os.path.normpath(os.path.join(os.path.dirname(klib), statement["lib_path"])))
    library.register(statement["lib_name"])

source = pya.Layout()
source.read(layout)
tops = [cell.name for cell in source.top_cells()]
if len(tops) != 1:
    raise RuntimeError(f"{layout} has more than one top cell: {tops}")

options = pya.SaveLayoutOptions()
options.select_all_cells()
options.select_all_layers()
options.set_format_from_filename(out)
options.write_context_info = False
source.write(out, options)
print(f"[INFO] Wrote {out} with top cell {tops[0]}.")
