import pandas as pd

class EnergyLevels:
    def __init__(self, EnergyLevelsDataFrame, SymmetryMap=None):
        self.EnergyLevelsDataFrame = EnergyLevelsDataFrame
        self.SymmetryMap = SymmetryMap

    def SetLevelsDataFrame(self, EnergyLevelsDataFrame):
        self.EnergyLevelsDataFrame = EnergyLevelsDataFrame

    def GetLevelsDataFrame(self):
        return self.EnergyLevelsDataFrame
    
    def SetSymmetryMap(self, SymmetryMap):
        self.SymmetryMap = SymmetryMap
    
    def GetSymmetryMap(self):
        return self.SymmetryMap