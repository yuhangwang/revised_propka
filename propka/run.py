# entry point for propka script

import propka.lib, propka.molecular_container
import os
from prody import Trajectory, parsePDB, writePDBStream
import json

class PdbLines:
    def __init__(self):
        self.lines = []
    def write(self, string):
        self.lines.append(string.rstrip())
    def get_lines(self):
        return self.lines


def expand_dict(old_d, new_d):
    for k in new_d.keys():
        if k not in old_d:
            old_d[k] = [new_d[k]]
        else:
            old_d[k].append(new_d[k])

def get_pka(atoms, pdb_file, options):
        p = PdbLines()
        writePDBStream(p, atoms)
        pdb_lines = p.get_lines()
        my_molecule = propka.molecular_container.Molecular_container(pdb_file, pdb_lines, options)
        my_molecule.calculate_pka()
        return my_molecule.get_pka_results()

# def main():
#     """
#     Reads in structure files, calculates pKa values, and prints pKa files
#     """
#     # loading options, flaggs and arguments
#     options, pdbfiles = propka.lib.loadOptions()

#     print("pdbfiles", pdbfiles)

#     for pdbfile in pdbfiles:
#         my_molecule = propka.molecular_container.Molecular_container(pdbfile, options)
#         my_molecule.calculate_pka()
#         my_molecule.write_pka()
def main():
    """
    Reads in structure files, calculates pKa values, and prints pKa files
    """
    # loading options, flaggs and arguments
    options, files = propka.lib.loadOptions()

    output = {}
    file_output = files[0]
    pdb_file = files[1]

    atoms = parsePDB(pdb_file)
    
    if len(files) > 2:
        dcd_files = files[2:]
        traj = Trajectory(dcd_files[0])
        for f in dcd_files[1:]:
            if not os.path.isfile(f):
                print("ERROR HINT: file {} doesn't exist".format(f))
                exit()
            traj.addFile(f)
        traj.link(atoms)

        print("trajectory length:", len(traj))

        for i in range(0, len(traj), options.skip+1):
            traj.next()
            expand_dict(output, get_pka(atoms, pdb_file, options))
            if options.skip > 0:
                traj.skip(options.skip)
    else:
        expand_dict(output, get_pka(atoms, pdb_file, options))

    with open(file_output, "w") as OUT:
        OUT.write(json.dumps(output, indent=4))

def single(pdbfile, optargs=None):
    """Run a single PROPKA calculation using *pdbfile* as input.

    Command line options can be passed as a **list** in *optargs*.

    .. rubric:: Example

    ::
       single("protein.pdb", optargs=["--mutation=N25R/N181D", "-v", "--pH=7.2"])
    """
    optargs = optargs if optargs is not None else []
    options, ignored_pdbfiles = propka.lib.loadOptions(*optargs)

    my_molecule = propka.molecular_container.Molecular_container(pdbfile, options)
    my_molecule.calculate_pka()
    my_molecule.write_pka()
    return my_molecule
