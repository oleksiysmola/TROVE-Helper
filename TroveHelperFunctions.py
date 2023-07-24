import pandas as pd
import numpy as np
import re
from pandarallel import pandarallel
from EnergyLevels import EnergyLevels
pandarallel.initialize(progress_bar=False)

def ReadTroveEnergies(TroveEnergiesFile):
    # Defines variables for regular expression search
    AnyBracketedExpression = r'\([^)]+\)'
    CharactersToDrop = r"[();]"
    with open(TroveEnergiesFile) as TroveEnergiesToRead:
        TroveEnergies = []
        for TroveEnergy in TroveEnergiesToRead:
            TroveEnergySplit = TroveEnergy.split()
            BracketedExpressions = re.findall(AnyBracketedExpression, TroveEnergy)
            RotationalQuanta = re.sub(CharactersToDrop, "", BracketedExpressions[0]).split()
            VibrationalQuanta = re.sub(CharactersToDrop, "", BracketedExpressions[1]).split()
            TroveEnergies += [TroveEnergySplit[:3] + RotationalQuanta + VibrationalQuanta]
    NumberOfVibrationalModes = len(VibrationalQuanta) - 1
    VibrationalQuantumNumbers = []
    for i in range(NumberOfVibrationalModes):
        VibrationalQuantumNumbers += [f"v{i + 1}"]
    EnergyLevelsDataFrameColumns = ["Gamma", "N", "Energy", "GammaRotational", 
                                    "J", "Ka", "t", "GammaVibrational"]
    EnergyLevelsDataFrameColumns += VibrationalQuantumNumbers
    EnergyLevelsDataFrame = pd.DataFrame(TroveEnergies, columns=EnergyLevelsDataFrameColumns)
    EnergyLevelsDataFrame["Energy"] = EnergyLevelsDataFrame["Energy"].astype(float)
    EnergyLevelsDataFrame["N"] = EnergyLevelsDataFrame["N"].astype(int)
    EnergyLevelsObject = EnergyLevels(EnergyLevelsDataFrame)
    return EnergyLevelsObject

def ReadMarvelEnergies(MarvelEnergiesFile):
    EnergyLevelsDataFrame = pd.read_csv(MarvelEnergiesFile, delim_whitespace=True)
    EnergyLevelsObject = EnergyLevels(EnergyLevelsDataFrame)
    return EnergyLevelsObject
        
def ObtainSymmetryMap(EnergyLevelsObject):
    EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    SymmetryMap = {}
    # Obtain all unique entries for the symmetry gamma
    SymmetriesList = EnergyLevelsDataFrame["Gamma"].unique()
    for i in range(len(SymmetriesList)):
        SymmetryMap[SymmetriesList[i]] = i + 1 
    EnergyLevelsObject.SetSymmetryMap(SymmetryMap)
    return EnergyLevelsObject

def ApplySymmetryMapping(EnergyLevelsObject):
    EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    SymmetryMap = EnergyLevelsObject.GetSymmetryMap()
    EnergyLevelsDataFrame["Gamma"] = EnergyLevelsDataFrame["Gamma"].map(SymmetryMap)
    EnergyLevelsObject.SetEnergyLevelsDataFrame(EnergyLevelsDataFrame)
    return EnergyLevelsObject

def SortEnergyLevelsByJSymmetryAndEnergy(EnergyLevelsObject):
    EnergyLevelDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    # Ensuring the types of the parameters we use to sort are numerical rather than string
    EnergyLevelDataFrame["J"] = EnergyLevelDataFrame["J"].astype(int)
    EnergyLevelDataFrame["Gamma"] = EnergyLevelDataFrame["Gamma"].astype(int)
    EnergyLevelDataFrame["Energy"] = EnergyLevelDataFrame["Energy"].astype(float)
    EnergyLevelDataFrame = EnergyLevelDataFrame.sort_values(by=["J", "Gamma", "Energy"])
    EnergyLevelDataFrame = EnergyLevelDataFrame.reset_index().drop("index", axis=1)
    EnergyLevelsObject.SetEnergyLevelsDataFrame(EnergyLevelDataFrame)
    return EnergyLevelsObject

