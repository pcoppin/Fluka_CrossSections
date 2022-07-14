from __future__ import print_function, division, absolute_import
import numpy as np
import os

setup_txt = """*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
TITLE
Charged protons on aluminium
*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
BEAM         {:.1e}                                                  PROTON
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
ASSIGNMAT  ALUMINUM   regBE3    regBE4
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

# E_range = np.logspace(-3,6,4)
# for E in E_range[:2]:
#     txt = setup_txt.format(E)
#     with open("setup.inp", "w") as f:
#         f.write(txt)
#     os.system("rfluka -N0 -M1 setup.inp")

Fluka_out = "setup001.out"
with open(Fluka_out, 'r') as f:
    for line in f:
        if( "MYALUMIN" in line and "*" not in line ):
            values = line.split()
            AtomicNumber,AtomicWeight,Density,InelasticScatteringLength = [float(x) for x in values[2:6]]
            
            print( AtomicNumber,AtomicWeight,Density,InelasticScatteringLength )
            
            NumberDensity = Na*Density/AtomicWeight
            # CrossSection in barn
            CrossSection = cm2tobarn / (NumberDensity*InelasticScatteringLength)
            
# Now save in array and run loops