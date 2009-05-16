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
    """Class to hold all holidays

    >>> Holiday(datetime.date(2009, 1, 1), 'Nyårsdagen') #doctest: +ELLIPSIS
    <__main__.Holiday instance at 0x...>
    >>> Holiday.holidays #doctest: +ELLIPSIS
    [<__main__.Holiday instance at 0x...>]
    >>> Holiday(datetime.date(2009, 12, 25), 'Juldagen') #doctest: +ELLIPSIS
    <__main__.Holiday instance at 0x...>
    >>> Holiday.holidays #doctest: +ELLIPSIS
    ...                  #doctest: +NORMALIZE_WHITESPACE
    [<__main__.Holiday instance at 0x...>, \
            <__main__.Holiday instance at 0x...>]
    >>> Holiday.holidays[0] < Holiday.holidays[1]
    True
    >>> Holiday.holidays[0] == Holiday.holidays[1]
    False
    >>> Holiday.holidays[0] > Holiday.holidays[1]
    False
    >>> Holiday.holidays = [] #Destroy the objects we just created
    """

    holidays = []

    def __init__(self, date, name):
        self.date = date
        self.name = name
        Holiday.holidays.append(self)

    def __cmp__(self, other):
        return cmp(self.date, other.date)


def midsommardagen(year):
    """Return the date of midsommardagen(Midsummer's Day)

    The result is returned as a datetime.date()

    Midsommardagen is always the saturday in the period June 20-26.
    Before 1954 it was always on June 24.
    >>> midsommardagen(2009)
    datetime.date(2009, 6, 20)
    >>> midsommardagen(1950)
    datetime.date(1950, 6, 24)
    >>> midsommardagen('foo')
    Traceback (most recent call last):
    TypeError: an integer is required
    """

    if year >= 1954:
        date = datetime.date(year, 6, 20)
        while date.weekday() != 5:
            date = date + datetime.timedelta(days = 1)
    else:
        date = datetime.date(year, 6, 24)

    return date


def alla_helgons_dag(year):
    """Return the date of alla helgons dag(All Saints' Day) of a given year

    The result is returned as a datetime.date()

    Alla helgons dag is always the saturday in the period October 31 -
    November 6. Before 1954 it was always on November 1st.


    >>> alla_helgons_dag(2009)
    datetime.date(2009, 10, 31)
    >>> alla_helgons_dag(1950)
    datetime.date(1950, 11, 1)
    >>> alla_helgons_dag('foo')
    Traceback (most recent call last):
    TypeError: an integer is required
    """

    if year >= 1954:
        date = datetime.date(year, 10, 31)
        while date.weekday() != 5:
            date = date + datetime.timedelta(days = 1)
    else:
        date = datetime.date(year, 11, 1)

    return date


def paskdagen(year):
    """Return the date of påskdagen(Easter sunday) of a given year

    The result is returned as a datetime.date()

    Påskdagen is the first Sunday after the first Full Moon on or after
    March 21. Spencer Jones algorithm for calculating Easter Sunday is used
    (http://sv.wikipedia.org/wiki/Påskdagen#Algoritm_för_påskdagen)


    >>> paskdagen(2009)
    datetime.date(2009, 4, 12)
    >>> paskdagen('foo')
    Traceback (most recent call last):
    TypeError: an integer is required
    """

    if not type(year) is int:
        raise TypeError('an integer is required')

    a = year % 19
    b = year / 100
    c = year % 100
    d = b / 4
    e = b % 4
    f = (b + 8) / 25
    g = (b - f + 1) / 3
    h = (19 * a + b - d - g + 15) % 30
    i = c / 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) / 451
    month = (h + l - 7 * m + 114) / 31
    date = (h + l - 7 * m + 114) % 31 + 1

    return datetime.date(year, month, date)


def _generate_holidays(year):
    """Generates all the holidays for a given year

    If the holidays are already generated, don't do anything


    >>> _generate_holidays(2009)
    >>> len(Holiday.holidays)
    11
    >>> _generate_holidays(1999)
    >>> len(Holiday.holidays)
    22
    >>> _generate_holidays('foo')
    Traceback (most recent call last):
    TypeError: an integer is required
    """

    # If nyårsdagen of the year that we are querying is not in the list of
    # holidays, we need to generate the holidays of this year
    if not datetime.date(year, 1, 1) in [h.date for h in Holiday.holidays]:
        Holiday(datetime.date(year, 1, 1), "Nyårsdagen")
        Holiday(datetime.date(year, 1, 6), "Trettondedag jul")

        #Jungfru Marias bebådelsedag was removed in 1954
        if year <= 1953: Holiday(datetime.date(year, 3, 25), \
                "Jungfru Marias bebådelsedag")

        _paskdagen = paskdagen(year)
        Holiday(_paskdagen, "Påskdagen")
        #Långfredagen is the friday before påskdagen,
        #which is always an sunday
        Holiday(_paskdagen - datetime.timedelta(days = 2), "Långfredagen")
        #Annandag påsk is always the day after påskdagen
        Holiday(_paskdagen + datetime.timedelta(days = 1), "Annandag påsk")

        #Första maj was introduced in 1939
        if year >= 1939: Holiday(datetime.date(year, 5, 1), "Första maj")

        #Annandag pingst was replaced in 2005 with nationaldagen
        if year <= 2004:
            Holiday(_paskdagen + datetime.timedelta(days = 50), \
                    "Annandag pingst")
        else:
            Holiday(datetime.date(year, 6, 6), "Nationaldagen")

        Holiday(midsommardagen(year), "Midsommardagen")
        Holiday(alla_helgons_dag(year), "Alla helgons dag")
        Holiday(datetime.date(year, 12, 25), "Juldagen")
        Holiday(datetime.date(year, 12, 26), "Annandag jul")


def is_holiday(date):
    """Test if a given datetime.date is a holiday


    >>> is_holiday(datetime.date(2009, 1, 1))
    True
    >>> is_holiday(datetime.date(2010, 2, 2))
    False
    >>> is_holiday('foo')
    Traceback (most recent call last):
    TypeError: an datetime.date object is required
    """

    if not isinstance(date, datetime.date):
        raise TypeError('an datetime.date object is required')

    _generate_holidays(date.year)

    return date in [h.date for h in Holiday.holidays]


def all_holidays(start_date, end_date):
    """Returns all holidays between two dates

    The reslut is returned as a list of Holiday objects sorted by date.


    >>> all_holidays(datetime.date(2010, 01, 01), datetime.date(2009, 01, 01))
    Traceback (most recent call last):
    ValueError: start_date needs to be earlier than end_date
    >>> len(all_holidays(datetime.date(2009, 01, 01), \
            datetime.date(2009, 04, 01)))
    2
    """

    if start_date > end_date:
        raise ValueError('start_date needs to be earlier than end_date')

    #Generate the holidays for the period between the dates
    for year in range(start_date.year, end_date.year + 1):
        _generate_holidays(year)

    holidays = [holiday for holiday in Holiday.holidays \
            if holiday.date >= start_date and holiday.date <= end_date]
    holidays.sort()
    return holidays


if __name__ == "__main__":
    import doctest
    doctest.testmod()
