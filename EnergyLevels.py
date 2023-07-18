import pandas as pd

class EnergyLevels:
    def __init__(self, EnergyLevelsDataFrame, SymmetryMap=None, ObsMinusCalc=None):
        self.EnergyLevelsDataFrame = EnergyLevelsDataFrame
        self.SymmetryMap = SymmetryMap
        self.ObsMinusCalc = ObsMinusCalc

    def SetEnergyLevelsDataFrame(self, EnergyLevelsDataFrame):
        self.EnergyLevelsDataFrame = EnergyLevelsDataFrame

    def GetEnergyLevelsDataFrame(self):
        return self.EnergyLevelsDataFrame
    
    def SetSymmetryMap(self, SymmetryMap):
        self.SymmetryMap = SymmetryMap
    
    def GetSymmetryMap(self):
        return self.SymmetryMap
    
    def SetObsMinusCalc(self, ObsMinusCalc):
        self.ObsMinusCalc = ObsMinusCalc
    
    def GetObsMinusCalc(self):
        return self.ObsMinusCalc
    
    def __eq__(self, OtherEnergyLevelsObject):
        if isinstance(OtherEnergyLevelsObject, EnergyLevels):
            return self.EnergyLevelsDataFrame.equals(OtherEnergyLevelsObject.EnergyLevelsDataFrame) and self.SymmetryMap == OtherEnergyLevelsObject.SymmetryMap and self.ObsMinusCalc == OtherEnergyLevelsObject.ObsMinusCalc
        return False