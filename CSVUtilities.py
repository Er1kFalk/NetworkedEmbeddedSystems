# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 16:20:31 2024

@author: Erik
"""

import csv

def getCsvLines(file):
    """
    Given a path to a CSV file, a 2d array with the lines are returned

    Parameters
    ----------
    file : string
        path to csv file.

    Returns
    -------
    lines : 2d array
        each csv line is an array.

    """
    lines = []
    with open(file, mode='r') as fileObj:
        csvFile = csv.reader(fileObj)
        for l in csvFile:
            lines.append(l)
        return lines