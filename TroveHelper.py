import pandas as pd
import re
from pandarallel import pandarallel
from EnergyLevels import EnergyLevels
pandarallel.initialize(progress_bar=True)

def ReadTroveEnergies(TroveEnergiesFile):
    # Defines variables for regular expression search
    AnyBracketedExpression = r'\([^)]+\)'
    NumericalBracketedExpression = r'\([^)a-zA-Z;]*\)'
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
        
def ObtainSymmetryMap(EnergyLevelsObject):
    EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
    SymmetryMap = {}
    # Obtain all unique entries for the symmetry gamma
    SymmetriesList = EnergyLevelsDataFrame["Gamma"].unique()
    for i in range(len(SymmetriesList)):
        SymmetryMap[SymmetriesList[i]] = i + 1 
    EnergyLevelsObject.SetSymmetryMap(SymmetryMap)