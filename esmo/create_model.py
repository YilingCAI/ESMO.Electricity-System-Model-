# Title: Abstract model creation
# Description: This fonction is used to create an abstract electricity system model without data.

from __future__ import print_function, division, absolute_import

import logging

from pyomo.environ import *
from pyomo.core import *
from pyomo.core.expr.numeric_expr import *

logger = logging.getLogger(__name__)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s")

file_handler = logging.FileHandler('log/create_model.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# This is the function to create mathematical model. In the model, it includes set, parameter
def create_model():

    M = AbstractModel()

    ###########################################SET##################################################
    M.REGION_ID = Set()
    M.TIMESLICE = Set(ordered=True)
    M.TECH_GENERATION = Set()
    M.TECH_STORAGE = Set()
    M.TECH_TRANSMISSION = Set()
    M.TECH_VRES = Set(within=M.TECH_GENERATION)
    M.TECH_IRES = Set(within=M.TECH_VRES)
    M.TECH_TPP = Set(within=M.TECH_GENERATION)
    M.TECH_HD = Set(within=M.TECH_GENERATION)
    M.YEAR = Set(ordered=True)
    M.YEARPERIOD = Set(dimen=2, ordered=True)
    M.WEEK = Set(ordered=True)
    M.DAY = Set(ordered=True)
    M.LINE = Set()

    M.TECH_MustRun = Set(within=M.TECH_TPP)
    M.TECH_FOSSIL = Set(within=M.TECH_TPP)
    M.TECH_NUC = Set(within=M.TECH_TPP)
    M.TECH_UC = Set(within=M.TECH_GENERATION | M.TECH_STORAGE)
    M.TECH_GAS = Set(within=M.TECH_TPP)
    M.TECH_PHS = Set(within=M.TECH_STORAGE)
    M.TECH_DSM = Set(within=M.TECH_STORAGE)
    M.TECH_PTG = Set(within=M.TECH_STORAGE)
    M.TECH_PTH = Set(within=M.TECH_STORAGE)
    M.TECH_STORAGE_NO_DSM = Set(initialize=M.TECH_STORAGE - M.TECH_DSM)
    M.TECH_STORAGE_NO_DSM_PTG = Set(initialize=M.TECH_STORAGE - M.TECH_DSM -
                                    M.TECH_PTG)

    M.TECH_FCRup = Set(within=M.TECH_GENERATION | M.TECH_STORAGE)
    M.TECH_FCRdown = Set(within=M.TECH_GENERATION | M.TECH_STORAGE)
    M.TECH_aFRRup = Set(within=M.TECH_GENERATION | M.TECH_STORAGE)
    M.TECH_aFRRdown = Set(within=M.TECH_GENERATION | M.TECH_STORAGE)
    M.TECH_mFRRup = Set(within=M.TECH_GENERATION | M.TECH_STORAGE)
    M.TECH_mFRRdown = Set(within=M.TECH_GENERATION | M.TECH_STORAGE)

    M.REGION_YEAR_TECH_GENERATION = Set(within=M.REGION_ID * M.YEAR *
                                        M.TECH_GENERATION)
    M.REGION_YEAR_TECH_STORAGE = Set(within=M.REGION_ID * M.YEAR *
                                     M.TECH_STORAGE)
    M.REGION_YEAR_TECH_VRES = Set(initialize=M.REGION_YEAR_TECH_GENERATION
                                  & (M.REGION_ID * M.YEAR * M.TECH_VRES))
    M.REGION_YEAR_TECH_TPP = Set(initialize=M.REGION_YEAR_TECH_GENERATION
                                 & (M.REGION_ID * M.YEAR * M.TECH_TPP))
    M.REGION_YEAR_TECH_HD = Set(initialize=M.REGION_YEAR_TECH_GENERATION
                                & (M.REGION_ID * M.YEAR * M.TECH_HD))
    M.REGION_YEAR_TECH_MustRun = Set(initialize=M.REGION_YEAR_TECH_GENERATION
                                     & (M.REGION_ID * M.YEAR * M.TECH_MustRun))
    M.REGION_YEAR_TECH_FOSSIL = Set(initialize=M.REGION_YEAR_TECH_GENERATION
                                    & (M.REGION_ID * M.YEAR * M.TECH_FOSSIL))
    M.REGION_YEAR_TECH_UC = Set(initialize=(M.REGION_YEAR_TECH_GENERATION
                                            | M.REGION_YEAR_TECH_STORAGE)
                                & (M.REGION_ID * M.YEAR * M.TECH_UC))
    M.REGION_YEAR_TECH_UC_Gen = Set(initialize=(M.REGION_YEAR_TECH_GENERATION)
                                    & (M.REGION_ID * M.YEAR * M.TECH_UC))
    M.REGION_YEAR_TECH_UC_Stor = Set(initialize=(M.REGION_YEAR_TECH_STORAGE)
                                     & (M.REGION_ID * M.YEAR * M.TECH_UC))
    M.REGION_YEAR_TECH_GAS = Set(initialize=M.REGION_YEAR_TECH_GENERATION
                                 & (M.REGION_ID * M.YEAR * M.TECH_GAS))
    M.REGION_YEAR_TECH_NUC = Set(initialize=M.REGION_YEAR_TECH_GENERATION
                                 & (M.REGION_ID * M.YEAR * M.TECH_NUC))
    M.REGION_YEAR_TECH_DSM = Set(initialize=M.REGION_YEAR_TECH_STORAGE
                                 & (M.REGION_ID * M.YEAR * M.TECH_DSM))
    M.REGION_YEAR_TECH_PTG = Set(initialize=M.REGION_YEAR_TECH_STORAGE
                                 & (M.REGION_ID * M.YEAR * M.TECH_PTG))
    M.REGION_YEAR_TECH_PTH = Set(initialize=M.REGION_YEAR_TECH_STORAGE
                                 & (M.REGION_ID * M.YEAR * M.TECH_PTH))
    M.REGION_YEAR_TECH_PHS = Set(initialize=M.REGION_YEAR_TECH_STORAGE
                                 & (M.REGION_ID * M.YEAR * M.TECH_PHS))
    M.REGION_YEAR_TECH_AVAIL = Set(initialize=M.REGION_YEAR_TECH_GENERATION
                                   | M.REGION_YEAR_TECH_STORAGE)

    M.REGION_YEAR_TECH_FCRup = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION | M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_FCRup))
    M.REGION_YEAR_TECH_FCRdown = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION | M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_FCRdown))
    M.REGION_YEAR_TECH_aFRRup = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION | M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_aFRRup))
    M.REGION_YEAR_TECH_aFRRdown = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION | M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_aFRRdown))
    M.REGION_YEAR_TECH_mFRRup = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION | M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_mFRRup))
    M.REGION_YEAR_TECH_mFRRdown = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION | M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_mFRRdown))

    M.REGION_YEAR_TECH_Gen_FCRup = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION)
        & (M.REGION_ID * M.YEAR * M.TECH_FCRup))
    M.REGION_YEAR_TECH_Gen_FCRdown = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION)
        & (M.REGION_ID * M.YEAR * M.TECH_FCRdown))
    M.REGION_YEAR_TECH_Gen_aFRRup = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION)
        & (M.REGION_ID * M.YEAR * M.TECH_aFRRup))
    M.REGION_YEAR_TECH_Gen_aFRRdown = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION)
        & (M.REGION_ID * M.YEAR * M.TECH_aFRRdown))
    M.REGION_YEAR_TECH_Gen_mFRRup = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION)
        & (M.REGION_ID * M.YEAR * M.TECH_mFRRup))
    M.REGION_YEAR_TECH_Gen_mFRRdown = Set(
        initialize=(M.REGION_YEAR_TECH_GENERATION)
        & (M.REGION_ID * M.YEAR * M.TECH_mFRRdown))

    M.REGION_YEAR_TECH_Stor_FCRup = Set(
        initialize=(M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_FCRup))
    M.REGION_YEAR_TECH_Stor_FCRdown = Set(
        initialize=(M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_FCRdown))
    M.REGION_YEAR_TECH_Stor_aFRRup = Set(
        initialize=(M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_aFRRup))
    M.REGION_YEAR_TECH_Stor_aFRRdown = Set(
        initialize=(M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_aFRRdown))

    M.REGION_YEAR_TECH_Stor_mFRRup = Set(
        initialize=(M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_mFRRup))
    M.REGION_YEAR_TECH_Stor_mFRRdown = Set(
        initialize=(M.REGION_YEAR_TECH_STORAGE)
        & (M.REGION_ID * M.YEAR * M.TECH_mFRRdown))

    ###########################################PARAMETER##################################################

    # Timeseries
    M.Demand = Param(M.REGION_ID,
                     M.YEAR,
                     M.TIMESLICE,
                     default=0,
                     domain=NonNegativeReals)
    M.MustRun = Param(M.REGION_YEAR_TECH_MustRun,
                      M.TIMESLICE,
                      default=0,
                      domain=NonNegativeReals)
    M.CapacityFactor = Param(M.REGION_YEAR_TECH_VRES,
                             M.TIMESLICE,
                             domain=NonNegativeReals)
    M.Availability = Param(M.REGION_YEAR_TECH_AVAIL,
                           M.TIMESLICE,
                           default=1,
                           domain=NonNegativeReals)

    # Generation
    M.GenResidualCapacity = Param(M.REGION_YEAR_TECH_GENERATION,
                                  domain=NonNegativeReals)
    M.GenMaxInstalledCapacity = Param(M.REGION_YEAR_TECH_GENERATION,
                                      domain=NonNegativeReals)
    M.GenMaxEnergy = Param(M.REGION_YEAR_TECH_GENERATION,
                           domain=NonNegativeReals)
    M.GenFuel = Param(M.YEAR, M.TECH_GENERATION, domain=Any)
    M.GenCAPEX = Param(M.YEAR, M.TECH_GENERATION, domain=NonNegativeReals)
    M.GenOPEXfix = Param(M.YEAR, M.TECH_GENERATION, domain=NonNegativeReals)
    M.GenFullLoadEffi = Param(M.YEAR,
                              M.TECH_GENERATION,
                              domain=NonNegativeReals)
    M.GenOPEXvar = Param(M.YEAR, M.TECH_GENERATION, domain=NonNegativeReals)
    M.GenTLifetime = Param(M.YEAR, M.TECH_GENERATION, domain=NonNegativeReals)
    M.GenELifetime = Param(M.YEAR, M.TECH_GENERATION, domain=NonNegativeReals)
    M.GenWACC = Param(M.YEAR, M.TECH_GENERATION, domain=NonNegativeReals)
    M.EmissionFactor = Param(M.YEAR,
                             M.TECH_GENERATION,
                             domain=NonNegativeReals)
    M.CCSRatio = Param(M.YEAR, M.TECH_GENERATION, domain=Reals)

    # Nuclear LTO power plant match with existing Power Plant
    M.NM = Param(M.TECH_NUC, M.TECH_NUC, default=0, domain=NonNegativeReals)

    # Hydro dam
    M.HDMaxStock = Param(M.REGION_YEAR_TECH_HD, domain=NonNegativeReals)
    M.HDStorIniLevel = Param(M.REGION_YEAR_TECH_HD, domain=NonNegativeReals)
    M.HDEffi = Param(M.REGION_YEAR_TECH_HD, domain=NonNegativeReals)
    M.HDWeekInflow = Param(M.REGION_YEAR_TECH_HD,
                           M.WEEK,
                           domain=NonNegativeReals)
    M.HDMinLevel = Param(M.REGION_YEAR_TECH_HD,
                         M.WEEK,
                         domain=NonNegativeReals)
    M.HDMaxLevel = Param(M.REGION_YEAR_TECH_HD,
                         M.WEEK,
                         domain=NonNegativeReals)

    # Storage
    M.StorResidualPower = Param(M.REGION_YEAR_TECH_STORAGE,
                                domain=NonNegativeReals)
    M.StorMaxInstalledPower = Param(M.REGION_YEAR_TECH_STORAGE,
                                    domain=NonNegativeReals)
    M.StorCAPEXp = Param(M.YEAR, M.TECH_STORAGE, domain=NonNegativeReals)
    M.StorCAPEXe = Param(M.YEAR, M.TECH_STORAGE, domain=NonNegativeReals)
    M.StorOPEXfix = Param(M.YEAR, M.TECH_STORAGE, domain=NonNegativeReals)
    M.StorOPEXvar = Param(M.YEAR, M.TECH_STORAGE, domain=NonNegativeReals)
    M.StorTLifetime = Param(M.YEAR, M.TECH_STORAGE, domain=NonNegativeReals)
    M.StorELifetime = Param(M.YEAR, M.TECH_STORAGE, domain=NonNegativeReals)
    M.StorWACC = Param(M.YEAR, M.TECH_STORAGE, domain=NonNegativeReals)
    M.StorIni = Param(M.YEAR, M.TECH_STORAGE, domain=NonNegativeReals)
    M.StorCharEfficiency = Param(M.YEAR,
                                 M.TECH_STORAGE,
                                 domain=NonNegativeReals)
    M.StorDiscEfficiency = Param(M.YEAR,
                                 M.TECH_STORAGE,
                                 domain=NonNegativeReals)
    M.StorEnergyPowerRatio = Param(M.YEAR,
                                   M.TECH_STORAGE,
                                   domain=NonNegativeReals)

    # Transmission
    M.TransResidualImportCapacity = Param(M.LINE,
                                          M.YEAR,
                                          domain=NonNegativeReals)
    M.TransMaxInstalledImportCapacity = Param(M.LINE,
                                              M.YEAR,
                                              domain=NonNegativeReals)
    M.TransResidualExportCapacity = Param(M.LINE,
                                          M.YEAR,
                                          domain=NonNegativeReals)
    M.TransMaxInstalledExportCapacity = Param(M.LINE,
                                              M.YEAR,
                                              domain=NonNegativeReals)
    M.LineRegion = Param(M.LINE, M.REGION_ID, default=0)
    M.ContraryRegion = Param(M.LINE, M.REGION_ID, default=0)
    M.TransTech = Param(M.LINE, within=Any)
    M.TransDis = Param(M.LINE, domain=NonNegativeReals)
    M.TransCAPEXline = Param(M.YEAR,
                             M.TECH_TRANSMISSION,
                             domain=NonNegativeReals)
    M.TransCAPEXstation = Param(M.YEAR,
                                M.TECH_TRANSMISSION,
                                domain=NonNegativeReals)
    M.TransOPEXfixline = Param(M.YEAR,
                               M.TECH_TRANSMISSION,
                               domain=NonNegativeReals)
    M.TransOPEXfixstation = Param(M.YEAR,
                                  M.TECH_TRANSMISSION,
                                  domain=NonNegativeReals)
    M.TransTLifetime = Param(M.YEAR,
                             M.TECH_TRANSMISSION,
                             domain=NonNegativeReals)
    M.TransELifetime = Param(M.YEAR,
                             M.TECH_TRANSMISSION,
                             domain=NonNegativeReals)
    M.TransWACC = Param(M.YEAR, M.TECH_TRANSMISSION, domain=NonNegativeReals)
    M.TransLosses = Param(M.YEAR, M.TECH_TRANSMISSION, domain=NonNegativeReals)
    M.TransAvailability = Param(M.YEAR,
                                M.TECH_TRANSMISSION,
                                domain=NonNegativeReals)

    # Unit-commitment and Reserve
    M.GenSize = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.GenStarUpCost = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.GenMinPower = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.GenRampUpRate = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.GenRampDownRate = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.GenMinStartUpHour = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.GenMinShutDownHour = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.GenFCRup = Param(M.YEAR, M.TECH_FCRup, domain=NonNegativeReals)
    M.GenFCRdown = Param(M.YEAR, M.TECH_FCRdown, domain=NonNegativeReals)
    M.GenAFRRup = Param(M.YEAR, M.TECH_aFRRup, domain=NonNegativeReals)
    M.GenAFRRdown = Param(M.YEAR, M.TECH_aFRRdown, domain=NonNegativeReals)
    M.GenMFRRup = Param(M.YEAR, M.TECH_mFRRup, domain=NonNegativeReals)
    M.GenMFRRdown = Param(M.YEAR, M.TECH_mFRRdown, domain=NonNegativeReals)

    M.StorStarUpCost = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.StorSize = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.StorMinPower = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.StorRampUpRate = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.StorRampDownRate = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.StorMinStartUpHour = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.StorMinShutDownHour = Param(M.YEAR, M.TECH_UC, domain=NonNegativeReals)
    M.StorFCRup = Param(M.YEAR, M.TECH_FCRup, domain=NonNegativeReals)
    M.StorFCRdown = Param(M.YEAR, M.TECH_FCRdown, domain=NonNegativeReals)
    M.StorAFRRup = Param(M.YEAR, M.TECH_aFRRup, domain=NonNegativeReals)
    M.StorAFRRdown = Param(M.YEAR, M.TECH_aFRRdown, domain=NonNegativeReals)
    M.StorMFRRup = Param(M.YEAR, M.TECH_mFRRup, domain=NonNegativeReals)
    M.StorMFRRdown = Param(M.YEAR, M.TECH_mFRRdown, domain=NonNegativeReals)

    M.FCRRequired = Param(M.REGION_ID, M.YEAR, domain=NonNegativeReals)
    M.ErrAFRRup = Param(M.TECH_VRES, domain=NonNegativeReals)
    M.ErrAFRRdown = Param(M.TECH_VRES, domain=NonNegativeReals)
    M.ErrMFRRup = Param(M.TECH_VRES, domain=NonNegativeReals)
    M.ErrMFRRdown = Param(M.TECH_VRES, domain=NonNegativeReals)
    M.DErrAFRRup = Param(domain=NonNegativeReals)
    M.DErrAFRRdown = Param(domain=NonNegativeReals)
    M.DErrMFRRup = Param(domain=NonNegativeReals)
    M.DErrMFRRdown = Param(domain=NonNegativeReals)

    # Others
    M.SDR = Param(domain=NonNegativeReals)
    M.REFYEAR = Param(default=2020, domain=NonNegativeReals)
    M.AnnualMaxEmission = Param(M.REGION_ID, M.YEAR, domain=NonNegativeReals)
    M.EmissionBudget = Param(M.REGION_ID, domain=NonNegativeReals)
    M.RESPer = Param(M.REGION_ID, M.YEAR, domain=NonNegativeReals,
                     default=0)  # RES percentage minimum
    M.NUCPer = Param(M.REGION_ID, M.YEAR, domain=NonNegativeReals,
                     default=1)  # NUC percentage maximum
    M.CO2Cost = Param(M.YEAR, domain=NonNegativeReals)
    M.PERIODYEAR = Param(M.YEAR, domain=NonNegativeReals)
    M.HydrogenNeeds = Param(M.REGION_ID, M.YEAR,
                            domain=NonNegativeReals)  # HydrogenNeeds
    M.FlexBiogasQuantity = Param(
        M.REGION_ID, M.YEAR,
        domain=NonNegativeReals)  # Flexible Biogas Quantity
    M.BiogasPrice = Param(M.REGION_ID, M.YEAR,
                          domain=NonNegativeReals)  # Flexible Biogas Price

    # DSM load shedding
    M.DSMSheddingCapacity = Param(M.REGION_ID, M.YEAR, domain=NonNegativeReals)
    M.DSMSheddingOPEXfix = Param(M.REGION_ID, M.YEAR, domain=NonNegativeReals)
    M.DSMSheddingOPEXvar = Param(M.REGION_ID, M.YEAR, domain=NonNegativeReals)

    ###########################################VARIABLE##################################################
    ## cost
    M.regionalcost = Var(M.REGION_ID, domain=NonNegativeReals, initialize=0)
    M.regionalcostinv = Var(M.REGION_ID, domain=NonNegativeReals, initialize=0)
    M.regionalcostfix = Var(M.REGION_ID, domain=NonNegativeReals, initialize=0)
    M.regionalcostvar = Var(M.REGION_ID, domain=NonNegativeReals, initialize=0)
    M.regionalcostco2 = Var(M.REGION_ID, domain=NonNegativeReals, initialize=0)

    # investement cost
    M.regionalyearcostinv = Var(M.REGION_ID,
                                M.YEAR,
                                domain=NonNegativeReals,
                                initialize=0)
    M.regionalyearcostinvgen = Var(M.REGION_ID,
                                   M.YEAR,
                                   domain=NonNegativeReals,
                                   initialize=0)
    M.regionalyearcostinvstor = Var(M.REGION_ID,
                                    M.YEAR,
                                    domain=NonNegativeReals,
                                    initialize=0)
    M.regionalyearcostinvgrid = Var(M.REGION_ID,
                                    M.YEAR,
                                    domain=NonNegativeReals,
                                    initialize=0)
    M.regionalyearcostinvgentech = Var(M.REGION_YEAR_TECH_GENERATION,
                                       domain=NonNegativeReals,
                                       initialize=0)
    M.regionalyearcostinvstortech = Var(M.REGION_YEAR_TECH_STORAGE,
                                        domain=NonNegativeReals,
                                        initialize=0)
    M.regionalyearcostinvgridline = Var(M.REGION_ID,
                                        M.YEAR,
                                        M.LINE,
                                        domain=NonNegativeReals,
                                        initialize=0)

    # fixed operaion and maintenance cost
    M.regionalyearcostfix = Var(M.REGION_ID,
                                M.YEAR,
                                domain=NonNegativeReals,
                                initialize=0)
    M.regionalyearcostfixgen = Var(M.REGION_ID,
                                   M.YEAR,
                                   domain=NonNegativeReals,
                                   initialize=0)
    M.regionalyearcostfixstor = Var(M.REGION_ID,
                                    M.YEAR,
                                    domain=NonNegativeReals,
                                    initialize=0)
    M.regionalyearcostfixgrid = Var(M.REGION_ID,
                                    M.YEAR,
                                    domain=NonNegativeReals,
                                    initialize=0)
    M.regionalyearcostfixloadshedding = Var(M.REGION_ID,
                                            M.YEAR,
                                            domain=NonNegativeReals,
                                            initialize=0)
    M.regionalyearcostfixgentech = Var(M.REGION_YEAR_TECH_GENERATION,
                                       domain=NonNegativeReals,
                                       initialize=0)
    M.regionalyearcostfixstortech = Var(M.REGION_YEAR_TECH_STORAGE,
                                        domain=NonNegativeReals,
                                        initialize=0)
    M.regionalyearcostfixgridline = Var(M.REGION_ID,
                                        M.YEAR,
                                        M.LINE,
                                        domain=NonNegativeReals,
                                        initialize=0)

    # variable operaion and maintenance cost
    M.regionalyearcostvar = Var(M.REGION_ID,
                                M.YEAR,
                                domain=NonNegativeReals,
                                initialize=0)
    M.regionalyearcostvargen = Var(M.REGION_ID,
                                   M.YEAR,
                                   domain=NonNegativeReals,
                                   initialize=0)
    M.regionalyearcostvarstor = Var(M.REGION_ID,
                                    M.YEAR,
                                    domain=NonNegativeReals,
                                    initialize=0)
    M.regionalyearcostvargentech = Var(M.REGION_YEAR_TECH_GENERATION,
                                       domain=NonNegativeReals,
                                       initialize=0)
    M.regionalyearcostvarstortech = Var(M.REGION_YEAR_TECH_STORAGE,
                                        domain=NonNegativeReals,
                                        initialize=0)
    M.regionalyearcostvarloadshedding = Var(M.REGION_ID,
                                            M.YEAR,
                                            domain=NonNegativeReals,
                                            initialize=0)
    M.regionalyearcostvarstartup = Var(M.REGION_ID,
                                       M.YEAR,
                                       domain=NonNegativeReals,
                                       initialize=0)
    M.regionalyearcostvarstartuptech = Var(M.REGION_YEAR_TECH_UC,
                                           domain=NonNegativeReals,
                                           initialize=0)

    # co2 cost
    M.regionalyearcostco2 = Var(M.REGION_ID,
                                M.YEAR,
                                domain=NonNegativeReals,
                                initialize=0)

    M.regionalyearcost = Var(M.REGION_ID,
                             M.YEAR,
                             domain=NonNegativeReals,
                             initialize=0)

    ## capacity
    M.newinstalledgencapacity = Var(M.REGION_YEAR_TECH_GENERATION,
                                    domain=NonNegativeReals,
                                    initialize=0)
    M.accunewinstalledgencapacity = Var(M.REGION_YEAR_TECH_GENERATION,
                                        domain=NonNegativeReals,
                                        initialize=0)
    M.totalinstalledgencapacity = Var(M.REGION_YEAR_TECH_GENERATION,
                                      domain=NonNegativeReals,
                                      initialize=0)

    M.newinstalledstorpower = Var(M.REGION_YEAR_TECH_STORAGE,
                                  domain=NonNegativeReals,
                                  initialize=0)
    M.accunewinstalledstorpower = Var(M.REGION_YEAR_TECH_STORAGE,
                                      domain=NonNegativeReals,
                                      initialize=0)
    M.totalinstalledstorpower = Var(M.REGION_YEAR_TECH_STORAGE,
                                    domain=NonNegativeReals,
                                    initialize=0)
    M.newinstalledstorenergy = Var(M.REGION_YEAR_TECH_STORAGE,
                                   domain=NonNegativeReals,
                                   initialize=0)
    M.accunewinstalledstorenergy = Var(M.REGION_YEAR_TECH_STORAGE,
                                       domain=NonNegativeReals,
                                       initialize=0)
    M.totalinstalledstorenergy = Var(M.REGION_YEAR_TECH_STORAGE,
                                     domain=NonNegativeReals,
                                     initialize=0)
    M.totalinstalledstordiscpower = Var(M.REGION_YEAR_TECH_STORAGE,
                                        domain=NonNegativeReals,
                                        initialize=0)

    M.newinstalledimporttranscapacity = Var(M.LINE,
                                            M.YEAR,
                                            domain=NonNegativeReals,
                                            initialize=0)
    M.accunewinstalledimporttranscapacity = Var(M.LINE,
                                                M.YEAR,
                                                domain=NonNegativeReals,
                                                initialize=0)
    M.totalinstalledimporttranscapacity = Var(M.LINE,
                                              M.YEAR,
                                              domain=NonNegativeReals,
                                              initialize=0)
    M.newinstalledexporttranscapacity = Var(M.LINE,
                                            M.YEAR,
                                            domain=NonNegativeReals,
                                            initialize=0)
    M.accunewinstalledexporttranscapacity = Var(M.LINE,
                                                M.YEAR,
                                                domain=NonNegativeReals,
                                                initialize=0)
    M.totalinstalledexporttranscapacity = Var(M.LINE,
                                              M.YEAR,
                                              domain=NonNegativeReals,
                                              initialize=0)

    # production
    M.electechgen = Var(M.REGION_YEAR_TECH_GENERATION,
                        M.TIMESLICE,
                        domain=NonNegativeReals,
                        initialize=0)
    M.electechtpp = Var(M.REGION_YEAR_TECH_TPP,
                        M.TIMESLICE,
                        domain=NonNegativeReals,
                        initialize=0)
    M.electechvres = Var(M.REGION_YEAR_TECH_VRES,
                         M.TIMESLICE,
                         domain=NonNegativeReals,
                         initialize=0)
    M.electechhd = Var(M.REGION_YEAR_TECH_HD,
                       M.TIMESLICE,
                       domain=NonNegativeReals,
                       initialize=0)
    M.electechnaturalgas = Var(M.REGION_YEAR_TECH_GAS,
                               M.TIMESLICE,
                               domain=NonNegativeReals,
                               initialize=0)
    M.electechbiogas = Var(M.REGION_YEAR_TECH_GAS,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)
    M.electechgtp = Var(M.REGION_YEAR_TECH_GAS,
                        M.TIMESLICE,
                        domain=NonNegativeReals,
                        initialize=0)
    M.annualelectechgen = Var(M.REGION_YEAR_TECH_GENERATION,
                              domain=NonNegativeReals,
                              initialize=0)
    M.annualelecnaturalgas = Var(M.REGION_ID,
                                 M.YEAR,
                                 domain=NonNegativeReals,
                                 initialize=0)
    M.annualelecbiogas = Var(M.REGION_ID,
                             M.YEAR,
                             domain=NonNegativeReals,
                             initialize=0)
    M.annualelecgtp = Var(M.REGION_ID,
                          M.YEAR,
                          domain=NonNegativeReals,
                          initialize=0)
    M.annualelecgen = Var(M.REGION_ID,
                          M.YEAR,
                          domain=NonNegativeReals,
                          initialize=0)
    M.annualelecnucgen = Var(M.REGION_ID,
                             M.YEAR,
                             domain=NonNegativeReals,
                             initialize=0)
    M.annualelecfossilgen = Var(M.REGION_ID,
                                M.YEAR,
                                domain=NonNegativeReals,
                                initialize=0)
    # Hydro dam
    M.elechdweekinilevel = Var(M.REGION_YEAR_TECH_HD,
                               M.WEEK,
                               domain=NonNegativeReals,
                               initialize=0)
    M.elechdweekprod = Var(M.REGION_YEAR_TECH_HD,
                           M.WEEK,
                           domain=NonNegativeReals,
                           initialize=0)

    # Storage
    M.electechchar = Var(M.REGION_YEAR_TECH_STORAGE,
                         M.TIMESLICE,
                         domain=NonNegativeReals,
                         initialize=0)
    M.annualelectechchar = Var(M.REGION_YEAR_TECH_STORAGE,
                               domain=NonNegativeReals,
                               initialize=0)
    M.electechdisc = Var(M.REGION_YEAR_TECH_STORAGE,
                         M.TIMESLICE,
                         domain=NonNegativeReals,
                         initialize=0)
    M.annualelectechdisc = Var(M.REGION_YEAR_TECH_STORAGE,
                               domain=NonNegativeReals,
                               initialize=0)
    M.electechstored = Var(M.REGION_YEAR_TECH_STORAGE,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)

    # transmission
    M.eleclexchange = Var(M.LINE, M.YEAR, M.TIMESLICE, initialize=0)
    M.elecexchange = Var(M.REGION_ID, M.YEAR, M.TIMESLICE, initialize=0)
    M.annualelecexchange = Var(M.REGION_ID, M.YEAR, initialize=0)

    # excess
    M.elecexcess = Var(M.REGION_ID,
                       M.YEAR,
                       M.TIMESLICE,
                       domain=NonNegativeReals,
                       initialize=0)
    M.annualelecexcess = Var(M.REGION_ID,
                             M.YEAR,
                             domain=NonNegativeReals,
                             initialize=0)

    # load shedding
    M.elecloadshedding = Var(M.REGION_ID,
                             M.YEAR,
                             M.TIMESLICE,
                             domain=NonNegativeReals,
                             initialize=0)
    M.annualelecloadshedding = Var(M.REGION_ID,
                                   M.YEAR,
                                   domain=NonNegativeReals,
                                   initialize=0)

    # demand
    M.annualdemand = Var(M.REGION_ID,
                         M.YEAR,
                         domain=NonNegativeReals,
                         initialize=0)

    # Unit commitment
    M.eleccommitnumbergen = Var(M.REGION_YEAR_TECH_UC_Gen,
                                M.TIMESLICE,
                                domain=NonNegativeReals,
                                initialize=0)
    M.eleccommitnumberstorchar = Var(M.REGION_YEAR_TECH_UC_Stor,
                                     M.TIMESLICE,
                                     domain=NonNegativeReals,
                                     initialize=0)
    M.eleccommitnumberstordisc = Var(M.REGION_YEAR_TECH_UC_Stor,
                                     M.TIMESLICE,
                                     domain=NonNegativeReals,
                                     initialize=0)

    M.eleccommitgen = Var(M.REGION_YEAR_TECH_UC_Gen,
                          M.TIMESLICE,
                          domain=NonNegativeReals,
                          initialize=0)
    M.eleccommitstorchar = Var(M.REGION_YEAR_TECH_UC_Stor,
                               M.TIMESLICE,
                               domain=NonNegativeReals,
                               initialize=0)
    M.eleccommitstordisc = Var(M.REGION_YEAR_TECH_UC_Stor,
                               M.TIMESLICE,
                               domain=NonNegativeReals,
                               initialize=0)

    M.elecstartupgen = Var(M.REGION_YEAR_TECH_UC_Gen,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)
    M.elecstartupstorchar = Var(M.REGION_YEAR_TECH_UC_Stor,
                                M.TIMESLICE,
                                domain=NonNegativeReals,
                                initialize=0)
    M.elecstartupstordisc = Var(M.REGION_YEAR_TECH_UC_Stor,
                                M.TIMESLICE,
                                domain=NonNegativeReals,
                                initialize=0)
    M.elecshutdowngen = Var(M.REGION_YEAR_TECH_UC_Gen,
                            M.TIMESLICE,
                            domain=NonNegativeReals,
                            initialize=0)
    M.elecshutdownstorchar = Var(M.REGION_YEAR_TECH_UC_Stor,
                                 M.TIMESLICE,
                                 domain=NonNegativeReals,
                                 initialize=0)
    M.elecshutdownstordisc = Var(M.REGION_YEAR_TECH_UC_Stor,
                                 M.TIMESLICE,
                                 domain=NonNegativeReals,
                                 initialize=0)

    # Reserve
    M.aFRRuprequired = Var(M.REGION_ID,
                           M.YEAR,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)
    M.aFRRdownrequired = Var(M.REGION_ID,
                             M.YEAR,
                             M.TIMESLICE,
                             domain=NonNegativeReals,
                             initialize=0)
    M.mFRRuprequired = Var(M.REGION_ID,
                           M.YEAR,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)
    M.mFRRdownrequired = Var(M.REGION_ID,
                             M.YEAR,
                             M.TIMESLICE,
                             domain=NonNegativeReals,
                             initialize=0)

    M.aFCRupGen = Var(M.REGION_YEAR_TECH_Gen_FCRup,
                      M.TIMESLICE,
                      domain=NonNegativeReals,
                      initialize=0)

    M.aFCRdownGen = Var(M.REGION_YEAR_TECH_Gen_FCRdown,
                        M.TIMESLICE,
                        domain=NonNegativeReals,
                        initialize=0)

    M.aFRRupGen = Var(M.REGION_YEAR_TECH_Gen_aFRRup,
                      M.TIMESLICE,
                      domain=NonNegativeReals,
                      initialize=0)

    M.aFRRdownGen = Var(M.REGION_YEAR_TECH_Gen_aFRRdown,
                        M.TIMESLICE,
                        domain=NonNegativeReals,
                        initialize=0)

    M.mFRRupGen = Var(M.REGION_YEAR_TECH_Gen_mFRRup,
                      M.TIMESLICE,
                      domain=NonNegativeReals,
                      initialize=0)

    M.mFRRdownGen = Var(M.REGION_YEAR_TECH_Gen_mFRRdown,
                        M.TIMESLICE,
                        domain=NonNegativeReals,
                        initialize=0)

    M.aFCRupStorChar = Var(M.REGION_YEAR_TECH_Stor_FCRup,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)

    M.aFCRdownStorChar = Var(M.REGION_YEAR_TECH_Stor_FCRdown,
                             M.TIMESLICE,
                             domain=NonNegativeReals,
                             initialize=0)

    M.aFRRupStorChar = Var(M.REGION_YEAR_TECH_Stor_aFRRup,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)

    M.aFRRdownStorChar = Var(M.REGION_YEAR_TECH_Stor_aFRRdown,
                             M.TIMESLICE,
                             domain=NonNegativeReals,
                             initialize=0)

    M.mFRRupStorChar = Var(M.REGION_YEAR_TECH_Stor_mFRRup,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)

    M.mFRRdownStorChar = Var(M.REGION_YEAR_TECH_Stor_mFRRdown,
                             M.TIMESLICE,
                             domain=NonNegativeReals,
                             initialize=0)

    M.aFCRupStorDisc = Var(M.REGION_YEAR_TECH_Stor_FCRup,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)

    M.aFCRdownStorDisc = Var(M.REGION_YEAR_TECH_Stor_FCRdown,
                             M.TIMESLICE,
                             domain=NonNegativeReals,
                             initialize=0)

    M.aFRRupStorDisc = Var(M.REGION_YEAR_TECH_Stor_aFRRup,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)

    M.aFRRdownStorDisc = Var(M.REGION_YEAR_TECH_Stor_aFRRdown,
                             M.TIMESLICE,
                             domain=NonNegativeReals,
                             initialize=0)

    M.mFRRupStorDisc = Var(M.REGION_YEAR_TECH_Stor_mFRRup,
                           M.TIMESLICE,
                           domain=NonNegativeReals,
                           initialize=0)

    M.mFRRdownStorDisc = Var(M.REGION_YEAR_TECH_Stor_mFRRdown,
                             M.TIMESLICE,
                             domain=NonNegativeReals,
                             initialize=0)

    # Emission
    M.annualemission = Var(M.REGION_ID,
                           M.YEAR,
                           domain=NonNegativeReals,
                           initialize=0)

    # RES / nuclear / fossil  percentage with respect to demand
    M.respercentage = Var(M.REGION_ID,
                          M.YEAR,
                          domain=NonNegativeReals,
                          initialize=0)
    M.irescapacity = Var(M.REGION_ID,
                         M.YEAR,
                         domain=NonNegativeReals,
                         initialize=0)
    M.nucpercentage = Var(M.REGION_ID,
                          M.YEAR,
                          domain=NonNegativeReals,
                          initialize=0)
    M.fossilpercentage = Var(M.REGION_ID,
                             M.YEAR,
                             domain=NonNegativeReals,
                             initialize=0)

    # Hydrogen and gas stored
    M.gasstored = Var(M.REGION_ID,
                      M.YEAR,
                      domain=NonNegativeReals,
                      initialize=0)

    ###########################################OBJECTIVE##################################################

    M.obj = Objective(sense=minimize, rule=obj_rule, doc='total_costs')

    ###########################################CONSTRAINTS##################################################

    # Costs constraints
    M.RegionalCost = Constraint(M.REGION_ID, rule=RegionalCost_rule)
    M.RegionalCostInv = Constraint(M.REGION_ID, rule=RegionalCostInv_rule)
    M.RegionalCostFix = Constraint(M.REGION_ID, rule=RegionalCostFix_rule)
    M.RegionalCostVar = Constraint(M.REGION_ID, rule=RegionalCostVar_rule)
    M.RegionalCostCO2 = Constraint(M.REGION_ID, rule=RegionalCostCO2_rule)

    M.RegionalYearCostInv = Constraint(M.REGION_ID,
                                       M.YEAR,
                                       rule=RegionalYearCostInv_rule)
    M.RegionalYearCostInvGen = Constraint(M.REGION_ID,
                                          M.YEAR,
                                          rule=RegionalYearCostInvGen_rule)
    M.RegionalYearCostInvStor = Constraint(M.REGION_ID,
                                           M.YEAR,
                                           rule=RegionalYearCostInvStor_rule)
    M.RegionalYearCostInvGrid = Constraint(M.REGION_ID,
                                           M.YEAR,
                                           rule=RegionalYearCostInvGrid_rule)
    M.RegionalYearCostInvGenTech = Constraint(
        M.REGION_YEAR_TECH_GENERATION, rule=RegionalYearCostInvGenTech_rule)
    M.RegionalYearCostInvStorTech = Constraint(
        M.REGION_YEAR_TECH_STORAGE, rule=RegionalYearCostInvStorTech_rule)
    M.RegionalYearCostInvGridLine = Constraint(
        M.REGION_ID, M.YEAR, M.LINE, rule=RegionalYearCostInvGridLine_rule)

    M.RegionalYearCostFix = Constraint(M.REGION_ID,
                                       M.YEAR,
                                       rule=RegionalYearCostFix_rule)
    M.RegionalYearCostFixGen = Constraint(M.REGION_ID,
                                          M.YEAR,
                                          rule=RegionalYearCostFixGen_rule)
    M.RegionalYearCostFixStor = Constraint(M.REGION_ID,
                                           M.YEAR,
                                           rule=RegionalYearCostFixStor_rule)
    M.RegionalYearCostFixGrid = Constraint(M.REGION_ID,
                                           M.YEAR,
                                           rule=RegionalYearCostFixGrid_rule)
    M.RegionalYearCostFixLoadShedding = Constraint(
        M.REGION_ID, M.YEAR, rule=RegionalYearCostFixLoadShedding_rule)
    M.RegionalYearCostFixGenTech = Constraint(
        M.REGION_YEAR_TECH_GENERATION, rule=RegionalYearCostFixGenTech_rule)
    M.RegionalYearCostFixStorTech = Constraint(
        M.REGION_YEAR_TECH_STORAGE, rule=RegionalYearCostFixStorTech_rule)
    M.RegionalYearCostFixGridLine = Constraint(
        M.REGION_ID, M.YEAR, M.LINE, rule=RegionalYearCostFixGridLine_rule)

    M.RegionalYearCostVar = Constraint(M.REGION_ID,
                                       M.YEAR,
                                       rule=RegionalYearCostVar_rule)
    M.RegionalYearCostVarGen = Constraint(M.REGION_ID,
                                          M.YEAR,
                                          rule=RegionalYearCostVarGen_rule)
    M.RegionalYearCostVarStor = Constraint(M.REGION_ID,
                                           M.YEAR,
                                           rule=RegionalYearCostVarStor_rule)
    M.RegionalYearCostVarGenTech = Constraint(
        M.REGION_YEAR_TECH_GENERATION, rule=RegionalYearCostVarGenTech_rule)
    M.RegionalYearCostVarStorTech = Constraint(
        M.REGION_YEAR_TECH_STORAGE, rule=RegionalYearCostVarStorTech_rule)
    M.RegionalYearCostVarLoadShedding = Constraint(
        M.REGION_ID, M.YEAR, rule=RegionalYearCostVarLoadShedding_rule)
    M.RegionalYearCostVarStartUp = Constraint(
        M.REGION_ID, M.YEAR, rule=RegionalYearCostVarStartUp_rule)
    M.RegionalYearCostVarStartUpTech = Constraint(
        M.REGION_YEAR_TECH_UC, rule=RegionalYearCostVarStartUpTech_rule)

    M.RegionalYearCostCO2 = Constraint(M.REGION_ID,
                                       M.YEAR,
                                       rule=RegionalYearCostCO2_rule)

    M.RegionalYearCost = Constraint(M.REGION_ID,
                                    M.YEAR,
                                    rule=RegionalYearCost_rule)

    # Capacity constraints
    M.TotalInstalledGenCapacityConstraint = Constraint(
        M.REGION_YEAR_TECH_GENERATION,
        rule=TotalInstalledGenCapacityConstraint_rule)
    M.AccuNewGenCapacityConstraint = Constraint(
        M.REGION_YEAR_TECH_GENERATION, rule=AccuNewGenCapacityConstraint_rule)
    M.NewNUCLTOCapacityConstraint = Constraint(
        M.REGION_YEAR_TECH_NUC,
        M.REGION_YEAR_TECH_NUC,
        rule=NewNUCLTOCapacityConstraint_rule)
    M.MaxElecGenCapacityConstraint = Constraint(
        M.REGION_YEAR_TECH_GENERATION, rule=MaxElecGenCapacityConstraint_rule)
    M.TotalInstalledStorPowerConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE,
        rule=TotalInstalledStorPowerConstraint_rule)
    M.AccuNewStorPowerConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE, rule=AccuNewStorPowerConstraint_rule)
    M.NewStorEnergyConstraint = Constraint(M.REGION_YEAR_TECH_STORAGE,
                                           rule=NewStorEnergyConstraint_rule)
    M.AccuNewStorEnergyConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE, rule=AccuNewStorEnergyConstraint_rule)
    M.TotalInstalledStorEnergyConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE,
        rule=TotalInstalledStorEnergyConstraint_rule)
    M.TotalInstalledImportTransCapacityConstraint = Constraint(
        M.LINE, M.YEAR, rule=TotalInstalledImportTransCapacityConstraint_rule)
    M.AccuNewImportTransCapacityConstraint = Constraint(
        M.LINE, M.YEAR, rule=AccuNewImportTransCapacityConstraint_rule)
    M.TotalInstalledExportTransCapacityConstraint = Constraint(
        M.LINE, M.YEAR, rule=TotalInstalledExportTransCapacityConstraint_rule)
    M.AccuNewExportTransCapacityConstraint = Constraint(
        M.LINE, M.YEAR, rule=AccuNewExportTransCapacityConstraint_rule)

    # Electricity balance
    M.ElecBalanceConstraint = Constraint(M.REGION_ID,
                                         M.YEAR,
                                         M.TIMESLICE,
                                         rule=ElecBalanceConstraint_rule)
    M.ElecTechGenConstraint = Constraint(M.REGION_YEAR_TECH_GENERATION,
                                         M.TIMESLICE,
                                         rule=ElecTechGenConstraint_rule)
    M.AnnualElecTechGenConstraint = Constraint(
        M.REGION_YEAR_TECH_GENERATION, rule=AnnualElecTechGenConstraint_rule)
    M.AnnualElecGenConstraint = Constraint(M.REGION_ID,
                                           M.YEAR,
                                           rule=AnnualElecGenConstraint_rule)
    M.AnnualElecNucGenConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=AnnualElecNucGenConstraint_rule)
    M.AnnualElecNaturalGasConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=AnnualElecNaturalGasConstraint_rule)
    M.AnnualElecBioGasConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=AnnualElecBioGasConstraint_rule)
    M.AnnualElecGtPConstraint = Constraint(M.REGION_ID,
                                           M.YEAR,
                                           rule=AnnualElecGtPConstraint_rule)
    M.AnnualElecFossilGenConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=AnnualElecFossilGenConstraint_rule)
    M.AnnualElecTechCharConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE, rule=AnnualElecTechCharConstraint_rule)
    M.AnnualElecTechDiscConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE, rule=AnnualElecTechDiscConstraint_rule)
    M.AnnualElecExcessConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=AnnualElecExcessConstraint_rule)
    M.AnnualElecLoadSheddingConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=AnnualElecLoadSheddingConstraint_rule)
    M.AnnualDemandConstraint = Constraint(M.REGION_ID,
                                          M.YEAR,
                                          rule=AnnualDemandConstraint_rule)

    # Generation constraints
    M.ElecVRESCapacityConstraint = Constraint(
        M.REGION_YEAR_TECH_VRES,
        M.TIMESLICE,
        rule=ElecVRESCapacityConstraint_rule)
    M.ElecTPPCapacityConstraint = Constraint(
        M.REGION_YEAR_TECH_TPP,
        M.TIMESLICE,
        rule=ElecTPPCapacityConstraint_rule)
    M.ElecMustRunMinConstraint = Constraint(M.REGION_YEAR_TECH_MustRun,
                                            M.TIMESLICE,
                                            rule=ElecMustRunMinConstraint_rule)
    M.ElecHDCapacityConstraint = Constraint(M.REGION_YEAR_TECH_HD,
                                            M.TIMESLICE,
                                            rule=ElecHDCapacityConstraint_rule)

    # Bioenergy constraints
    M.MaxAnnualEnergyGenConstraint = Constraint(
        M.REGION_YEAR_TECH_TPP, rule=MaxAnnualEnergyGenConstraint_rule)

    # Hydro dam constraints
    M.ElecHDWeekIniLevelConstraint = Constraint(
        M.REGION_YEAR_TECH_HD, M.WEEK, rule=ElecHDWeekIniLevelConstraint_rule)
    M.ElecHDWeekMinLevelConstraint = Constraint(
        M.REGION_YEAR_TECH_HD, M.WEEK, rule=ElecHDWeekMinLevelConstraint_rule)
    M.ElecHDWeekMaxLevelConstraint = Constraint(
        M.REGION_YEAR_TECH_HD, M.WEEK, rule=ElecHDWeekMaxLevelConstraint_rule)
    M.ElecHDWeekProdConstraint = Constraint(M.REGION_YEAR_TECH_HD,
                                            M.WEEK,
                                            rule=ElecHDWeekProdConstraint_rule)

    # Storage constraints
    M.ElecTechStoredConstraint = Constraint(M.REGION_YEAR_TECH_STORAGE,
                                            M.TIMESLICE,
                                            rule=ElecTechStoredConstraint_rule)
    M.MaxElecStorPowerConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE, rule=MaxElecStorPowerConstraint_rule)
    M.MaxElecTechStoredConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE,
        M.TIMESLICE,
        rule=MaxElecTechStoredConstraint_rule)
    M.MaxElecTechCharDiscConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE,
        M.TIMESLICE,
        rule=MaxElecTechCharDiscConstraint_rule)

    # DSM load shifting constraints
    M.MaxDSMShiftCharConstraint = Constraint(
        M.REGION_YEAR_TECH_DSM,
        M.TIMESLICE,
        rule=MaxDSMShiftCharConstraint_rule)
    M.MaxDSMShiftDiscConstraint = Constraint(
        M.REGION_YEAR_TECH_DSM,
        M.TIMESLICE,
        rule=MaxDSMShiftDiscConstraint_rule)

    # DSM load shedding constraints
    M.MaxDSMSheddingConstraint = Constraint(M.REGION_ID,
                                            M.YEAR,
                                            M.TIMESLICE,
                                            rule=MaxDSMSheddingConstraint_rule)

    # Gas power plant gas source constraints
    M.GasPPGasSourceConstraint = Constraint(M.REGION_YEAR_TECH_GAS,
                                            M.TIMESLICE,
                                            rule=GasPPGasSourceConstraint_rule)

    # Flexible biogas quantity constraints
    M.FlexibleBiogasQuantityConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=FlexibleBiogasQuantityConstraint_rule)

    # PtG constraints
    M.TotalInstalledStorDiscPowerConstraint = Constraint(
        M.REGION_YEAR_TECH_STORAGE,
        M.REGION_YEAR_TECH_GAS,
        rule=TotalInstalledStorDiscPowerConstraint_rule)
    M.PTGDiscConstraint = Constraint(M.REGION_ID,
                                     M.YEAR,
                                     M.TECH_PTG,
                                     M.TIMESLICE,
                                     rule=PTGDiscConstraint_rule)

    # PtH constraints
    M.HydrogenNeedsConstraint = Constraint(M.REGION_YEAR_TECH_PTH,
                                           M.TIMESLICE,
                                           rule=HydrogenNeedsConstraint_rule)
    M.NoPTHDischargeConstraint = Constraint(M.REGION_YEAR_TECH_PTH,
                                            M.TIMESLICE,
                                            rule=NoPTHDischargeConstraint_rule)

    # Transmission contraints
    M.MaxElecImportTransCapacityConstraint = Constraint(
        M.LINE, M.YEAR, rule=MaxElecImportTransCapacityConstraint_rule)
    M.MaxElecExportTransCapacityConstraint = Constraint(
        M.LINE, M.YEAR, rule=MaxElecExportTransCapacityConstraint_rule)
    M.ElecImportExportTransCapacityConstraint = Constraint(
        M.LINE, M.YEAR, rule=ElecImportExportTransCapacityConstraint_rule)
    M.TransImpCapacityLimitConstraint = Constraint(
        M.LINE, M.YEAR, M.TIMESLICE, rule=TransImpCapacityLimitConstraint_rule)
    M.TransExpCapacityLimitConstraint = Constraint(
        M.LINE, M.YEAR, M.TIMESLICE, rule=TransExpCapacityLimitConstraint_rule)
    M.ElecRegionalExchangeConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ElecRegionalExchangeConstraint_rule)
    M.AnnualElecExchangeConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=AnnualElecExchangeConstraint_rule)

    # Unit commitment
    M.ElecCommitNumberGenConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Gen,
        M.TIMESLICE,
        rule=ElecCommitNumberGenConstraint_rule)
    M.ElecCommitGenConstraint = Constraint(M.REGION_YEAR_TECH_UC_Gen,
                                           M.TIMESLICE,
                                           rule=ElecCommitGenConstraint_rule)
    M.ElecCommitBalanceGenConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Gen,
        M.TIMESLICE,
        rule=ElecCommitBalanceGenConstraint_rule)
    M.ElecCommitNumberStorCharConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecCommitNumberStorCharConstraint_rule)
    M.ElecCommitStorConstraint = Constraint(M.REGION_YEAR_TECH_UC_Stor,
                                            M.TIMESLICE,
                                            rule=ElecCommitStorConstraint_rule)
    M.ElecCommitBalanceStorCharConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecCommitBalanceStorCharConstraint_rule)
    M.ElecCommitNumberStorDiscConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecCommitNumberStorDiscConstraint_rule)
    M.ElecCommitBalanceStorDiscConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecCommitBalanceStorDiscConstraint_rule)

    M.ElecMinOutputGenConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Gen,
        M.TIMESLICE,
        rule=ElecMinOutputGenConstraint_rule)
    M.ElecMinOutputGenQuickStartConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Gen,
        M.TIMESLICE,
        rule=ElecMinOutputGenQuickStartConstraint_rule)
    M.ElecMinOutputStorCharConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMinOutputStorCharConstraint_rule)
    M.ElecMinOutputStorCharQuickStartConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMinOutputStorCharQuickStartConstraint_rule)
    M.ElecMinOutputStorDiscConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMinOutputStorDiscConstraint_rule)
    M.ElecMinOutputStorDiscQuickStartConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMinOutputStorDiscQuickStartConstraint_rule)
    M.ElecMaxOutputGenConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Gen,
        M.TIMESLICE,
        rule=ElecMaxOutputGenConstraint_rule)
    M.ElecMaxOutputGenQuickStartConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Gen,
        M.TIMESLICE,
        rule=ElecMaxOutputGenQuickStartConstraint_rule)
    M.ElecMaxOutputStorCharConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMaxOutputStorCharConstraint_rule)
    M.ElecMaxOutputStorCharQuickStartConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMaxOutputStorCharQuickStartConstraint_rule)
    M.ElecMaxOutputStorDiscConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMaxOutputStorDiscConstraint_rule)
    M.ElecMaxOutputStorDiscQuickStartConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMaxOutputStorDiscQuickStartConstraint_rule)
    M.ElecMaxOutputStorDiscConstraint1 = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMaxOutputStorDiscConstraint1_rule)

    M.ElecMinStartUpHourGenConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Gen,
        M.TIMESLICE,
        rule=ElecMinStartUpHourGenConstraint_rule)
    M.ElecMinStartUpHourStorCharConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMinStartUpHourStorCharConstraint_rule)
    M.ElecMinStartUpHourStorDiscConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMinStartUpHourStorDiscConstraint_rule)
    M.ElecMinShutDownHourGenConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Gen,
        M.TIMESLICE,
        rule=ElecMinShutDownHourGenConstraint_rule)
    M.ElecMinShutDownHourStorCharConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMinShutDownHourStorCharConstraint_rule)
    M.ElecMinShutDownHourStorDiscConstraint = Constraint(
        M.REGION_YEAR_TECH_UC_Stor,
        M.TIMESLICE,
        rule=ElecMinShutDownHourStorDiscConstraint_rule)

    # reserve requirement
    M.ReserveRequiredaFRRupConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReserveRequiredaFRRupConstraint_rule)

    M.ReserveRequiredaFRRdownConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReserveRequiredaFRRdownConstraint_rule)

    M.ReserveRequiredmFRRupConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReserveRequiredmFRRupConstraint_rule)

    M.ReserveRequiredmFRRdownConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReserveRequiredmFRRdownConstraint_rule)

    M.ReserveaFCRUpBalanceConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReserveaFCRUpBalanceConstraint_rule)

    M.ReserveaFCRDownBalanceConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReserveaFCRDownBalanceConstraint_rule)

    M.ReserveaFRRUpBalanceConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReserveaFRRUpBalanceConstraint_rule)

    M.ReserveaFRRDownBalanceConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReserveaFRRDownBalanceConstraint_rule)

    M.ReservemFRRUpBalanceConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReservemFRRUpBalanceConstraint_rule)

    M.ReservemFRRDownBalanceConstraint = Constraint(
        M.REGION_ID,
        M.YEAR,
        M.TIMESLICE,
        rule=ReservemFRRDownBalanceConstraint_rule)

    M.ReserveaFCRUpGenLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Gen_FCRup,
        M.TIMESLICE,
        rule=ReserveaFCRUpGenLimitConstraint_rule)

    M.ReserveaFCRDownGenLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Gen_FCRdown,
        M.TIMESLICE,
        rule=ReserveaFCRDownGenLimitConstraint_rule)

    M.ReserveaFRRUpGenLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Gen_aFRRup,
        M.TIMESLICE,
        rule=ReserveaFRRUpGenLimitConstraint_rule)

    M.ReserveaFRRDownGenLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Gen_aFRRdown,
        M.TIMESLICE,
        rule=ReserveaFRRDownGenLimitConstraint_rule)

    M.ReservemFRRUpGenLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Gen_mFRRup,
        M.TIMESLICE,
        rule=ReservemFRRUpGenLimitConstraint_rule)

    M.ReservemFRRDownGenLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Gen_mFRRdown,
        M.TIMESLICE,
        rule=ReservemFRRDownGenLimitConstraint_rule)

    M.ReserveaFCRUpStorCharLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_FCRup,
        M.TIMESLICE,
        rule=ReserveaFCRUpStorCharLimitConstraint_rule)

    M.ReserveaFCRDownStorCharLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_FCRdown,
        M.TIMESLICE,
        rule=ReserveaFCRDownStorCharLimitConstraint_rule)

    M.ReserveaFRRUpStorCharLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_aFRRup,
        M.TIMESLICE,
        rule=ReserveaFRRUpStorCharLimitConstraint_rule)

    M.ReserveaFRRDownStorCharLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_aFRRdown,
        M.TIMESLICE,
        rule=ReserveaFRRDownStorCharLimitConstraint_rule)

    M.ReservemFRRUpStorCharLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_mFRRup,
        M.TIMESLICE,
        rule=ReservemFRRUpStorCharLimitConstraint_rule)

    M.ReservemFRRDownStorCharLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_mFRRdown,
        M.TIMESLICE,
        rule=ReservemFRRDownStorCharLimitConstraint_rule)

    M.ReserveaFCRUpStorDiscLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_FCRup,
        M.TIMESLICE,
        rule=ReserveaFCRUpStorDiscLimitConstraint_rule)

    M.ReserveaFCRDownStorDiscLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_FCRdown,
        M.TIMESLICE,
        rule=ReserveaFCRDownStorDiscLimitConstraint_rule)

    M.ReserveaFRRUpStorDiscLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_aFRRup,
        M.TIMESLICE,
        rule=ReserveaFRRUpStorDiscLimitConstraint_rule)

    M.ReserveaFRRDownStorDiscLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_aFRRdown,
        M.TIMESLICE,
        rule=ReserveaFRRDownStorDiscLimitConstraint_rule)

    M.ReservemFRRUpStorDiscLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_mFRRup,
        M.TIMESLICE,
        rule=ReservemFRRUpStorDiscLimitConstraint_rule)

    M.ReservemFRRDownStorDiscLimitConstraint = Constraint(
        M.REGION_YEAR_TECH_Stor_mFRRdown,
        M.TIMESLICE,
        rule=ReservemFRRDownStorDiscLimitConstraint_rule)

    # Emission constraints
    M.AnnualEmissionConstraint = Constraint(M.REGION_ID,
                                            M.YEAR,
                                            rule=AnnualEmissionConstraint_rule)
    M.MaxAnnualRegEmissionConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=MaxAnnualRegEmissionConstraint_rule)
    M.TotalEmissionBudgetConstraint = Constraint(
        M.REGION_ID, rule=TotalEmissionBudgetConstraint_rule)

    # RES / NUC / FOSSIL percentage + RES/NUC Limit
    M.RESPercentageLimitConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=RESPercentageLimitConstraint_rule)
    M.RESPercentageConstraint = Constraint(M.REGION_ID,
                                           M.YEAR,
                                           rule=RESPercentageConstraint_rule)
    M.IRESCapacityConstraint = Constraint(M.REGION_ID,
                                          M.YEAR,
                                          rule=IRESCapacityConstraint_rule)
    M.NUCPercentageLimitConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=NUCPercentageLimitConstraint_rule)
    M.NUCPercentageConstraint = Constraint(M.REGION_ID,
                                           M.YEAR,
                                           rule=NUCPercentageConstraint_rule)
    M.FOSSILPercentageConstraint = Constraint(
        M.REGION_ID, M.YEAR, rule=FOSSILPercentageConstraint_rule)

    return M


