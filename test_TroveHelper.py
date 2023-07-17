import pytest
import pandas as pd
from TroveHelper import *
from EnergyLevels import EnergyLevels

@pytest.fixture
def SetupFormaldehydeTest():
    EnergyLevelsColumnsFormaldehyde = ["Gamma", "N", "Energy", "GammaRotational", "J", "Ka", "t", 
                                       "GammaVibrational", "v1", "v2", "v3", "v4", "v5", "v6"]
    EnergyLevelsTestInput = [["A1", "1", "102.330982", "A1", "10", "0", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["A1", "2", "123.276297", "A1", "10", "2", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["A2", "1",  "20.820897", "A2",  "2", "2", "1", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["A2", "2", "932.241834", "B2",  "2", "1", "1", "B1", "0", "0", "0", "0", "0", "1"], 
                        ["A2", "3", "990.607820", "B1",  "2", "1", "0", "B2", "0", "0", "0", "0", "1", "0"], 
                        ["B1", "1",  "14.686424", "B1",  "3", "1", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["B1", "2",  "45.404075", "B1",  "3", "3", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["B2", "1",  "15.869367", "B2",  "3", "1", "1", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["B2", "2",  "45.404265", "B2",  "3", "3", "1", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["B2", "3", "934.866750", "A2",  "3", "0", "1", "B1", "0", "0", "0", "0", "0", "1"]]
    TestEnergyLevelsDataFrame = pd.DataFrame(EnergyLevelsTestInput, columns=EnergyLevelsColumnsFormaldehyde)
    TestEnergyLevelsObject = EnergyLevels(TestEnergyLevelsDataFrame) 
    MarvelLevelsColumnsFormaldehyde = ["Gamma",	"GammaRot", "J", "Ka", "Kc", "GammaVib", "v1", "v2", "v3", "v4", "v5", "v6", "Tag", "Energy", "Uncertainty", "Source"]
    MarvelLevelsTestInput = [
        [2, 3, 2, 1, 1, 4, 0, 0, 1, 0, 0, 1, "2-1-1-0-0-1-0-0-1", 2083.32885, 0.0026, "05LoUlBe"],
        [1, 4, 3, 1, 2, 4, 0, 0, 1, 0, 0, 1, "3-1-2-0-0-1-0-0-1", 2089.59045, 0.0026, "05LoUlBe"],
        [1, 4, 2, 1, 2, 4, 0, 0, 1, 0, 0, 1, "2-1-2-0-0-1-0-0-1", 2082.71350, 0.0026, "05LoUlBe"]
    ]
    TestMarvelLevelsDataFrame = pd.DataFrame(MarvelLevelsTestInput, columns=MarvelLevelsColumnsFormaldehyde)
    TestMarvelLevelsObject = EnergyLevels(TestMarvelLevelsDataFrame)
    SortedMarvelLevelsTestInput = [
        [1, 4, 2, 1, 2, 4, 0, 0, 1, 0, 0, 1, "2-1-2-0-0-1-0-0-1", 2082.71350, 0.0026, "05LoUlBe"],
        [2, 3, 2, 1, 1, 4, 0, 0, 1, 0, 0, 1, "2-1-1-0-0-1-0-0-1", 2083.32885, 0.0026, "05LoUlBe"],
        [1, 4, 3, 1, 2, 4, 0, 0, 1, 0, 0, 1, "3-1-2-0-0-1-0-0-1", 2089.59045, 0.0026, "05LoUlBe"]
    ]
    TestSortedMarvelLevelsDataFrame = pd.DataFrame(SortedMarvelLevelsTestInput, columns=MarvelLevelsColumnsFormaldehyde)
    TestSortedMarvelLevelsObject = EnergyLevels(TestSortedMarvelLevelsDataFrame)
    yield TestEnergyLevelsObject, TestMarvelLevelsObject, TestSortedMarvelLevelsObject

def test_ReadTroveEnergies(SetupFormaldehydeTest):
    ExpectedEnergyLevelsObject, _, _ = SetupFormaldehydeTest
    OutputEnergyLevelsObject = ReadTroveEnergies("ReadTroveEnergiesH2CO.test")
    assert OutputEnergyLevelsObject == ExpectedEnergyLevelsObject

def test_ReadMarvelEnergies(SetupFormaldehydeTest):
    _, ExpectedMarvelLevelsObject, _ = SetupFormaldehydeTest
    OutputMarvelLevelsObject = ReadMarvelEnergies("ReadMarvelEnergies.test")
    assert OutputMarvelLevelsObject == ExpectedMarvelLevelsObject

def test_ObtainSymmetryMap(SetupFormaldehydeTest):
    TestEnergyLevelsObject, _, _ = SetupFormaldehydeTest
    ExpectedSymmetryMap = {"A1": 1,
                           "A2": 2,
                           "B1": 3,
                           "B2": 4}
    ObtainSymmetryMap(TestEnergyLevelsObject)
    OutputSymmetryMap = TestEnergyLevelsObject.GetSymmetryMap()
    assert OutputSymmetryMap == ExpectedSymmetryMap

def test_SortEnergyLevelsByJAndSymmetry(SetupFormaldehydeTest):
    _, TestMarvelLevelsObject, ExpectedSortedMarvelLevelsObject = SetupFormaldehydeTest
    OutputSortedMarvelLevelsObject = SortEnergyLevelsByJAndSymmetry(TestMarvelLevelsObject)
    assert OutputSortedMarvelLevelsObject == ExpectedSortedMarvelLevelsObject

    