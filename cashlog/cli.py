#!/usr/bin/env python3

import argparse
import csv
import sys

from contextlib import ExitStack
from datetime import datetime as dt
from typing import TextIO

from dateutil import parser as dup


def is_aware(d: dt):
    '''
    Returns true if the datetime object `d` is timezone-aware, false otherwise.
    See https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    '''
    return d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None


def load_data(file: TextIO) -> tuple[list[dict], str]:
    '''
    Loads data from a CSV file. It automatically detects the delimiter based on
    the file content
    '''
    preview = file.readline(9)

    if preview.startswith('sep='):
        delimiter = preview[4]
    elif preview.startswith('datetime'):
        delimiter = preview[8]
        file.seek(0)
    else:
        raise ValueError('Content must start with either "sep=" or "datetime"')

    data = list(csv.DictReader(file, delimiter=delimiter))

    for entry in data:
        entry['datetime'] = dup.parse(entry['datetime'])

        if not is_aware(entry['datetime']):
            entry['datetime'] = entry['datetime'].astimezone()

        if not entry['amount'].startswith(('-', '+')):
            raise ValueError(f'Amount {entry['amount']} does not start with - '
                             'or +')

        entry['amount'] = float(entry['amount'])

    for i in range(1, len(data)):
        prev, curr = data[i - 1], data[i]

        if prev['datetime'] > curr['datetime']:
            raise ValueError(f'Invalid entry order: {prev['datetime']} > ' +
                             f'{curr['datetime']}')

    return data, delimiter


def save_data(data: list[dict], file: TextIO, delimiter: str = ',',
              fmt_currency: str = ''):
    '''
    Saves data into a CSV file
    '''
    func_currency = str if fmt_currency == '' \
        else lambda x: fmt_currency.format(x)

    fields = {
        'datetime': str,
        'amount': func_currency,  # TODO split into fmt_amount and fmt_total
        'total': func_currency,
        'desc': str,
    }

    print(delimiter.join(fields.keys()), file=file)
    for x in data:
        print(delimiter.join(f(x[k]) for k, f in fields.items()), file=file)


def compute_totals(data: list[dict]):
    '''
    Computes totals
    '''
    total = 0

    for entry in data:
        total += entry['amount']
        yield {
            'datetime': entry['datetime'],
            'amount': entry['amount'],
            'total': total,
            'desc': entry['desc'],
        }


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='Cash flow tracker'
    )

    parser.add_argument('file_in', metavar='FILE_IN', type=str,
                        nargs='?', default='-',
                        help='Input file. If set to "-" then stdin is used '
                        '(default: -)')
    parser.add_argument('file_out', metavar='FILE_OUT', type=str,
                        nargs='?', default='-',
                        help='Output file. If set to "-" then stdout is used '
                        '(default: -)')

    parser.add_argument('--fmt-currency', type=str, default='',
                        help='If specified, formats the currency values with '
                        'this format string (e.g. "{:+.2f}")')

    args = parser.parse_args(argv[1:])

    ############################################################################

    with ExitStack() as stack:
        file_in = (sys.stdin if args.file_in == '-'
                   else stack.enter_context(open(args.file_in, 'r')))
        file_out = (sys.stdout if args.file_out == '-'
                    else stack.enter_context(open(args.file_out, 'w')))

        data_in, delimiter = load_data(file_in, delimiter)
        data_out = compute_totals(data_in)
        save_data(data_out, file_out, delimiter, args.fmt_currency)

    return 0
