#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2009 Gustav Larson

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import datetime

class Holiday:
    holidays = []

    def __init__(self, date, name):
        self.date = date
        self.name = name
        Holiday.holidays.append(self)

#Midsommardagen is always the saturday in the period june 20-26
def midsommardagen(year):
    date = datetime.date(year, 6, 20)
    while date.weekday() != 5:
        date = date + datetime.timedelta(days = 1)

    return date

#Alla helgons dag is always the saturday in the period october 31 - november 6
def alla_helgons_dag(year):
    date = datetime.date(year, 10, 31)
    while date.weekday() != 5:
        date = date + datetime.timedelta(days = 1)

    return date

#Påskdagen is the first Sunday after the first Full Moon on or after March 21.
#Method used is from http://www.bbc.co.uk/dna/h2g2/A653267
def paskdagen(year):
    a = year % 19
    b = year / 100
    c = year % 100
    d = b / 4
    e = b % 4
    f = (b + 8) / 25;
    g = (b - f + 1) / 3;
    h = (19 * a + b - d - g + 15) % 30
    i = c / 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) / 451
    month = (h + l - 7 * m + 114) / 31
    date = (h + l - 7 * m + 114) % 31 + 1

    return datetime.date(year, month, date)

def generate_holidays(year):
    Holiday(datetime.date(year, 1, 1), "Nyårsdagen")
    Holiday(datetime.date(year, 1, 6), "Trettondedag jul")
    _paskdagen = paskdagen(year)
    Holiday(_paskdagen, "Påskdagen")
    #Långfredagen is the friday before påskdagen, which is always an sunday
    Holiday(_paskdagen - datetime.timedelta(days = 2), "Långfredagen")
    #Annandag påsk is always the day after påskdagen
    Holiday(_paskdagen + datetime.timedelta(days = 1), "Annandag påsk")
    Holiday(datetime.date(year, 5, 1), "Första maj")
    Holiday(datetime.date(year, 6, 6), "Nationaldagen")
    Holiday(midsommardagen(year), "Midsommardagen")
    Holiday(alla_helgons_dag(year), "Alla helgons dag")
    Holiday(datetime.date(year, 12, 25), "Juldagen")
    Holiday(datetime.date(year, 12, 26), "Annandag jul")

def is_holiday(date):
    year = date.year

    # If nyårsdagen of the year that we are querying is not in the list of
    # holidays, we need to generate the holidays of this year
    if not datetime.date(year, 1, 1) in [ h.date for h in Holiday.holidays ]:
        generate_holidays(year)

    return date in [ h.date for h in Holiday.holidays ]
