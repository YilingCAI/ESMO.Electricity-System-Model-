# -*- coding: utf-8 -*-

# Title: Importing and Exporting CSV Data
# Description: This functions includes getting the demand data

from __future__ import print_function, division, absolute_import

import pandas as pd
import os
import sys
import logging

logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s")

file_handler = logging.FileHandler('log/io_data.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def get_path(path):
    cwd = str(os.getcwd()).replace('\\', '/')
    path = cwd + path
    return path


class ImportCSV(object):
    def __init__(self, path):
        self.path = get_path(path)

    def read_csv(self, header, index_col, parse_dates, squeeze):
        fn = self.path
        try:
            df = pd.read_csv(fn,
                             parse_dates=parse_dates,
                             header=header,
                             index_col=index_col,
                             squeeze=squeeze)
            if parse_dates == 'True':
                df['Date'] = pd.to_datetime(df.date)
                df = df.set_index('Date')
                df.drop(['date'], axis=1, inplace=True)

        except Exception as ex:
            logger.exception(ex)
            sys.exit(1)

        return df


class ExportCSV(object):
    def __init__(self, path):
        self.path = get_path(path)

    def write_csv(self, df, column, index):
        fn = self.path
        try:
            fn = open(fn, 'w', newline='')
            df.to_csv(fn, columns=column, index=index)

        except Exception as ex:
            logger.exception(ex)
            sys.exit(1)

        return


if __name__ == '__main__':
    pass
