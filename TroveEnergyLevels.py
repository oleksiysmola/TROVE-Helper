import pandas as pd

class TroveEnergyLevels:
    def __init__(self, TroveLevelsDataFrame):
        self.TroveLevelsDataFrame = TroveLevelsDataFrame
    def SetTroveLevelsDataFrame(self, TroveLevelsDataFrame):
        self.TroveLevelsDataFrame = TroveLevelsDataFrame
    def GetTroveLevelsDataFrame(self):
        return self.TroveLevelsDataFrame