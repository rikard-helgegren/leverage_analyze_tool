#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from src.view.styling.light_mode.color_palet import *

def get_styling():
    styling = {
        "background_color_cell"          : default_color,
        "background_color_selected_cell" : default_selected_color,
        "background_color_header"        : default_back_ground_color,
        "background_color"               : default_color,
        "elevation"                      : 0
    }
    
    return styling