def obj_rule(M):
    return sum(M.regionalcost[r] for r in M.REGION_ID)


def RegionalCost_rule(M, r):
    return M.regionalcost[r] == M.regionalcostinv[r] + M.regionalcostfix[
        r] + M.regionalcostvar[r] + M.regionalcostco2[r]


def RegionalCostInv_rule(M, r):
    return M.regionalcostinv[r] == sum(
        sum(
            sum((1 + M.SDR)**(M.REFYEAR - y - i) *
                M.regionalyearcostinvgentech[r, y, t] for i in sequence(
                    0,
                    min(
                        M.GenELifetime[y,
                                       t], M.YEARPERIOD[len(M.YEARPERIOD)][0] +
                        M.YEARPERIOD[len(M.YEARPERIOD)][1] - y) - 1))
            for t in M.TECH_GENERATION
            if (r, y, t) in M.REGION_YEAR_TECH_GENERATION)
        for y in M.YEAR) + sum(
            sum(
                sum((1 + M.SDR)**(M.REFYEAR - y - i) *
                    M.regionalyearcostinvstortech[r, y, tt] for i in sequence(
                        0,
                        min(
                            M.StorELifetime[
                                y, tt], M.YEARPERIOD[len(M.YEARPERIOD)][0] +
                            M.YEARPERIOD[len(M.YEARPERIOD)][1] - y) - 1))
                for tt in M.TECH_STORAGE
                if (r, y, tt) in M.REGION_YEAR_TECH_STORAGE)
            for y in M.YEAR) + sum(
                sum(
                    sum((1 + M.SDR)**(M.REFYEAR - y - i) *
                        M.regionalyearcostinvgridline[r, y, l]
                        for i in sequence(
                            0,
                            min(
                                M.TransELifetime[y, M.TransTech[l]],
                                M.YEARPERIOD[len(M.YEARPERIOD)][0] +
                                M.YEARPERIOD[len(M.YEARPERIOD)][1] - y) - 1))
                    for l in M.LINE) for y in M.YEAR)


