#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') #removes bug: red dot on right click

from src.view.vertical_subframe_left.widgets_in_vertical import setup_vertical_frame as setup_vertical_frame_left
from src.view.vertical_subframe_middle.widgets_in_vertical import setup_vertical_frame as setup_vertical_frame_middle
from src.view.vertical_subframe_right.widgets_in_vertical import setup_vertical_frame as setup_vertical_frame_right
from src.view.Keyboard_observable import Keyboard_observable

_MOUSE_STARTER_POSITION = (1.0, 1.0)

class View(GridLayout):
    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        Window.size = (1700, 900)

        Window.bind(on_key_down=self._keydown)
        Window.bind(mouse_pos=self.set_mouse_position)
        self.keyboard_observable =Keyboard_observable()
        self.mouse_position = _MOUSE_STARTER_POSITION

        self.controller = None # Placeholder for controller
        self.show_trades = False
        
        self.cols=3

        setup_vertical_frame_left(self)
        setup_vertical_frame_middle(self)
        setup_vertical_frame_right(self)

    def set_mouse_position(self, w, position):
        self.mouse_position = position
    
    def _keydown(self, window, key, scancode, codepoint, modifiers):
        self.keyboard_observable.notify_observers(key, self.mouse_position)

    def set_controller(self, controller):
        logging.debug("View: set_controller")
        self.controller = controller

    def add_model(self):
        logging.debug("View: add_model")
        self.controller.add_model()

    def update_portfolio_view(self,
            leverage,
            strategy,
            strategy_parameters,
            model_nbr,
            instruments_selected,
            loan,
            include_fees_status):
        logging.debug("View: update_portfolio_view")
        self.leverage_slider.set_leverage(leverage)
        self.strategy_menue.set_strategy_by_model(strategy, strategy_parameters)
        self.table_of_instruments.clear_old_and_set_new_selected_instruments(instruments_selected, model_nbr)
        self.loan.set_loan(loan)
        self.use_fees.active = include_fees_status

    def set_selected_model(self, model_nbr):
        logging.debug("View: set_selected_model")
        self.controller.set_selected_model(model_nbr)

    def update_fee_status(self, status):
        logging.debug("View: update_fee_status")
        self.controller.update_fee_status(status)
    
    def update_years_histogram_interval(self, years):
        logging.debug("View: update_years_histogram_interval")
        self.controller.update_years_histogram_interval(years)

    def update_loan(self, loan):
        logging.debug("View: update_loan")
        self.controller.update_loan(loan / 100)
        # TODO not fully implemented (hist)

    def update_harvest_point(self, harvest_point):
        logging.debug("View: update_harvest_point")
        self.controller.update_harvest_point(harvest_point)

    def update_refill_point(self, refill_point):
        logging.debug("View: update_refill_point")
        self.controller.update_refill_point(refill_point)

    def update_rebalnce_intervall(self, intervall):
        logging.debug("View: update_rebalance_point")
        self.controller.update_rebalance_point(intervall)

    def update_variance_calc_sample_size(self, value):
        logging.debug("View: update_variance_calc_sample_size")
        self.controller.update_variance_calc_sample_size(value)

    def update_volatility_strategie_sample_size(self, value):
        logging.debug("View: update_volatility_strategie_sample_size")
        self.controller.update_volatility_strategie_sample_size(value)

    def update_volatility_strategie_level(self, value):
        logging.debug("View: update_volatility_strategie_level")
        self.controller.update_volatility_strategie_level(value)

    def update_amount_leverage(self, value):
        """The amount of leverage should be a value between 0 and 100"""
        logging.debug("View: update_amount_leverage")
        self.controller.set_update_amount_leverage(value)

    def draw_histogram(self, data):
        logging.debug("View: draw_histogram")
        self.histogram.draw(data)

    def draw_line_graph(self, time_union, values_list, time_span_list, buy_sell_log_list):
        logging.debug("View: draw_line_graph")
        self.line_graph.draw(time_union, values_list, time_span_list, buy_sell_log_list)

    def set_table_of_instruments(self, names, countries):
        logging.debug("View: set_market_table")
        self.table_of_instruments.set_instruments_in_table(names, countries)
        
    def update_instrument_selected(self, table_focus_item):
        logging.debug("View: table_item_focused")
        self.controller.update_instrument_selected(table_focus_item)

    def update_strategy_selected(self, menu_focus_item):
        logging.debug("View: update_strategy_selected")
        self.controller.update_strategy_selected(menu_focus_item)

    def update_time_limits(self, from_time, to_time):
        logging.debug("View: update_time_limits")
        self.controller.set_time_limits(from_time, to_time)

    def update_table_of_statistics(self, key_values_list):
        logging.debug("View update_table_of_statistics")
        self.table_of_statistics.set_table(key_values_list)

    def update_pie_chart(self, key_values):
        logging.debug("View update_pie_chart")
        self.pie_frame1.draw(key_values['Mean'])
        self.pie_frame2.draw(key_values['Median'])
        self.pie_frame3.draw(key_values['Risk'])

    def update_reference(self):
        logging.debug("View: update_reference")
        """ Set reference or remove it depending on if data is identical to when last pressed"""
        self.histogram.update_reference()
        self.line_graph.update_reference()
        self.table_of_statistics.update_reference()

    def wipe_selected_instruments(self):
        logging.debug("View: wipe_selected_instruments")
        self.table_of_instruments.remove_selectons()
        self.controller.wipe_instrument_selected()
    
    def set_pause_state(self, pausing_state):
        logging.debug("View: set_pause_state")
        self.controller.set_pause_state(pausing_state)
