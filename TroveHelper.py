from TroveHelperFunctions import *
from EnergyLevels import EnergyLevels
import sys


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: Should give a Marvel energies file along with a Trove .energies file")
    else:
        MarvelEnergiesFile = sys.argv[1]
        TroveEnergiesFile = sys.argv[2]
        OutputFileName = TroveEnergiesFile.split(".")[0] + ".results"
        RefinementFileName = TroveEnergiesFile.split(".")[0] + ".refine"
        MarvelEnergyLevelsObject = ReadMarvelEnergies(MarvelEnergiesFile)
        TroveEnergyLevelsObject = ReadTroveEnergies(TroveEnergiesFile)
        TroveEnergyLevelsObject = ObtainSymmetryMap(TroveEnergyLevelsObject)
        TroveEnergyLevelsObject = ApplySymmetryMapping(TroveEnergyLevelsObject)
        TroveEnergyLevelsObject = GenerateRoVibrationalTags(TroveEnergyLevelsObject)
        MarvelEnergyLevelsObject = SortEnergyLevelsByJSymmetryAndEnergy(MarvelEnergyLevelsObject)
        MarvelEnergyLevelsObject = GenerateRoVibrationalTags(MarvelEnergyLevelsObject)
        MarvelEnergyLevelsObject = ApplyFindMatchingLevels(MarvelEnergyLevelsObject, TroveEnergyLevelsObject)
        MarvelEnergyLevelsObject = ObtainObsMinusCalc(MarvelEnergyLevelsObject)
        WriteToFile(MarvelEnergyLevelsObject, OutputFileName)
        MarvelEnergyLevelsObject = ApplyReplaceWithTroveQuantumNumbers(MarvelEnergyLevelsObject)
        RefinementEnergyLevelsObject = ConvertToTroveRefinementInput(MarvelEnergyLevelsObject)
        RefinementEnergyLevelsObject.SetObsMinusCalc(None)
        WriteToFile(RefinementEnergyLevelsObject, RefinementFileName)