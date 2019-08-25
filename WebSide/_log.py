#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/21 14:44
#!@File     : .py


import sys
import logging
import time
import os
import struct#import fcntl

from logging.handlers import TimedRotatingFileHandler


class MultiProcessTimedRotatingFileHandler(TimedRotatingFileHandler):

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        # if self.stream:
        #    self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        # if os.path.exists(dfn):
        #    os.remove(dfn)
        #lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, 0, 0, 0, 0, 0)
        #fcntl.fcntl(self.stream, fcntl.F_SETLKW, lockdata)
        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
            with open(self.baseFilename, 'a'):
                pass
        if self.backupCount > 0:
            # find the oldest log file and delete it
            # s = glob.glob(self.baseFilename + ".20*")
            # if len(s) > self.backupCount:
            #    s.sort()
            #    os.remove(s[0])
            for s in self.getFilesToDelete():
                os.remove(s)
        # print "%s -> %s" % (self.baseFilename, dfn)
        if self.stream:
            self.stream.close()
        self.mode = 'a'
        self.stream = self._open()
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstNow = time.localtime(currentTime)[-1]
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    newRolloverAt = newRolloverAt - 3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    newRolloverAt = newRolloverAt + 3600
        self.rolloverAt = newRolloverAt


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


def init_log(log_path, tags):
    # from tornado.options import options
    logger = logging.getLogger()
    for i in logger.handlers:
        logger.removeHandler(i)
        # i.setLevel(logging.INFO)

    hdlr = MultiProcessTimedRotatingFileHandler(log_path, 'midnight', 1, 0)
    # hdlr = logging.handlers.TimedRotatingFileHandler(log_path, 'midnight', 1, 0)

    header_fmt = '[%s]' % (tags) + '%(asctime)s %(message)s'
    # header_fmt = '%(asctime)s %(filename)s[%(lineno)d] %(message)s'
    # datafmt = '%Y-%m-%d %H:%M:%S'
    # formatter = logging.Formatter(header_fmt, datafmt)
    formatter = logging.Formatter(header_fmt)
    hdlr.setFormatter(formatter)
    hdlr.suffix = '_%Y%m%d'
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    # logger.datefmt = '%a, %d %b %Y %H:%M:%S'

    direct_logger = StreamToLogger(logger, logging.INFO)
    sys.stdout = direct_logger
    sys.stderr = direct_logger

    # logging.getLogger("tornado.access").addHandler(hdlr)
    # logging.getLogger("tornado.access").propagate = False
    # logging.getLogger("tornado.access").disabled = True





