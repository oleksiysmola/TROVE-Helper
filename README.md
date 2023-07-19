## Trove Helper
This is intended to be a tool to aid one in the management of TROVE (Theoretical Ro-Vibrational Energy Levels) (Yurchenko et al. 2007) output and matching such results to empirical energy levels from MARVEL (Measured Active Ro-Vibrational Energy Levels) (Furtenbacher et al. 2007). 

## Requirements
Trove Helper utilises the Pandas, Numpy, re and Pandarallel libraries in Python 3.8.13. The Pytest library is used for testing. Before running the code you'll want to ensure these libraries are installed via pip as follows:
`pip install pandas`
`pip install Numpy`
`pip install re`
`pip install pandarallel`
`pip install pytest`

## Tests
To run the tests, use the following shell command:
`python3 -m pytest -v`

## Compilation
Trove Helper can be compiled into an executable. First, in shell run `pip install pyinstaller` and then run the command `pyinstaller --onefile TroveHelper.py`. The executable `TroveHelper` file can then be found in the `dist` directory.

## References
 SN Yurchenko, W Thiel, P Jensen; (2007) Theoretical ROVibrational Energies (TROVE): A robust numerical approach to the calculation of rovibrational energies for polyatomic molecules - Journal of Molecular Spectroscopy, https://doi.org/10.1016/j.jms.2007.07.009

 Furtenbacher, T; Csaszar, AG; Tennyson, J; (2007) MARVEL: measured active rotational-vibrational energy levels. J MOL SPECTROSC , 245 (2) 115 - 125  https://doi.org/10.1016/j.jms.2007.07.005