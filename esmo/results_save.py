# Title: Optimization result saving
# Description: This incldes hourly dispatch/import&export/hydro level/cost/detailed information related to the model variable.

from __future__ import print_function, division, absolute_import

import os
import pandas as pd
import logging
from pyomo.environ import *
from pyomo.core import *
from pyomo.core import Constraint
from pyomo.core.expr.numeric_expr import *

logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s")

file_handler = logging.FileHandler('log/results_save.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

sce = []
annualcost = []
capex = []
inv_gen = []
inv_stor = []
inv_grid = []
opexfix = []
fix_gen = []
fix_stor = []
fix_grid = []
opexvar = []
var_gen = []
var_stor = []
var_startup = []
var_co2 = []
var_exchange = []
nuc = []
pv_large = []
pv_small = []
CCGT_new = []
OCGT_new = []
onshore = []
offshore = []
ires = []
hydro_ror = []
hydro_dam = []
phs_power = []
phs_energy = []
battery1_power = []
battery1_energy = []
battery4_power = []
battery4_energy = []
battery8_power = []
battery8_energy = []
ptg_power = []
importtranscapacity = []
exporttranscapacity = []
nucpro = []
pvlargepro = []
pvsmallpro = []
onshorepro = []
offshorepro = []
gasccgtpro = []
gasocgtpro = []
hydro_rorpro = []
hydro_dampro = []
phs_char = []
phs_disc = []
battery1_char = []
battery1_disc = []
battery4_char = []
battery4_disc = []
battery8_char = []
battery8_disc = []
ptg_char = []
ptg_disc = []
excess = []
exchange = []
demand = []
nucper = []
resper = []
fossilper = []
emission = []
totalemission = []
shadowprice = []


def detail_save_results_no_uc(instance, sce_name, outputpath):

    dirName = outputpath + sce_name

    cobject = getattr(instance, 'ElecBalanceConstraint')

    # Create target directory if it doesn't exist
    if not os.path.exists(dirName):
        os.mkdir(dirName)

    save_path = dirName + '/cost.csv'

    with open(save_path, 'w') as f:
        # f.write('Total system discounted cost:\n')

        f.write(
            '\nTotal regional discounted cost(bneuro) all studied period:\n')
        f.write('region,type,value\n')
        for r in instance.REGION_ID:
            exchangecost = 0
            for (y, ny) in instance.YEARPERIOD:
                for i in range(0, ny):
                    exchangecost = exchangecost + (1 + instance.SDR)**(
                        instance.REFYEAR - y - i) * sum(
                            ExchangeHourlyCostFunction(instance, r, y))

            f.write('%s,%s,%s\n' %
                    (r, 'total',
                     (instance.regionalcost[r].value + exchangecost) / 1e9))
            f.write('%s,%s,%s\n' %
                    (r, 'inv', instance.regionalcostinv[r].value / 1e9))
            f.write('%s,%s,%s\n' %
                    (r, 'fix', instance.regionalcostfix[r].value / 1e9))
            f.write('%s,%s,%s\n' %
                    (r, 'var', instance.regionalcostvar[r].value / 1e9))
            f.write('%s,%s,%s\n' %
                    (r, 'co2', instance.regionalcostco2[r].value / 1e9))
            f.write('%s,%s,%s\n' % (r, 'exchange', exchangecost / 1e9))

        f.write('\nRegional year non-discounted cost(bneuro):\n')
        f.write('region,year,type,value\n')

        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'average_shadow_price(euro/MWh)',
                         sum(instance.dual[cobject[r, y, h]]
                             for h in instance.TIMESLICE) / 8760))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'year',
                     (instance.regionalyearcost[r, y].value +
                      sum(ExchangeHourlyCostFunction(instance, r, y))) / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'investment (bneuro)',
                         instance.regionalyearcostinv[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'inv-gen (bneuro)',
                         instance.regionalyearcostinvgen[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'inv-stor (bneuro)',
                         instance.regionalyearcostinvstor[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'inv-grid (bneuro)',
                         instance.regionalyearcostinvgrid[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'opexfix (bneuro)',
                         instance.regionalyearcostfix[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'fix-gen (bneuro)',
                         instance.regionalyearcostfixgen[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'fix-stor (bneuro)',
                         instance.regionalyearcostfixstor[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'fix-grid (bneuro)',
                         instance.regionalyearcostfixgrid[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'opexvar (bneuro)',
                         instance.regionalyearcostvar[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'var-gen (bneuro)',
                         instance.regionalyearcostvargen[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'var-stor (bneuro)',
                         instance.regionalyearcostvarstor[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'var-loadshedding (bneuro)',
                         instance.regionalyearcostvarloadshedding[r, y].value /
                         1e9))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'var-startup (bneuro)',
                     instance.regionalyearcostvarstartup[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'var-co2 (bneuro)',
                         instance.regionalyearcostco2[r, y].value / 1e9))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'var-exchange (bneuro)',
                     sum(ExchangeHourlyCostFunction(instance, r, y)) / 1e9))

        f.write('\nRegional year cost per technology:\n')
        f.write('region,year,technology,type,value\n')
        for r, y, d in instance.REGION_YEAR_TECH_GENERATION:
            f.write('%s,%s,%s,%s,%s\n' %
                    (r, y, d, 'gen-inv (bneuro)',
                     instance.regionalyearcostinvgentech[r, y, d].value / 1e9))
            f.write('%s,%s,%s,%s,%s\n' %
                    (r, y, d, 'gen-fix (bneuro)',
                     instance.regionalyearcostfixgentech[r, y, d].value / 1e9))
            f.write('%s,%s,%s,%s,%s\n' %
                    (r, y, d, 'gen-var (bneuro)',
                     instance.regionalyearcostvargentech[r, y, d].value / 1e9))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            f.write(
                '%s,%s,%s,%s,%s\n' %
                (r, y, tt, 'stor-inv (bneuro)',
                 instance.regionalyearcostinvstortech[r, y, tt].value / 1e9))
            f.write(
                '%s,%s,%s,%s,%s\n' %
                (r, y, tt, 'stor-fix (bneuro)',
                 instance.regionalyearcostfixstortech[r, y, tt].value / 1e9))
            f.write(
                '%s,%s,%s,%s,%s\n' %
                (r, y, tt, 'stor-var (bneuro)',
                 instance.regionalyearcostvarstortech[r, y, tt].value / 1e9))
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                for l in instance.LINE:
                    f.write(
                        '%s,%s,%s,%s,%s\n' %
                        (r, y, l, 'grid-inv (bneuro)',
                         instance.regionalyearcostinvgridline[r, y, l].value /
                         1e9))
                    f.write(
                        '%s,%s,%s,%s,%s\n' %
                        (r, y, l, 'grid-fix (bneuro)',
                         instance.regionalyearcostfixgridline[r, y, l].value /
                         1e9))

    save_path1 = dirName + "/detail.csv"
    with open(save_path1, 'w') as f:
        f.write('Production composition:\n')
        f.write('region,year,type,value\n')
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'RES%',
                         round(
                             1 - instance.annualelecnucgen[r, y].value /
                             instance.annualelecgen[r, y].value -
                             instance.annualelecfossilgen[r, y].value /
                             instance.annualelecgen[r, y].value, 3)))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'NUC%',
                         round(
                             instance.annualelecnucgen[r, y].value /
                             instance.annualelecgen[r, y].value, 3)))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'FOSSIL%',
                         round(
                             instance.annualelecfossilgen[r, y].value /
                             instance.annualelecgen[r, y].value, 3)))

        f.write('\nNew installed capacity (GW):\n')
        f.write('region,year,technology,value\n')
        for r, y, t in instance.REGION_YEAR_TECH_GENERATION:
            f.write('%s,%s,%s,%s\n' %
                    (r, y, t,
                     instance.newinstalledgencapacity[r, y, t].value / 1000))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            f.write('%s,%s,%s,%s\n' %
                    (r, y, tt + '_power',
                     instance.newinstalledstorpower[r, y, tt].value / 1000))
            f.write('%s,%s,%s,%s\n' %
                    (r, y, tt + '_energy',
                     instance.newinstalledstorenergy[r, y, tt].value / 1000))

        f.write('\nAccumulated new installed capacity (GW):\n')
        f.write('region,year,technology,value\n')
        for r, y, t in instance.REGION_YEAR_TECH_GENERATION:
            f.write(
                '%s,%s,%s,%s\n' %
                (r, y, t,
                 instance.accunewinstalledgencapacity[r, y, t].value / 1000))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            f.write(
                '%s,%s,%s,%s\n' %
                (r, y, tt + '_power',
                 instance.accunewinstalledstorpower[r, y, tt].value / 1000))
            f.write(
                '%s,%s,%s,%s\n' %
                (r, y, tt + '_energy',
                 instance.accunewinstalledstorenergy[r, y, tt].value / 1000))

        f.write('\nTotal installed capacity (GW):\n')
        f.write('region,year,technology,value\n')
        for r, y, t in instance.REGION_YEAR_TECH_GENERATION:
            f.write('%s,%s,%s,%s\n' %
                    (r, y, t,
                     instance.totalinstalledgencapacity[r, y, t].value / 1000))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            f.write('%s,%s,%s,%s\n' %
                    (r, y, tt + '_power',
                     instance.totalinstalledstorpower[r, y, tt].value / 1000))
            f.write('%s,%s,%s,%s\n' %
                    (r, y, tt + '_energy (GWh)',
                     instance.totalinstalledstorenergy[r, y, tt].value / 1000))

        f.write('\nNew installed transmission capacity (GW):\n')
        f.write('line,year,value\n')
        for l in instance.LINE:
            for y in instance.YEAR:
                f.write(
                    '%s,%s,%s\n' %
                    (l, y, instance.newinstalledimporttranscapacity[l, y].value
                     / 1000))
                f.write(
                    '%s,%s,%s\n' %
                    (l, y, instance.newinstalledexporttranscapacity[l, y].value
                     / 1000))

        f.write('\nAccumulated new installed transmission capacity (GW):\n')
        f.write('line,year,value\n')
        for l in instance.LINE:
            for y in instance.YEAR:
                f.write(
                    '%s,%s,%s\n' %
                    (l, y, instance.newinstalledimporttranscapacity[l, y].value
                     / 1000))
                f.write(
                    '%s,%s,%s\n' %
                    (l, y, instance.newinstalledexporttranscapacity[l, y].value
                     / 1000))

        f.write('\nTotal installed transmission capacity (GW):\n')
        f.write('line,year,value\n')
        for l in instance.LINE:
            for y in instance.YEAR:
                f.write(
                    '%s,%s,%s\n' %
                    (l, y,
                     instance.totalinstalledimporttranscapacity[l, y].value /
                     1000))
                f.write(
                    '%s,%s,%s\n' %
                    (l, y,
                     instance.totalinstalledexporttranscapacity[l, y].value /
                     1000))

        f.write('\nAnnual demand (TWh):\n')
        f.write('region,year,value\n')
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s,%s,%s\n' %
                        (r, y, round(instance.annualdemand[r, y].value / 1e6)))

        f.write('\nAnnual production (TWh):\n')
        f.write('region,year,technology,value\n')
        for r, y, d in instance.REGION_YEAR_TECH_GENERATION:
            f.write(
                '%s,%s,%s,%s\n' %
                (r, y, d,
                 round(instance.annualelectechgen[r, y, d].value / 1e6, 2)))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            if tt in instance.TECH_DSM:
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, tt + '_delayed',
                     round(instance.annualelectechchar[r, y, tt].value / 1e6,
                           2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, tt + '_served',
                     round(-instance.annualelectechdisc[r, y, tt].value / 1e6,
                           2)))
            else:
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, tt + '_char',
                     round(-instance.annualelectechchar[r, y, tt].value / 1e6,
                           2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, tt + '_disc',
                     round(instance.annualelectechdisc[r, y, tt].value / 1e6,
                           2)))
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'exchange',
                     round(instance.annualelecexchange[r, y].value / 1e6, 2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'excess',
                     round(-instance.annualelecexcess[r, y].value / 1e6, 2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'load_shedding',
                     round(instance.annualelecloadshedding[r, y].value / 1e6,
                           2)))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'naturalgas',
                         round(instance.annualelecnaturalgas[r, y].value / 1e6,
                               2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'flex_biogas',
                     round(instance.annualelecbiogas[r, y].value / 1e6, 2)))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'gtp',
                         round(instance.annualelecgtp[r, y].value / 1e6, 2)))

        f.write('\nAnnual emissions (MT CO2eq):\n')
        f.write('REGION_ID,YEAR, value\n')
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s, %s, %s\n' %
                        (r, y,
                         round(instance.annualemission[r, y].value / 1e9, 2)))

        f.write('\nEmissions per kwh (gCO2eq/kWh):\n')
        f.write('REGION_ID,YEAR, value\n')
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s, %s, %s\n' %
                        (r, y,
                         round(
                             instance.annualemission[r, y].value /
                             instance.annualdemand[r, y].value, 2)))

    for r in instance.REGION_ID:
        for y in instance.YEAR:
            save_path = dirName + '/' + str(r) + '_' + str(
                y) + '_' + 'production1_MW.csv'
            save_path1 = dirName + '/' + str(r) + '_' + str(
                y) + '_' + 'production_MW.csv'
            with open(save_path, 'w') as f:
                f.write('hour,technology,value\n')
                for h in instance.TIMESLICE:
                    for d in instance.TECH_GENERATION:
                        if [r, y, d] in instance.REGION_YEAR_TECH_GENERATION:
                            f.write('%s,%s,%s\n' %
                                    (h, d,
                                     round(instance.electechgen[r, y, d,
                                                                h].value)))
                    for d in instance.TECH_GAS:
                        if [r, y, d] in instance.REGION_YEAR_TECH_GAS:
                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_naturalgas',
                                 round(instance.electechnaturalgas[r, y, d,
                                                                   h].value)))
                            f.write('%s,%s,%s\n' %
                                    (h, d + '_biogas',
                                     round(instance.electechbiogas[r, y, d,
                                                                   h].value *
                                           instance.GenFullLoadEffi[y, d])))
                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_gtp',
                                 round(instance.electechgtp[r, y, d, h].value *
                                       instance.GenFullLoadEffi[y, d])))

                    for tt in instance.TECH_STORAGE:
                        if [r, y, tt] in instance.REGION_YEAR_TECH_STORAGE:
                            if tt in instance.TECH_DSM:
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_delayed',
                                     round(instance.electechchar[r, y, tt,
                                                                 h].value)))
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_served',
                                     round(-instance.electechdisc[r, y, tt,
                                                                  h].value)))
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_delayed_stored',
                                     round(instance.electechstored[r, y, tt,
                                                                   h].value)))
                            else:
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_char',
                                     round(-instance.electechchar[r, y, tt,
                                                                  h].value)))
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_disc',
                                     round(instance.electechdisc[r, y, tt,
                                                                 h].value)))
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_stored',
                                     round(instance.electechstored[r, y, tt,
                                                                   h].value)))

                    f.write('%s,%s,%s\n' %
                            (h, 'demand', round(instance.Demand[r, y, h])))
                    f.write(
                        '%s,%s,%s\n' %
                        (h, 'shadow_price', instance.dual[cobject[r, y, h]]))
                    f.write('%s,%s,%s\n' %
                            (h, 'exchange',
                             round(instance.elecexchange[r, y, h].value)))
                    f.write('%s,%s,%s\n' %
                            (h, 'excess',
                             round(-instance.elecexcess[r, y, h].value)))
                    f.write('%s,%s,%s\n' %
                            (h, 'load_shedding',
                             round(instance.elecloadshedding[r, y, h].value)))

                f.close()

                open(save_path1, 'w')
                pd.read_csv(save_path).pivot(index='hour',
                                             columns='technology',
                                             values='value').to_csv(save_path1)
                os.remove(save_path)

    for y in instance.YEAR:
        save_path = dirName + '/' + str(y) + '_' + 'transmission1_MW.csv'
        save_path1 = dirName + '/' + str(y) + '_' + 'transmission_MW.csv'
        with open(save_path, 'w') as f:
            f.write('hour,line,value\n')
            for h in instance.TIMESLICE:
                for l in instance.LINE:
                    f.write(
                        '%s,%s,%s\n' %
                        (h, l, round(instance.eleclexchange[l, y, h].value)))
            f.close()

            open(save_path1, 'w')
            pd.read_csv(save_path).pivot(index='hour',
                                         columns='line',
                                         values='value').to_csv(save_path1)
            os.remove(save_path)

    save_path = dirName + '/' + 'HydroDamWeekIniLevel.csv'
    with open(save_path, 'w') as f:
        f.write('region,year,week,tech,storage-level,weekprod(MWh)\n')
        for w in instance.WEEK:
            for r, y, t in instance.REGION_YEAR_TECH_HD:
                f.write(
                    '%s,%s,%s,%s,%s,%s\n' %
                    (r, y, w, t,
                     round(instance.elechdweekinilevel[r, y, t, w].value, 3),
                     round(instance.elechdweekprod[r, y, t, w].value)))

    return


