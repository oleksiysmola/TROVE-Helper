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

def FindMatchingLevels(MarvelEnergyLevelsDataFrame, TroveEnergyLevelsDataFrame):
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["J"] == MarvelEnergyLevelsDataFrame.head(1).squeeze()["J"]]
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["Gamma"] == MarvelEnergyLevelsDataFrame.head(1).squeeze()["Gamma"]]
    EnergyMatches = {}
    EnergyMatchedToCountingNumber = {}
    for MarvelEnergyLevel in MarvelEnergyLevelsDataFrame:
        TroveEnergyLevelsDataFrame["Obs-Calc"] = abs(MarvelEnergyLevel["Energy"] - TroveEnergyLevelsDataFrame["Energy"])
        MatchingTroveEnergyLevel = TroveEnergyLevelsDataFrame[TroveEnergyLevelsDataFrame["Obs-Calc"] == TroveEnergyLevelsDataFrame["Obs-Calc"].min()].squeeze()
        EnergyMatches[MarvelEnergyLevel["Energy"]] = MatchingTroveEnergyLevel["Energy"]
        EnergyMatchedToCountingNumber[MarvelEnergyLevel["Energy"]] = MatchingTroveEnergyLevel["N"]
        TroveEnergyLevelsDataFrame = TroveEnergyLevelsDataFrame.drop("Obs-Calc", axis=1)
    MarvelEnergyLevelsDataFrame["Calculated"] = MarvelEnergyLevelsDataFrame["Energy"].map(EnergyMatches)
    MarvelEnergyLevelsDataFrame["N"] = MarvelEnergyLevelsDataFrame["Energy"].map(EnergyMatchedToCountingNumber)
    return MarvelEnergyLevelsDataFrame

def ApplyFindMatchingLevels(MarvelEnergyLevelsObject, TroveEnergyLevelsObject):
    MarvelEnergyLevelDataFrame = MarvelEnergyLevelsObject.GetEnergyLevelsDataFrame()
    TroveEnergyLevelsDataFrame = TroveEnergyLevelsObject.GetEnergyLevelsDataFrame()
    MarvelEnergyLevelsGroupedByJAndSymmetry = MarvelEnergyLevelDataFrame.groupby(["J", "Gamma"])
    MarvelEnergyLevelDataFrame = MarvelEnergyLevelsGroupedByJAndSymmetry.parallel_apply(lambda x:FindMatchingLevels(x, TroveEnergyLevelsDataFrame))
    MarvelEnergyLevelsObject.SetEnergyLevelsDataFrame(MarvelEnergyLevelDataFrame)
    return MarvelEnergyLevelsObject