def RegionalCostFix_rule(M, r):
    return M.regionalcostfix[r] == sum(
        sum((1 + M.SDR)**(M.REFYEAR - y - i) * M.regionalyearcostfix[r, y]
            for i in sequence(0, ny - 1)) for (y, ny) in M.YEARPERIOD)


def RegionalCostVar_rule(M, r):
    return M.regionalcostvar[r] == sum(
        sum((1 + M.SDR)**(M.REFYEAR - y - i) * M.regionalyearcostvar[r, y]
            for i in sequence(0, ny - 1)) for (y, ny) in M.YEARPERIOD)


def RegionalCostCO2_rule(M, r):
    return M.regionalcostco2[r] == sum(
        sum((1 + M.SDR)**(M.REFYEAR - y - i) * M.regionalyearcostco2[r, y]
            for i in sequence(0, ny - 1)) for (y, ny) in M.YEARPERIOD)


def RegionalYearCostInv_rule(M, r, y):
    return M.regionalyearcostinv[r, y] == M.regionalyearcostinvgen[
        r, y] + M.regionalyearcostinvstor[r, y] + M.regionalyearcostinvgrid[r,
                                                                            y]


def RegionalYearCostInvGen_rule(M, r, y):
    return M.regionalyearcostinvgen[r, y] == sum(
        M.regionalyearcostinvgentech[r, y, t] for t in M.TECH_GENERATION
        if (r, y, t) in M.REGION_YEAR_TECH_GENERATION)


