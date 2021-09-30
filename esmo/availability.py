# Title: Availability time series simulation
# Description:

from __future__ import print_function, division, absolute_import

import pandas as pd
import numpy as np
import sys


def availability(REGION_YEAR_TECH_STORAGE_ARR, REGION_YEAR_TECH_GENERATION_ARR,
                 TECH_NUC_LS, AVAIL_GEN_ARR, AVAIL_STOR_ARR):

    df_avail = pd.DataFrame()

    for i in range(len(REGION_YEAR_TECH_GENERATION_ARR)):
        year = REGION_YEAR_TECH_GENERATION_ARR['YEAR'].loc[i]
        region = REGION_YEAR_TECH_GENERATION_ARR['REGION'].loc[i]
        tech = REGION_YEAR_TECH_GENERATION_ARR['TECHNOLOGY'].loc[i]

        df_series = pd.DataFrame()
        print(year)
        print(region)
        print(tech)
        avail_avg = AVAIL_GEN_ARR.loc[
            (AVAIL_GEN_ARR['TECHNOLOGY'] == tech)
            & (AVAIL_GEN_ARR['YEAR'] == year)].AvailAvg.iat[0]
        avail_std = AVAIL_GEN_ARR.loc[
            (AVAIL_GEN_ARR['TECHNOLOGY'] == tech)
            & (AVAIL_GEN_ARR['YEAR'] == year)].AvailSTD.iat[0]

        avail_avg = float(avail_avg)
        avail_std = float(avail_std)

        if tech in TECH_NUC_LS:
            if region != 1:
                avail_avg = 0.85  # except for France

            df = nuclear_availability(avail_avg, avail_std)
            df = df.round(3)

        else:

            df = other_availability(avail_avg, avail_std)
            df = df.round(3)

        df_series['TIMESLICE'] = pd.Series(range(1, 8761)).astype(int)
        df_series['value'] = df
        df_series['TECHNOLOGY'] = tech
        df_series['REGION_ID'] = region
        df_series['YEAR'] = year

        df_avail = df_avail.append(df_series, True)

    for i in range(len(REGION_YEAR_TECH_STORAGE_ARR)):
        year = REGION_YEAR_TECH_STORAGE_ARR['YEAR'].loc[i]
        region = REGION_YEAR_TECH_STORAGE_ARR['REGION'].loc[i]
        tech = REGION_YEAR_TECH_STORAGE_ARR['TECHNOLOGY'].loc[i]

        df_series = pd.DataFrame()

        avail_avg = AVAIL_STOR_ARR.loc[
            (AVAIL_STOR_ARR['TECHNOLOGY'] == tech)
            & (AVAIL_STOR_ARR['YEAR'] == year)].AvailAvg.iat[0]
        avail_std = AVAIL_STOR_ARR.loc[
            (AVAIL_STOR_ARR['TECHNOLOGY'] == tech)
            & (AVAIL_STOR_ARR['YEAR'] == year)].AvailSTD.iat[0]
        avail_avg = float(avail_avg)
        avail_std = float(avail_std)

        df = other_availability(avail_avg, avail_std)
        df = df.round(3)

        df_series['TIMESLICE'] = pd.Series(range(1, 8761)).astype(int)
        df_series['value'] = df
        df_series['TECHNOLOGY'] = tech
        df_series['REGION_ID'] = region
        df_series['YEAR'] = year

        df_avail = df_avail.append(df_series, True)

    df_avail = df_avail[[
        'REGION_ID', 'YEAR', 'TECHNOLOGY', 'TIMESLICE', 'value'
    ]]

    return df_avail


def nuclear_availability(avail_avg, avail_std):

    df = pd.DataFrame()
    timeseries = pd.Series(range(1, 8761)).astype(int)
    df = avail_avg + avail_std * np.cos(timeseries * 3.14159 * 2 / 8760)

    return df


def other_availability(avail_avg, avail_std):

    df = pd.DataFrame()
    timeseries = pd.Series(np.array([avail_avg] * 8760))
    df = timeseries

    return df


if __name__ == '__main__':
    pass
