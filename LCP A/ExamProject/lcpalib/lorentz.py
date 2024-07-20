import numpy as np
from lcpalib import const

pc = const.PhysConst().get()
electron_mass = pc['pmass']['e']

# boosts energy and momentum from the LAB to the COM system
def boost2CoM(p_lab, E_lab):
    beta = p_lab / (E_lab + electron_mass)
    gamma = 1/np.sqrt(1-beta**2)
    pCom = gamma*(p_lab - beta*E_lab)
    eCom = gamma*(E_lab - beta*p_lab)
    return {'pz*':pCom, 'E*': eCom, 'beta':beta, 'gamma':gamma}

# boosts energy and momentum from the CoM to the LAB system
def boost2LAB(p_cm, E_cm):
    this_sqrt_s = 2*E_cm
    beta = -np.sqrt( 1. - ((2*electron_mass)**2)/(this_sqrt_s)**2 )
    gamma = 1./np.sqrt(1-beta**2)
    pLab = gamma*(p_cm - beta*E_cm)
    eLab = gamma*(E_cm - beta*p_cm)
    return {'pz':pLab, 'E': eLab, 'beta':beta, 'gamma':gamma}

# boosts energy and momentum from the LAB to the COM system
def boost2CoM_ext(p_lab_positron, E_lab_positron, p_lab_particle, E_lab_particle):
    beta = p_lab_positron / (E_lab_positron + electron_mass)
    gamma = 1/np.sqrt(1-beta**2)
    pCom = gamma*(p_lab_particle - beta*E_lab_particle)
    eCom = gamma*(E_lab_particle - beta*p_lab_particle)
    return {'pz*':pCom, 'E*': eCom, 'beta':beta, 'gamma':gamma}


# defining a boost for any other particle besides positron or electron
class LorentzBoost(object):
    def __init__(self, particle_mass, E_positron_cm=None, E_positron_lab=None):
        self.pmass = particle_mass
        # initializing
        self.positron_E_cm = None
        self.positron_E_lab = None
        self.positron_P_cm = None
        self.positron_P_lab = None
        # obtaining the linking quantities
        if (E_positron_cm is not None):
            self.positron_E_cm = E_positron_cm
            self.positron_P_cm = np.sqrt(E_positron_cm**2 - electron_mass**2)
            # calculating the lab energies from here
            b2L = boost2LAB(self.positron_P_cm, self.positron_E_cm)
            self.positron_E_lab = b2L['E']
            self.positron_P_lab = b2L['pz']
        else:
            self.positron_E_lab = E_positron_lab
            self.positron_P_lab = np.sqrt(E_positron_lab**2 - electron_mass**2)
            # calculating the lab energies from here
            b2C = boost2CoM(self.positron_P_lab, self.positron_E_lab)
            self.positron_E_cm = b2C['E*']
            self.positron_P_cm = b2C['pz*']
        # calculating gammas and betas
        self.beta_L2C = self.positron_P_lab / (self.positron_E_lab + electron_mass)
        self.gamma_L2C = np.sqrt(1/(1-self.beta_L2C**2))
        self.beta_C2L = -np.sqrt(1.0 - ((electron_mass)**2)/(self.positron_E_cm)**2)
        self.gamma_C2L = np.sqrt(1/(1-self.beta_C2L**2))
    
    def boost2COM(self, p_lab, E_lab):
        # transforming into COM
        Pcom = self.gamma_L2C*(p_lab - self.beta_L2C*E_lab)
        Ecom = self.gamma_L2C*(E_lab - self.beta_L2C*p_lab)
        return [Pcom, Ecom]
    
    def boost2LAB(self, p_com, E_com):
        # transforming into LAB
        Plab = self.gamma_C2L*(p_com - self.beta_C2L*E_com)
        Elab = self.gamma_C2L*(E_com - self.beta_C2L*p_com)
        return [Plab, Elab]