def RegionalYearCostInvStor_rule(M, r, y):
    return M.regionalyearcostinvstor[r, y] == sum(
        M.regionalyearcostinvstortech[r, y, t] for t in M.TECH_STORAGE
        if (r, y, t) in M.REGION_YEAR_TECH_STORAGE)


def RegionalYearCostInvGrid_rule(M, r, y):
    return M.regionalyearcostinvgrid[r,
                                     y] == sum(M.regionalyearcostinvgridline[r,
                                                                             y,
                                                                             l]
                                               for l in M.LINE)


def RegionalYearCostInvGenTech_rule(M, r, y, t):
    return M.regionalyearcostinvgentech[
        r, y, t] == M.GenCAPEX[y, t] * M.newinstalledgencapacity[r, y, t] * (
            1 + M.GenWACC[y, t])**M.GenELifetime[y, t] * M.GenWACC[y, t] / (
                (1 + M.GenWACC[y, t])**M.GenELifetime[y, t] - 1)


def RegionalYearCostInvStorTech_rule(M, r, y, t):
    return M.regionalyearcostinvstortech[r, y, t] == (
        M.StorCAPEXp[y, t] * M.newinstalledstorpower[r, y, t] +
        M.StorCAPEXe[y, t] * M.newinstalledstorenergy[r, y, t]) * (
            1 + M.StorWACC[y, t])**M.StorELifetime[y, t] * M.StorWACC[y, t] / (
                (1 + M.StorWACC[y, t])**M.StorELifetime[y, t] - 1)


