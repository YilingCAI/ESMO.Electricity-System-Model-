# Title: Instance constraction
# Description: This fonction is used to import the scenatio data and then to construct a concrete model.

from __future__ import print_function, division, absolute_import

import os
import logging
import sys
import pandas as pd

from pyomo.environ import *
from pyomo.environ import DataPortal

logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s")

file_handler = logging.FileHandler('log/create_instance.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def get_path(path, sce_name):
    cwd = str(os.getcwd()).replace('\\', '/')
    path = cwd + '/input_data/' + sce_name + '/' + path
    return path


def create_instance(M, sce_name):

    try:
        data = DataPortal(model=M)

        data.load(filename=get_path("set/REGION_ID.csv", sce_name),
                  format='set',
                  set='REGION_ID')
        data.load(filename=get_path("set/TIMESLICE.csv", sce_name),
                  format='set',
                  set='TIMESLICE')
        data.load(filename=get_path("set/YEAR.csv", sce_name),
                  format='set',
                  set='YEAR')
        data.load(filename=get_path("set/YEARPERIOD.csv", sce_name),
                  format='set',
                  set='YEARPERIOD')
        data.load(filename=get_path("set/WEEK.csv", sce_name),
                  format='set',
                  set='WEEK')
        data.load(filename=get_path("set/LINE.csv", sce_name),
                  format='set',
                  set='LINE')

        data.load(filename=get_path("set/TECH_GENERATION.csv", sce_name),
                  format='set',
                  set='TECH_GENERATION')
        data.load(filename=get_path("set/TECH_STORAGE.csv", sce_name),
                  format='set',
                  set='TECH_STORAGE')
        data.load(filename=get_path("set/TECH_TRANSMISSION.csv", sce_name),
                  format='set',
                  set='TECH_TRANSMISSION')
        data.load(filename=get_path("set/TECH_VRES.csv", sce_name),
                  format='set',
                  set='TECH_VRES')
        data.load(filename=get_path("set/TECH_IRES.csv", sce_name),
                  format='set',
                  set='TECH_IRES')
        data.load(filename=get_path("set/TECH_TPP.csv", sce_name),
                  format='set',
                  set='TECH_TPP')
        data.load(filename=get_path("set/TECH_HD.csv", sce_name),
                  format='set',
                  set='TECH_HD')
        data.load(filename=get_path("set/TECH_FOSSIL.csv", sce_name),
                  format='set',
                  set='TECH_FOSSIL')
        data.load(filename=get_path("set/TECH_MUSTRUN.csv", sce_name),
                  format='set',
                  set='TECH_MustRun')
        data.load(filename=get_path("set/TECH_GAS.csv", sce_name),
                  format='set',
                  set='TECH_GAS')
        data.load(filename=get_path("set/TECH_NUC.csv", sce_name),
                  format='set',
                  set='TECH_NUC')
        data.load(filename=get_path("set/TECH_UC.csv", sce_name),
                  format='set',
                  set='TECH_UC')
        data.load(filename=get_path("set/TECH_PHS.csv", sce_name),
                  format='set',
                  set='TECH_PHS')
        data.load(filename=get_path("set/TECH_DSM.csv", sce_name),
                  format='set',
                  set='TECH_DSM')
        data.load(filename=get_path("set/TECH_PTG.csv", sce_name),
                  format='set',
                  set='TECH_PTG')
        data.load(filename=get_path("set/TECH_PTH.csv", sce_name),
                  format='set',
                  set='TECH_PTH')
        data.load(filename=get_path("set/TECH_FCRup.csv", sce_name),
                  format='set',
                  set='TECH_FCRup')
        data.load(filename=get_path("set/TECH_FCRdown.csv", sce_name),
                  format='set',
                  set='TECH_FCRdown')
        data.load(filename=get_path("set/TECH_aFRRup.csv", sce_name),
                  format='set',
                  set='TECH_aFRRup')
        data.load(filename=get_path("set/TECH_aFRRdown.csv", sce_name),
                  format='set',
                  set='TECH_aFRRdown')
        data.load(filename=get_path("set/TECH_mFRRup.csv", sce_name),
                  format='set',
                  set='TECH_mFRRup')
        data.load(filename=get_path("set/TECH_mFRRdown.csv", sce_name),
                  format='set',
                  set='TECH_mFRRdown')
        data.load(filename=get_path("set/REGION_YEAR_TECH_GENERATION.csv",
                                    sce_name),
                  format='set',
                  set='REGION_YEAR_TECH_GENERATION')
        data.load(filename=get_path("set/REGION_YEAR_TECH_STORAGE.csv",
                                    sce_name),
                  format='set',
                  set='REGION_YEAR_TECH_STORAGE')

        df = pd.read_csv(get_path("parameter/mustrun.csv", sce_name), header=0)
        if len(df) != 0:
            data.load(filename=get_path("parameter/mustrun.csv", sce_name),
                      param="MustRun",
                      format="table")

        data.load(filename=get_path("parameter/demand.csv", sce_name),
                  param="Demand",
                  format="table")

        data.load(filename=get_path("parameter/capacity_factor.csv", sce_name),
                  param="CapacityFactor",
                  format="table")
        data.load(filename=get_path("parameter/availability.csv", sce_name),
                  param="Availability",
                  format="table")
        data.load(filename=get_path("parameter/co2_cost.csv", sce_name),
                  param="CO2Cost",
                  format="table")
        data.load(filename=get_path("parameter/dsm_shedding.csv", sce_name),
                  param=[
                      'DSMSheddingCapacity', 'DSMSheddingOPEXfix',
                      'DSMSheddingOPEXvar'
                  ],
                  format="table")
        data.load(filename=get_path("parameter/res_percentage_min.csv",
                                    sce_name),
                  param="RESPer",
                  format="table")
        data.load(filename=get_path("parameter/nuc_percentage_max.csv",
                                    sce_name),
                  param="NUCPer",
                  format="table")
        data.load(filename=get_path("parameter/periodyear.csv", sce_name),
                  param="PERIODYEAR",
                  format="table")

        data.load(filename=get_path("parameter/generation_capacity.csv",
                                    sce_name),
                  param=[
                      'GenResidualCapacity', 'GenMaxInstalledCapacity',
                      'GenMaxEnergy'
                  ],
                  format="table")
        data.load(filename=get_path("parameter/generation_parameter.csv",
                                    sce_name),
                  param=[
                      'GenFuel', 'GenCAPEX', 'GenOPEXfix', 'GenFuelCost',
                      'GenFullLoadEffi', 'Genvar', 'GenOPEXvar',
                      'GenTLifetime', 'GenELifetime', 'GenWACC', 'CO2 content',
                      'EmissionFactor', 'CCSRatio', 'GenSize', 'GenStarUpCost',
                      'GenMinPower', 'GenRampUpRate', 'GenRampDownRate',
                      'GenMinStartUpHour', 'GenMinShutDownHour', 'GenFCRup',
                      'GenFCRdown', 'GenAFRRup', 'GenAFRRdown', 'GenMFRRup',
                      'GenMFRRdown', 'AvailAvg', 'AvailSTD', 'MustRunWinter',
                      'MustRunSummer'
                  ],
                  format="table")

        data.load(filename=get_path("parameter/reserve_fcr.csv", sce_name),
                  param=['FCRRequired'],
                  format="table")

        data.load(
            filename=get_path("parameter/err.csv", sce_name),
            param=['ErrAFRRup', 'ErrAFRRdown', 'ErrMFRRup', 'ErrMFRRdown'],
            format="table")

        data.load(
            filename=get_path("parameter/derr.csv", sce_name),
            param=['DErrAFRRup', 'DErrAFRRdown', 'DErrMFRRup', 'DErrMFRRdown'],
            format="table")

        data.load(filename=get_path("parameter/nuclear_lto_match.csv",
                                    sce_name),
                  param=['NM'],
                  format="table")

        data.load(filename=get_path("parameter/hydrodam_extra_parameter.csv",
                                    sce_name),
                  param=['HDMaxStock', 'HDStorIniLevel', 'HDEffi'],
                  format="table")
        data.load(filename=get_path("parameter/hydrodam_weekly_inflow.csv",
                                    sce_name),
                  param=['HDWeekInflow', 'HDMinLevel', 'HDMaxLevel'],
                  format="table")

        data.load(filename=get_path("parameter/storage_capacity.csv",
                                    sce_name),
                  param=['StorResidualPower', 'StorMaxInstalledPower'],
                  format="table")
        data.load(filename=get_path("parameter/storage_parameter.csv",
                                    sce_name),
                  param=[
                      'StorCAPEXp', 'StorCAPEXe', 'StorOPEXfix', 'StorOPEXvar',
                      'StorTLifetime', 'StorELifetime', 'StorWACC', 'StorSize',
                      'StorStarUpCost', 'StorMinPower', 'StorRampUpRate',
                      'StorRampDownRate', 'StorMinStartUpHour',
                      'StorMinShutDownHour', 'StorFCRup', 'StorFCRdown',
                      'StorAFRRup', 'StorAFRRdown', 'StorMFRRup',
                      'StorMFRRdown', 'StorIni', 'StorCharEfficiency',
                      'StorDiscEfficiency', 'StorEnergyPowerRatio', 'AvailAvg',
                      'AvailSTD'
                  ],
                  format="table")
        data.load(filename=get_path("parameter/transmission_capacity.csv",
                                    sce_name),
                  param=[
                      'TransResidualImportCapacity',
                      'TransMaxInstalledImportCapacity',
                      'TransResidualExportCapacity',
                      'TransMaxInstalledExportCapacity'
                  ],
                  format="table")
        data.load(filename=get_path("parameter/transmission_parameter.csv",
                                    sce_name),
                  param=[
                      'TransCAPEXline', 'TransCAPEXstation',
                      'TransOPEXfixline', 'TransOPEXfixstation',
                      'TransTLifetime', 'TransELifetime', 'TransWACC',
                      'TransLosses', 'TransAvailability'
                  ],
                  format="table")
        data.load(filename=get_path("parameter/trans_line.csv", sce_name),
                  param=['TransTech', 'TransDis'],
                  format="table")
        data.load(filename=get_path("parameter/lineregion.csv", sce_name),
                  param=['LineRegion', 'ContraryRegion'],
                  format="table")

        data.load(filename=get_path("parameter/annual_max_emission.csv",
                                    sce_name),
                  param="AnnualMaxEmission",
                  format="table")
        data.load(filename=get_path("parameter/emission_budget.csv", sce_name),
                  param="EmissionBudget",
                  format="table")

        data.load(filename=get_path("parameter/sdr.csv", sce_name),
                  param="SDR",
                  format="table")

        data.load(filename=get_path("parameter/hydrogen_needs.csv", sce_name),
                  param="HydrogenNeeds",
                  format="table")

        data.load(filename=get_path("parameter/flexbiogas.csv", sce_name),
                  param=['FlexBiogasQuantity', 'BiogasPrice'],
                  format="table")

        instance = M.create_instance(data, report_timing=True)

    except Exception as ex:
        logger.exception(ex)
        sys.exit(1)

    return instance


def uc_constraint_deactivate(instance):

    instance.ElecCommitNumberGenConstraint.deactivate()
    instance.ElecCommitGenConstraint.deactivate()
    instance.ElecCommitBalanceGenConstraint.deactivate()
    instance.ElecCommitNumberStorCharConstraint.deactivate()
    instance.ElecCommitStorConstraint.deactivate()
    instance.ElecCommitBalanceStorCharConstraint.deactivate()
    instance.ElecCommitNumberStorDiscConstraint.deactivate()
    instance.ElecCommitBalanceStorDiscConstraint.deactivate()
    instance.ElecMinOutputGenConstraint.deactivate()
    instance.ElecMinOutputGenQuickStartConstraint.deactivate()
    instance.ElecMinOutputStorCharConstraint.deactivate()
    instance.ElecMinOutputStorCharQuickStartConstraint.deactivate()
    instance.ElecMinOutputStorDiscConstraint.deactivate()
    instance.ElecMinOutputStorDiscQuickStartConstraint.deactivate()
    instance.ElecMaxOutputGenConstraint.deactivate()
    instance.ElecMaxOutputGenQuickStartConstraint.deactivate()
    instance.ElecMaxOutputStorCharConstraint.deactivate()
    instance.ElecMaxOutputStorCharQuickStartConstraint.deactivate()
    instance.ElecMaxOutputStorDiscConstraint.deactivate()
    instance.ElecMaxOutputStorDiscQuickStartConstraint.deactivate()
    instance.ElecMaxOutputStorDiscConstraint1.deactivate()
    instance.ElecMinStartUpHourGenConstraint.deactivate()
    instance.ElecMinStartUpHourStorCharConstraint.deactivate()
    instance.ElecMinStartUpHourStorDiscConstraint.deactivate()
    instance.ElecMinShutDownHourGenConstraint.deactivate()
    instance.ElecMinShutDownHourStorCharConstraint.deactivate()
    instance.ElecMinShutDownHourStorDiscConstraint.deactivate()

    instance.ReserveRequiredaFRRupConstraint.deactivate()
    instance.ReserveRequiredaFRRdownConstraint.deactivate()
    instance.ReserveRequiredmFRRupConstraint.deactivate()
    instance.ReserveRequiredmFRRdownConstraint.deactivate()
    instance.ReserveaFCRUpBalanceConstraint.deactivate()
    instance.ReserveaFCRDownBalanceConstraint.deactivate()
    instance.ReserveaFRRUpBalanceConstraint.deactivate()
    instance.ReserveaFRRDownBalanceConstraint.deactivate()
    instance.ReservemFRRUpBalanceConstraint.deactivate()
    instance.ReservemFRRDownBalanceConstraint.deactivate()
    instance.ReserveaFCRUpGenLimitConstraint.deactivate()
    instance.ReserveaFCRDownGenLimitConstraint.deactivate()
    instance.ReserveaFRRUpGenLimitConstraint.deactivate()
    instance.ReserveaFRRDownGenLimitConstraint.deactivate()
    instance.ReservemFRRUpGenLimitConstraint.deactivate()
    instance.ReservemFRRDownGenLimitConstraint.deactivate()
    instance.ReserveaFCRUpStorCharLimitConstraint.deactivate()
    instance.ReserveaFCRDownStorCharLimitConstraint.deactivate()
    instance.ReserveaFRRUpStorCharLimitConstraint.deactivate()
    instance.ReserveaFRRDownStorCharLimitConstraint.deactivate()
    instance.ReservemFRRUpStorCharLimitConstraint.deactivate()
    instance.ReservemFRRDownStorCharLimitConstraint.deactivate()
    instance.ReserveaFCRUpStorDiscLimitConstraint.deactivate()
    instance.ReserveaFCRDownStorDiscLimitConstraint.deactivate()
    instance.ReserveaFRRUpStorDiscLimitConstraint.deactivate()
    instance.ReserveaFRRDownStorDiscLimitConstraint.deactivate()
    instance.ReservemFRRUpStorDiscLimitConstraint.deactivate()
    instance.ReservemFRRDownStorDiscLimitConstraint.deactivate()

    return


def uc_constraint_activate(instance):
    instance.ElecCommitNumberGenConstraint.activate()
    instance.ElecCommitGenConstraint.activate()
    instance.ElecCommitBalanceGenConstraint.activate()
    instance.ElecCommitNumberStorCharConstraint.activate()
    instance.ElecCommitStorConstraint.activate()
    instance.ElecCommitBalanceStorCharConstraint.activate()
    instance.ElecCommitNumberStorDiscConstraint.activate()
    instance.ElecCommitBalanceStorDiscConstraint.activate()
    instance.ElecMinOutputGenConstraint.activate()
    instance.ElecMinOutputGenQuickStartConstraint.activate()
    instance.ElecMinOutputStorCharConstraint.activate()
    instance.ElecMinOutputStorCharQuickStartConstraint.activate()
    instance.ElecMinOutputStorDiscConstraint.activate()
    instance.ElecMinOutputStorDiscQuickStartConstraint.activate()
    instance.ElecMaxOutputGenConstraint.activate()
    instance.ElecMaxOutputGenQuickStartConstraint.activate()
    instance.ElecMaxOutputStorCharConstraint.activate()
    instance.ElecMaxOutputStorCharQuickStartConstraint.activate()
    instance.ElecMaxOutputStorDiscConstraint.activate()
    instance.ElecMaxOutputStorDiscQuickStartConstraint.activate()
    instance.ElecMaxOutputStorDiscConstraint1.activate()
    instance.ElecMinStartUpHourGenConstraint.activate()
    instance.ElecMinStartUpHourStorCharConstraint.activate()
    instance.ElecMinStartUpHourStorDiscConstraint.activate()
    instance.ElecMinShutDownHourGenConstraint.activate()
    instance.ElecMinShutDownHourStorCharConstraint.activate()
    instance.ElecMinShutDownHourStorDiscConstraint.activate()

    instance.ReserveRequiredaFRRupConstraint.activate()
    instance.ReserveRequiredaFRRdownConstraint.activate()
    instance.ReserveRequiredmFRRupConstraint.activate()
    instance.ReserveRequiredmFRRdownConstraint.activate()
    instance.ReserveaFCRUpBalanceConstraint.activate()
    instance.ReserveaFCRDownBalanceConstraint.activate()
    instance.ReserveaFRRUpBalanceConstraint.activate()
    instance.ReserveaFRRDownBalanceConstraint.activate()
    instance.ReservemFRRUpBalanceConstraint.activate()
    instance.ReservemFRRDownBalanceConstraint.activate()
    instance.ReserveaFCRUpGenLimitConstraint.activate()
    instance.ReserveaFCRDownGenLimitConstraint.activate()
    instance.ReserveaFRRUpGenLimitConstraint.activate()
    instance.ReserveaFRRDownGenLimitConstraint.activate()
    instance.ReservemFRRUpGenLimitConstraint.activate()
    instance.ReservemFRRDownGenLimitConstraint.activate()
    instance.ReserveaFCRUpStorCharLimitConstraint.activate()
    instance.ReserveaFCRDownStorCharLimitConstraint.activate()
    instance.ReserveaFRRUpStorCharLimitConstraint.activate()
    instance.ReserveaFRRDownStorCharLimitConstraint.activate()
    instance.ReservemFRRUpStorCharLimitConstraint.activate()
    instance.ReservemFRRDownStorCharLimitConstraint.activate()
    instance.ReserveaFCRUpStorDiscLimitConstraint.activate()
    instance.ReserveaFCRDownStorDiscLimitConstraint.activate()
    instance.ReserveaFRRUpStorDiscLimitConstraint.activate()
    instance.ReserveaFRRDownStorDiscLimitConstraint.activate()
    instance.ReservemFRRUpStorDiscLimitConstraint.activate()
    instance.ReservemFRRDownStorDiscLimitConstraint.activate()

    return


if __name__ == "__main__":
    pass
