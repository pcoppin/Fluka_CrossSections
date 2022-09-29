# First source /cvmfs/dampe.cern.ch/centos7/etc/setup.sh,
#    then /cvmfs/sft.cern.ch/lcg/contrib/gcc/9.2.0/x86_64-centos7/setup.sh
#    to get both correct version of python and gfortran

# Probably, this is far for the ideal way to do this, but is works \_()_/

from __future__ import print_function, division, absolute_import
import numpy as np
import os

Primary = ["PROTON", "4-HELIUM"][1]
Material = ["ALUMINUM","CARBON","MYCARBON","GRAPHITE"][1]

setup_txt = """*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
TITLE
Charged protons on aluminium
*...+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8
BEAM      {:10.3e}                                                  {}
BEAMPOS          0.0       0.0     -50.0
*
GEOBEGIN                                                              COMBNAME
  0 0                       A simple Be target inside vacuum
RPP body1 -5000000.0 +5000000.0 -5000000.0 +5000000.0 -5000000.0 +5000000.0
RPP body2 -1000000.0 +1000000.0 -1000000.0 +1000000.0    -100.0  +1000000.0
RPP body3     -20.0      +20.0      -20.0      +20.0        0.0       +5.0
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
*MATERIAL        13.0                 2.7      14.0                    MYALUMIN
*MATERIAL         6.0                 2.0       6.0                    MYCARBON
*MATERIAL         6.0                 2.0       6.0                    CARBON
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

# MATERIAl         6.0                 2.0       6.0                    MYCARBON

Na = 6.02214076e23
cm2tobarn = 1e24

#E_range = np.logspace(-0.4,5,100)
E_range = np.logspace(-0.4,1,10)
#E_range = np.logspace(-0.4,5,20)
#E_range = [1]
CrossSections = []

# For heavy ions, use the name HEAVYION and specify further the ion
#                properties by means of option HI-PROPErt. In this case WHAT(1)
#                will mean the energy (or momentum) PER UNIT ATOMIC MASS, and not
#                the total energy or momentum.
#                The light nuclei 4He, 3He, triton and deuteron are defined with
#                their own names (4-HELIUM, 3-HELIUM, TRITON and DEUTERON) and
#                WHAT(1) will be the total energy or momentum.
#                For (radioactive) isotopes, use the name ISOTOPE and specify
#                further the isotope properties by means of option HI-PROPErt.
#                In this case WHAT(1) and WHAT(2) are meaningless. If no
#                radioactive isotope evolution or decay is requested, or if a
#                stable isotope is input, nothing will occur, and no particle will
#                be transported.

for E in E_range:
    
    E_kin = E        # Take energy to make kinetic energy, as this is what Geant does
    
    txt = setup_txt.format(-1*E_kin,Primary,Material)
    
    ### But Fluka wants the momentum, so need to do a little conversion
    ###    Manually varied that the E_kin output files again matches the value we started from
    #m = 4.002603*0.931494102 # Mass in Dalton times GeV/Dalton
    #E_total = E_kin + m
    #Momentum = np.sqrt(E_total**2 - m**2)
    #txt = setup_txt.format(Momentum,Primary,Material)
    #   Note to self: need to add extra space in setup_text to account for minus sign not there
    
    CrossSection = None
    Found_pos = False
    with open("setup.inp", "w") as f:
        f.write(txt)
    
    ### Run CERN FLUKA, need -d option to activate DPMjetIII
    #os.system("/dpnc/beegfs/users/coppinp/FLUKA/fluka4-2.2/bin/rfluka -N0 -M1 -d setup.inp") 
    
    ### Run non-CERN FLUKA
    #os.system("/dpnc/beegfs/users/coppinp/FLUKA_INFN/install_glibc/flutil/rfluka -N0 -M1 setup.inp")
    
    ### Run non-CERN FLUKA with DPMjet
    #os.system("/dpnc/beegfs/users/coppinp/FLUKA_INFN/install_glibc/flutil/rfluka -e /dpnc/beegfs/users/coppinp/FLUKA_INFN/install_glibc/flutil/flukadpm3 -N0 -M1 setup.inp")
    
    ### Run non-CERN FLUKA with DAMPE executable, requires loading Dampe_init_vary_XS
    #os.system("/dpnc/beegfs/users/coppinp/FLUKA_INFN/install_glibc/flutil/rfluka -e /home/users/c/coppinp/DmpSoftware/Trunk-with-vary-XS/Install/share/FlukaSimulation/bin/flukaDAMPE_iso -N0 -M1 setup.inp")
    
    
    
    
    ### Run DAMPE FLUKA with DPMjet
    #os.system("/dpnc/beegfs/users/coppinp/FLUKA_DAMPE/FLUKA_2011.2x7/flutil/rfluka -e /dpnc/beegfs/users/coppinp/FLUKA_DAMPE/FLUKA_2011.2x7/flukadpm3 -N0 -M1 setup.inp")  
    ### Run DAMPE FLUKA with DAMPE custom executable thingy
    os.system("/dpnc/beegfs/users/coppinp/FLUKA_DAMPE/FLUKA_2011.2x7/flutil/rfluka -e /home/users/c/coppinp/DmpSoftware/Trunk-with-vary-XS/Install/share/FlukaSimulation/bin/flukaDAMPE_iso -N0 -M1 setup.inp")  
    
    
    
    # run 'make' in install_glibc or '$FLUPRO/flutil/ldpmqmd' in flutil if it complains about libflukahp.a is newer than ...
    
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
                print("\n", E_kin, CrossSection)
                break
    
    if( CrossSection is not None ):
        CrossSections.append( CrossSection )
    else:
        raise Exception( "No cross section found in output file!" )


with open("CrossSections/Fluka_DAMPE_{}_on_{}.txt".format(Primary,Material), "w") as f:
    f.write("# Energy (GeV)      Cross section (barn)\n")
    for E, s in zip(E_range,CrossSections):
        f.write("  {:<17.3e} {:.3e}\n".format(E,s))