def RegionalYearCostInvGridLine_rule(M, r, y, l):
    return M.regionalyearcostinvgridline[r, y, l] == (
        M.TransCAPEXline[y, M.TransTech[l]] * M.TransDis[l] +
        M.TransCAPEXstation[y, M.TransTech[l]]
    ) * M.newinstalledexporttranscapacity[l, y] * abs(M.LineRegion[l, r]) * (
        1 + M.TransWACC[y, M.TransTech[l]]
    )**M.TransELifetime[y, M.TransTech[l]] * M.TransWACC[y, M.TransTech[l]] / (
        (1 + M.TransWACC[y, M.TransTech[l]])**
        M.TransELifetime[y, M.TransTech[l]] - 1) * 0.5


def RegionalYearCostFix_rule(M, r, y):
    return M.regionalyearcostfix[r, y] == M.regionalyearcostfixgen[
        r, y] + M.regionalyearcostfixstor[r, y] + M.regionalyearcostfixgrid[
            r, y] + M.regionalyearcostfixloadshedding[r, y]


def RegionalYearCostFixGen_rule(M, r, y):
    return M.regionalyearcostfixgen[r, y] == sum(
        M.regionalyearcostfixgentech[r, y, t] for t in M.TECH_GENERATION
        if (r, y, t) in M.REGION_YEAR_TECH_GENERATION)


def RegionalYearCostFixStor_rule(M, r, y):
    return M.regionalyearcostfixstor[r, y] == sum(
        M.regionalyearcostfixstortech[r, y, t] for t in M.TECH_STORAGE
        if (r, y, t) in M.REGION_YEAR_TECH_STORAGE)


def RegionalYearCostFixGrid_rule(M, r, y):
    return M.regionalyearcostfixgrid[r,
                                     y] == sum(M.regionalyearcostfixgridline[r,
                                                                             y,
                                                                             l]
                                               for l in M.LINE)


def RegionalYearCostFixLoadShedding_rule(M, r, y):
    return M.regionalyearcostfixloadshedding[
        r, y] == M.DSMSheddingOPEXfix[r, y] * M.DSMSheddingCapacity[r, y]


def RegionalYearCostFixGenTech_rule(M, r, y, t):
    return M.regionalyearcostfixgentech[
        r, y, t] == M.GenOPEXfix[y, t] * M.totalinstalledgencapacity[r, y, t]


def RegionalYearCostFixStorTech_rule(M, r, y, t):
    return M.regionalyearcostfixstortech[
        r, y, t] == M.StorOPEXfix[y, t] * M.totalinstalledstorpower[r, y, t]


def RegionalYearCostFixGridLine_rule(M, r, y, l):
    return M.regionalyearcostfixgridline[r, y, l] == (
        M.TransCAPEXline[y, M.TransTech[l]] * M.TransDis[l] *
        M.TransOPEXfixline[y, M.TransTech[l]] +
        M.TransCAPEXstation[y, M.TransTech[l]] *
        M.TransOPEXfixstation[y, M.TransTech[l]]
    ) * M.totalinstalledexporttranscapacity[l, y] * abs(M.LineRegion[l, r]) * (
        1 + M.TransWACC[y, M.TransTech[l]]
    )**M.TransELifetime[y, M.TransTech[l]] * M.TransWACC[y, M.TransTech[l]] / (
        (1 + M.TransWACC[y, M.TransTech[l]])**
        M.TransELifetime[y, M.TransTech[l]] - 1) * 0.5


def RegionalYearCostVar_rule(M, r, y):
    return M.regionalyearcostvar[
        r, y] == M.regionalyearcostvargen[r, y] + M.regionalyearcostvarstor[
            r, y] + M.regionalyearcostvarloadshedding[
                r, y] + M.regionalyearcostvarstartup[r, y]


def RegionalYearCostVarGen_rule(M, r, y):
    return M.regionalyearcostvargen[r, y] == sum(
        M.regionalyearcostvargentech[r, y, t] for t in M.TECH_GENERATION
        if (r, y, t) in M.REGION_YEAR_TECH_GENERATION)


def RegionalYearCostVarStor_rule(M, r, y):
    return M.regionalyearcostvarstor[r, y] == sum(
        M.regionalyearcostvarstortech[r, y, t] for t in M.TECH_STORAGE
        if (r, y, t) in M.REGION_YEAR_TECH_STORAGE)


def RegionalYearCostVarLoadShedding_rule(M, r, y):
    return M.regionalyearcostvarloadshedding[
        r, y] == M.DSMSheddingOPEXvar[r, y] * M.annualelecloadshedding[r, y]


def RegionalYearCostVarGenTech_rule(M, r, y, t):
    if t in M.TECH_GAS:
        return M.regionalyearcostvargentech[r, y, t] == M.GenOPEXvar[
            y, t] * sum(M.electechnaturalgas[r, y, t, h]
                        for h in M.TIMESLICE) + M.BiogasPrice[r, y] * sum(
                            M.electechbiogas[r, y, t, h] for h in M.TIMESLICE)
    else:
        return M.regionalyearcostvargentech[
            r, y, t] == M.GenOPEXvar[y, t] * M.annualelectechgen[r, y, t]


def RegionalYearCostVarStorTech_rule(M, r, y, t):
    return M.regionalyearcostvarstortech[r, y, t] == M.StorOPEXvar[y, t] * (
        M.annualelectechdisc[r, y, t] + M.annualelectechchar[r, y, t])


def RegionalYearCostVarStartUp_rule(M, r, y):
    return M.regionalyearcostvarstartup[r, y] == sum(
        M.regionalyearcostvarstartuptech[r, y, t] for t in M.TECH_UC
        if (r, y, t) in M.REGION_YEAR_TECH_UC)


def RegionalYearCostVarStartUpTech_rule(M, r, y, t):
    if t in M.TECH_GENERATION:
        return M.regionalyearcostvarstartuptech[
            r, y,
            t] == M.GenStarUpCost[y, t] * sum(M.elecstartupgen[r, y, t, h]
                                              for h in M.TIMESLICE)
    elif t in M.TECH_STORAGE:
        return M.regionalyearcostvarstartuptech[
            r, y, t] == M.StorStarUpCost[y, t] * sum(
                (M.elecstartupstorchar[r, y, t, h] +
                 M.elecstartupstordisc[r, y, t, h]) for h in M.TIMESLICE)


def RegionalYearCostCO2_rule(M, r, y):
    return M.annualemission[r, y] * M.CO2Cost[y] == M.regionalyearcostco2[r, y]


def RegionalYearCost_rule(M, r, y):
    return M.regionalyearcost[
        r, y] == M.regionalyearcostinv[r, y] + M.regionalyearcostfix[
            r, y] + M.regionalyearcostvar[r, y] + M.regionalyearcostco2[r, y]


def TotalInstalledGenCapacityConstraint_rule(M, r, y, t):
    return M.GenResidualCapacity[r, y, t] + M.accunewinstalledgencapacity[
        r, y, t] == M.totalinstalledgencapacity[r, y, t]


def AccuNewGenCapacityConstraint_rule(M, r, y, t):
    return sum(
        M.newinstalledgencapacity[r, yy, t] for yy in M.YEAR
        if ((y - yy < M.GenTLifetime[y, t]) and (y - yy >= 0) and (r, yy, t) in
            M.REGION_YEAR_TECH_GENERATION)) == M.accunewinstalledgencapacity[r,
                                                                             y,
                                                                             t]


def NewNUCLTOCapacityConstraint_rule(M, r, y, t, rr, yy, tt):
    if r == rr and y == yy and M.NM[t, tt] != 0:
        if y == M.YEAR.first():
            return Constraint.Skip
        else:
            return M.newinstalledgencapacity[r, y, tt] <= (
                M.GenResidualCapacity[r, y - M.PERIODYEAR[y], t] -
                M.GenResidualCapacity[r, y, t]) * M.NM[t, tt]
    else:
        return Constraint.Skip


def MaxElecGenCapacityConstraint_rule(M, r, y, t):
    return M.totalinstalledgencapacity[r, y,
                                       t] <= M.GenMaxInstalledCapacity[r, y, t]


def TotalInstalledStorPowerConstraint_rule(M, r, y, t):
    return M.StorResidualPower[r, y, t] + M.accunewinstalledstorpower[
        r, y, t] == M.totalinstalledstorpower[r, y, t]


