# First source /cvmfs/dampe.cern.ch/centos7/etc/setup.sh,
#    then /cvmfs/dampe.cern.ch/centos7/etc/setup_conda_python2.7_tensorflow2.1.sh
#    to get both correct version of python and gfortran

# Probably, this is far for the ideal way to do this, but is works \_()_/

from __future__ import print_function, division, absolute_import
import numpy as np
import os

Primary = ["PROTON", "4-HELIUM"][1]
Material = ["ALUMINUM","CARBON"][1]

setup_txt = """*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
TITLE
Charged protons on aluminium
*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
BEAM         {:.1e}                                                  {}
BEAMPOS          0.0       0.0     -50.0
*
GEOBEGIN                                                              COMBNAME
  0 0                       A simple Be target inside vacuum
RPP body1 -5000000.0 +5000000.0 -5000000.0 +5000000.0 -5000000.0 +5000000.0
RPP body2 -1000000.0 +1000000.0 -1000000.0 +1000000.0    -100.0  +1000000.0
RPP body3     -10.0      +10.0      -10.0      +10.0        0.0       +5.0
* plane to separate the upstream and downstream part of the target
XYP body4       2.5
END
* black hole
regBH1    5     +body1 -body2
* vacuum around
regVA2    5     +body2 -body3
* Be target 1st half
regBE3    5     +body3 +body4  
* Be target 2nd half
regBE4    5     +body3 -body4  
END
GEOEND
*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
*MATERIAL         4.0               1.848       5.0                    TEST
*MATERIAL     protons             Density  Neutrons                    NAME   
*MATERIAL        13.0                 2.7      14.0                    ALUMINUM
MATERIAL        13.0                 2.7      14.0                    MYALUMIN
*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
*  Be target, 1st and 2nd half
*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
ASSIGNMAT  {:>8}   regBE3    regBE4
*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
*  External Black Hole
ASSIGNMAT  BLCKHOLE   regBH1
*  Vacuum
ASSIGNMAT   VACUUM    regVA2
*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
RANDOMIZE        1.0
*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
START       1.0
STOP"""

Na = 6.02214076e23
cm2tobarn = 1e24

E_range = np.logspace(-3,6,91)
CrossSections = []
for E in E_range:
    CrossSection = None
    Found_pos = False
    txt = setup_txt.format(E,Primary,Material)
    with open("setup.inp", "w") as f:
        f.write(txt)
    os.system("rfluka -N0 -M1 -d setup.inp")
    Fluka_out = "setup001.out"
    with open(Fluka_out, 'r') as f:
        for line in f:
            if( not Found_pos ):
                if( "Material compositions" not in line ):
                    continue
                else:
                    Found_pos = True
            elif( Material in line and "*" not in line ):
                values = line.split()
                AtomicNumber,AtomicWeight,Density,InelasticScatteringLength = [float(x) for x in values[2:6]]
                NumberDensity = Na*Density/AtomicWeight
                CrossSection = cm2tobarn / (NumberDensity*InelasticScatteringLength)
                break
    
    if( CrossSection is not None ):
        CrossSections.append( CrossSection )
    else:
        raise Exception( "No cross section found in output file!" )


with open("CrossSections/Fluka_{}_on_{}.txt".format(Primary,Material), "w") as f:
    f.write("# Energy (GeV)      Cross section (barn)\n")
    for E, s in zip(E_range,CrossSections):
        f.write("  {:<17.3e} {:.3e}\n".format(E,s))