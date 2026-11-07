# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2026 The HeiChips Contributors, Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Author: Simon Dorrer
# Created: 07.11.2026
# Last Modified: 07.11.2026
# Description: This file reads the data from the ring oscillator transient analysis and saves it to a .csv file.
# ============================================

# Imports
import numpy as np
from typing import Any
from pathlib import Path
# ============================================

# Functions
def postprocess(results: dict[str, list], conditions: dict[str, Any]) -> dict[str, list]:
    # Do not print from this hook. CACE 2.11.0 redirects stdout into its rich logger while the
    # script runs, and the logger writes back to stdout, so any print recurses without end.
    fosc_arr = list(results['fosc'])
    Idd_arr = list(results['Idd'])

    # Save data as .csv
    csv_filename = Path(__file__).with_suffix('.csv').name
    min_len = min(len(fosc_arr), len(Idd_arr))
    np.savetxt(f'cace/scripts/{csv_filename}',
               np.column_stack((np.array(fosc_arr[:min_len]), np.array(Idd_arr[:min_len]))),
               comments = "", header = "fosc_arr,Idd_arr", delimiter = ",")

    return {'fosc_arr': fosc_arr, 'Idd_arr': Idd_arr}
# ============================================
