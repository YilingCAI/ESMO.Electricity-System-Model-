from __future__ import print_function, division, absolute_import

import pandas as pd


def capacity_factor(REGION_YEAR_TECH_GENERATION_ARR, TECH_VRES_LS):

    df_cf = pd.DataFrame()

    for i in range(len(REGION_YEAR_TECH_GENERATION_ARR)):
        year = REGION_YEAR_TECH_GENERATION_ARR['YEAR'].loc[i]
        region = REGION_YEAR_TECH_GENERATION_ARR['REGION'].loc[i]
        tech = REGION_YEAR_TECH_GENERATION_ARR['TECHNOLOGY'].loc[i]

        df_series = pd.DataFrame()

        if tech in TECH_VRES_LS:

            df_series['TIMESLICE'] = pd.Series(range(1, 8761)).astype(int)
            df_series['TECHNOLOGY'] = tech
            df_series['REGION_ID'] = region
            df_series['YEAR'] = year
            df_series['VALUE'] = 0

            df_cf = df_cf.append(df_series, True)

    df_cf = df_cf[[
        'REGION_ID', 'YEAR', 'TECHNOLOGY', 'TIMESLICE', 'VALUE'
    ]]

    return df_cf


if __name__ == '__main__':
    pass
