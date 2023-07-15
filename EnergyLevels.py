import pandas as pd

class EnergyLevels:
    def __init__(self, EnergyLevelsDataFrame, SymmetryMap=None):
        self.EnergyLevelsDataFrame = EnergyLevelsDataFrame
        self.SymmetryMap = SymmetryMap

    def SetEnergyLevelsDataFrame(self, EnergyLevelsDataFrame):
        self.EnergyLevelsDataFrame = EnergyLevelsDataFrame

    def GetEnergyLevelsDataFrame(self):
        return self.EnergyLevelsDataFrame
    
    def SetSymmetryMap(self, SymmetryMap):
        self.SymmetryMap = SymmetryMap
    
    def GetSymmetryMap(self):
        return self.SymmetryMap
    
    def __eq__(self, OtherEnergyLevelsObject):
        if isinstance(OtherEnergyLevelsObject, EnergyLevels):
            return self.EnergyLevelsDataFrame.equals(OtherEnergyLevelsObject.EnergyLevelsDataFrame) and self.SymmetryMap == OtherEnergyLevelsObject.SymmetryMap
        return False