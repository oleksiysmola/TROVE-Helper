import pytest
import pandas as pd
from TroveHelperFunctions import *
from EnergyLevels import EnergyLevels

@pytest.fixture
def SetupFormaldehydeTest():
    EnergyLevelsColumnsFormaldehyde = ["Gamma", "N", "Energy", "GammaRotational", "J", "Ka", "t", 
                                       "GammaVibrational", "v1", "v2", "v3", "v4", "v5", "v6"]
    EnergyLevelsTestInput = [["A1", 1, 102.330982, "A1", "10", "0", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["A1", 2, 123.276297, "A1", "10", "2", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["A2", 1,  20.820897, "A2",  "2", "2", "1", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["A2", 2, 932.241834, "B2",  "2", "1", "1", "B1", "0", "0", "0", "0", "0", "1"], 
                        ["A2", 3, 990.607820, "B1",  "2", "1", "0", "B2", "0", "0", "0", "0", "1", "0"], 
                        ["B1", 1,  14.686424, "B1",  "3", "1", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["B1", 2,  45.404075, "B1",  "3", "3", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["B2", 1,  15.869367, "B2",  "3", "1", "1", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["B2", 2,  45.404265, "B2",  "3", "3", "1", "A1", "0", "0", "0", "0", "0", "0"], 
                        ["B2", 3, 934.866750, "A2",  "3", "0", "1", "B1", "0", "0", "0", "0", "0", "1"],
                        ["A2", 10, 2047.476778, "B2", "2", "1", "1", "B1", "0", "0", "0", "1", "0", "1"],
                        ["A2", 11, 2081.682660, "A2", "2", "2", "1", "A1", "0", "0", "1", "0", "0", "0"],
                        ["A2", 12, 2083.299075, "B1", "2", "1", "0", "B2", "0", "0", "0", "0", "2", "0"],
                        ["A1", 13, 2079.099006, "B1", "3", "3", "0", "B1", "0", "0", "0", "1", "0", "1"],
                        ["A1", 14, 2087.522393, "A1", "3", "2", "0", "A1", "0", "0", "1", "0", "0", "0"],
                        ["A1", 15, 2089.573425, "B2", "3", "1", "1", "B2", "0", "0", "0", "0", "2", "0"],
                        ["A1", 16, 2081.675216, "A1", "2", "2", "0", "A1", "0", "0", "1", "0", "0", "0"],
                        ["A1", 17, 2082.696539, "B2", "2", "1", "1", "B2", "0", "0", "0", "0", "2", "0"],
                        ["A1", 18, 2172.217193, "B2", "2", "1", "1", "B2", "0", "1", "0", "0", "0", "0"]]
    TestEnergyLevelsDataFrame = pd.DataFrame(EnergyLevelsTestInput, columns=EnergyLevelsColumnsFormaldehyde)
    TestEnergyLevelsObject = EnergyLevels(TestEnergyLevelsDataFrame)
    EnergyLevelsSymmetriesMappedTestInput = [[1, 1, 102.330982, "A1", "10", "0", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        [1, 2, 123.276297, "A1", "10", "2", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        [2, 1,  20.820897, "A2",  "2", "2", "1", "A1", "0", "0", "0", "0", "0", "0"], 
                        [2, 2, 932.241834, "B2",  "2", "1", "1", "B1", "0", "0", "0", "0", "0", "1"], 
                        [2, 3, 990.607820, "B1",  "2", "1", "0", "B2", "0", "0", "0", "0", "1", "0"], 
                        [3, 1,  14.686424, "B1",  "3", "1", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        [3, 2,  45.404075, "B1",  "3", "3", "0", "A1", "0", "0", "0", "0", "0", "0"], 
                        [4, 1,  15.869367, "B2",  "3", "1", "1", "A1", "0", "0", "0", "0", "0", "0"], 
                        [4, 2,  45.404265, "B2",  "3", "3", "1", "A1", "0", "0", "0", "0", "0", "0"], 
                        [4, 3, 934.866750, "A2",  "3", "0", "1", "B1", "0", "0", "0", "0", "0", "1"],
                        [2, 10, 2047.476778, "B2", "2", "1", "1", "B1", "0", "0", "0", "1", "0", "1"],
                        [2, 11, 2081.682660, "A2", "2", "2", "1", "A1", "0", "0", "1", "0", "0", "0"],
                        [2, 12, 2083.299075, "B1", "2", "1", "0", "B2", "0", "0", "0", "0", "2", "0"],
                        [1, 13, 2079.099006, "B1", "3", "3", "0", "B1", "0", "0", "0", "1", "0", "1"],
                        [1, 14, 2087.522393, "A1", "3", "2", "0", "A1", "0", "0", "1", "0", "0", "0"],
                        [1, 15, 2089.573425, "B2", "3", "1", "1", "B2", "0", "0", "0", "0", "2", "0"],
                        [1, 16, 2081.675216, "A1", "2", "2", "0", "A1", "0", "0", "1", "0", "0", "0"],
                        [1, 17, 2082.696539, "B2", "2", "1", "1", "B2", "0", "0", "0", "0", "2", "0"],
                        [1, 18, 2172.217193, "B2", "2", "1", "1", "B2", "0", "1", "0", "0", "0", "0"]]
    TestEnergyLevelsSymmetriesMappedDataFrame = pd.DataFrame(EnergyLevelsSymmetriesMappedTestInput, columns=EnergyLevelsColumnsFormaldehyde)
    TestEnergyLevelsSymmetriesMappedObject = EnergyLevels(TestEnergyLevelsSymmetriesMappedDataFrame) 
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
    MatchedMarvelLevelsColumnsFormaldehyde = ["Gamma",	"GammaRot", "J", "Ka", "Kc", "GammaVib", "v1", "v2", "v3", "v4", "v5", "v6", "Tag", "Energy", "Uncertainty", "Source", "Calculated", "N"]
    MatchedMarvelLevelsTestInput = [
        [1, 4, 2, 1, 2, 4, 0, 0, 1, 0, 0, 1, "2-1-2-0-0-1-0-0-1", 2082.71350, 0.0026, "05LoUlBe", 2082.696539, 17],
        [2, 3, 2, 1, 1, 4, 0, 0, 1, 0, 0, 1, "2-1-1-0-0-1-0-0-1", 2083.32885, 0.0026, "05LoUlBe", 2083.299075, 12],
        [1, 4, 3, 1, 2, 4, 0, 0, 1, 0, 0, 1, "3-1-2-0-0-1-0-0-1", 2089.59045, 0.0026, "05LoUlBe", 2089.573425, 15]
    ]
    TestMatchedMarvelLevelsDataFrame = pd.DataFrame(MatchedMarvelLevelsTestInput, columns=MatchedMarvelLevelsColumnsFormaldehyde)
    TestMarvelMatchedLevelsObject = EnergyLevels(TestMatchedMarvelLevelsDataFrame)
    TaggedMarvelLevelsColumnsFormaldehyde = ["Gamma",	"GammaRot", "J", "Ka", "Kc", "GammaVib", "v1", "v2", "v3", "v4", "v5", "v6", "Tag", "Energy", "Uncertainty", "Source", "VibrationalTag", "RoVibrationalTag"]
    TaggedMarvelLevelsTestInput = [
        [2, 3, 2, 1, 1, 4, 0, 0, 1, 0, 0, 1, "2-1-1-0-0-1-0-0-1", 2083.32885, 0.0026, "05LoUlBe", "0-0-1-0-0-1", "1-0-0-1-0-0-1"],
        [1, 4, 3, 1, 2, 4, 0, 0, 1, 0, 0, 1, "3-1-2-0-0-1-0-0-1", 2089.59045, 0.0026, "05LoUlBe", "0-0-1-0-0-1", "1-0-0-1-0-0-1"],
        [1, 4, 2, 1, 2, 4, 0, 0, 1, 0, 0, 1, "2-1-2-0-0-1-0-0-1", 2082.71350, 0.0026, "05LoUlBe", "0-0-1-0-0-1", "1-0-0-1-0-0-1"]
    ]
    TestTaggedMarvelLevelsDataFrame = pd.DataFrame(TaggedMarvelLevelsTestInput, columns=TaggedMarvelLevelsColumnsFormaldehyde)
    TestTaggedMarvelLevelsObject = EnergyLevels(TestTaggedMarvelLevelsDataFrame)
    MarvelWithObsMinusCalcLevelsColumnsFormaldehyde = ["Gamma",	"GammaRot", "J", "Ka", "Kc", "GammaVib", "v1", "v2", "v3", "v4", "v5", "v6", "Tag", "Energy", "Uncertainty", "Source", "Calculated", "N", "VibrationalTag", "RoVibrationalTag", "Obs-Calc"]
    MarvelWithObsMinusCalcLevelsTestInput = [
        [1, 4, 2, 1, 2, 4, 0, 0, 1, 0, 0, 1, "2-1-2-0-0-1-0-0-1", 2082.71350, 0.0026, "05LoUlBe", 2082.696539, 17, "0-0-1-0-0-1", "1-0-0-1-0-0-1", 0.016961],
        [2, 3, 2, 1, 1, 4, 0, 0, 1, 0, 0, 1, "2-1-1-0-0-1-0-0-1", 2083.32885, 0.0026, "05LoUlBe", 2083.299075, 12, "0-0-1-0-0-1", "1-0-0-1-0-0-1", 0.029775],
        [1, 4, 3, 1, 2, 4, 0, 0, 1, 0, 0, 1, "3-1-2-0-0-1-0-0-1", 2089.59045, 0.0026, "05LoUlBe", 2089.573425, 15, "0-0-1-0-0-1", "1-0-0-1-0-0-1", 0.017025]
    ]
    TestMarvelWithObsMinusCalcLevelsDataFrame = pd.DataFrame(MarvelWithObsMinusCalcLevelsTestInput, columns=MarvelWithObsMinusCalcLevelsColumnsFormaldehyde)
    MarvelWithObsMinusCalcMatchedLevelsObject = EnergyLevels(TestMarvelWithObsMinusCalcLevelsDataFrame)
    RefinementBlockColumnsFormaldehyde = ["J", "Gamma", "N", "Energy", "Ka", "v1", "v2", "v3", "v4", "v5", "v6", "Weight"]
    RefinementBlockTestInput = [
        [2, 1, 17, 2082.71350, 1, 0, 0, 1, 0, 0, 1, 1.00],
        [2, 2, 12, 2083.32885, 1, 0, 0, 1, 0, 0, 1, 1.00],
        [3, 1, 15, 2089.59045, 1, 0, 0, 1, 0, 0, 1, 1.00]
    ]
    TestRefinementBlockDataFrame = pd.DataFrame(RefinementBlockTestInput, columns=RefinementBlockColumnsFormaldehyde)
    TestRefinementBlockObject = EnergyLevels(TestRefinementBlockDataFrame)
    MarvelLevelsWithTroveTagsColumnsFormaldehyde = ["Gamma",	"GammaRot", "J", "Ka", "Kc", "GammaVib", "v1", "v2", "v3", "v4", "v5", "v6", "Tag", "Energy", "Uncertainty", "Source", "VibrationalTag", "RoVibrationalTag", "TroveVibrationalTag", "TroveRoVibrationalTag"]
    MarvelLevelsWithTroveTagsTestInput = [
        [2, 3, 2, 1, 1, 4, 0, 0, 1, 0, 0, 1, "2-1-1-0-0-1-0-0-1", 2083.32885, 0.0026, "05LoUlBe", "0-0-1-0-0-1", "1-0-0-1-0-0-1", "0-0-0-1-1-0", "1-0-0-0-1-1-0"],
        [1, 4, 3, 1, 2, 4, 0, 0, 1, 0, 0, 1, "3-1-2-0-0-1-0-0-1", 2089.59045, 0.0026, "05LoUlBe", "0-0-1-0-0-1", "1-0-0-1-0-0-1", "0-0-0-1-1-0", "1-0-0-0-1-1-0"],
        [1, 4, 2, 1, 2, 4, 0, 0, 1, 0, 0, 1, "2-1-2-0-0-1-0-0-1", 2082.71350, 0.0026, "05LoUlBe", "0-0-1-0-0-1", "1-0-0-1-0-0-1", "0-0-0-1-1-0", "1-0-0-0-1-1-0"]
    ]
    TestMarvelLevelsWithTroveTagsDataFrame = pd.DataFrame(MarvelLevelsWithTroveTagsTestInput, columns=MarvelLevelsWithTroveTagsColumnsFormaldehyde)
    TestMarvelLevelsWithTroveTagsObject = EnergyLevels(TestMarvelLevelsWithTroveTagsDataFrame)
    MarvelLevelsWithTroveTagsExpectedInput = [
        [2, 3, 2, 1, 1, 4, 0, 0, 0, 1, 1, 0, "2-1-1-0-0-1-0-0-1", 2083.32885, 0.0026, "05LoUlBe", "0-0-1-0-0-1", "1-0-0-1-0-0-1", "0-0-0-1-1-0", "1-0-0-0-1-1-0"],
        [1, 4, 3, 1, 2, 4, 0, 0, 0, 1, 1, 0, "3-1-2-0-0-1-0-0-1", 2089.59045, 0.0026, "05LoUlBe", "0-0-1-0-0-1", "1-0-0-1-0-0-1", "0-0-0-1-1-0", "1-0-0-0-1-1-0"],
        [1, 4, 2, 1, 2, 4, 0, 0, 0, 1, 1, 0, "2-1-2-0-0-1-0-0-1", 2082.71350, 0.0026, "05LoUlBe", "0-0-1-0-0-1", "1-0-0-1-0-0-1", "0-0-0-1-1-0", "1-0-0-0-1-1-0"]
    ]
    ExpectedMarvelLevelsWithTroveTagsDataFrame = pd.DataFrame(MarvelLevelsWithTroveTagsExpectedInput, columns=MarvelLevelsWithTroveTagsColumnsFormaldehyde)
    ExpectedMarvelLevelsWithTroveTagsObject = EnergyLevels(ExpectedMarvelLevelsWithTroveTagsDataFrame)
    yield TestEnergyLevelsObject, TestEnergyLevelsSymmetriesMappedObject, TestMarvelLevelsObject, TestSortedMarvelLevelsObject, TestMarvelMatchedLevelsObject,TestTaggedMarvelLevelsObject, MarvelWithObsMinusCalcMatchedLevelsObject, TestRefinementBlockObject, TestMarvelLevelsWithTroveTagsObject, ExpectedMarvelLevelsWithTroveTagsObject

def test_ReadTroveEnergies(SetupFormaldehydeTest):
    ExpectedEnergyLevelsObject, _, _, _, _, _, _, _, _, _ = SetupFormaldehydeTest
    OutputEnergyLevelsObject = ReadTroveEnergies("ReadTroveEnergiesH2CO.test")
    assert OutputEnergyLevelsObject == ExpectedEnergyLevelsObject

def test_ReadMarvelEnergies(SetupFormaldehydeTest):
    _, _, ExpectedMarvelLevelsObject, _, _, _, _, _, _, _ = SetupFormaldehydeTest
    OutputMarvelLevelsObject = ReadMarvelEnergies("ReadMarvelEnergies.test")
    assert OutputMarvelLevelsObject == ExpectedMarvelLevelsObject

def test_ObtainSymmetryMap(SetupFormaldehydeTest):
    TestEnergyLevelsObject, _,  _, _, _, _, _, _, _, _ = SetupFormaldehydeTest
    ExpectedSymmetryMap = {"A1": 1,
                           "A2": 2,
                           "B1": 3,
                           "B2": 4}
    ObtainSymmetryMap(TestEnergyLevelsObject)
    OutputSymmetryMap = TestEnergyLevelsObject.GetSymmetryMap()
    assert OutputSymmetryMap == ExpectedSymmetryMap

def test_ApplySymmetryMapping(SetupFormaldehydeTest):
    TestEnergyLevelsObject, ExpectedEnergyLevelsObject, _, _, _, _, _, _, _, _ = SetupFormaldehydeTest
    TestSymmetryMap = {"A1": 1,
                       "A2": 2,
                       "B1": 3,
                       "B2": 4}
    TestEnergyLevelsObject.SetSymmetryMap(TestSymmetryMap)
    ExpectedEnergyLevelsObject.SetSymmetryMap(TestSymmetryMap)
    OutputEnergyLevelsObject = ApplySymmetryMapping(TestEnergyLevelsObject)
    assert OutputEnergyLevelsObject == ExpectedEnergyLevelsObject

def test_SortEnergyLevelsByJSymmetryAndEnergy(SetupFormaldehydeTest):
    _, _, TestMarvelLevelsObject, ExpectedSortedMarvelLevelsObject, _, _, _, _, _, _ = SetupFormaldehydeTest
    OutputSortedMarvelLevelsObject = SortEnergyLevelsByJSymmetryAndEnergy(TestMarvelLevelsObject)
    assert OutputSortedMarvelLevelsObject == ExpectedSortedMarvelLevelsObject

def test_ApplyFindMatchingLevels(SetupFormaldehydeTest):
    _, TestTroveLevelsObject, _, TestMarvelLevelsObject, ExpectedMatchingMarvelLevelsObject, _, _, _, _, _ = SetupFormaldehydeTest
    OutputMatchingMarvelLevelsObject = ApplyFindMatchingLevels(TestMarvelLevelsObject, TestTroveLevelsObject)
    assert OutputMatchingMarvelLevelsObject == ExpectedMatchingMarvelLevelsObject

def test_GenerateRoVibrationalTags(SetupFormaldehydeTest):
    _, _, TestMarvelLevelsInputObject, _, _, ExpectedTaggedMarvelLevelsObject, _, _, _, _ = SetupFormaldehydeTest
    OutputTaggedMarvelLevelsObject = GenerateRoVibrationalTags(TestMarvelLevelsInputObject)
    assert OutputTaggedMarvelLevelsObject == ExpectedTaggedMarvelLevelsObject

def test_ObtainObsMinusCalc(SetupFormaldehydeTest):
    _, _, _, _, _, _, ExpectedMarvelWithObsMinusCalcEnergyLevelsObject, _, _, _ = SetupFormaldehydeTest
    ExpectedObsMinusCalc = {"Total rms": 0.02209130123672688, "0-0-1-0-0-1": 0.02209130123672688}
    ExpectedMarvelWithObsMinusCalcEnergyLevelsObject.SetObsMinusCalc(ExpectedObsMinusCalc)
    InputTaggedMarvelEnergyLevelsObject = EnergyLevels(ExpectedMarvelWithObsMinusCalcEnergyLevelsObject.GetEnergyLevelsDataFrame().drop("Obs-Calc", axis=1))
    OutputMarvelWithObsMinusCalcEnergyLevelsObject = ObtainObsMinusCalc(InputTaggedMarvelEnergyLevelsObject)
    assert OutputMarvelWithObsMinusCalcEnergyLevelsObject.GetEnergyLevelsDataFrame().to_string() == ExpectedMarvelWithObsMinusCalcEnergyLevelsObject.GetEnergyLevelsDataFrame().to_string() and OutputMarvelWithObsMinusCalcEnergyLevelsObject.GetObsMinusCalc() == ExpectedMarvelWithObsMinusCalcEnergyLevelsObject.GetObsMinusCalc()

def test_ConvertToTroveRefinementInput(SetupFormaldehydeTest):
    _, _, _, _, _, _, InputMarvelWithObsMinusCalcEnergyLevelsObject, ExpectedRefinementBlockObject, _, _ = SetupFormaldehydeTest
    OutputRefinementBlockObject = ConvertToTroveRefinementInput(InputMarvelWithObsMinusCalcEnergyLevelsObject)
    assert OutputRefinementBlockObject == ExpectedRefinementBlockObject

def test_ApplyReplaceWithTroveQuantumNumbers(SetupFormaldehydeTest):
    _, _, _, _, _, _, _, _, InputMarvelEnergyLevelsObject, ExpectedMarvelEnergyLevelsObject = SetupFormaldehydeTest
    OutputMarvelEnergyLevelsObject = ApplyReplaceWithTroveQuantumNumbers(InputMarvelEnergyLevelsObject)
    assert OutputMarvelEnergyLevelsObject == ExpectedMarvelEnergyLevelsObject