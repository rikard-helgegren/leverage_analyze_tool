#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
import src.constants as constants

from src.model.Market_data_loader import Market_data_loader
from src.controller.graph_handler import draw_line_graph
import src.model.Model as Model


class Controller:
    """ This is the controller of the application. Which has access to
        both the view and the model in order to keep the model updated
        and sending the right information to the view.
    """
    def __init__(self, view):
        model = Model.Model() #TODO remove the need of a model by default
        model.set_markets(Market_data_loader().get_data())
        self.models = [model] 
        self.selected_model_nbr = 0
        self.view = view

        self.pause_state = False

        self.set_table_of_instruments()
        self.set_table_of_statistics()

    def update_view(self):
        logging.debug("Controller: update_view")
        self.draw_histogram()        
        draw_line_graph(self.models, self.view)
        self.update_table_of_statistics()
        self.draw_pie_chart()

    def make_time_and_values_compatible_with_all_models(time_list, value_list):

        #time_lists_all_models = 

        #combined_time_list = 

        new_time_list = time_list

        return new_time_list



    def update_selected_model(self):
        logging.debug("Controller: update_selected_model")

        if self.pause_state:
            logging.info("Model updates are paused")
        else:
            self.models[self.selected_model_nbr].update_model()
    
    def update_all_models(self):
        logging.debug("Controller: update_all_models")
        for model in self.models:
            model.update_model()

    def add_model(self):
        logging.debug("Controller: add_model")
        self.models.append(Model.Model())
        self.selected_model_nbr += 1
        self.models[self.selected_model_nbr].set_markets(Market_data_loader().get_data())

    def remove_model(self, model_index):
        logging.debug("Controller: remove_model index: %r", model_index)
        del self.models[model_index]

    def set_selected_model(self, model_nbr):
        logging.debug("Controller: set_selected_model: %r", model_nbr)
        self.selected_model_nbr = model_nbr
        self.update_portfolio_view(self.models[self.selected_model_nbr])

    def update_portfolio_view(self, selected_portfolio):
        logging.debug("Controller: update_portfolio_view")
        
        self.view.update_portfolio_view(selected_portfolio.get_proportion_leverage(),
                selected_portfolio.get_portfolio_strategy(),
                self.get_strategy_parameters(selected_portfolio),
                self.selected_model_nbr,
                selected_portfolio.get_instruments_selected(),
                selected_portfolio.get_loan(),
                selected_portfolio.get_include_fees_status()) 
        
    def get_strategy_parameters(self, model):
        logging.debug("Controller: get_strategy_parameters")
        strategy_parameters = {}

        strategy_parameters['harvest_point'] = model.get_harvest_point()
        strategy_parameters['refill_point'] = model.get_refill_point()
        strategy_parameters['rebalance_period_months'] = model.get_rebalance_period_months()
        strategy_parameters['variance_calc_sample_size'] = model.get_variance_calc_sample_size()
        strategy_parameters['volatility_strategie_sample_size'] = model.get_volatility_strategie_sample_size()
        strategy_parameters['volatility_strategie_level'] = model.get_volatility_strategie_level()

        return strategy_parameters

    def update_fee_status(self, checkbutton_fee_state):
        logging.debug("Controller: fee_status: %r", checkbutton_fee_state)
        self.models[self.selected_model_nbr].set_include_fee_status(checkbutton_fee_state)
        self.update_selected_model()

        self.update_view()

    def set_pause_state(self, pausing_state):
        self.pause_state = pausing_state

        if  not self.pause_state:
            self.update_all_models()
            self.update_view()

    def draw_histogram(self):
        logging.debug("Controller: draw_histogram")
        data = [model.get_results_for_intervals() for model in self.models]

        self.view.draw_histogram(data)

    def set_table_of_statistics(self):
        """ Set the table with key values"""
        logging.debug("Controller: set_table_of_statistics")
        self.update_table_of_statistics([model.key_values.get_all_values() for model in self.models])
    
    def set_table_of_instruments(self):
        """ Set the table with information of available instruments"""
        logging.debug("Controller: set_table_of_instruments")
        names = []
        countries = []

        #TODO this information should be fetched from  a data object (Singelton), son not all models need to hold lots of data 
        for market in self.models[self.selected_model_nbr].get_markets().values():
            names.append(market.get_name())
            countries.append(market.get_country())

        self.view.set_table_of_instruments(names, countries)

    def update_instrument_selected(self, table_focus_item_data ):
        logging.debug("Controller: update_instrument_selected")

        self.models[self.selected_model_nbr].update_instrument_selected(table_focus_item_data)

        self.update_selected_model()
        self.update_view()

    def wipe_instrument_selected(self):
        self.models[self.selected_model_nbr].wipe_instrument_selected()

        self.update_selected_model()
        self.update_view()

    def update_strategy_selected(self, new_strategy):
        logging.debug("Controller: update_strategy_selected")
        self.models[self.selected_model_nbr].set_portfolio_strategy(new_strategy)

        self.update_selected_model()
        self.update_view()

    def set_update_amount_leverage(self, value_percent):
        logging.debug("Controller: set_update_amount_leverage")
        value = int(value_percent)/constants.CONVERT_PERCENT
        self.models[self.selected_model_nbr].set_proportion_leverage(value)
        self.models[self.selected_model_nbr].set_proportion_funds(1-value)

        self.update_selected_model()
        self.update_view()

    def update_years_histogram_interval(self, years):
        logging.debug("Controller: update_years_histogram_interval")
        for model in self.models:
            model.set_years_histogram_interval(years)

        self.update_all_models()
        self.update_view()

    def update_harvest_point(self, harvest_point):
        logging.debug("Controller: update_harvest_point")
        self.models[self.selected_model_nbr].set_harvest_point(harvest_point)

        self.update_selected_model()
        self.update_view()

    def update_refill_point(self, refill_point):
        logging.debug("Controller: update_refill_point")
        self.models[self.selected_model_nbr].set_refill_point(refill_point)

        self.update_selected_model()
        self.update_view()

    def update_rebalance_point(self, rebalance_period):
        logging.debug("Controller: update_rebalance_point")
        self.models[self.selected_model_nbr].set_rebalance_period_months(rebalance_period)

        self.update_selected_model()
        self.update_view()

    def update_variance_calc_sample_size(self, variance_calc_sample_size):
        logging.debug("Controller: update_variance_calc_sample_size")
        self.models[self.selected_model_nbr].set_variance_calc_sample_size(variance_calc_sample_size)

        self.update_selected_model()
        self.update_view()

    def update_volatility_strategie_sample_size(self, volatility_strategie_sample_size):
        logging.debug("Controller: update_volatility_strategie_sample_size")
        self.models[self.selected_model_nbr].set_volatility_strategie_sample_size(volatility_strategie_sample_size)
        
        self.update_selected_model()
        self.update_view()

    def update_volatility_strategie_level(self, volatility_strategie_level):
        logging.debug("Controller: update_volatility_strategie_level")
        self.models[self.selected_model_nbr].set_volatility_strategie_level(volatility_strategie_level)
        
        self.update_selected_model()
        self.update_view()

    def update_loan(self, loan):
        logging.debug("Controller: update_loan")
        self.models[self.selected_model_nbr].set_loan(loan)

        self.update_selected_model()
        self.update_view()

    def set_time_limits(self, from_time, to_time):
        logging.debug("Controller: set_time_limits")

        for model in self.models:
            model.set_chosen_start_date_time_limit(from_time)
            model.set_chosen_end_date_time_limit(to_time)

            # If time limit is not set, do not use it
            if from_time == 0 and to_time == 0:
                model.set_chosen_time_interval_status(False)
            else:
                model.set_chosen_time_interval_status(True)

        self.update_all_models() #TODO can fine tune this, if time is decreased it should be done without calculations
        self.update_view()

    def update_table_of_statistics(self):
        logging.debug("Controller: update_table_of_statistics")
        key_values_list = [model.key_values.get_all_values() for model in self.models]
        self.view.update_table_of_statistics(key_values_list)

    def draw_pie_chart(self):
        logging.debug("Controller: draw_pie_chart")
        key_values = self.models[self.selected_model_nbr].key_values.get_all_values()

        self.view.update_pie_chart(key_values)
