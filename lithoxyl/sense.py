# -*- coding: utf-8 -*-

from lithoxyl.logger import BaseLogger
from lithoxyl.formatters import Formatter
from lithoxyl.emitters import StreamEmitter
from lithoxyl.filters import ThresholdFilter
from lithoxyl.sinks import SensibleSink, QuantileSink


class SensibleLogger(BaseLogger):
    def __init__(self, name, **kwargs):
        enable_begin = kwargs.pop('enable_begin', True)
        if kwargs:
            raise TypeError('unexpected keyword arguments: %r' % kwargs)
        exc_filter = ThresholdFilter(exception=0)
        exc_formatter = Formatter('!! {exc_type}: {exc_tb_str}')
        exc_emitter = StreamEmitter('stderr')
        exc_sink = SensibleSink(exc_formatter, exc_emitter, [exc_filter])

        #out_filter = ThresholdFilter()
        # TODO: warn_char (requires len on FormatField)
        out_formatter = Formatter('{status_char} {logger_name}'
                                  ' {message} {duration_msecs}')
        out_emitter = StreamEmitter('stdout')
        out_sink = SensibleSink(out_formatter, out_emitter)
        sinks = [QuantileSink(), exc_sink, out_sink]
        if enable_begin:
            beg_filter = ThresholdFilter(begin=0)
            beg_formatter = Formatter('{status_char} {logger_name} {message}')
            beg_sink = SensibleSink(beg_formatter,
                                    out_emitter,
                                    filters=[beg_filter],
                                    on='begin')
            sinks.append(beg_sink)
        super(SensibleLogger, self).__init__(name, sinks)
