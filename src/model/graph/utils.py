#!/usr/bin/env python3
#
# Copyright (C) 2022 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging
import src.model.common.constants_model as constants_model
from src.model.Portfolio_item import Portfolio_Item

def create_portfolio(instruments_selected, number_of_leveraged_instruments, loan, proportion_funds, number_of_funds, proportion_leverage, markets_selected):
    logging.debug("Graph utils: create_portfolio")

    portfolio_items = []
    for instrument in instruments_selected:
        name = instrument[0]
        leverage = instrument[1]

        portfolio_item = Portfolio_Item(name, leverage)
        
        set_initial_portfolio_values(leverage, number_of_leveraged_instruments, loan, proportion_funds, number_of_funds, portfolio_item, proportion_leverage, name, markets_selected)   

        portfolio_items.append(portfolio_item)
    
    return portfolio_items


def get_last_index_of_days_from_instrument(a_instrument, markets_selected, end_time):
    logging.debug("Graph utils: get_last_index_of_days_from_instrument")
    
    market = markets_selected[a_instrument[0]]
    return market.get_time_span().index(end_time)


def calculate_nbr_of_funds_and_leverages(instruments_selected):
    logging.debug("Graph utils: calculate_nbr_of_funds_and_leverages")
    
    number_of_funds = 0
    number_of_leveraged_instruments = 0
    for instrument in instruments_selected:
        leverage = instrument[1]
        if leverage == 1:
            number_of_funds += 1
        else:
            number_of_leveraged_instruments += 1

    return [number_of_funds, number_of_leveraged_instruments]


def set_initial_portfolio_values(leverage, number_of_leveraged_instruments, loan, proportion_funds, number_of_funds, portfolio_item, proportion_leverage, name, markets_selected):
    logging.debug("Graph utils: set_initial_portfolio_values")

    if leverage == 1:
        if number_of_leveraged_instruments > 0:
            portfolio_item.set_current_value((1+loan) * proportion_funds/number_of_funds)
        else:
            portfolio_item.set_current_value((1+loan)/number_of_funds)  # TODO could remove?
    else:
        if number_of_funds > 0:
            portfolio_item.set_current_value((1+loan) * proportion_leverage/number_of_leveraged_instruments)
        else:
            portfolio_item.set_current_value((1+loan)/number_of_leveraged_instruments) # TODO could remove?

    portfolio_item.set_reference_value(portfolio_item.get_current_value())
    portfolio_item.set_country(markets_selected[name].get_country())
    portfolio_item.set_daily_change(markets_selected[name].get_daily_change())
    portfolio_item.set_values([portfolio_item.get_current_value()-loan])
    


def sum_porfolio_results_full_time(portfolio_items):
    """
        Summing the value for all time instances of each portfolio item together
        e.g. [1,2,3] + [1,2,3] = [2,4,6]
    """
    logging.debug("Graph utils: sum_porfolio_results_full_time")
    portfolio_results_full_time = []
    for item in portfolio_items:
        if portfolio_results_full_time == []:
            portfolio_results_full_time = item.get_values()
        else:
            portfolio_results_full_time = [start + adding for start, adding in zip(portfolio_results_full_time, item.get_values())]

    return portfolio_results_full_time


def convert_change_to_total_value(change_day_list):
    """
        Converting change to the representative market value for this period
    """
    
    logging.debug("Graph utils: convert_change_to_total_value")

    total_value_list = [1]
    for day_change in change_day_list:
        total_value_list.append(total_value_list[-1] + total_value_list[-1]*day_change)

    return total_value_list


def update_value_with_daily_change(item, day, use_fees):
    """
        Update instrument value with the daily change times its leverage 
    """  
    logging.debug("Graph utils: update_value_with_daily_change")
    current_value = item.get_current_value()
    oneDayChange = current_value * item.get_daily_change()[day] * item.get_leverage()

    currencyChange = 1  #TODO requires data and implementation

    if (use_fees is True):
        dailyFee = current_value * getFeeLevel(item.get_leverage())
    else:
        dailyFee = 0

    new_value =  (current_value  + oneDayChange - dailyFee) * currencyChange

    if (new_value <= 0):
        return 0

    return new_value


def getFeeLevel(leverage):
    """
        Return the fee rate related to the different leverage levels
    """
    logging.debug("Graph utils: getFeeLevel")
    if (leverage == 1):
        return constants_model.FEE_BULL_1
    elif (leverage >= 2 and leverage <= 4):
        return constants_model.FEE_BULL_2_TO_4
    elif (leverage >= 5):
        return constants_model.FEE_BULL_5_AND_MORE
    else:
        logging.ERROR("Graph utils: Invalid leverage")
        return -1
