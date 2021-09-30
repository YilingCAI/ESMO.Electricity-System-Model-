from __future__ import (  # to ensure compatibility with both Python2.6/2.7 and Python3.x
    absolute_import, division, print_function)

import logging
import sys
from datetime import datetime
from pyutilib.services import TempfileManager
import os
import pandas as pd

from pyomo.core import *
from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.core import Constraint

from esmo import (create_instance, create_model, io_data, pre_generation,
                  results_save)

# define temp file path
TempfileManager.tempdir = '/home/scratch01/ylcai/data/ESMO_test/'
outputpath = '/home/scratch01/ylcai/data/ESMO_test/output/'

# define log
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")

file_handler = logging.FileHandler('log/main.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# turn on log
pre_generation.logger.setLevel(logging.DEBUG)
io_data.logger.setLevel(logging.DEBUG)
create_model.logger.setLevel(logging.DEBUG)
create_instance.logger.setLevel(logging.DEBUG)
results_save.logger.setLevel(logging.DEBUG)

# create model framework
M = create_model.create_model()

# choose solver
opt = SolverFactory("cplex")

opt.options['thread'] = 1

# scenario parameter read
SCE_ARR = io_data.ImportCSV('/input_data/scenario_parameter.csv').read_csv(
    header=0, index_col=0, parse_dates=False, squeeze=False)
script = sys.argv[0]
run_name = sys.argv[1]

# run scenario
for i in range(len(SCE_ARR)):
    sce_name = SCE_ARR['sce_name'].iat[i]

    if sce_name == run_name:
        logger.debug(
            'This is the beginning of the {} scenario'.format(sce_name))
        start_time = datetime.now()

        # start pre_generation
        pre_generation.pre_generation_avail(sce_name)
        pre_generation.pre_generation_mustrun(sce_name)

        # create scenario instance
        instance = create_instance.create_instance(M, sce_name)

        ## instance.ElecMustRunMinConstraint.deactivate()
        instance.ElecImportExportTransCapacityConstraint.deactivate()
        # UC constraint deavtivate
        create_instance.uc_constraint_deactivate(instance)

        # solve instance
        instance.dual = Suffix(direction=Suffix.IMPORT)
        results = opt.solve(instance, tee=False, keepfiles=True)

        # detailed result save for each scenario
        name = sce_name + 'opt'
        results_save.detail_save_results_no_uc(instance, name, outputpath)

        # whole result save
        for r in [1, 2]:
            for y in [2050]:
                results_save.whole_result_append(instance, r, y,
                                                 'opt' + str(r))

        # UC constraint activate
        create_instance.uc_constraint_activate(instance)

        for r, y, t in instance.REGION_YEAR_TECH_PHS:
            for h in instance.TIMESLICE:
                instance.aFCRupStorChar[r, y, t, h].fix(0)
                instance.aFCRdownStorChar[r, y, t, h].fix(0)
                instance.aFRRupStorChar[r, y, t, h].fix(0)
                instance.aFRRdownStorChar[r, y, t, h].fix(0)
                instance.mFRRupStorChar[r, y, t, h].fix(0)
                instance.mFRRdownStorChar[r, y, t, h].fix(0)

        for r, y, t in instance.REGION_YEAR_TECH_GENERATION:
            if t != 'OCGT_new':
                instance.totalinstalledgencapacity[r, y, t].fix(
                    instance.totalinstalledgencapacity[r, y, t].value)

        for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
            instance.totalinstalledstorpower[r, y, tt].fix(
                instance.totalinstalledstorpower[r, y, tt].value)

        for l in instance.LINE:
            for y in instance.YEAR:
                instance.totalinstalledimporttranscapacity[l, y].fix(
                    instance.totalinstalledimporttranscapacity[l, y].value)
                instance.totalinstalledexporttranscapacity[l, y].fix(
                    instance.totalinstalledexporttranscapacity[l, y].value)

        # instance write to a lp file
        lp_name = '/home/scratch01/ylcai/data/ESMO_test/' + sce_name + '.lp'
        instance.write(lp_name, io_options={'symbolic_solver_labels': True})

        # solve instance
        instance.dual = Suffix(direction=Suffix.IMPORT)
        results = opt.solve(instance, tee=False, keepfiles=True)

        # detailed result save for each scenario
        name = sce_name + 'opt_uc'
        results_save.detail_save_results_uc(instance, name, outputpath)

        for r in [1, 2]:
            for y in [2050]:
                results_save.whole_result_append(instance, r, y,
                                                 'opt' + str(r) + '_uc')

        for i in range(0, 90000, 10000):
            for j in range(0, 320000, 40000):

                # create scenario instance
                instance = create_instance.create_instance(M, sce_name)

                instance.irescapacity[1, 2050].fix(j)
                instance.totalinstalledgencapacity[1, 2050,
                                                   'Nuclear_new'].fix(i)

                instance.irescapacity[2, 2050].fix(j)
                instance.totalinstalledgencapacity[2, 2050,
                                                   'Nuclear_new'].fix(i)

                ## instance.ElecMustRunMinConstraint.deactivate()
                instance.ElecImportExportTransCapacityConstraint.deactivate()
                # UC constraint deactivate
                create_instance.uc_constraint_deactivate(instance)

                # solve instance
                instance.dual = Suffix(direction=Suffix.IMPORT)
                results = opt.solve(instance, tee=False)

                # detailed result save for each scenario
                name = sce_name + '_' + str(i) + '_' + str(j)
                results_save.detail_save_results_no_uc(instance, name,
                                                       outputpath)

                # whole result save
                for r in [1, 2]:
                    for y in [2050]:
                        results_save.whole_result_append(
                            instance, r, y, str(r))

                # UC constraint activate
                create_instance.uc_constraint_activate(instance)

                for r, y, t in instance.REGION_YEAR_TECH_PHS:
                    for h in instance.TIMESLICE:
                        instance.aFCRupStorChar[r, y, t, h].fix(0)
                        instance.aFCRdownStorChar[r, y, t, h].fix(0)
                        instance.aFRRupStorChar[r, y, t, h].fix(0)
                        instance.aFRRdownStorChar[r, y, t, h].fix(0)
                        instance.mFRRupStorChar[r, y, t, h].fix(0)
                        instance.mFRRdownStorChar[r, y, t, h].fix(0)

                for r, y, t in instance.REGION_YEAR_TECH_GENERATION:
                    if t != 'OCGT_new':
                        instance.totalinstalledgencapacity[r, y, t].fix(
                            instance.totalinstalledgencapacity[r, y, t].value)

                for r, y, tt in instance.REGION_YEAR_TECH_STORAGE:
                    instance.totalinstalledstorpower[r, y, tt].fix(
                        instance.totalinstalledstorpower[r, y, tt].value)

                for l in instance.LINE:
                    for y in instance.YEAR:
                        instance.totalinstalledimporttranscapacity[l, y].fix(
                            instance.totalinstalledimporttranscapacity[
                                l, y].value)
                        instance.totalinstalledexporttranscapacity[l, y].fix(
                            instance.totalinstalledexporttranscapacity[
                                l, y].value)

                # solve instance
                instance.dual = Suffix(direction=Suffix.IMPORT)
                results = opt.solve(instance, tee=False)

                # detailed result save for each scenario
                name = sce_name + '_' + str(i) + '_' + str(j) + '_uc'
                results_save.detail_save_results_uc(instance, name, outputpath)

                for r in [1, 2]:
                    for y in [2050]:
                        results_save.whole_result_append(
                            instance, r, y,
                            str(r) + '_uc')

        results_save.whole_result_save(sce_name)
        running_time = datetime.now() - start_time
        logger.debug('This is the end of the {} scenario'.format(sce_name))
        logger.debug('The {} scenario running time is {}'.format(
            sce_name, running_time))