def AccuNewStorPowerConstraint_rule(M, r, y, t):
    return sum(
        M.newinstalledstorpower[r, yy, t] for yy in M.YEAR
        if ((y - yy < M.StorTLifetime[y, t]) and (y - yy >= 0) and (r, yy, t)
            in M.REGION_YEAR_TECH_STORAGE)) == M.accunewinstalledstorpower[r,
                                                                           y,
                                                                           t]


def NewStorEnergyConstraint_rule(M, r, y, t):
    return M.newinstalledstorpower[r, y, t] * M.StorEnergyPowerRatio[
        y, t] == M.newinstalledstorenergy[r, y, t]


def AccuNewStorEnergyConstraint_rule(M, r, y, t):
    return M.accunewinstalledstorpower[r, y, t] * M.StorEnergyPowerRatio[
        y, t] == M.accunewinstalledstorenergy[r, y, t]


def TotalInstalledStorEnergyConstraint_rule(M, r, y, t):
    return M.totalinstalledstorpower[r, y, t] * M.StorEnergyPowerRatio[
        y, t] == M.totalinstalledstorenergy[r, y, t]


def TotalInstalledImportTransCapacityConstraint_rule(M, l, y):
    return M.TransResidualImportCapacity[
        l, y] + M.accunewinstalledimporttranscapacity[
            l, y] == M.totalinstalledimporttranscapacity[l, y]


def AccuNewImportTransCapacityConstraint_rule(M, l, y):
    return sum(M.newinstalledimporttranscapacity[l, yy] for yy in M.YEAR
               if ((y - yy < M.TransTLifetime[y, M.TransTech[l]]) and (
                   y - yy >= 0))) == M.accunewinstalledimporttranscapacity[l,
                                                                           y]


def TotalInstalledExportTransCapacityConstraint_rule(M, l, y):
    return M.TransResidualExportCapacity[
        l, y] + M.accunewinstalledexporttranscapacity[
            l, y] == M.totalinstalledexporttranscapacity[l, y]


def AccuNewExportTransCapacityConstraint_rule(M, l, y):
    return sum(M.newinstalledexporttranscapacity[l, yy] for yy in M.YEAR
               if ((y - yy < M.TransTLifetime[y, M.TransTech[l]]) and (
                   y - yy >= 0))) == M.accunewinstalledexporttranscapacity[l,
                                                                           y]


def ElecBalanceConstraint_rule(M, r, y, h):
    return sum(M.electechgen[r, y, t, h] for t in M.TECH_GENERATION if (
        r, y, t) in M.REGION_YEAR_TECH_GENERATION) + sum(
            (M.electechdisc[r, y, t, h]) for t in M.TECH_STORAGE_NO_DSM_PTG
            if (r, y, t) in M.REGION_YEAR_TECH_STORAGE) - sum(
                (M.electechchar[r, y, t, h]) for t in M.TECH_STORAGE_NO_DSM
                if (r, y, t) in M.REGION_YEAR_TECH_STORAGE) + M.elecexchange[
                    r, y, h] - M.elecexcess[r, y, h] + M.elecloadshedding[
                        r, y, h] == M.Demand[r, y, h] + sum(
                            (M.electechdisc[r, y, t, h] -
                             M.electechchar[r, y, t, h]) for t in M.TECH_DSM
                            if (r, y, t) in M.REGION_YEAR_TECH_STORAGE)


def ElecTechGenConstraint_rule(M, r, y, t, h):
    if t in M.TECH_TPP:
        return M.electechgen[r, y, t, h] == M.electechtpp[r, y, t, h]
    if t in M.TECH_VRES:
        return M.electechgen[r, y, t, h] == M.electechvres[r, y, t, h]
    if t in M.TECH_HD:
        return M.electechgen[r, y, t, h] == M.electechhd[r, y, t, h]


def AnnualElecTechGenConstraint_rule(M, r, y, t):
    return sum(M.electechgen[r, y, t, h]
               for h in M.TIMESLICE) == M.annualelectechgen[r, y, t]


def AnnualElecNaturalGasConstraint_rule(M, r, y):
    return sum(
        sum(M.electechnaturalgas[r, y, t, h] for h in M.TIMESLICE)
        for t in M.TECH_GAS
        if (r, y, t) in M.REGION_YEAR_TECH_GAS) == M.annualelecnaturalgas[r, y]


def AnnualElecBioGasConstraint_rule(M, r, y):
    return sum(
        sum(M.electechbiogas[r, y, t, h] * M.GenFullLoadEffi[y, t]
            for h in M.TIMESLICE) for t in M.TECH_GAS
        if (r, y, t) in M.REGION_YEAR_TECH_GAS) == M.annualelecbiogas[r, y]


def AnnualElecGtPConstraint_rule(M, r, y):
    return sum(
        sum(M.electechgtp[r, y, t, h] * M.GenFullLoadEffi[y, t]
            for h in M.TIMESLICE) for t in M.TECH_GAS
        if (r, y, t) in M.REGION_YEAR_TECH_GAS) == M.annualelecgtp[r, y]


def AnnualElecGenConstraint_rule(M, r, y):
    return sum(M.annualelectechgen[r, y, t] for t in M.TECH_GENERATION
               if (r, y,
                   t) in M.REGION_YEAR_TECH_GENERATION) == M.annualelecgen[r,
                                                                           y]


def AnnualElecNucGenConstraint_rule(M, r, y):
    return sum(M.annualelectechgen[r, y, t] for t in M.TECH_NUC
               if (r, y, t) in M.REGION_YEAR_TECH_NUC) == M.annualelecnucgen[r,
                                                                             y]


def AnnualElecFossilGenConstraint_rule(M, r, y):
    return sum(M.annualelectechgen[r, y, t] for t in M.TECH_FOSSIL
               if (r, y,
                   t) in M.REGION_YEAR_TECH_FOSSIL) == M.annualelecfossilgen[r,
                                                                             y]


def AnnualElecTechCharConstraint_rule(M, r, y, t):
    return sum(M.electechchar[r, y, t, h]
               for h in M.TIMESLICE) == M.annualelectechchar[r, y, t]


def AnnualElecTechDiscConstraint_rule(M, r, y, t):
    return sum(M.electechdisc[r, y, t, h]
               for h in M.TIMESLICE) == M.annualelectechdisc[r, y, t]


def AnnualElecExcessConstraint_rule(M, r, y):
    return sum(M.elecexcess[r, y, h]
               for h in M.TIMESLICE) == M.annualelecexcess[r, y]


def AnnualElecLoadSheddingConstraint_rule(M, r, y):
    return sum(M.elecloadshedding[r, y, h]
               for h in M.TIMESLICE) == M.annualelecloadshedding[r, y]


def AnnualDemandConstraint_rule(M, r, y):
    return sum(M.Demand[r, y, h] for h in M.TIMESLICE) == M.annualdemand[r, y]


def ElecVRESCapacityConstraint_rule(M, r, y, t, h):
    return M.electechvres[r, y, t, h] == M.totalinstalledgencapacity[
        r, y, t] * M.CapacityFactor[r, y, t, h]


def ElecTPPCapacityConstraint_rule(M, r, y, t, h):
    return M.electechtpp[
        r, y, t,
        h] <= M.totalinstalledgencapacity[r, y, t] * M.Availability[r, y, t, h]


def ElecMustRunMinConstraint_rule(M, r, y, t, h):
    return M.electechtpp[
        r, y, t,
        h] >= M.totalinstalledgencapacity[r, y, t] * M.MustRun[r, y, t, h]


def ElecHDCapacityConstraint_rule(M, r, y, t, h):
    return M.electechhd[
        r, y, t,
        h] <= M.totalinstalledgencapacity[r, y, t] * M.Availability[r, y, t, h]


def MaxAnnualEnergyGenConstraint_rule(M, r, y, t):
    return M.annualelectechgen[r, y, t] <= M.GenMaxEnergy[r, y, t]


def ElecHDWeekIniLevelConstraint_rule(M, r, y, t, w):
    if w == M.WEEK.first():
        return M.elechdweekinilevel[r, y, t, w] == M.HDStorIniLevel[r, y, t]
    else:
        return M.elechdweekinilevel[r, y, t, w] == (
            M.elechdweekinilevel[r, y, t, w - 1] * M.HDMaxStock[r, y, t] +
            M.HDWeekInflow[r, y, t, w - 1] - M.elechdweekprod[r, y, t, w - 1] /
            M.HDEffi[r, y, t]) / M.HDMaxStock[r, y, t]


def ElecHDWeekProdConstraint_rule(M, r, y, t, w):
    if w == M.WEEK.last():
        return M.elechdweekprod[r, y, t, w] == sum(
            M.electechgen[r, y, t, h]
            for h in sequence((w - 1) * 168 + 1, 8760))
    else:
        return M.elechdweekprod[r, y, t, w] == sum(
            M.electechgen[r, y, t, h]
            for h in sequence((w - 1) * 168 + 1, (w) * 168))


def ElecHDWeekMinLevelConstraint_rule(M, r, y, t, w):
    return M.HDMinLevel[r, y, t, w] <= M.elechdweekinilevel[r, y, t, w]


def ElecHDWeekMaxLevelConstraint_rule(M, r, y, t, w):
    return M.elechdweekinilevel[r, y, t, w] <= M.HDMaxLevel[r, y, t, w]


def ElecTechStoredConstraint_rule(M, r, y, t, h):
    if h == 1:
        return M.electechstored[
            r, y, t, h] == M.StorIni[y, t] * M.totalinstalledstorpower[
                r, y, t] * M.StorEnergyPowerRatio[y, t] + M.electechchar[
                    r, y, t, h] * M.StorCharEfficiency[y, t] - M.electechdisc[
                        r, y, t, h] / M.StorDiscEfficiency[y, t]
    else:
        return M.electechstored[r, y, t, h] == M.electechstored[
            r, y, t,
            h - 1] + M.electechchar[r, y, t, h] * M.StorCharEfficiency[
                y, t] - M.electechdisc[r, y, t, h] / M.StorDiscEfficiency[y, t]


def MaxElecStorPowerConstraint_rule(M, r, y, t):
    return M.totalinstalledstorpower[r, y, t] <= M.StorMaxInstalledPower[r, y,
                                                                         t]


def MaxElecTechStoredConstraint_rule(M, r, y, t, h):
    return M.electechstored[r, y, t, h] <= M.totalinstalledstorenergy[r, y, t]


def MaxElecTechCharDiscConstraint_rule(M, r, y, t, h):
    if t in M.TECH_PTG:
        return M.electechchar[r, y, t, h] <= M.totalinstalledstorpower[
            r, y, t] * M.Availability[r, y, t, h]
    else:
        return M.electechchar[r, y, t, h] + M.electechdisc[
            r, y, t, h] <= M.totalinstalledstorpower[r, y, t] * M.Availability[
                r, y, t, h]


def MaxDSMShiftCharConstraint_rule(M, r, y, t, h):
    return M.electechstored[r, y, t, h] <= sum(
        M.electechchar[r, y, t, h - l + 1]
        for l in sequence(1, M.StorEnergyPowerRatio[y, t]) if h - l >= 0)


def MaxDSMShiftDiscConstraint_rule(M, r, y, t, h):
    return M.electechstored[r, y, t, h] <= sum(
        M.electechdisc[r, y, t, h + l]
        for l in sequence(1, M.StorEnergyPowerRatio[y, t]) if h + l <= 8760)


def MaxDSMSheddingConstraint_rule(M, r, y, h):
    return M.elecloadshedding[r, y, h] <= M.DSMSheddingCapacity[r, y]


def GasPPGasSourceConstraint_rule(M, r, y, t, h):
    return (M.electechgtp[r, y, t, h] + M.electechbiogas[r, y, t, h]
            ) * M.GenFullLoadEffi[y, t] + M.electechnaturalgas[
                r, y, t, h] == M.electechgen[r, y, t, h]


def TotalInstalledStorDiscPowerConstraint_rule(M, r, y, t, rr, yy, tt):
    if (t in M.TECH_PTG):
        return sum(M.totalinstalledgencapacity[r, y, tt] for tt in M.TECH_GAS
                   if (r, y, tt) in
                   M.REGION_YEAR_TECH_GAS) == M.totalinstalledstordiscpower[r,
                                                                            y,
                                                                            t]
    else:
        return M.totalinstalledstorpower[r, y,
                                         t] == M.totalinstalledstordiscpower[r,
                                                                             y,
                                                                             t]


def FlexibleBiogasQuantityConstraint_rule(M, r, y):
    return sum(
        sum(M.electechbiogas[r, y, t, h]
            for t in M.TECH_GAS if (r, y, t) in M.REGION_YEAR_TECH_GAS)
        for h in M.TIMESLICE) <= M.FlexBiogasQuantity[r, y]


def PTGDiscConstraint_rule(M, r, y, t, h):
    if (r, y, t) in M.REGION_YEAR_TECH_PTG:
        return M.electechdisc[r, y, t,
                              h] == sum(M.electechgtp[r, y, tt, h]
                                        for tt in M.TECH_GAS
                                        if (r, y,
                                            tt) in M.REGION_YEAR_TECH_GAS)
    else:
        return 0 == sum(M.electechgtp[r, y, tt, h] for tt in M.TECH_GAS
                        if (r, y, tt) in M.REGION_YEAR_TECH_GAS)


def HydrogenNeedsConstraint_rule(M, r, y, t, h):
    if h == 8760:
        return M.electechstored[r, y, t, h] == M.HydrogenNeeds[r, y]
    else:
        return Constraint.Skip


def NoPTHDischargeConstraint_rule(M, r, y, t, h):
    return M.electechdisc[r, y, t, h] == 0


def MaxElecImportTransCapacityConstraint_rule(M, l, y):
    return M.totalinstalledimporttranscapacity[
        l, y] <= M.TransMaxInstalledImportCapacity[l, y]


def MaxElecExportTransCapacityConstraint_rule(M, l, y):
    return M.totalinstalledexporttranscapacity[
        l, y] <= M.TransMaxInstalledExportCapacity[l, y]


def ElecImportExportTransCapacityConstraint_rule(M, l, y):
    return M.newinstalledimporttranscapacity[
        l, y] == M.newinstalledexporttranscapacity[l, y]


def TransImpCapacityLimitConstraint_rule(M, l, y, h):
    return M.eleclexchange[l, y, h] <= M.totalinstalledimporttranscapacity[
        l, y] * M.TransAvailability[y, M.TransTech[l]]


def TransExpCapacityLimitConstraint_rule(M, l, y, h):
    return M.eleclexchange[l, y, h] >= -M.totalinstalledexporttranscapacity[
        l, y] * M.TransAvailability[y, M.TransTech[l]]


