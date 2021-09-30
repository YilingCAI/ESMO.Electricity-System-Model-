from __future__ import print_function, division, absolute_import

import sys
import logging

from .availability import availability
from .capacity_factor import capacity_factor
from .mustrun import must_run
from .io_data import ImportCSV, ExportCSV

logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s")

file_handler = logging.FileHandler('log/pre_generation.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def pre_generation_avail(sce_name):
    logger.debug('Pre_generation_avail starts!')

    # calculate power plant availability time series
    try:

        # data reading

        pathset = '/input_data/' + sce_name + '/set/'
        pathpar = '/input_data/' + sce_name + '/parameter/'
        TECH_NUC_ARR = ImportCSV(pathset + 'TECH_NUC.csv').read_csv(
            header=0, index_col=False, parse_dates=False, squeeze=True)
        REGION_YEAR_TECH_GENERATION_ARR = ImportCSV(
            pathset + 'REGION_YEAR_TECH_GENERATION.csv').read_csv(
                header=0, index_col=False, parse_dates=False, squeeze=True)
        REGION_YEAR_TECH_STORAGE_ARR = ImportCSV(
            pathset + 'REGION_YEAR_TECH_STORAGE.csv').read_csv(
                header=0, index_col=False, parse_dates=False, squeeze=True)
        AVAIL_GEN_ARR = ImportCSV(pathpar +
                                  'generation_parameter.csv').read_csv(
                                      header=0,
                                      index_col=False,
                                      parse_dates=False,
                                      squeeze=True)
        AVAIL_STOR_ARR = ImportCSV(pathpar + 'storage_parameter.csv').read_csv(
            header=0, index_col=False, parse_dates=False, squeeze=True)  
        TECH_NUC_LS = TECH_NUC_ARR.tolist()
        df_avail = availability(REGION_YEAR_TECH_STORAGE_ARR,
                                REGION_YEAR_TECH_GENERATION_ARR, 
                                TECH_NUC_LS, AVAIL_GEN_ARR, AVAIL_STOR_ARR)
        column = list(df_avail.columns)
        ExportCSV(pathpar + 'availability.csv').write_csv(df_avail,
                                                          column=column,
                                                          index=False)

    except Exception as ex:
        logger.exception(ex)
        sys.exit(1)

    logger.debug('Pre_generation_avail ends!')

    return


def pre_generation_cf(sce_name):
    logger.debug('Pre_generation_cf starts!')

    # generate capacity factor time series
    try:

        # data reading
        pathset = '/input_data/' + sce_name + '/set/'
        pathpar = '/input_data/' + sce_name + '/parameter/'

        REGION_YEAR_TECH_GENERATION_ARR = ImportCSV(
            pathset + 'REGION_YEAR_TECH_GENERATION.csv').read_csv(
                header=0, index_col=False, parse_dates=False, squeeze=True)

        TECH_VRES_ARR = ImportCSV(pathset + 'TECH_VRES.csv').read_csv(
            header=0, index_col=False, parse_dates=False, squeeze=True)

        TECH_VRES_LS = TECH_VRES_ARR.tolist()

        df_cf = capacity_factor(REGION_YEAR_TECH_GENERATION_ARR, TECH_VRES_LS)

        column = list(df_cf.columns)

        ExportCSV(pathpar + 'capacity_factor.csv').write_csv(df_cf,
                                                             column=column,
                                                             index=False)

    except Exception as ex:
        logger.exception(ex)
        sys.exit(1)

    logger.debug('Pre_generation_cf ends!')

    return


def pre_generation_mustrun(sce_name):
    logger.debug('Pre_generation_mustrun starts!')

    # calculate heat demand profile time series (0,1)
    try:

        pathset = '/input_data/' + sce_name + '/set/'
        pathpar = '/input_data/' + sce_name + '/parameter/'

        REGION_YEAR_TECH_GENERATION_ARR = ImportCSV(
            pathset + 'REGION_YEAR_TECH_GENERATION.csv').read_csv(
                header=0, index_col=False, parse_dates=False, squeeze=True)

        TECH_MUSTRUN_ARR = ImportCSV(pathset + 'TECH_MUSTRUN.csv').read_csv(
            header=0, index_col=False, parse_dates=False, squeeze=True)

        AVAIL_GEN_ARR = ImportCSV(pathpar +
                                  'generation_parameter.csv').read_csv(
                                      header=0,
                                      index_col=False,
                                      parse_dates=False,
                                      squeeze=True)

        TECH_MUSTRUN_LS = TECH_MUSTRUN_ARR.tolist()

        df_hd = must_run(REGION_YEAR_TECH_GENERATION_ARR, TECH_MUSTRUN_LS,
                         AVAIL_GEN_ARR)

        column = list(df_hd.columns)

        ExportCSV(pathpar + 'mustrun.csv').write_csv(df_hd,
                                                     column=column,
                                                     index=False)

    except Exception as ex:
        logger.exception(ex)
        sys.exit(1)

    logger.debug('Pre_generation_mustrun ends!')


if __name__ == "__main__":
    pass
