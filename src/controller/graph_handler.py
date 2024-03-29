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

    time_union, time_lists, value_lists = interpolate_time_with_values_for_model(time_interval_list, portfolio_results_full_time_list)

    correct_index_of_buy_sell_log(buy_sell_log_list)
    time_lists = date_to_union_time_index(time_union,time_lists)

    view.draw_line_graph(time_union, value_lists, time_lists, buy_sell_log_list)

#TODO time can be improved by counter and not do full check, or use map
def interpolate_time_with_values_for_model(time_interval_lists, values_lists):
     
    time_union = fix_time_union(time_interval_lists)

    all_time_interval_lists = []
    all_values_lists = []
    
    for i, time_list in enumerate(time_interval_lists):
        if(len(time_list)==0):
            continue

        new_time_list = []
        new_value_list = []

        firs_date = time_list[0]
        last_date = time_list[-1]

        for date_common in time_union:
            if (date_common >= firs_date) and (date_common <= last_date):
                new_time_list.append(date_common)

                try:
                    index = time_list.index(date_common)                
                    new_value_list.append(values_lists[i][index])

                except:
                    if len(new_value_list) >= 1:
                        new_value_list.append(new_value_list[-1]) #Value did not move
                    
                    continue
        all_time_interval_lists.append(new_time_list)
        all_values_lists.append(new_value_list)
    
    return [time_union ,all_time_interval_lists, all_values_lists]
     

def fix_time_union(time_interval_list):

        time_union = []

        for time_span in time_interval_list:
            for date in time_span:
                if date not in time_union:
                    time_union.append(date)

        time_union.sort()

        return time_union

def date_to_union_time_index(time_union,time_lists):

    time_index_list = []

    for time_interval in time_lists:

        working_list = []
        for date in time_interval:
            working_list.append(time_union.index(date))
    
        time_index_list.append(working_list)  

    return time_index_list

def correct_index_of_buy_sell_log(buy_sell_log_list):

    return buy_sell_log_list
    #for entry in buy_sell_log_list:


