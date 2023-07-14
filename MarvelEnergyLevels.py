import pandas as pd

class MarvelEnergyLevels:
    def __init__(self, MarvelLevelsDataFrame):
        self.MarvelLevelsDataFrame = MarvelLevelsDataFrame
    def SetMarvelLevelsDataFrame(self, MarvelLevelsDataFrame):
        self.MarvelLevelsDataFrame = MarvelLevelsDataFrame
    def GetMarvelLevelsDataFrame(self):
        return self.MarvelLevelsDataFrame