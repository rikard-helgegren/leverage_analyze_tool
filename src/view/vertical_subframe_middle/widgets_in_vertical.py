#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.boxlayout import BoxLayout

from src.view.vertical_subframe_middle.Histogram import Histogram
from src.view.vertical_subframe_middle.Line_graph import Line_graph
from src.view.vertical_subframe_middle.Time_limiters import Time_limiters

def setup_vertical_frame(view):
    frame = BoxLayout(orientation='vertical', padding=5)

    view.histogram = Histogram(view, frame)
    view.line_graph = Line_graph(view, frame)
    view.time_limiters = Time_limiters(view, frame)

    view.add_widget(frame)