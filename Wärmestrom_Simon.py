# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 18:50:38 2019

@author: sbeckmann
"""

import numpy as np

def waermestromformel(temp_outside, temp_inside, r_lambda):
    return np.divide(temp_outside - temp_inside, r_lambda)

def calculate(list_of_temperatures_outside, r_lambda):
    waermestrom = list()

    for index, item in enumerate(list_of_temperatures_outside):
        hour = index % 24
        
        if 10 <= hour and hour <= 18:
            temp_inside = 21
        else:
            temp_inside = 18

        waermestrom.append(waermestromformel(item, temp_inside, r_lambda))
    return waermestrom




