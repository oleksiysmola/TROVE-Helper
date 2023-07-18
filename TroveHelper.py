import pandas as pd
import re
from pandarallel import pandarallel
from EnergyLevels import EnergyLevels
pandarallel.initialize(progress_bar=True)

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

def FindMatchingLevel(MarvelEnergyLevel, TroveEnergyLevelsDataFrame):
    TroveEnergyLevelsDataFrame["Obs-Calc"] = abs(MarvelEnergyLevel["Energy"] - TroveEnergyLevelsDataFrame["Energy"].astype(float))
    MatchingTroveEnergyLevel = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["Obs-Calc"] == TroveEnergyLevelsDataFrame["Obs-Calc"].min()].squeeze()
    MarvelEnergyLevel["Calculated"] = float(MatchingTroveEnergyLevel["Energy"])
    MarvelEnergyLevel["N"] = int(MatchingTroveEnergyLevel["N"])
    return MarvelEnergyLevel

def FindMatchingLevels(MarvelEnergyLevelsDataFrame, TroveEnergyLevelsDataFrame):
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["J"] == MarvelEnergyLevelsDataFrame.head(1).squeeze()["J"].astype(str)]
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["Gamma"] == MarvelEnergyLevelsDataFrame.head(1).squeeze()["Gamma"].astype(int)]
    MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsDataFrame.apply(lambda x:FindMatchingLevel(x, TroveEnergyLevelsDataFrame), axis=1, result_type="expand")
    return MarvelEnergyLevelsDataFrame

def ApplyFindMatchingLevels(MarvelEnergyLevelsObject, TroveEnergyLevelsObject):
    MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsObject.GetEnergyLevelsDataFrame()
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsObject.GetEnergyLevelsDataFrame()
    MarvelEnergyLevelsGroupedByJAndSymmetry = MarvelEnergyLevelsDataFrame.groupby(["J", "Gamma"])
    MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsGroupedByJAndSymmetry.parallel_apply(lambda x:FindMatchingLevels(x, TroveEnergyLevelsDataFrame))
    MarvelEnergyLevelsDataFrame = MarvelEnergyLevelsDataFrame.reset_index(drop=True)
    MarvelEnergyLevelsObject.SetEnergyLevelsDataFrame(MarvelEnergyLevelsDataFrame)
    return MarvelEnergyLevelsObject

def GenerateRoVibrationalTag(EnergyLevelsObject):
    EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    EnergyLevelsDataFrame["RoVibrationalTag"] = EnergyLevelsDataFrame["Ka"].astype(str)
    VibrationalQuantaStillRemaining = True
    VibrationalQuantumNumber = 1
    while VibrationalQuantaStillRemaining:
        try:
            EnergyLevelsDataFrame["RoVibrationalTag"] += "-" + EnergyLevelsDataFrame[f"v{VibrationalQuantumNumber}"].astype(str)
        except KeyError:
            VibrationalQuantaStillRemaining = False
        VibrationalQuantumNumber += 1
    EnergyLevelsObject.SetEnergyLevelsDataFrame(EnergyLevelsDataFrame)
    return EnergyLevelsObject