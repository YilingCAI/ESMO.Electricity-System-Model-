from __future__ import print_function, division, absolute_import

import pandas as pd


def must_run(REGION_YEAR_TECH_GENERATION_ARR, TECH_MUSTRUN_LS, AVAIL_GEN_ARR):

    df_hd = pd.DataFrame(columns = ['REGION_ID', 'YEAR', 'TECHNOLOGY', 'TIMESLICE', 'VALUE'])

    for i in range(len(REGION_YEAR_TECH_GENERATION_ARR)):
        year = REGION_YEAR_TECH_GENERATION_ARR['YEAR'].loc[i]
        region = REGION_YEAR_TECH_GENERATION_ARR['REGION'].loc[i]
        tech = REGION_YEAR_TECH_GENERATION_ARR['TECHNOLOGY'].loc[i]

        df_series = pd.DataFrame()

        if tech in TECH_MUSTRUN_LS:

            mustrun_winter = AVAIL_GEN_ARR.loc[
                (AVAIL_GEN_ARR['TECHNOLOGY'] == tech)
                & (AVAIL_GEN_ARR['YEAR'] == year)].MustRunWinter.iat[0]
            mustrun_summer = AVAIL_GEN_ARR.loc[
                (AVAIL_GEN_ARR['TECHNOLOGY'] == tech)
                & (AVAIL_GEN_ARR['YEAR'] == year)].MustRunSummer.iat[0]
            mustrun_winter = float(mustrun_winter)
            mustrun_summer = float(mustrun_summer)

            df_series['TIMESLICE'] = pd.Series(range(1, 8761)).astype(int)
            df_series['TECHNOLOGY'] = tech
            df_series['REGION_ID'] = region
            df_series['YEAR'] = year

            df_series['VALUE'] = df_series['TIMESLICE'].apply(
                lambda x: mustrun_winter if x < 2161 else mustrun_summer
                if 2160 < x < 7296 else mustrun_winter)

            df_hd = df_hd.append(df_series, True)
    

    return df_hd


if __name__ == '__main__':
    pass
