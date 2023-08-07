from TroveHelperFunctions import *
from EnergyLevels import EnergyLevels
import copy
import sys


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: Should give a Marvel energies file along with a Trove .energies file")
    else:
        MarvelEnergiesFile = sys.argv[1]
        TroveEnergiesFile = sys.argv[2]
        OutputFileName = TroveEnergiesFile.split(".")[0] + ".results"
        RefinementFileName = TroveEnergiesFile.split(".")[0] + ".refine"
        GainMarvelFileName = TroveEnergiesFile.split(".")[0] + ".gain"
        TroveEnergyLevelsFileName = TroveEnergiesFile.split(".")[0] + ".levels"
        MarvelEnergyLevelsObject = ReadMarvelEnergies(MarvelEnergiesFile)
        TroveEnergyLevelsObject = ReadTroveEnergies(TroveEnergiesFile)
        TroveEnergyLevelsObject = ObtainSymmetryMap(TroveEnergyLevelsObject)
        TroveEnergyLevelsObject = ApplySymmetryMapping(TroveEnergyLevelsObject)
        TroveEnergyLevelsObject = GenerateRoVibrationalTags(TroveEnergyLevelsObject)
        MarvelEnergyLevelsObject = SortEnergyLevelsByJSymmetryAndEnergy(MarvelEnergyLevelsObject)
        MarvelEnergyLevelsObject = GenerateRoVibrationalTags(MarvelEnergyLevelsObject)
        (MarvelEnergyLevelsObject, VibrationalTagMap) = ApplyFindMatchingLevels(MarvelEnergyLevelsObject, TroveEnergyLevelsObject)
        MarvelEnergyLevelsObject = ObtainObsMinusCalc(MarvelEnergyLevelsObject)
        MarvelEnergyLevelsObject = RaiseWeights(MarvelEnergyLevelsObject)
        WriteToFile(MarvelEnergyLevelsObject, OutputFileName)
        MarvelEnergyLevelsObject = ApplyReplaceWithQuantumNumbersFromTag(MarvelEnergyLevelsObject)
        RefinementEnergyLevelsObject = ConvertToTroveRefinementInput(copy.deepcopy(MarvelEnergyLevelsObject))
        RefinementEnergyLevelsObject.SetObsMinusCalc(None)
        WriteToFile(RefinementEnergyLevelsObject, RefinementFileName)
        GainMarvelEnergyLevelsObject = ConvertToMarvelStatesFormat(copy.deepcopy(MarvelEnergyLevelsObject))
        GainMarvelEnergyLevelsObject.SetObsMinusCalc(None)
        WriteToFile(GainMarvelEnergyLevelsObject, GainMarvelFileName)
        TroveEnergyLevelsObject = FindTroveAssignments(TroveEnergyLevelsObject, VibrationalTagMap)
        TroveEnergyLevelsObject = ApplyReplaceWithQuantumNumbersFromTag(TroveEnergyLevelsObject)
        WriteToFile(TroveEnergyLevelsObject, TroveEnergyLevelsFileName)