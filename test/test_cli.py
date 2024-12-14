#!/usr/bin/env python3

import io
import textwrap

import pytest

from datetime import datetime as dt
from datetime import timezone as tz

from cashlog import load_data, save_data, compute_totals


def test_load_data():
    csv = textwrap.dedent('''\
        datetime,amount,desc
        2020-01-01 00:00:00+00:00,+5,First gift
        2020-01-03 00:00:00+00:00,+7.500,Second gift
        2020-01-05 00:00:00+00:00,-3.1,First expense
        2020-01-05 00:00:00+00:00,+0,Zero
        2020-01-05 00:00:00+00:00,-0,Negative zero
    ''')

    data = load_data(io.StringIO(csv))

    assert data == [
        {'datetime': dt(2020, 1, 1, tzinfo=tz.utc),
         'amount': 5, 'desc': 'First gift'},
        {'datetime': dt(2020, 1, 3, tzinfo=tz.utc),
         'amount': 7.5, 'desc': 'Second gift'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': -3.1, 'desc': 'First expense'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': 0, 'desc': 'Zero'},
        {'datetime': dt(2020, 1, 5, tzinfo=tz.utc),
         'amount': 0, 'desc': 'Negative zero'},
    ]

    # with pytest.raises(ValueError) as exc_info: # TODO
    #     load_data(io.StringIO(csv))
    # assert exc_info.value.args == (
    #     'TODO',)


def test_save_data():
    data = [
        # TODO
    ]

    csv = textwrap.dedent('''\
        datetime,amount,total,desc
        2020-01-01 00:00:00+00:00,+5,First gift
        2020-01-03 00:00:00+00:00,+7.500,Second gift
        2020-01-05 00:00:00+00:00,-3.1,First expense
        2020-01-05 00:00:00+00:00,+0,Zero
        2020-01-05 00:00:00+00:00,-0,Negative zero
    ''')

    buf = io.StringIO()
    save_data(data, buf)
    buf.seek(0)

    # assert buf.read() == csv # TODO


def test_compute_totals():
    data_in_orig = [
        # TODO
    ]

    data_out_expected = [
        # TODO
    ]

    data_in = [x.copy() for x in data_in_orig]
    data_in_copy = [x.copy() for x in data_in]
    data_out = list(compute_totals(data_in))
    # assert data_in == data_in_copy # TODO
    # assert data_out == data_out_expected # TODO
