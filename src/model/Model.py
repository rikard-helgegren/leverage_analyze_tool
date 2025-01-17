#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging

from copy import deepcopy

###### IMPORT MODEL ######
from src.Config import Config
from src.model.common.calcultate_daily_change           import calcultate_daily_change
from src.model.graph.calculate_graph                    import calculate_graph
from src.model.common.fill_in_missing_dates             import fill_gaps_data
from src.model.common.calculate_common_time_interval    import calculate_common_time_interval
from src.model.histogram.calculate_histograms_strategy  import calculate_histogram
from src.model.Performance_key_values                   import Performance_Key_values

import src.model.constants_model as constants_model
import src.constants as constants

class Model:
    """ This is the model of the application. It models stock market index
        instruments and calculates portfolio performance as well as other
        measures of interest.

        In order to model the instruments and support a range of portfolios
        the model have plenty of variables.
    """
    def __init__(self):
        logging.debug("Model: __init__")

        self.config = Config()

        ############## Config values ###################

        self.loan                                      = self.config.DEFAUT_LOAN
        self.years_histogram_interval                  = self.config.DEFAUT_YEARS_HISTOGRAM_INTERVAL
        self.harvest_point                             = self.config.DEFAUT_HARVEST_POINT
        self.refill_point                              = self.config.DEFAUT_REFILL_POINT
        self.update_harvest_refill                     = self.config.DEFAUT_UPDATE_HARVEST_REFILL
        self.rebalance_period_months                   = self.config.DEFAUT_REBALANCE_PERIOD_MONTHS
        #self.proportion_cash                          = self.config.DEFAUT_PROPORTION_CASH
        self.proportion_funds                          = self.config.DEFAUT_PROPORTION_FUNDS 
        self.proportion_leverage                       = self.config.DEFAUT_PROPORTION_LEVERAGE
        self.include_fees_status                       = self.config.DEFAUT_INCLUDE_FEES_STATUS
        self.rebalance_between_instruments_status      = self.config.DEFAUT_REBALANCE_BETWEEN_INSTRUMENTS_STATUS
        self.correction_of_inflation_status            = self.config.DEFAUT_CORRECTION_OF_INFLATION_STATUS
        self.correction_of_currency_status             = self.config.DEFAUT_CORRECTION_OF_CURRENCY_STATUS
        self.delay_of_correction                       = self.config.DEFAUT_DELAY_OF_CORRECTION
        self.chosen_time_interval_start_date           = 0
        self.chosen_time_interval_end_date             = 0
        self.chosen_time_interval_status               = False
        self.portfolio_strategy                        = constants.PORTFOLIO_STRATEGIES[0]
        self.default_variance_sample_size              = self.config.DEFAUT_VARIANCE_SAMPLE_SIZE
        self.default_volatility_strategie_sample_size  = self.config.DEFAUT_VOLATILITY_STRATEGIE_SAMPLE_SIZE
        self.default_volatility_strategie_level        = self.config.DEFAUT_VOLATILITY_STRATEGIE_LEVEL
        


        ################ Data Processed ################

        self.markets = {}
        """ Dictionary of Market objects representing the data files
            Dictionary keys are same as the market abbreviation
        """

        self.markets_selected = {}
        """ Dictionary of Market objects selected from the GUI Instrument table
            Copies of the self.markets, and these will be modified as needed to be compatible
        """

        self.instruments_selected = []
        """ List of the instruments selected from the GUI Instrument table
            each item is a list with instrument name and leverage
            e.g. [[SP500, 1], [SP500, 5], [OMXS30, 1], ...]
        """

        self.portfolio_results_full_time = []
        """ List of the portfolios value for each day with an update.
            The portfolio is made up of all selected instruments
        """

        self.portfolio_results_full_time_without_leverage = []
        """ List of the portfolios value for each day with an update.
            The portfolio is made up of only non leverage items. This is
            needed for some statistical performance meters.
        """

        self.common_time_interval = []
        """ List of all days in the time span that the selected instruments
            have data for. Missing days within the common time span are added
        """

        self.results_for_intervals = []
        """ List of results for all the continuous time intervals of length 
            'self.years_histogram_interval' in the time investigated.
            
            The purpose of this variable is to be ploted in histogram
        """

        self.buys_sells = {}
        """ Dict of buy and sell information for each day. e.x.
            ['19990310'] = [{
                Action: Sell
                Certificate: OMXS30_X3
                },
                {
                Action: Buy
                Certificate: OMXS30_X5
                }
            ]
        """

        self.key_values = Performance_Key_values(self)


    ######################
    # Central methods
    ######################

    def update_model(self):
        """ Make the markets selected compatible, and calculate the new results"""
        logging.debug("Model: update_model")

        self.update_data()
        self.update_graph()
        self.update_histogram()

    def update_graph(self):
        calculate_graph(self)

    def update_histogram(self):
        calculate_histogram(self)
        self.key_values.update_values(self.results_for_intervals, self.portfolio_results_full_time)

    def update_data(self):
        self.common_time_interval = calculate_common_time_interval(self)  # TODO: doing double work some times

        if len(self.common_time_interval) > 0:
            first_day = self.common_time_interval[0]
            last_day = self.common_time_interval[-1]
        else:
            first_day = self.chosen_time_interval_start_date
            last_day = self.chosen_time_interval_end_date

        self.markets_selected = fill_gaps_data(self.markets_selected,
                                               first_day,
                                               last_day)
        
        self.markets_selected = calcultate_daily_change(self.markets_selected)


    ######################
    # Other methods
    ######################
    def update_instrument_selected(self, table_focus_item_data):
        """ Update the instruments selected based on what item was
            selected in the table of instruments.

            Param: table_focus_item_data: [Name: String, leverage: Int]
        """
        logging.debug("Model: update_instrument_selected")
        if table_focus_item_data in self.instruments_selected:
            self.instruments_selected.remove(table_focus_item_data)
        else:
            self.instruments_selected.append(table_focus_item_data)

        self.update_market_selected()

    def wipe_instrument_selected(self):
        self.instruments_selected = []

    def update_market_selected(self):
        """ Copy the markets of the instruments selected in the instrument
            table, into the variable self.markets_selected.
        """
        logging.debug("Model: update_market_selected")

        # TODO: this part maybe tries to add same market multiple times, takes some extra time
        self.markets_selected = {}
        for instrument in self.instruments_selected:
            name = instrument[0]
            self.markets_selected[name] = deepcopy(self.markets[name])


    ##########################
    #  Getters and Setters
    ##########################
    def get_loan(self):
        logging.debug("Model: get_loan")
        return self.loan
    def set_loan(self, loan):
        logging.debug("Model: set_loan")
        self.loan = loan
    
    def get_years_histogram_interval(self):
        logging.debug("Model: get_years_histogram_interval")
        return self.years_histogram_interval
    def set_years_histogram_interval(self, years):
        logging.debug("Model: set_years_histogram_interval")
        self.years_histogram_interval = years

    def get_harvest_point(self):
        logging.debug("Model: get_harvest_point")
        return self.harvest_point
    def set_harvest_point(self, harvest_point):
        logging.debug("Model: set_harvest_point")
        self.harvest_point = harvest_point

    def get_refill_point(self):
        logging.debug("Model: get_refill_point")
        return self.refill_point
    def set_refill_point(self, refill_point):
        logging.debug("Model: set_refill_point")
        self.refill_point = refill_point

    def get_update_harvest_refill(self):
        logging.debug("Model: get_update_harvest_refill")
        return self.update_harvest_refill
    def set_update_harvest_refill(self, update_harvest_refill):
        logging.debug("Model: set_update_harvest_refill")
        self.update_harvest_refill = update_harvest_refill

    def get_rebalance_period_months(self):
        logging.debug("Model: get_rebalance_period_months")
        return self.rebalance_period_months
    def set_rebalance_period_months(self, rebalance_period_months):
        logging.debug("Model: set_rebalance_period_months %f", rebalance_period_months)
        self.rebalance_period_months = rebalance_period_months

    def get_proportion_cash(self):
        logging.debug("Model: get_proportion_cash")
        return self.proportion_cash
    def set_proportion_cash(self, proportion_cash):
        logging.debug("Model: set_proportion_cash")
        self.proportion_cash = proportion_cash

    def get_proportion_funds(self):
        logging.debug("Model: get_proportion_funds")
        return self.proportion_funds
    def set_proportion_funds(self, proportion_funds):
        logging.debug("Model: set_proportion_funds %f", proportion_funds)
        self.proportion_funds = proportion_funds

    def get_proportion_leverage(self):
        logging.debug("Model: get_proportion_leverage")
        return self.proportion_leverage
    def set_proportion_leverage(self, proportion_leverage):
        """The proportion of leverage should be a value between 0 and 1"""
        logging.debug("Model: set_proportion_leverage %f", proportion_leverage)
        self.proportion_leverage = proportion_leverage

    def get_include_fees_status(self):
        logging.debug("Model: get_include_fees_status")
        return self.include_fees_status
    def set_include_fee_status(self, include_fee_status):
        logging.debug("Model: set_include_fee_status")
        self.include_fees_status = include_fee_status
        logging.debug("Model, fee_status: %f", include_fee_status)


    def get_rebalance_between_instruments_status(self):
        logging.debug("Model: get_rebalance_between_instruments_status")
        return self.rebalance_between_instruments_status
    def set_rebalance_between_instruments_status(self, rebalance_between_instruments_status):
        logging.debug("Model: set_rebalance_between_instruments_status")
        self.rebalance_between_instruments_status = rebalance_between_instruments_status

    def get_correction_of_inflation_status(self):
        logging.debug("Model: get_correction_of_inflation_status")
        return self.correction_of_inflation_status
    def set_correction_of_inflation_status(self, correction_of_inflation_status):
        logging.debug("Model: set_rebalance_between_instruments_status")
        self.correction_of_inflation_status = correction_of_inflation_status

    def get_correction_of_currency_status(self):
        logging.debug("Model: get_correction_of_currency_status")
        return self.correction_of_currency_status
    def set_correction_of_currency_status(self, correction_of_currency_status):
        logging.debug("Model: set_correction_of_currency_status")
        self.correction_of_currency_status = correction_of_currency_status

    def get_delay_of_correction(self):
        logging.debug("Model: get_delay_of_correction")
        return self.delay_of_correction
    def set_delay_of_correction(self, delay_of_correction):
        logging.debug("Model: set_delay_of_correction")
        self.delay_of_correction = delay_of_correction

    def get_markets(self):
        logging.debug("Model: get_markets")
        return self.markets
    def set_markets(self, markets):
        logging.debug("Model: set_markets %f", len(markets)  )
        self.markets = markets

    def get_instruments_selected(self):
        logging.debug("Model: get_instruments_selected")
        return self.instruments_selected
    def set_instruments_selected(self, instruments_selected):
        logging.debug("Model: set_instruments_selected")
        self.instruments_selected = instruments_selected

    def get_portfolio_results_full_time(self):
        logging.debug("Model: get_portfolio_results_full_time")
        return self.portfolio_results_full_time
    def set_portfolio_results_full_time(self, portfolio_results_full_time):
        logging.debug("Model: set_portfolio_results_full_time")
        self.portfolio_results_full_time = portfolio_results_full_time

    def get_common_time_interval(self):
        logging.debug("Model: get_common_time_interval")
        return self.common_time_interval
    def set_common_time_interval(self, common_time_interval):
        logging.debug("Model: set_common_time_interval")
        self.common_time_interval = common_time_interval

    def get_markets_selected(self):
        logging.debug("Model: get_markets_selected")
        return self.markets_selected
    def set_markets_selected(self, markets_selected):
        logging.debug("Model: set_markets_selected")
        self.markets_selected = markets_selected

    def get_results_for_intervals(self):
        logging.debug("Model: get_results_for_intervals")
        return self.results_for_intervals
    def set_results_for_intervals(self, results_for_intervals):
        logging.debug("Model: set_results_for_intervals")
        self.results_for_intervals = results_for_intervals

    def set_chosen_start_date_time_limit(self, start_date):
        logging.debug("Model: set_chosen_start_date_time_limit")
        self.chosen_time_interval_start_date = start_date
    def get_chosen_start_date_time_limit(self):
        logging.debug("Model: get_chosen_start_date_time_limit")
        return self.chosen_time_interval_start_date

    def set_chosen_end_date_time_limit(self, end_date):
        logging.debug("Model: set_chosen_end_date_time_limit")
        self.chosen_time_interval_end_date = end_date
    def get_chosen_end_date_time_limit(self):
        logging.debug("Model: get_chosen_end_date_time_limit")
        return self.chosen_time_interval_end_date

    def set_chosen_time_interval_status(self, status_time_limit):
        logging.debug("Model: set_chosen_time_interval_status")
        self.chosen_time_interval_status = status_time_limit
        # Need to refresh markets in order to not keep old times
        self.update_market_selected()

    def get_chosen_time_interval_status(self):
        logging.debug("Model: get_chosen_time_interval_status")
        return self.chosen_time_interval_status

    def get_all_portfolio_strategies(self):
        logging.debug("Model: get_all_portfolio_strategies")
        return constants.PORTFOLIO_STRATEGIES

    def set_portfolio_strategy(self, portfolio_strategy):
        logging.debug("Model: set_portfolio_strategy")
        if portfolio_strategy in constants.PORTFOLIO_STRATEGIES:
            self.portfolio_strategy = portfolio_strategy
        else:
            logging.error(" portfolio_strategy from view is valid in Model")

    def get_portfolio_strategy(self):
        logging.debug("Model: get_portfolio_strategy")
        return self.portfolio_strategy

    
    def get_variance_calc_sample_size(self):
        logging.debug("Model: get_variance_calc_sample_size")
        return self.default_variance_sample_size
    def set_variance_calc_sample_size(self, variance_calc_sample_size):
        logging.debug("Model: set_variance_calc_sample_size")
        self.default_variance_sample_size = variance_calc_sample_size


    def get_volatility_strategie_sample_size(self):
        logging.debug("Model: get_volatility_strategie_sample_size")
        return self.default_volatility_strategie_sample_size 
    def set_volatility_strategie_sample_size(self, volatility_strategie_sample_size):
        logging.debug("Model: set_volatility_strategie_sample_size")
        self.default_volatility_strategie_sample_size = volatility_strategie_sample_size
    
    def get_volatility_strategie_level(self):
        logging.debug("Model: get_volatility_strategie_level")
        return self.default_volatility_strategie_level
    def set_volatility_strategie_level(self, volatility_strategie_level):
        logging.debug("Model: set_volatility_strategie_level")
        self.default_volatility_strategie_level = volatility_strategie_level

    def get_buy_sell_log(self):
        logging.debug("Model: get_buy_sell_log")
        return self.buys_sells
    
    def set_buy_sell_by_lists(self, date_list, action_list):
        logging.debug("Model: set_buy_sell_by_lists, len both lists " + str(len(date_list)) + " " + str(len(action_list)))
        if date_list == []:
            self.buys_sells = {}
            return
        
        if len(date_list) != len(action_list): 
            logging.warn("Model: set_buy_sell_by_lists, the lists have different size, %r and %r ", len(date_list), len(action_list))
            self.buys_sells = {}
            return

        buy_sell_dict = {}
        reference_date = date_list[0]
        events_this_day = []

        action_list = self.convert_int_to_buy_sell_enum(action_list)

        for index in range(0, len(date_list)):
            if reference_date == date_list[index]:
                events_this_day.append({'Action': action_list[index]})
            else: # New day add prev day
                buy_sell_dict[reference_date] = events_this_day

                reference_date = date_list[index]
                events_this_day = []
                events_this_day.append({'Action': action_list[index]})
        
        buy_sell_dict[reference_date] = events_this_day

        self.buys_sells = buy_sell_dict
    
    def convert_int_to_buy_sell_enum(self, buy_sell_action_list):
        logging.debug("Model: convert_int_to_buy_sell_enum")
        new_action_list = []

        for action in buy_sell_action_list:
            if action == 1:
                new_action_list.append(constants_model.Order.BUY)
            elif action == 2:
                new_action_list.append(constants_model.Order.SELL)
        
        return new_action_list
