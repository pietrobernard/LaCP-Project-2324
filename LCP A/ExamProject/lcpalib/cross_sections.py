import numpy as np
from lcpalib import const

#####################################################################################################################
# CROSS SECTIONS
class CS(object):
    def __init__(self):
        pc = const.PhysConst().get()
        self.alpha = pc['const']['alpha']
        self.m_mu = pc['pmass']['mu']
        self.c0 = pc['const']['c0']
    
    # total e+e-->mu+mu- cross section at a given invariant mass s
    def sigma_nb(self, s):
        first_term = (4*np.pi*self.alpha**2)/(3*s)
        second_term = (1+(2*self.m_mu**2)/s)
        third_term = np.sqrt(1-(4*self.m_mu**2)/s)
        return first_term*second_term*third_term*self.c0

    # differential cross section e+e->mu+mu- at given invariant mass s and solid angle dOmega
    def dsigma_domega_nb(self, theta, s):
        first = self.alpha**2 / (4*s)
        secon = np.sqrt(1.0 - (4*self.m_mu**2)/s)
        third = ((1+(4*self.m_mu**2)/s) + (1-(4*self.m_mu**2)/s)*np.cos(theta)**2)
        return first*secon*third*self.c0

    # differential cross section e+e-->mu+mu- at given invariant mass s and angle theta, integrated over dPhi
    def dsigma_dtheta_nb(self, s, theta):
        return 2.0*np.pi*np.sin(theta)*self.dsigma_domega_nb(theta, s)

    # theta angle PDF
    def pdf_theta(self, s, theta):
        return self.dsigma_dtheta_nb(s, theta)/self.sigma_nb(s)
    
    # theta CDF
    def cdf_theta(self, cos_theta, s):
        l0 = 3/8*1/(1+((2*self.m_mu**2)/s))
        l1 = 1/3*(1-((4*self.m_mu**2)/s))
        l2 = 1+((4*self.m_mu**2)/s)
        l3 = 4/3*(1+((2*self.m_mu**2)/s))
        return -1.0*l0*(l1*cos_theta**3 + l2*cos_theta - l3)
