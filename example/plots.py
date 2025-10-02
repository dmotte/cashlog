#!/usr/bin/env python3

import argparse
import csv
import sys

from contextlib import ExitStack
from typing import TextIO

from dateutil import parser as dup
import plotly.express as px


def load_data(file: TextIO) -> tuple[list[dict], str]:
    '''
    Loads data from a CSV file. It automatically detects the delimiter based on
    the file content
    '''
    preview = file.readline(9)
    file.seek(0)

    if not preview.startswith('datetime'):
        raise ValueError('Content must start with "datetime"')

    delimiter = preview[8]

    data = list(csv.DictReader(file, delimiter=delimiter))

    for entry in data:
        entry['datetime'] = dup.parse(entry['datetime'])
        entry['amount'] = float(entry['amount'])
        entry['total'] = float(entry['total'])

    return data, delimiter


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description='Generate plots based on data computed with cashlog'
    )

    parser.add_argument('file_in', metavar='FILE_IN', type=str,
                        nargs='?', default='-',
                        help='Input file. If set to "-" then stdin is used '
                        '(default: %(default)s)')

    parser.add_argument('-a', '--plot-amount', action='store_true',
                        help='Generate plot based on amount values')
    parser.add_argument('-t', '--plot-total', action='store_true',
                        help='Generate plot based on total values')

    args = parser.parse_args(argv[1:])

    ############################################################################

    with ExitStack() as stack:
        file_in = (sys.stdin if args.file_in == '-'
                   else stack.enter_context(open(args.file_in, 'r')))
        data, _ = load_data(file_in)

    if args.plot_amount:
        fig = px.bar(
            data,
            y='amount',
            template='plotly_dark',
            title='Amount values',

            color_discrete_sequence=['#fd0'],
            hover_name='datetime',
            hover_data=['desc'],
        )
        fig.show()

    if args.plot_total:
        fig = px.line(
            data,
            x='datetime',
            y='total',
            template='plotly_dark',
            title='Total values',

            line_shape='hv',
            hover_name='datetime',
            hover_data=['amount', 'desc'],
            markers=True,
        )
        fig.update_traces(marker={'size': 8, 'color': '#fd0'})
        fig.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
