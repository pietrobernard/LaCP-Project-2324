#############################################################################################
# General Parameters
#
class PhysConst(object):
    def __init__(self):
        self.phys = {}
        #
        # Physical constants
        self.phys['const'] = {
            'alpha':0.007297,   # fine structure constant
            'Na':6.0221408e23,  # Avogadro's number
            'c0':0.389379e6     # conversion constant to obtain cross section in nanobarns
        }
        #
        # Particle masses
        self.phys['pmass'] = {
            'mu':0.105658374524,    # muon mass, GeV
            'e':0.0005109989461     # electron mass, GeV
            }
        #
        # Berillium's physical properties (sourced from Particle Data Group)
        self.phys['Be'] = {
            'A':9.0121831,  # molar mass, g/mol
            'Z':4,          # atomic number
            'rho':1.848,    # density, g/cm^3
            'X0':35.28      # radiation length cm
        }
        #
        # Berillium target properties
        self.phys['target'] = {
            'Zmax': 3.0,    # target depth, cm
            'Ne': self.phys['Be']['Z']*self.phys['Be']['rho']*self.phys['const']['Na'] / self.phys['Be']['A'] # volume density of electrons, cm^{-3}
        }
        #
        # Beam properties
        self.phys['beam'] = {
            'R': 1.0, # radius of the beam, cm
            's': 0.5  # energy width of the beam, GeV
        }
    
    def get(self):
        return self.phys
#
#############################################################################################
# 