def FindMatchingLevel(MarvelEnergyLevel, TroveEnergyLevelsDataFrame, VibrationalTagMap=None):
    if VibrationalTagMap != None:
        TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["VibrationalTag"] == VibrationalTagMap[MarvelEnergyLevel["VibrationalTag"]]]
    else:
        TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["J"] == str(MarvelEnergyLevel["J"])]
        TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["Gamma"] == int(MarvelEnergyLevel["Gamma"])]
    TroveEnergyLevelsDataFrame["Obs-Calc"] = abs(MarvelEnergyLevel["Energy"] - TroveEnergyLevelsDataFrame["Energy"].astype(float))
    MatchingTroveEnergyLevel = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["Obs-Calc"] == TroveEnergyLevelsDataFrame["Obs-Calc"].min()].squeeze()
    MarvelEnergyLevel["Calculated"] = MatchingTroveEnergyLevel["Energy"]
    MarvelEnergyLevel["N"] = MatchingTroveEnergyLevel["N"]
    try:
        MarvelEnergyLevel["TroveVibrationalTag"] = MatchingTroveEnergyLevel["VibrationalTag"]
        MarvelEnergyLevel["TroveRoVibrationalTag"] = MatchingTroveEnergyLevel["RoVibrationalTag"]
    except:
        print("No, TROVE tags to map")
    return MarvelEnergyLevel

def FindMatchingLevels(MarvelEnergyLevelsDataFrame, TroveEnergyLevelsDataFrame, VibrationalTagMap=None):
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["J"] == str(MarvelEnergyLevelsDataFrame.head(1).squeeze()["J"])]
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["Gamma"] == int(MarvelEnergyLevelsDataFrame.head(1).squeeze()["Gamma"])]
    MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsDataFrame.apply(lambda x:FindMatchingLevel(x, TroveEnergyLevelsDataFrame, VibrationalTagMap), axis=1, result_type="expand")
    return MarvelEnergyLevelsDataFrame

def ApplyFindMatchingLevels(MarvelEnergyLevelsObject, TroveEnergyLevelsObject):
    MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsObject.GetEnergyLevelsDataFrame()
    # Temporary dummy column so apply doesn't change all the dtypes into floats!
    MarvelEnergyLevelsDataFrame["Dud"] = "s"
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsObject.GetEnergyLevelsDataFrame()
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["Energy"] < MarvelEnergyLevelsDataFrame["Energy"].max() + 10]
    MarvelEnergyLevelsGroupedByJAndSymmetry = MarvelEnergyLevelsDataFrame.groupby(["J", "Gamma"])
    try:
        TroveEnergyLevelsDataFrameCopy = TroveEnergyLevelsDataFrame.copy()
        VibrationalBands = MarvelEnergyLevelsDataFrame["VibrationalTag"].unique()
        VibrationalTagMap = {}
        for VibrationalBand in VibrationalBands:
            LowestEnergyLevelInBand = MarvelEnergyLevelsDataFrame[MarvelEnergyLevelsDataFrame["VibrationalTag"] == VibrationalBand].head(1).squeeze()
            LowestEnergyLevelInBand = FindMatchingLevel(LowestEnergyLevelInBand, TroveEnergyLevelsDataFrameCopy)
            VibrationalTagMap[VibrationalBand] = LowestEnergyLevelInBand["TroveVibrationalTag"]
        MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsGroupedByJAndSymmetry.parallel_apply(lambda x:FindMatchingLevels(x, TroveEnergyLevelsDataFrame, VibrationalTagMap))
    except:
        print("No vibrational tags assigned to Marvel levels, assign tags for more accurate matching!")
    MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsGroupedByJAndSymmetry.parallel_apply(lambda x:FindMatchingLevels(x, TroveEnergyLevelsDataFrame))
    MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsDataFrame.drop("Dud", axis=1)
    MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsDataFrame.reset_index(drop=True)
    MarvelEnergyLevelsObject.SetEnergyLevelsDataFrame(MarvelEnergyLevelsDataFrame)
    return MarvelEnergyLevelsObject

def GenerateRoVibrationalTags(EnergyLevelsObject):
    EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    EnergyLevelsDataFrame["VibrationalTag"] = EnergyLevelsDataFrame["v1"].astype(str)
    EnergyLevelsDataFrame["RoVibrationalTag"] = EnergyLevelsDataFrame["Ka"].astype(str)
    VibrationalQuantaStillRemaining = True
    VibrationalQuantumNumber = 1
    while VibrationalQuantaStillRemaining:
        try:
            EnergyLevelsDataFrame["RoVibrationalTag"] += "-" + EnergyLevelsDataFrame[f"v{VibrationalQuantumNumber}"].astype(str)
            EnergyLevelsDataFrame["VibrationalTag"] += "-" + EnergyLevelsDataFrame[f"v{VibrationalQuantumNumber + 1}"].astype(str)
        except KeyError:
            VibrationalQuantaStillRemaining = False
        VibrationalQuantumNumber += 1
    EnergyLevelsObject.SetEnergyLevelsDataFrame(EnergyLevelsDataFrame)
    return EnergyLevelsObject

