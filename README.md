# Revised-PROPKA
This is a revised version of [PROPKA3.1](https://github.com/jensengroup/propka-3.1.git).  
If you are looking for the original version, please go to 
https://github.com/jensengroup/propka-3.1.git


## Changes
* Allow user to load trajectories instead of pdb files
* The output is in JSON format
* No change to the pKa calculation modules

## Install
```python
git clone https://github.com/yuhangwang/revised_propka
cd revised_propka
python setup.py develop
```

You also need to install `ProDy` which is used for parsing PDB/DCD files.
```
pip install -U ProDy
```

## Usage
To see the usage, type `propka -h`.  

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
from all frames.

I also added one more option `-s` or `--skip` to allow users to down-sample 
the trajectory frames.

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
```
import json

with open("output_pka.json", "r") as IN:
    data = json.loads(IN.read())

for k, pkas in data.items():
    print(k, pkas)
```
