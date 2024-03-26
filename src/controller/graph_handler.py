#!/usr/bin/env python3
#
# Copyright (C) 2024 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

import logging

def draw_line_graph(all_models, view):
    logging.debug("draw_line_graph: draw_line_graph")
    time_interval_list =  [model.get_common_time_interval() for model in all_models]
    portfolio_results_full_time_list = [model.get_portfolio_results_full_time() for model in all_models]
    buy_sell_log_list = [model.get_buy_sell_log() for model in all_models]

    

    time_lists, value_lists = interpolate_time_with_values_for_model(time_interval_list, portfolio_results_full_time_list)


    view.draw_line_graph(portfolio_results_full_time_list, time_interval_list, buy_sell_log_list)

#TODO time can be improved by counter and not do full check, or use map
def interpolate_time_with_values_for_model(time_interval_lists, values_lists):
     
    common_time = fix_common_time(time_interval_lists)

    all_time_interval_lists = []
    all_values_lists = []
    new_time_list = []
    new_value_list = []

    
    for i, time_list in enumerate(time_interval_lists):
        firs_date = time_list[0]
        last_date = time_list[-1]

        for date_common in common_time:
            if (date_common > firs_date) and (date_common < last_date):
                new_time_list.append(date_common)

                try:
                    index = time_list.indexof(date_common)                
                    new_value_list.append(values_lists[i][index])

                except:
                    new_value_list.append(new_value_list[-1]) #Value did not move
                    logging.warn("Do I Throw Wrarnings???? It is OKAY")
                    continue
        all_time_interval_lists.append(new_time_list)
        all_values_lists.append(new_value_list)
    
    return [all_time_interval_lists, all_values_lists]
     

def fix_common_time(time_interval_list):

        common_time = []

        for time_span in time_interval_list:
            for date in time_span:
                if date not in common_time:
                    common_time.append(date)

        common_time.sort()

        return common_time