def detail_save_results_uc(instance, sce_name, outputpath):

    dirName = outputpath + sce_name

    cobject = getattr(instance, 'ElecBalanceConstraint')

    # Create target directory if it doesn't exist
    if not os.path.exists(dirName):
        os.mkdir(dirName)

    save_path = dirName + '/cost.csv'

    with open(save_path, 'w') as f:
        # f.write('Total system discounted cost:\n')

        f.write(
            '\nTotal regional discounted cost(bneuro) all studied period:\n')
        f.write('region,type,value\n')
        for r in instance.REGION_ID:
            exchangecost = 0
            for (y, ny) in instance.YEARPERIOD:
                for i in range(0, ny - 1):
                    exchangecost = exchangecost + (1 + instance.SDR)**(
                        instance.REFYEAR - y - i) * sum(
                            ExchangeHourlyCostFunction(instance, r, y))

            f.write('%s,%s,%s\n' %
                    (r, 'total',
                     (instance.regionalcost[r].value + exchangecost) / 1e9))
            f.write('%s,%s,%s\n' %
                    (r, 'inv', instance.regionalcostinv[r].value / 1e9))
            f.write('%s,%s,%s\n' %
                    (r, 'fix', instance.regionalcostfix[r].value / 1e9))
            f.write('%s,%s,%s\n' %
                    (r, 'var', instance.regionalcostvar[r].value / 1e9))
            f.write('%s,%s,%s\n' %
                    (r, 'co2', instance.regionalcostco2[r].value / 1e9))
            f.write('%s,%s,%s\n' % (r, 'exchange', exchangecost / 1e9))

        f.write('\nRegional year non-discounted cost(bneuro):\n')
        f.write('region,year,type,value\n')

        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'average_shadow_price(euro/MWh)',
                         sum(instance.dual[cobject[r, y, h]]
                             for h in instance.TIMESLICE) / 8760))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'year',
                     (instance.regionalyearcost[r, y].value +
                      sum(ExchangeHourlyCostFunction(instance, r, y))) / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'investment (bneuro)',
                         instance.regionalyearcostinv[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'inv-gen (bneuro)',
                         instance.regionalyearcostinvgen[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'inv-stor (bneuro)',
                         instance.regionalyearcostinvstor[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'inv-grid (bneuro)',
                         instance.regionalyearcostinvgrid[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'opexfix (bneuro)',
                         instance.regionalyearcostfix[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'fix-gen (bneuro)',
                         instance.regionalyearcostfixgen[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'fix-stor (bneuro)',
                         instance.regionalyearcostfixstor[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'fix-grid (bneuro)',
                         instance.regionalyearcostfixgrid[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'opexvar (bneuro)',
                         instance.regionalyearcostvar[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'var-gen (bneuro)',
                         instance.regionalyearcostvargen[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'var-stor (bneuro)',
                         instance.regionalyearcostvarstor[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'var-loadshedding (bneuro)',
                         instance.regionalyearcostvarloadshedding[r, y].value /
                         1e9))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'var-startup (bneuro)',
                     instance.regionalyearcostvarstartup[r, y].value / 1e9))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'var-co2 (bneuro)',
                         instance.regionalyearcostco2[r, y].value / 1e9))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'var-exchange (bneuro)',
                     sum(ExchangeHourlyCostFunction(instance, r, y)) / 1e9))

        f.write('\nRegional year cost per technology:\n')
        f.write('region,year,technology,type,value\n')
        for r, y, d in instance.REGION_YEAR_TECH_GENERATION:
            f.write('%s,%s,%s,%s,%s\n' %
                    (r, y, d, 'gen-inv (bneuro)',
                     instance.regionalyearcostinvgentech[r, y, d].value / 1e9))
            f.write('%s,%s,%s,%s,%s\n' %
                    (r, y, d, 'gen-fix (bneuro)',
                     instance.regionalyearcostfixgentech[r, y, d].value / 1e9))
            f.write('%s,%s,%s,%s,%s\n' %
                    (r, y, d, 'gen-var (bneuro)',
                     instance.regionalyearcostvargentech[r, y, d].value / 1e9))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            f.write(
                '%s,%s,%s,%s,%s\n' %
                (r, y, tt, 'stor-inv (bneuro)',
                 instance.regionalyearcostinvstortech[r, y, tt].value / 1e9))
            f.write(
                '%s,%s,%s,%s,%s\n' %
                (r, y, tt, 'stor-fix (bneuro)',
                 instance.regionalyearcostfixstortech[r, y, tt].value / 1e9))
            f.write(
                '%s,%s,%s,%s,%s\n' %
                (r, y, tt, 'stor-var (bneuro)',
                 instance.regionalyearcostvarstortech[r, y, tt].value / 1e9))
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                for l in instance.LINE:
                    f.write(
                        '%s,%s,%s,%s,%s\n' %
                        (r, y, l, 'grid-inv (bneuro)',
                         instance.regionalyearcostinvgridline[r, y, l].value /
                         1e9))
                    f.write(
                        '%s,%s,%s,%s,%s\n' %
                        (r, y, l, 'grid-fix (bneuro)',
                         instance.regionalyearcostfixgridline[r, y, l].value /
                         1e9))

    save_path1 = dirName + "/detail.csv"
    with open(save_path1, 'w') as f:
        f.write('Production composition:\n')
        f.write('region,year,type,value\n')
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'RES%',
                         round(
                             1 - instance.annualelecnucgen[r, y].value /
                             instance.annualelecgen[r, y].value -
                             instance.annualelecfossilgen[r, y].value /
                             instance.annualelecgen[r, y].value, 3)))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'NUC%',
                         round(
                             instance.annualelecnucgen[r, y].value /
                             instance.annualelecgen[r, y].value, 3)))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'FOSSIL%',
                         round(
                             instance.annualelecfossilgen[r, y].value /
                             instance.annualelecgen[r, y].value, 3)))

        f.write('\nNew installed capacity (GW):\n')
        f.write('region,year,technology,value\n')
        for r, y, t in instance.REGION_YEAR_TECH_GENERATION:
            f.write('%s,%s,%s,%s\n' %
                    (r, y, t,
                     instance.newinstalledgencapacity[r, y, t].value / 1000))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            f.write('%s,%s,%s,%s\n' %
                    (r, y, tt + '_power',
                     instance.newinstalledstorpower[r, y, tt].value / 1000))
            f.write('%s,%s,%s,%s\n' %
                    (r, y, tt + '_energy',
                     instance.newinstalledstorenergy[r, y, tt].value / 1000))

        f.write('\nAccumulated new installed capacity (GW):\n')
        f.write('region,year,technology,value\n')
        for r, y, t in instance.REGION_YEAR_TECH_GENERATION:
            f.write(
                '%s,%s,%s,%s\n' %
                (r, y, t,
                 instance.accunewinstalledgencapacity[r, y, t].value / 1000))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            f.write(
                '%s,%s,%s,%s\n' %
                (r, y, tt + '_power',
                 instance.accunewinstalledstorpower[r, y, tt].value / 1000))
            f.write(
                '%s,%s,%s,%s\n' %
                (r, y, tt + '_energy',
                 instance.accunewinstalledstorenergy[r, y, tt].value / 1000))

        f.write('\nTotal installed capacity (GW):\n')
        f.write('region,year,technology,value\n')
        for r, y, t in instance.REGION_YEAR_TECH_GENERATION:
            f.write('%s,%s,%s,%s\n' %
                    (r, y, t,
                     instance.totalinstalledgencapacity[r, y, t].value / 1000))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            f.write('%s,%s,%s,%s\n' %
                    (r, y, tt + '_power',
                     instance.totalinstalledstorpower[r, y, tt].value / 1000))
            f.write('%s,%s,%s,%s\n' %
                    (r, y, tt + '_energy (GWh)',
                     instance.totalinstalledstorenergy[r, y, tt].value / 1000))

        f.write('\nNew installed transmission capacity (GW):\n')
        f.write('line,year,value\n')
        for l in instance.LINE:
            for y in instance.YEAR:
                f.write(
                    '%s,%s,%s\n' %
                    (l, y, instance.newinstalledimporttranscapacity[l, y].value
                     / 1000))
                f.write(
                    '%s,%s,%s\n' %
                    (l, y, instance.newinstalledexporttranscapacity[l, y].value
                     / 1000))

        f.write('\nAccumulated new installed transmission capacity (GW):\n')
        f.write('line,year,value\n')
        for l in instance.LINE:
            for y in instance.YEAR:
                f.write(
                    '%s,%s,%s\n' %
                    (l, y, instance.newinstalledimporttranscapacity[l, y].value
                     / 1000))
                f.write(
                    '%s,%s,%s\n' %
                    (l, y, instance.newinstalledexporttranscapacity[l, y].value
                     / 1000))

        f.write('\nTotal installed transmission capacity (GW):\n')
        f.write('line,year,value\n')
        for l in instance.LINE:
            for y in instance.YEAR:
                f.write(
                    '%s,%s,%s\n' %
                    (l, y,
                     instance.totalinstalledimporttranscapacity[l, y].value /
                     1000))
                f.write(
                    '%s,%s,%s\n' %
                    (l, y,
                     instance.totalinstalledexporttranscapacity[l, y].value /
                     1000))

        f.write('\nAnnual demand (TWh):\n')
        f.write('region,year,value\n')
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s,%s,%s\n' %
                        (r, y, round(instance.annualdemand[r, y].value / 1e6)))

        f.write('\nAnnual production (TWh):\n')
        f.write('region,year,technology,value\n')
        for r, y, d in instance.REGION_YEAR_TECH_GENERATION:
            f.write(
                '%s,%s,%s,%s\n' %
                (r, y, d,
                 round(instance.annualelectechgen[r, y, d].value / 1e6, 2)))
        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            if tt in instance.TECH_DSM:
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, tt + '_delayed',
                     round(instance.annualelectechchar[r, y, tt].value / 1e6,
                           2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, tt + '_served',
                     round(-instance.annualelectechdisc[r, y, tt].value / 1e6,
                           2)))
            else:
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, tt + '_char',
                     round(-instance.annualelectechchar[r, y, tt].value / 1e6,
                           2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, tt + '_disc',
                     round(instance.annualelectechdisc[r, y, tt].value / 1e6,
                           2)))
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'exchange',
                     round(instance.annualelecexchange[r, y].value / 1e6, 2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'excess',
                     round(-instance.annualelecexcess[r, y].value / 1e6, 2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'load_shedding',
                     round(instance.annualelecloadshedding[r, y].value / 1e6,
                           2)))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'naturalgas',
                         round(instance.annualelecnaturalgas[r, y].value / 1e6,
                               2)))
                f.write(
                    '%s,%s,%s,%s\n' %
                    (r, y, 'flex_biogas',
                     round(instance.annualelecbiogas[r, y].value / 1e6, 2)))
                f.write('%s,%s,%s,%s\n' %
                        (r, y, 'gtp',
                         round(instance.annualelecgtp[r, y].value / 1e6, 2)))

        f.write('\nAnnual emissions (MT CO2eq):\n')
        f.write('REGION_ID,YEAR, value\n')
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s, %s, %s\n' %
                        (r, y,
                         round(instance.annualemission[r, y].value / 1e9, 2)))

        f.write('\nEmissions per kwh (gCO2eq/kWh):\n')
        f.write('REGION_ID,YEAR, value\n')
        for r in instance.REGION_ID:
            for y in instance.YEAR:
                f.write('%s, %s, %s\n' %
                        (r, y,
                         round(
                             instance.annualemission[r, y].value /
                             instance.annualdemand[r, y].value, 2)))

    for r in instance.REGION_ID:
        for y in instance.YEAR:
            save_path = dirName + '/' + str(r) + '_' + str(
                y) + '_' + 'production1_MW.csv'
            save_path1 = dirName + '/' + str(r) + '_' + str(
                y) + '_' + 'production_MW.csv'
            with open(save_path, 'w') as f:
                f.write('hour,technology,value\n')
                for h in instance.TIMESLICE:
                    for d in instance.TECH_GENERATION:
                        if [r, y, d] in instance.REGION_YEAR_TECH_GENERATION:
                            f.write('%s,%s,%s\n' %
                                    (h, d,
                                     round(instance.electechgen[r, y, d,
                                                                h].value)))

                    for d in instance.TECH_GAS:
                        if [r, y, d] in instance.REGION_YEAR_TECH_GAS:
                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_naturalgas',
                                 round(instance.electechnaturalgas[r, y, d,
                                                                   h].value)))
                            f.write('%s,%s,%s\n' %
                                    (h, d + '_biogas',
                                     round(instance.electechbiogas[r, y, d,
                                                                   h].value *
                                           instance.GenFullLoadEffi[y, d])))
                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_gtp',
                                 round(instance.electechgtp[r, y, d, h].value *
                                       instance.GenFullLoadEffi[y, d])))

                    for d in instance.TECH_UC:
                        if [r, y, d] in instance.REGION_YEAR_TECH_UC_Gen:
                            f.write('%s,%s,%s\n' %
                                    (h, d + '_committed',
                                     round(instance.eleccommitgen[r, y, d,
                                                                  h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_startup',
                                     round(instance.elecstartupgen[r, y, d,
                                                                   h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_shutdown',
                                     round(instance.elecshutdowngen[r, y, d,
                                                                    h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_aFCRUp',
                                 round(instance.aFCRupGen[r, y, d, h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_aFCRDown',
                                     round(instance.aFCRdownGen[r, y, d,
                                                                h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_aFRRup',
                                 round(instance.aFRRupGen[r, y, d, h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_aFRRdown',
                                     round(instance.aFRRdownGen[r, y, d,
                                                                h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_mFRRup',
                                 round(instance.mFRRupGen[r, y, d, h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_mFRRdown',
                                     round(instance.mFRRdownGen[r, y, d,
                                                                h].value)))

                        if [r, y, d] in instance.REGION_YEAR_TECH_UC_Stor:
                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_char_committed',
                                 round(instance.eleccommitstorchar[r, y, d,
                                                                   h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_char_startup',
                                 round(instance.elecstartupstorchar[r, y, d,
                                                                    h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_char_shutdown',
                                 round(
                                     instance.elecshutdownstorchar[r, y, d,
                                                                   h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_aFCRUpChar',
                                     round(instance.aFCRupStorChar[r, y, d,
                                                                   h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_aFCRDownChar',
                                 round(instance.aFCRdownStorChar[r, y, d,
                                                                 h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_aFRRupChar',
                                     round(instance.aFRRupStorChar[r, y, d,
                                                                   h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_aFRRdownChar',
                                 round(instance.aFRRdownStorChar[r, y, d,
                                                                 h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_mFRRupChar',
                                     round(instance.mFRRupStorChar[r, y, d,
                                                                   h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_mFRRdownChar',
                                 round(instance.mFRRdownStorChar[r, y, d,
                                                                 h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_disc_committed',
                                 round(instance.eleccommitstordisc[r, y, d,
                                                                   h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_discstartup',
                                 round(instance.elecstartupstordisc[r, y, d,
                                                                    h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_disc_shutdown',
                                 round(
                                     instance.elecshutdownstordisc[r, y, d,
                                                                   h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_aFCRUpDisc',
                                     round(instance.aFCRupStorDisc[r, y, d,
                                                                   h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_aFCRDownDisc',
                                 round(instance.aFCRdownStorDisc[r, y, d,
                                                                 h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_aFRRupDisc',
                                     round(instance.aFRRupStorDisc[r, y, d,
                                                                   h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_aFRRdownDisc',
                                 round(instance.aFRRdownStorDisc[r, y, d,
                                                                 h].value)))

                            f.write('%s,%s,%s\n' %
                                    (h, d + '_mFRRupDisc',
                                     round(instance.mFRRupStorDisc[r, y, d,
                                                                   h].value)))

                            f.write(
                                '%s,%s,%s\n' %
                                (h, d + '_mFRRdownDisc',
                                 round(instance.mFRRdownStorDisc[r, y, d,
                                                                 h].value)))

                    for tt in instance.TECH_STORAGE:
                        if [r, y, tt] in instance.REGION_YEAR_TECH_STORAGE:
                            if tt in instance.TECH_DSM:
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_delayed',
                                     round(instance.electechchar[r, y, tt,
                                                                 h].value)))
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_served',
                                     round(-instance.electechdisc[r, y, tt,
                                                                  h].value)))
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_delayed_stored',
                                     round(instance.electechstored[r, y, tt,
                                                                   h].value)))
                            else:
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_char',
                                     round(-instance.electechchar[r, y, tt,
                                                                  h].value)))
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_disc',
                                     round(instance.electechdisc[r, y, tt,
                                                                 h].value)))
                                f.write(
                                    '%s,%s,%s\n' %
                                    (h, tt + '_stored',
                                     round(instance.electechstored[r, y, tt,
                                                                   h].value)))

                    f.write('%s,%s,%s\n' %
                            (h, 'demand', round(instance.Demand[r, y, h])))
                    f.write(
                        '%s,%s,%s\n' %
                        (h, 'shadow_price', instance.dual[cobject[r, y, h]]))

                    f.write('%s,%s,%s\n' %
                            (h, 'exchange',
                             round(instance.elecexchange[r, y, h].value)))
                    f.write('%s,%s,%s\n' %
                            (h, 'excess',
                             round(-instance.elecexcess[r, y, h].value)))
                    f.write('%s,%s,%s\n' %
                            (h, 'load_shedding',
                             round(instance.elecloadshedding[r, y, h].value)))
                    f.write(
                        '%s,%s,%s\n' %
                        (h, 'FCR_required', round(instance.FCRRequired[r, y])))
                    f.write('%s,%s,%s\n' %
                            (h, 'aFRRup_required',
                             round(instance.aFRRuprequired[r, y, h].value)))
                    f.write('%s,%s,%s\n' %
                            (h, 'aFRRdown_required',
                             round(instance.aFRRdownrequired[r, y, h].value)))
                    f.write('%s,%s,%s\n' %
                            (h, 'mFRRup_required',
                             round(instance.mFRRuprequired[r, y, h].value)))
                    f.write('%s,%s,%s\n' %
                            (h, 'mFRRdown_required',
                             round(instance.mFRRdownrequired[r, y, h].value)))

                f.close()

                open(save_path1, 'w')
                pd.read_csv(save_path).pivot(index='hour',
                                             columns='technology',
                                             values='value').to_csv(save_path1)
                os.remove(save_path)

    for y in instance.YEAR:
        save_path = dirName + '/' + str(y) + '_' + 'transmission1_MW.csv'
        save_path1 = dirName + '/' + str(y) + '_' + 'transmission_MW.csv'
        with open(save_path, 'w') as f:
            f.write('hour,line,value\n')
            for h in instance.TIMESLICE:
                for l in instance.LINE:
                    f.write(
                        '%s,%s,%s\n' %
                        (h, l, round(instance.eleclexchange[l, y, h].value)))
            f.close()

            open(save_path1, 'w')
            pd.read_csv(save_path).pivot(index='hour',
                                         columns='line',
                                         values='value').to_csv(save_path1)
            os.remove(save_path)

    save_path = dirName + '/' + 'HydroDamWeekIniLevel.csv'
    with open(save_path, 'w') as f:
        f.write('region,year,week,tech,storage-level,weekprod(MWh)\n')
        for w in instance.WEEK:
            for r, y, t in instance.REGION_YEAR_TECH_HD:
                f.write(
                    '%s,%s,%s,%s,%s,%s\n' %
                    (r, y, w, t,
                     round(instance.elechdweekinilevel[r, y, t, w].value, 3),
                     round(instance.elechdweekprod[r, y, t, w].value)))

    return


def whole_result_append(instance, r, y, scenario):
    cobject = getattr(instance, 'ElecBalanceConstraint')
    sce.append(scenario)
    annualcost.append(instance.regionalyearcost[r, y].value +
                      sum(ExchangeHourlyCostFunction(instance, r, y)))
    capex.append(instance.regionalyearcostinv[r, y].value)
    inv_gen.append(instance.regionalyearcostinvgen[r, y].value)
    inv_stor.append(instance.regionalyearcostinvstor[r, y].value)
    inv_grid.append(instance.regionalyearcostinvgrid[r, y].value)
    opexfix.append(instance.regionalyearcostfix[r, y].value)
    fix_gen.append(instance.regionalyearcostfixgen[r, y].value)
    fix_stor.append(instance.regionalyearcostfixstor[r, y].value)
    fix_grid.append(instance.regionalyearcostfixgrid[r, y].value)
    opexvar.append(instance.regionalyearcostvar[r, y].value)
    var_gen.append(instance.regionalyearcostvargen[r, y].value)
    var_stor.append(instance.regionalyearcostvarstor[r, y].value)
    var_startup.append(instance.regionalyearcostvarstartup[r, y].value)
    var_co2.append(instance.regionalyearcostco2[r, y].value)
    var_exchange.append(sum(ExchangeHourlyCostFunction(instance, r, y)))
    nuc.append(instance.totalinstalledgencapacity[r, y, 'Nuclear_new'].value)
    CCGT_new.append(instance.totalinstalledgencapacity[r, y, 'CCGT_new'].value)
    OCGT_new.append(instance.totalinstalledgencapacity[r, y, 'OCGT_new'].value)
    pv_large.append(instance.totalinstalledgencapacity[r, y, 'PV_large'].value)
    pv_small.append(instance.totalinstalledgencapacity[r, y, 'PV_small'].value)
    onshore.append(instance.totalinstalledgencapacity[r, y,
                                                      'Wind_onshore'].value)
    offshore.append(instance.totalinstalledgencapacity[r, y,
                                                       'Wind_offshore'].value)
    ires.append(instance.irescapacity[r, y].value)
    hydro_ror.append(instance.totalinstalledgencapacity[r, y,
                                                        'Hydro_ROR'].value)
    hydro_dam.append(instance.totalinstalledgencapacity[r, y,
                                                        'Hydro_Dam'].value)
    phs_power.append(instance.totalinstalledstorpower[r, y, 'PHS20'].value)
    phs_energy.append(instance.totalinstalledstorenergy[r, y, 'PHS20'].value)
    nucpro.append(instance.annualelectechgen[r, y, 'Nuclear_new'].value)
    pvlargepro.append(instance.annualelectechgen[r, y, 'PV_large'].value)
    pvsmallpro.append(instance.annualelectechgen[r, y, 'PV_small'].value)
    onshorepro.append(instance.annualelectechgen[r, y, 'Wind_onshore'].value)
    offshorepro.append(instance.annualelectechgen[r, y, 'Wind_offshore'].value)
    gasccgtpro.append(instance.annualelectechgen[r, y, 'CCGT_new'].value)
    gasocgtpro.append(instance.annualelectechgen[r, y, 'OCGT_new'].value)
    hydro_rorpro.append(instance.annualelectechgen[r, y, 'Hydro_ROR'].value)
    hydro_dampro.append(instance.annualelectechgen[r, y, 'Hydro_Dam'].value)
    phs_char.append(-instance.annualelectechchar[r, y, 'PHS20'].value)
    phs_disc.append(instance.annualelectechdisc[r, y, 'PHS20'].value)
    exchange.append(instance.annualelecexchange[r, y].value)
    excess.append(-instance.annualelecexcess[r, y].value)
    demand.append(instance.annualdemand[r, y].value)
    nucper.append(
        round(
            instance.annualelecnucgen[r, y].value /
            instance.annualelecgen[r, y].value, 3))
    resper.append(
        round(
            1 - instance.annualelecnucgen[r, y].value /
            instance.annualelecgen[r, y].value -
            instance.annualelecfossilgen[r, y].value /
            instance.annualelecgen[r, y].value, 3))
    fossilper.append(
        round(
            instance.annualelecfossilgen[r, y].value /
            instance.annualelecgen[r, y].value, 3))
    emission.append(instance.annualemission[r, y].value)
    totalemission.append(
        sum(instance.annualemission[rr, y].value for rr in instance.REGION_ID))
    shadowprice.append(
        sum(instance.dual[cobject[r, y, h]]
            for h in instance.TIMESLICE) / 8760)

    importtranscapacity.append(0)
    exporttranscapacity.append(0)

    battery1_power.append(0)
    battery1_energy.append(0)
    battery4_power.append(0)
    battery4_energy.append(0)
    battery8_power.append(0)
    battery8_energy.append(0)
    battery1_char.append(0)
    battery1_disc.append(0)
    battery4_char.append(0)
    battery4_disc.append(0)
    battery8_char.append(0)
    battery8_disc.append(0)

    ptg_power.append(0)
    ptg_char.append(0)
    ptg_disc.append(0)

    return


def whole_result_save(sce_name):
    df = pd.DataFrame(
        data={
            "sce": sce,
            "annualcost(bn)": [round(x / 1e9, 2) for x in annualcost],
            "capex": [round(x / 1e9, 2) for x in capex],
            "inv_gen": [round(x / 1e9, 2) for x in inv_gen],
            "inv_stor": [round(x / 1e9, 2) for x in inv_stor],
            "inv_grid": [round(x / 1e9, 2) for x in inv_grid],
            "opexfix": [round(x / 1e9, 2) for x in opexfix],
            "fix_gen": [round(x / 1e9, 2) for x in fix_gen],
            "fix_stor": [round(x / 1e9, 2) for x in fix_stor],
            "fix_grid": [round(x / 1e9, 2) for x in fix_grid],
            "opexvar": [round(x / 1e9, 2) for x in opexvar],
            "var_gen": [round(x / 1e9, 2) for x in var_gen],
            "var_stor": [round(x / 1e9, 2) for x in var_stor],
            "var_startup": [round(x / 1e9, 2) for x in var_startup],
            "var_co2": [round(x / 1e9, 2) for x in var_co2],
            "var_exchange": [round(x / 1e9, 2) for x in var_exchange],
            "nuc(GW)": [round(x / 1000, 1) for x in nuc],
            "CCGT_new(GW)": [round(x / 1000, 1) for x in CCGT_new],
            "OCGT_new(GW)": [round(x / 1000, 1) for x in OCGT_new],
            "pv_large(GW)": [round(x / 1000, 1) for x in pv_large],
            "pv_small(GW)": [round(x / 1000, 1) for x in pv_small],
            "onshore(GW)": [round(x / 1000, 1) for x in onshore],
            "offshore(GW)": [round(x / 1000, 1) for x in offshore],
            "ires(GW)": [round(x / 1000, 1) for x in ires],
            "hydro_ror(GW)": [round(x / 1000, 1) for x in hydro_ror],
            "hydro_dam(GW)": [round(x / 1000, 1) for x in hydro_dam],
            "phs_power(GW)": [round(x / 1000, 1) for x in phs_power],
            "phs_energy(GWh)": [round(x / 1000, 1) for x in phs_energy],
            "ptg_power(GW)": [round(x / 1000, 1) for x in ptg_power],
            "battery1_power(GW)": [round(x / 1000, 1) for x in battery1_power],
            "battery1_energy(GWh)":
            [round(x / 1000, 1) for x in battery1_energy],
            "battery4_power(GW)": [round(x / 1000, 1) for x in battery4_power],
            "battery4_energy(GWh)":
            [round(x / 1000, 1) for x in battery4_energy],
            "battery8_power(GW)": [round(x / 1000, 1) for x in battery8_power],
            "battery8_energy(GWh)":
            [round(x / 1000, 1) for x in battery8_energy],
            "import(GW)": [round(x / 1000, 1) for x in importtranscapacity],
            "export(GW)": [round(x / 1000, 1) for x in exporttranscapacity],
            "nucpro(TWh)": [round(x / 1e6, 1) for x in nucpro],
            "pvlargepro(TWh)": [round(x / 1e6, 1) for x in pvlargepro],
            "pvsmallpro(TWh)": [round(x / 1e6, 1) for x in pvsmallpro],
            "onshorepro(TWh)": [round(x / 1e6, 1) for x in onshorepro],
            "offshorepro(TWh)": [round(x / 1e6, 1) for x in offshorepro],
            "gasccgtpro(TWh)": [round(x / 1e6, 1) for x in gasccgtpro],
            "gasocgtpro(TWh)": [round(x / 1e6, 1) for x in gasocgtpro],
            "hydro_rorpro(TWh)": [round(x / 1e6, 1) for x in hydro_rorpro],
            "hydro_dampro(TWh)": [round(x / 1e6, 1) for x in hydro_dampro],
            "phs_char(TWh)": [round(x / 1e6, 1) for x in phs_char],
            "phs_disc(TWh)": [round(x / 1e6, 1) for x in phs_disc],
            "ptg_char(TWh)": [round(x / 1e6, 1) for x in ptg_char],
            "ptg_disc(TWh)": [round(x / 1e6, 1) for x in ptg_disc],
            "battery1_char(TWh)": [round(x / 1e6, 1) for x in battery1_char],
            "battery1_disc(TWh)": [round(x / 1e6, 1) for x in battery1_disc],
            "battery4_char(TWh)": [round(x / 1e6, 1) for x in battery4_char],
            "battery4_disc(TWh)": [round(x / 1e6, 1) for x in battery4_disc],
            "battery8_char(TWh)": [round(x / 1e6, 1) for x in battery8_char],
            "battery8_disc(TWh)": [round(x / 1e6, 1) for x in battery8_disc],
            "excess&loss(TWh)": [round(x / 1e6, 1) for x in excess],
            "exchange(TWh)": [round(x / 1e6, 1) for x in exchange],
            "demand(TWh)": [round(x / 1e6) for x in demand],
            "nucper": [round(x, 3) for x in nucper],
            "resper": [round(x, 3) for x in resper],
            "fossilper": [round(x, 3) for x in fossilper],
            "emission(MT)": [round(x / 1e9, 2) for x in emission],
            "totalemission(MT)": [round(x / 1e9, 2) for x in totalemission],
            "averageshadowprice(euro/MWh)": shadowprice
        })

    dirName = str(os.getcwd()).replace('\\', '/') + "/output_data/" + sce_name

    # Create target directory if it doesn't exist
    if not os.path.exists(dirName):
        os.mkdir(dirName)

    save_path = dirName + '/result_' + sce_name + '.csv'
    df.to_csv(save_path, sep=',', index=False)

    return


def ExchangeHourlyCostFunction(instance, r, y):
    cobject = getattr(instance, 'ElecBalanceConstraint')

    exchangehourlycostlist = []

    for h in instance.TIMESLICE:
        exchangehourlycost = 0
        for l in instance.LINE:
            if (instance.eleclexchange[l, y, h].value *
                    instance.LineRegion[l, r]) > 0:  # import
                exchangehourlycost = exchangehourlycost + instance.eleclexchange[
                    l, y, h].value * instance.LineRegion[l, r] * instance.dual[
                        cobject[instance.ContraryRegion[l, r], y, h]] / (
                            1 - instance.TransLosses[y, instance.TransTech[l]]
                            * instance.TransDis[l] / 100)

            else:  #export
                exchangehourlycost = exchangehourlycost + instance.eleclexchange[
                    l, y, h].value * instance.LineRegion[l, r] * instance.dual[
                        cobject[r, y, h]] / (
                            1 - instance.TransLosses[y, instance.TransTech[l]]
                            * instance.TransDis[l] / 100)
        exchangehourlycostlist.append(exchangehourlycost)

    return exchangehourlycostlist


if __name__ == "__main__":
    pass
