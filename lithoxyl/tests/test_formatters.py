# -*- coding: utf-8 -*-

from logger import Record, DEBUG
from formatters import Formatter, RecordFormatter, RobustFormatter

template = ('{start_timestamp} - {start_local_iso8601} - {start_iso8601}'
            ' - {logger_name} - {record_status} - {record_name}')


RECS = [Record('Riker', DEBUG).success('Hello, Thomas.')]


TCS = [[('{logger_name}', '""'),
        ('{record_status}', 'success'),
        ('{level_number}', '20'),
        ('{record_name}', '"Riker"'),
        ('{message}', '"Hello, Thomas."')]
       ]


def test_formatter_basic():
    riker = Record('hello_thomas', DEBUG).success('')
    forming = Formatter(template)
    output = forming.format_record(riker)
    assert output.endswith('"" - success - "hello_thomas"')


def test_individual_fields():
    for record, field_pairs in zip(RECS, TCS):
        for field_tmpl, result in field_pairs:
            forming = Formatter(field_tmpl)
            output = forming.format_record(record)
            assert output == result
    return


def test_rec_formatter():
    """
    * no args/kwargs
    * sufficient, correct args/kwargs
    * anonymous args
    * missing kwarg
    * missing arg
    * type mismatch args
    * type mismatch kwargs
    * usage of "builtin" fields
    """

    rec = Record('Wharf')
    recf = RecordFormatter(rec)
    rec.success('Mr. Wolf')

    print recf.format(template)
    template2 = template + ' - {rank}'
    print recf.format(template2, rank='lieutenant')
    template3 = template2 + ' - {stank}'
    print recf.format(template3, rank='lieutenant')
    print recf.format(template3, 'dank', rank='lieutenant')
    print recf.format(template3 + ' - <{}>', rank='lieutenant')


def test_rob_formatter():
    """
    * no args/kwargs
    * sufficient, correct args/kwargs
    * anonymous args
    * missing kwarg
    * missing arg
    * type mismatch args
    * type mismatch kwargs
    * usage of "builtin" fields
    """

    rec = Record('Wharf')
    robf = RobustFormatter(template)
    rec.success('Mr. Wolf')
    ret = robf.format_record(rec)
    print ret
    return ret
