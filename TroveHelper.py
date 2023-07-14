import pandas as pd
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

class TroveHelper:
    def SetSymmetryMap(EnergyLevelsObject):
        EnergyLevelsDataFrame = EnergyLevelsObject.GetEnergyLevelsDataFrame()
        SymmetryMap = {}
        SymmetriesList = EnergyLevelsDataFrame["Gamma"].unique()
        for i in range(len(SymmetriesList)):
            self.SymmetryMap[SymmetriesList[i]] = i + 1 
        EnergyLevelsObject.SetSymmetryMap(SymmetryMap)