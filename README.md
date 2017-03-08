# Revised-PROPKA
This is a revised version of [PROPKA3.1](https://github.com/jensengroup/propka-3.1.git).  
If you are looking for the original version, please go to 
https://github.com/jensengroup/propka-3.1.git


## Changes
* Allow user to load trajectories instead of pdb files
* The output is in JSON format
* Allow large pdb files as inputs by switching to counter based atom index
* No change to the pKa calculation modules

## Install
It is preferred to have [MiniConda](https://conda.io/miniconda.html) installed.

```
git clone https://github.com/yuhangwang/revised_propka
cd revised_propka
python setup.py develop
```

You also need to install [ProDy](http://prody.csb.pitt.edu/downloads/)
which is used for parsing PDB/DCD files.
```
pip install -U ProDy
```

`ProDy` depends on `numpy`. To install `numpy`, type the following if you
have `conda` installed.
```
conda install numpy
```

## Update
To get the latest update, just do `git pull` inside the `revised_propka` folder.  
Since the package was installed in development mode, the command line tool `propka`
will be updated instantly, much like the the way how symbolic links work.

## Usage
To see the usage, type `propka -h`.  

A typical usage:
```
propka output_pka.json my.pdb md1.dcd md2.dcd md3.dcd
```
The output will be output_pka.json

If you only need the pKa for a particular residue and  
save computation time, use the following command:
```
propka -q -i A:100,B:100 output.json my.pdb md1.dcd
```
This will compute the pKa values for residue 100 from chain A and B
from all frames. The `-q` option will suppress printing message on the screen.

I also added one more option `-s` or `--skip` to allow users to down-sample 
the trajectory frames.
```
propka -q -s 100 my.pdb md1.dcd
```
This will calculate pKa's very 100 frames.


## Example output
```
{
    "ARG_100_A": [
        12.246243386088594,
        12.246243386088594
    ],
    "ARG_100_D": [
        11.908591649550003,
        11.908591649550003
    ]
}
```

## Reading JSON files
To read the output file, you can use python's built-in module `json`:
```python
import json
import numpy

with open("output_pka.json", "r") as IN:
    data = json.loads(IN.read())

for k, pkas in data.items():
    print(k, pkas)
    print("Average pKa =", numpy.average(pkas))
```
