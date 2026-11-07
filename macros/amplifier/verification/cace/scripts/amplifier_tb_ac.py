# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2026 The HeiChips Contributors, Simon Dorrer and Harald Pretl
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# Author: Simon Dorrer
# Created: 07.11.2026
# Last Modified: 07.11.2026
# Description: This file reads the data from the amplifier AC analysis and saves it to a .csv file.
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
    Av_dB_arr = list(results['Av_dB'])
    fcu_arr = list(results['fcu'])

    # Save data as .csv
    csv_filename = Path(__file__).with_suffix('.csv').name
    min_len = min(len(Av_dB_arr), len(fcu_arr))
    np.savetxt(f'cace/scripts/{csv_filename}',
               np.column_stack((np.array(Av_dB_arr[:min_len]), np.array(fcu_arr[:min_len]))),
               comments = "", header = "Av_dB_arr,fcu_arr", delimiter = ",")

    return {'Av_dB_arr': Av_dB_arr, 'fcu_arr': fcu_arr}
# ============================================