def ElecRegionalExchangeConstraint_rule(M, r, y, h):
    return M.elecexchange[r, y, h] == sum(
        M.eleclexchange[l, y, h] * M.LineRegion[l, r] /
        (1 - M.TransLosses[y, M.TransTech[l]] * M.TransDis[l] / 100)
        for l in M.LINE)


def AnnualElecExchangeConstraint_rule(M, r, y):
    return M.annualelecexchange[r, y] == sum(
        sum(M.eleclexchange[l, y, h] * M.LineRegion[l, r] /
            (1 - M.TransLosses[y, M.TransTech[l]] * M.TransDis[l] / 100)
            for l in M.LINE) for h in M.TIMESLICE)


def ElecCommitNumberGenConstraint_rule(M, r, y, t, h):
    return M.eleccommitgen[r, y, t,
                           h] / M.GenSize[y, t] == M.eleccommitnumbergen[r, y,
                                                                         t, h]


def ElecCommitNumberStorCharConstraint_rule(M, r, y, t, h):
    return M.eleccommitstorchar[r, y, t, h] / M.StorSize[
        y, t] == M.eleccommitnumberstorchar[r, y, t, h]


def ElecCommitNumberStorDiscConstraint_rule(M, r, y, t, h):
    return M.eleccommitstordisc[r, y, t, h] / M.StorSize[
        y, t] == M.eleccommitnumberstordisc[r, y, t, h]


def ElecCommitGenConstraint_rule(M, r, y, t, h):
    return M.eleccommitgen[
        r, y, t,
        h] <= M.totalinstalledgencapacity[r, y, t] * M.Availability[r, y, t, h]


def ElecCommitStorConstraint_rule(M, r, y, t, h):
    return M.eleccommitstorchar[r, y, t, h] + M.eleccommitstordisc[
        r, y, t, h] <= M.totalinstalledstordiscpower[r, y, t] * M.Availability[
            r, y, t, h]


def ElecCommitBalanceGenConstraint_rule(M, r, y, t, h):
    if h == M.TIMESLICE.first():
        return Constraint.Skip
    else:
        return M.eleccommitgen[r, y, t, h] == M.eleccommitgen[
            r, y, t, h -
            1] + M.elecstartupgen[r, y, t, h] - M.elecshutdowngen[r, y, t, h]


def ElecCommitBalanceStorCharConstraint_rule(M, r, y, t, h):
    if h == M.TIMESLICE.first():
        return Constraint.Skip
    else:
        return M.eleccommitstorchar[
            r, y, t,
            h] == M.eleccommitstorchar[r, y, t, h - 1] + M.elecstartupstorchar[
                r, y, t, h] - M.elecshutdownstorchar[r, y, t, h]


def ElecCommitBalanceStorDiscConstraint_rule(M, r, y, t, h):
    if h == M.TIMESLICE.first():
        return Constraint.Skip
    else:
        return M.eleccommitstordisc[
            r, y, t,
            h] == M.eleccommitstordisc[r, y, t, h - 1] + M.elecstartupstordisc[
                r, y, t, h] - M.elecshutdownstordisc[r, y, t, h]


def ElecMinOutputGenConstraint_rule(M, r, y, t, h):
    return M.electechgen[r, y, t, h] >= M.GenMinPower[y, t] * M.eleccommitgen[
        r, y, t, h] + M.aFCRdownGen[r, y, t, h] + M.aFRRdownGen[r, y, t, h]


def ElecMinOutputGenQuickStartConstraint_rule(M, r, y, t, h):
    if M.GenMFRRdown[y, t] == 1:
        return M.electechgen[r, y, t, h] >= M.aFCRdownGen[
            r, y, t, h] + M.aFRRdownGen[r, y, t, h] + M.mFRRdownGen[r, y, t, h]
    else:
        return M.electechgen[r, y, t, h] >= M.GenMinPower[
            y, t] * M.eleccommitgen[r, y, t, h] + M.aFCRdownGen[
                r, y, t, h] + M.aFRRdownGen[r, y, t, h] + M.mFRRdownGen[r, y,
                                                                        t, h]


def ElecMinOutputStorCharConstraint_rule(M, r, y, t, h):
    if t in M.TECH_DSM:
        return M.electechchar[r, y, t, h] >= M.StorMinPower[
            y, t] * M.eleccommitstorchar[r, y, t, h] + M.aFCRdownStorChar[
                r, y, t, h] + M.aFRRdownStorChar[r, y, t, h]
    else:
        return M.electechchar[r, y, t, h] >= M.StorMinPower[
            y, t] * M.eleccommitstorchar[r, y, t, h] + M.aFCRupStorChar[
                r, y, t, h] + M.aFRRupStorChar[r, y, t, h]


def ElecMinOutputStorCharQuickStartConstraint_rule(M, r, y, t, h):
    if M.StorMFRRdown[y, t] == 1:
        if t in M.TECH_DSM:
            return M.electechchar[
                r, y, t,
                h] >= M.aFCRdownStorChar[r, y, t, h] + M.aFRRdownStorChar[
                    r, y, t, h] + M.mFRRdownStorChar[r, y, t, h]
        else:
            return M.electechchar[
                r, y, t, h] >= M.aFCRupStorChar[r, y, t, h] + M.aFRRupStorChar[
                    r, y, t, h] + M.mFRRupStorChar[r, y, t, h]
    else:
        if t in M.TECH_DSM:
            return M.electechchar[r, y, t, h] >= M.StorMinPower[
                y, t] * M.eleccommitstorchar[r, y, t, h] + M.aFCRdownStorChar[
                    r, y, t, h] + M.aFRRdownStorChar[
                        r, y, t, h] + M.mFRRdownStorChar[r, y, t, h]
        else:
            return M.electechchar[r, y, t, h] >= M.StorMinPower[
                y, t] * M.eleccommitstorchar[r, y, t, h] + M.aFCRupStorChar[
                    r, y, t, h] + M.aFRRupStorChar[
                        r, y, t, h] + M.mFRRupStorChar[r, y, t, h]


def ElecMinOutputStorDiscConstraint_rule(M, r, y, t, h):
    if t in M.TECH_DSM:
        return M.electechdisc[r, y, t, h] >= M.StorMinPower[
            y, t] * M.eleccommitstordisc[r, y, t, h] + M.aFCRupStorDisc[
                r, y, t, h] + M.aFRRupStorDisc[r, y, t, h]
    else:
        return M.electechdisc[r, y, t, h] >= M.StorMinPower[
            y, t] * M.eleccommitstordisc[r, y, t, h] + M.aFCRdownStorDisc[
                r, y, t, h] + M.aFRRdownStorDisc[r, y, t, h]


def ElecMinOutputStorDiscQuickStartConstraint_rule(M, r, y, t, h):
    if M.StorMFRRdown[y, t] == 1:
        if t in M.TECH_DSM:
            return M.electechdisc[
                r, y, t, h] >= M.aFCRupStorDisc[r, y, t, h] + M.aFRRupStorDisc[
                    r, y, t, h] + M.mFRRupStorDisc[r, y, t, h]
        else:
            return M.electechdisc[
                r, y, t,
                h] >= M.aFCRdownStorDisc[r, y, t, h] + M.aFRRdownStorDisc[
                    r, y, t, h] + M.mFRRdownStorDisc[r, y, t, h]
    else:
        if t in M.TECH_DSM:
            return M.electechdisc[r, y, t, h] >= M.StorMinPower[
                y, t] * M.eleccommitstordisc[r, y, t, h] + M.aFCRupStorDisc[
                    r, y, t, h] + M.aFRRupStorDisc[
                        r, y, t, h] + M.mFRRupStorDisc[r, y, t, h]
        else:
            return M.electechdisc[r, y, t, h] >= M.StorMinPower[
                y, t] * M.eleccommitstordisc[r, y, t, h] + M.aFCRdownStorDisc[
                    r, y, t, h] + M.aFRRdownStorDisc[
                        r, y, t, h] + M.mFRRdownStorDisc[r, y, t, h]


def ElecMaxOutputGenConstraint_rule(M, r, y, t, h):
    return M.electechgen[r, y, t, h] + M.aFCRupGen[r, y, t, h] + M.aFRRupGen[
        r, y, t, h] <= M.eleccommitgen[r, y, t, h]


def ElecMaxOutputGenQuickStartConstraint_rule(M, r, y, t, h):
    if M.GenMFRRup[y, t] == 1:
        return M.electechgen[r, y, t, h] + M.aFCRupGen[
            r, y, t, h] + M.aFRRupGen[r, y, t, h] + M.mFRRupGen[
                r, y, t, h] <= M.totalinstalledgencapacity[
                    r, y, t] * M.Availability[r, y, t, h]
    else:
        return M.electechgen[r, y, t, h] + M.aFCRupGen[
            r, y, t, h] + M.aFRRupGen[r, y, t, h] + M.mFRRupGen[
                r, y, t, h] <= M.eleccommitgen[r, y, t, h]


def ElecMaxOutputStorCharConstraint_rule(M, r, y, t, h):
    if t in M.TECH_DSM:
        return M.electechchar[r, y, t, h] + M.aFCRupStorChar[
            r, y, t, h] + M.aFRRupStorChar[r, y, t, h] <= M.eleccommitstorchar[
                r, y, t, h]
    else:
        return M.electechchar[r, y, t, h] + M.aFCRdownStorChar[
            r, y, t, h] + M.aFRRdownStorChar[r, y, t,
                                             h] <= M.eleccommitstorchar[r, y,
                                                                        t, h]


def ElecMaxOutputStorCharQuickStartConstraint_rule(M, r, y, t, h):
    if M.StorMFRRup[y, t] == 1:
        if t in M.TECH_DSM:
            return M.electechchar[r, y, t, h] + M.aFCRupStorChar[
                r, y, t, h] + M.aFRRupStorChar[r, y, t, h] + M.mFRRupStorChar[
                    r, y, t, h] <= M.totalinstalledstordiscpower[
                        r, y, t] * M.Availability[
                            r, y, t, h] - M.eleccommitstordisc[r, y, t, h]
        else:
            return M.electechchar[r, y, t, h] + M.aFCRdownStorChar[
                r, y, t,
                h] + M.aFRRdownStorChar[r, y, t, h] + M.mFRRdownStorChar[
                    r, y, t, h] <= M.totalinstalledstordiscpower[
                        r, y, t] * M.Availability[
                            r, y, t, h] - M.eleccommitstordisc[r, y, t, h]
    else:
        if t in M.TECH_DSM:
            return M.electechchar[r, y, t, h] + M.aFCRupStorChar[
                r, y, t, h] + M.aFRRupStorChar[r, y, t, h] + M.mFRRupStorChar[
                    r, y, t, h] <= M.eleccommitstorchar[r, y, t, h]
        else:
            return M.electechchar[r, y, t, h] + M.aFCRdownStorChar[
                r, y, t,
                h] + M.aFRRdownStorChar[r, y, t, h] + M.mFRRdownStorChar[
                    r, y, t, h] <= M.eleccommitstorchar[r, y, t, h]


def ElecMaxOutputStorDiscConstraint_rule(M, r, y, t, h):
    if t in M.TECH_DSM:
        return M.electechdisc[r, y, t, h] + M.aFCRdownStorDisc[
            r, y, t, h] + M.aFRRdownStorDisc[r, y, t,
                                             h] <= M.eleccommitstordisc[r, y,
                                                                        t, h]
    else:
        return M.electechdisc[r, y, t, h] + M.aFCRupStorDisc[
            r, y, t, h] + M.aFRRupStorDisc[r, y, t, h] <= M.eleccommitstordisc[
                r, y, t, h]


def ElecMaxOutputStorDiscQuickStartConstraint_rule(M, r, y, t, h):
    if M.StorMFRRup[y, t] == 1:
        if t in M.TECH_DSM:
            return M.electechdisc[r, y, t, h] + M.aFCRdownStorDisc[
                r, y, t,
                h] + M.aFRRdownStorDisc[r, y, t, h] + M.mFRRdownStorDisc[
                    r, y, t, h] <= M.totalinstalledstordiscpower[
                        r, y, t] * M.Availability[
                            r, y, t, h] - M.eleccommitstorchar[r, y, t, h]
        else:
            return M.electechdisc[r, y, t, h] + M.aFCRupStorDisc[
                r, y, t, h] + M.aFRRupStorDisc[r, y, t, h] + M.mFRRupStorDisc[
                    r, y, t, h] <= M.totalinstalledstordiscpower[
                        r, y, t] * M.Availability[
                            r, y, t, h] - M.eleccommitstorchar[r, y, t, h]
    else:
        if t in M.TECH_DSM:
            return M.electechdisc[r, y, t, h] + M.aFCRdownStorDisc[
                r, y, t,
                h] + M.aFRRdownStorDisc[r, y, t, h] + M.mFRRdownStorDisc[
                    r, y, t, h] <= M.eleccommitstordisc[r, y, t, h]
        else:
            return M.electechdisc[r, y, t, h] + M.aFCRupStorDisc[
                r, y, t, h] + M.aFRRupStorDisc[r, y, t, h] + M.mFRRupStorDisc[
                    r, y, t, h] <= M.eleccommitstordisc[r, y, t, h]


def ElecMaxOutputStorDiscConstraint1_rule(M, r, y, t, h):
    if t in M.TECH_DSM:
        return M.electechdisc[r, y, t, h] + M.aFCRdownStorDisc[
            r, y, t, h] + M.aFRRdownStorDisc[r, y, t, h] + M.mFRRdownStorDisc[
                r, y, t, h] <= M.electechstored[r, y, t, h]
    else:
        return M.electechdisc[r, y, t, h] + M.aFCRupStorDisc[
            r, y, t, h] + M.aFRRupStorDisc[r, y, t, h] + M.mFRRupStorDisc[
                r, y, t, h] <= M.electechstored[r, y, t, h]


def ElecMinStartUpHourGenConstraint_rule(M, r, y, t, h):
    return M.eleccommitgen[r, y, t, h] >= sum(
        M.elecstartupgen[r, y, t, h]
        for h in sequence(h - M.GenMinStartUpHour[y, t], h)
        if h - M.GenMinShutDownHour[y, t] > 0)


def ElecMinStartUpHourStorCharConstraint_rule(M, r, y, t, h):
    return M.eleccommitstorchar[r, y, t, h] >= sum(
        M.elecstartupstorchar[r, y, t, h]
        for h in sequence(h - M.StorMinStartUpHour[y, t], h)
        if h - M.StorMinShutDownHour[y, t] > 0)


def ElecMinStartUpHourStorDiscConstraint_rule(M, r, y, t, h):
    return M.eleccommitstordisc[r, y, t, h] >= sum(
        M.elecstartupstordisc[r, y, t, h]
        for h in sequence(h - M.StorMinStartUpHour[y, t], h)
        if h - M.StorMinShutDownHour[y, t] > 0)