def ObtainObsMinusCalc(EnergyLevelsObject):
    EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    try:
        VibrationalBands = EnergyLevelsDataFrame["VibrationalTag"].unique()
        ObsMinusCalc = {}
        try:
            EnergyLevelsDataFrame["Obs-Calc"] = EnergyLevelsDataFrame["Energy"] - EnergyLevelsDataFrame["Calculated"]
            ObsMinusCalc["Total rms"] = (EnergyLevelsDataFrame["Obs-Calc"]*EnergyLevelsDataFrame["Obs-Calc"]).mean()**0.5
            for VibrationalBand in VibrationalBands:
                EnergyLevelsInVibrationalBand = EnergyLevelsDataFrame[EnergyLevelsDataFrame["VibrationalTag"] == VibrationalBand]
                ObsMinusCalc[VibrationalBand] = (EnergyLevelsInVibrationalBand["Obs-Calc"]*EnergyLevelsInVibrationalBand["Obs-Calc"]).mean()**0.5
            EnergyLevelsObject.SetEnergyLevelsDataFrame(EnergyLevelsDataFrame)
            EnergyLevelsObject.SetObsMinusCalc(ObsMinusCalc)
        except:
            print("Could not compute Obs-Calc, please ensure MARVEL energy dataframe includes a matched Calculated column")
    except:
        print("No vibrational tags in energy levels dataframe, please generate a VibrationalTag column before proceeding")
    return EnergyLevelsObject

def ConvertToTroveRefinementInput(EnergyLevelsObject):
    EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    RefinementBlockColumns = ["J", "Gamma", "N", "Energy", "Ka"]
    VibrationalQuantumNumber = 1
    DataFrameColumnNames = EnergyLevelsDataFrame.columns
    while f"v{VibrationalQuantumNumber}" in DataFrameColumnNames:
        RefinementBlockColumns += [f"v{VibrationalQuantumNumber}"]
        VibrationalQuantumNumber += 1
    RefinementBlockColumns += ["Weight"]
    if "Weight" in DataFrameColumnNames:
        EnergyLevelsDataFrame = EnergyLevelsDataFrame[RefinementBlockColumns]
    elif "Uncertainty" and "Transitions" in DataFrameColumnNames:
        print("No weight column... generating weights based on transitions and uncertainties")
        EnergyLevelsDataFrame["Weight"] =  np.log(EnergyLevelsDataFrame["Transitions"]/EnergyLevelsDataFrame["Uncertainty"])
    else:
        print("No weights, uncertainties or transitions given... weights shall all be set to equal unity")
        EnergyLevelsDataFrame["Weight"] = 1.00
    EnergyLevelsDataFrame = EnergyLevelsDataFrame[RefinementBlockColumns]
    EnergyLevelsObject.SetEnergyLevelsDataFrame(EnergyLevelsDataFrame)
    return EnergyLevelsObject

def WriteToFile(EnergyLevelsObject, FileName):
    EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    EnergyLevelObsMinusCalc = EnergyLevelsObject.GetObsMinusCalc()
    EnergyLevelsDataFrameToString =  EnergyLevelsDataFrame.to_string(index=False)
    with open(FileName, "w+") as EnergyLevelsFile:
        EnergyLevelsFile.write(EnergyLevelsDataFrameToString)
        if EnergyLevelObsMinusCalc != None:
            EnergyLevelsFile.write("\n" + str(EnergyLevelObsMinusCalc))

def ReplaceWithTroveQuantumNumbers(EnergyLevel):
    TroveQuantumNumbers = EnergyLevel["TroveVibrationalTag"].split("-")
    for i in range(len(TroveQuantumNumbers)):
        EnergyLevel[f"v{i + 1}"] = int(TroveQuantumNumbers[i])
    return EnergyLevel

def ApplyReplaceWithTroveQuantumNumbers(EnergyLevelsObject):
    EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    EnergyLevelsDataFrame = EnergyLevelsDataFrame.parallel_apply(lambda x:ReplaceWithTroveQuantumNumbers(x), axis=1, result_type="expand")
    EnergyLevelsObject.SetEnergyLevelsDataFrame(EnergyLevelsDataFrame)
    return EnergyLevelsObject