def ElecMinShutDownHourGenConstraint_rule(M, r, y, t, h):
    return M.totalinstalledgencapacity[r, y, t] * M.Availability[
        r, y, t, h] - M.eleccommitgen[r, y, t, h] >= sum(
            M.elecshutdowngen[r, y, t, h]
            for h in sequence(h - M.GenMinShutDownHour[y, t], h)
            if h - M.GenMinShutDownHour[y, t] > 0)


def ElecMinShutDownHourStorCharConstraint_rule(M, r, y, t, h):
    return M.totalinstalledstordiscpower[r, y, t] * M.Availability[
        r, y, t, h] - M.eleccommitstorchar[r, y, t, h] >= sum(
            (M.elecshutdownstorchar[r, y, t, h])
            for h in sequence(h - M.StorMinShutDownHour[y, t], h)
            if h - M.StorMinShutDownHour[y, t] > 0)


def ElecMinShutDownHourStorDiscConstraint_rule(M, r, y, t, h):
    return M.totalinstalledstordiscpower[r, y, t] * M.Availability[
        r, y, t, h] - M.eleccommitstordisc[r, y, t, h] >= sum(
            (M.elecshutdownstordisc[r, y, t, h])
            for h in sequence(h - M.StorMinShutDownHour[y, t], h)
            if h - M.StorMinShutDownHour[y, t] > 0)


def ReserveRequiredaFRRupConstraint_rule(M, r, y, h):
    return M.aFRRuprequired[r, y, h] == M.Demand[r, y, h] * M.DErrAFRRup + sum(
        M.ErrAFRRup[t] * M.electechgen[r, y, t, h]
        for t in M.TECH_VRES if (r, y, t) in M.REGION_YEAR_TECH_VRES)


def ReserveRequiredaFRRdownConstraint_rule(M, r, y, h):
    return M.aFRRdownrequired[r, y,
                              h] == M.Demand[r, y, h] * M.DErrAFRRdown + sum(
                                  M.ErrAFRRdown[t] * M.electechgen[r, y, t, h]
                                  for t in M.TECH_VRES
                                  if (r, y, t) in M.REGION_YEAR_TECH_VRES)


def ReserveRequiredmFRRupConstraint_rule(M, r, y, h):
    return M.mFRRuprequired[r, y, h] == M.Demand[r, y, h] * M.DErrMFRRup + sum(
        M.ErrMFRRup[t] * M.electechgen[r, y, t, h]
        for t in M.TECH_VRES if (r, y, t) in M.REGION_YEAR_TECH_VRES)


def ReserveRequiredmFRRdownConstraint_rule(M, r, y, h):
    return M.mFRRdownrequired[r, y,
                              h] == M.Demand[r, y, h] * M.DErrMFRRdown + sum(
                                  M.ErrMFRRdown[t] * M.electechgen[r, y, t, h]
                                  for t in M.TECH_VRES
                                  if (r, y, t) in M.REGION_YEAR_TECH_VRES)


def ReserveaFCRUpBalanceConstraint_rule(M, r, y, h):
    return sum(M.aFCRupGen[r, y, t, h] for t in M.TECH_FCRup if (
        r, y, t) in M.REGION_YEAR_TECH_Gen_FCRup) + sum(
            M.aFCRupStorChar[r, y, t, h] for t in M.TECH_FCRup
            if (r, y, t) in M.REGION_YEAR_TECH_Stor_FCRup) + +sum(
                M.aFCRupStorDisc[r, y, t, h] for t in M.TECH_FCRup if
                (r, y, t) in M.REGION_YEAR_TECH_Stor_FCRup) == M.FCRRequired[r,
                                                                             y]


def ReserveaFCRDownBalanceConstraint_rule(M, r, y, h):
    return sum(M.aFCRdownGen[r, y, t, h] for t in M.TECH_FCRdown
               if (r, y, t) in M.REGION_YEAR_TECH_Gen_FCRdown) + sum(
                   M.aFCRdownStorChar[r, y, t, h] for t in M.TECH_FCRdown
                   if (r, y, t) in M.REGION_YEAR_TECH_Stor_FCRdown) + +sum(
                       M.aFCRdownStorDisc[r, y, t, h]
                       for t in M.TECH_FCRdown if (r, y, t) in
                       M.REGION_YEAR_TECH_Stor_FCRdown) == M.FCRRequired[r, y]


def ReserveaFRRUpBalanceConstraint_rule(M, r, y, h):
    return sum(M.aFRRupGen[r, y, t, h] for t in M.TECH_aFRRup
               if (r, y, t) in M.REGION_YEAR_TECH_Gen_aFRRup) + sum(
                   M.aFRRupStorChar[r, y, t, h] for t in M.TECH_aFRRup
                   if (r, y, t) in M.REGION_YEAR_TECH_Stor_aFRRup) + +sum(
                       M.aFRRupStorDisc[r, y, t, h]
                       for t in M.TECH_aFRRup if (r, y, t) in
                       M.REGION_YEAR_TECH_Stor_aFRRup) == M.aFRRuprequired[r,
                                                                           y,
                                                                           h]


def ReserveaFRRDownBalanceConstraint_rule(M, r, y, h):
    return sum(M.aFRRdownGen[r, y, t, h] for t in M.TECH_aFRRdown
               if (r, y, t) in M.REGION_YEAR_TECH_Gen_aFRRdown) + sum(
                   M.aFRRdownStorChar[r, y, t, h] for t in M.TECH_aFRRdown
                   if (r, y, t) in M.REGION_YEAR_TECH_Stor_aFRRdown) + sum(
                       M.aFRRdownStorDisc[r, y, t, h]
                       for t in M.TECH_aFRRdown if (r, y, t) in M.
                       REGION_YEAR_TECH_Stor_aFRRdown) == M.aFRRdownrequired[r,
                                                                             y,
                                                                             h]


def ReservemFRRUpBalanceConstraint_rule(M, r, y, h):
    return sum(M.mFRRupGen[r, y, t, h] for t in M.TECH_mFRRup
               if (r, y, t) in M.REGION_YEAR_TECH_Gen_mFRRup) + sum(
                   M.mFRRupStorChar[r, y, t, h] for t in M.TECH_mFRRup
                   if (r, y, t) in M.REGION_YEAR_TECH_Stor_mFRRup) + +sum(
                       M.mFRRupStorDisc[r, y, t, h]
                       for t in M.TECH_mFRRup if (r, y, t) in
                       M.REGION_YEAR_TECH_Stor_mFRRup) == M.mFRRuprequired[r,
                                                                           y,
                                                                           h]


def ReservemFRRDownBalanceConstraint_rule(M, r, y, h):
    return sum(M.mFRRdownGen[r, y, t, h] for t in M.TECH_mFRRdown
               if (r, y, t) in M.REGION_YEAR_TECH_Gen_mFRRdown) + sum(
                   M.mFRRdownStorChar[r, y, t, h] for t in M.TECH_mFRRdown
                   if (r, y, t) in M.REGION_YEAR_TECH_Stor_mFRRdown) + sum(
                       M.mFRRdownStorDisc[r, y, t, h]
                       for t in M.TECH_mFRRdown if (r, y, t) in M.
                       REGION_YEAR_TECH_Stor_mFRRdown) == M.mFRRdownrequired[r,
                                                                             y,
                                                                             h]


def ReserveaFCRUpGenLimitConstraint_rule(M, r, y, t, h):
    return M.aFCRupGen[r, y, t,
                       h] <= M.eleccommitgen[r, y, t, h] * M.GenFCRup[y, t]


def ReserveaFCRUpStorCharLimitConstraint_rule(M, r, y, t, h):
    return M.aFCRupStorChar[
        r, y, t, h] <= M.eleccommitstorchar[r, y, t, h] * M.StorFCRup[y, t]


def ReserveaFCRUpStorDiscLimitConstraint_rule(M, r, y, t, h):
    return M.aFCRupStorDisc[
        r, y, t, h] <= M.eleccommitstordisc[r, y, t, h] * M.StorFCRup[y, t]


def ReserveaFCRDownGenLimitConstraint_rule(M, r, y, t, h):
    return M.aFCRdownGen[r, y, t,
                         h] <= M.eleccommitgen[r, y, t, h] * M.GenFCRdown[y, t]


def ReserveaFCRDownStorCharLimitConstraint_rule(M, r, y, t, h):
    return M.aFCRdownStorChar[
        r, y, t, h] <= M.eleccommitstorchar[r, y, t, h] * M.StorFCRdown[y, t]


def ReserveaFCRDownStorDiscLimitConstraint_rule(M, r, y, t, h):
    return M.aFCRdownStorDisc[
        r, y, t, h] <= M.eleccommitstordisc[r, y, t, h] * M.StorFCRdown[y, t]


def ReserveaFRRUpGenLimitConstraint_rule(M, r, y, t, h):
    return M.aFRRupGen[r, y, t,
                       h] <= M.eleccommitgen[r, y, t, h] * M.GenAFRRup[y, t]


def ReserveaFRRUpStorCharLimitConstraint_rule(M, r, y, t, h):
    return M.aFRRupStorChar[
        r, y, t, h] <= M.eleccommitstorchar[r, y, t, h] * M.StorAFRRup[y, t]


def ReserveaFRRUpStorDiscLimitConstraint_rule(M, r, y, t, h):
    return M.aFRRupStorDisc[
        r, y, t, h] <= M.eleccommitstordisc[r, y, t, h] * M.StorAFRRup[y, t]


def ReserveaFRRDownGenLimitConstraint_rule(M, r, y, t, h):
    return M.aFRRdownGen[
        r, y, t, h] <= M.eleccommitgen[r, y, t, h] * M.GenAFRRdown[y, t]


def ReserveaFRRDownStorCharLimitConstraint_rule(M, r, y, t, h):
    return M.aFRRdownStorChar[
        r, y, t, h] <= M.eleccommitstorchar[r, y, t, h] * M.StorAFRRdown[y, t]


def ReserveaFRRDownStorDiscLimitConstraint_rule(M, r, y, t, h):
    return M.aFRRdownStorDisc[
        r, y, t, h] <= M.eleccommitstordisc[r, y, t, h] * M.StorAFRRdown[y, t]


def ReservemFRRUpGenLimitConstraint_rule(M, r, y, t, h):
    if M.GenMFRRup[y, t] == 1:
        return M.mFRRupGen[r, y, t, h] <= M.totalinstalledgencapacity[
            r, y, t] * M.Availability[r, y, t, h] * M.GenMFRRup[y, t]
    else:
        return M.mFRRupGen[
            r, y, t, h] <= M.eleccommitgen[r, y, t, h] * M.GenMFRRup[y, t]


def ReservemFRRUpStorCharLimitConstraint_rule(M, r, y, t, h):
    return M.mFRRupStorChar[
        r, y, t, h] <= M.eleccommitstorchar[r, y, t, h] * M.StorMFRRdown[y, t]


def ReservemFRRUpStorDiscLimitConstraint_rule(M, r, y, t, h):
    if M.StorMFRRup[y, t] == 1:
        return M.mFRRupStorDisc[r, y, t, h] <= M.totalinstalledstordiscpower[
            r, y, t] * M.Availability[r, y, t, h] - M.eleccommitstorchar[r, y,
                                                                         t, h]
    else:
        return M.mFRRupStorDisc[
            r, y, t,
            h] <= M.eleccommitstordisc[r, y, t, h] * M.StorMFRRup[y, t]


def ReservemFRRDownGenLimitConstraint_rule(M, r, y, t, h):
    return M.mFRRdownGen[
        r, y, t, h] <= M.eleccommitgen[r, y, t, h] * M.GenMFRRdown[y, t]


def ReservemFRRDownStorCharLimitConstraint_rule(M, r, y, t, h):
    if M.StorMFRRup[y, t] == 1:
        return M.mFRRdownStorChar[r, y, t, h] <= M.totalinstalledstordiscpower[
            r, y, t] * M.Availability[r, y, t, h] - M.eleccommitstordisc[r, y,
                                                                         t, h]
    else:
        return M.mFRRdownStorChar[
            r, y, t,
            h] <= M.eleccommitstorchar[r, y, t, h] * M.StorMFRRup[y, t]


def ReservemFRRDownStorDiscLimitConstraint_rule(M, r, y, t, h):
    return M.mFRRdownStorDisc[
        r, y, t, h] <= M.eleccommitstordisc[r, y, t, h] * M.StorMFRRdown[y, t]


def AnnualEmissionConstraint_rule(M, r, y):
    return sum(
        (M.annualelectechgen[r, y, t] * M.EmissionFactor[y, t] *
         (1 - M.CCSRatio[y, t])) for t in M.TECH_GENERATION
        if (r, y, t) in M.REGION_YEAR_TECH_GENERATION) - sum(
            (sum((M.electechgtp[r, y, t, h] + M.electechbiogas[r, y, t, h])
                 for h in M.TIMESLICE) * M.GenFullLoadEffi[y, t] *
             M.EmissionFactor[y, t] * (1 - M.CCSRatio[y, t]))
            for t in M.TECH_GAS
            if (r, y, t) in M.REGION_YEAR_TECH_GAS) == M.annualemission[r, y]


def MaxAnnualRegEmissionConstraint_rule(M, r, y):
    return M.annualemission[r, y] <= M.AnnualMaxEmission[r, y]


def TotalEmissionBudgetConstraint_rule(M, r):
    return sum(M.annualemission[r, y] * ny
               for (y, ny) in M.YEARPERIOD) <= M.EmissionBudget[r]


def RESPercentageLimitConstraint_rule(M, r, y):
    return M.respercentage[r, y] >= M.RESPer[r, y]


def RESPercentageConstraint_rule(M, r, y):
    return 1 - M.nucpercentage[r,
                               y] - M.fossilpercentage[r,
                                                       y] == M.respercentage[r,
                                                                             y]


def IRESCapacityConstraint_rule(M, r, y):
    return sum(M.totalinstalledgencapacity[r, y, t] for t in M.TECH_IRES
               if (r, y,
                   t) in M.REGION_YEAR_TECH_GENERATION) == M.irescapacity[r, y]


def NUCPercentageLimitConstraint_rule(M, r, y):
    return M.nucpercentage[r, y] <= M.NUCPer[r, y]


def NUCPercentageConstraint_rule(M, r, y):
    return sum(
        M.annualelectechgen[r, y, t]
        for t in M.TECH_NUC if (r, y, t) in M.REGION_YEAR_TECH_NUC) / sum(
            M.Demand[r, y, h] for h in M.TIMESLICE) == M.nucpercentage[r, y]


def FOSSILPercentageConstraint_rule(M, r, y):
    return sum(M.annualelectechgen[r, y, t] for t in M.TECH_FOSSIL
               if (r, y, t) in M.REGION_YEAR_TECH_FOSSIL) / sum(
                   M.Demand[r, y, h]
                   for h in M.TIMESLICE) == M.fossilpercentage[r, y]


if __name__ == "__main__":
    pass
