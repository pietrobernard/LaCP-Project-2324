from scipy.optimize import brentq
import numpy as np


#####################################################################################################################
# INVERSE SAMPLER OBJECT
class InverseSampler(object):
    def __init__(self, N, cdf, transform_callback):
        self.N_samples = N
        self.cdf = cdf
        self.samples = None
        self.transform_callback = transform_callback
    
    def cdfFunc(self, y, s, u):
        return self.cdf(y,s) - u

    def run(self, sqrt_s):
        unif_samples = np.random.uniform(0,1,self.N_samples)
        self.samples = [brentq(self.cdfFunc,-1,1,args=(s,u)) for u,s in zip(unif_samples,[sqrt_s**2]*self.N_samples)]
    
    def runDifferentE(self, sqrt_s_array):
        unif_samples = np.random.uniform(0,1,self.N_samples)
        self.samples = [brentq(self.cdfFunc,-1,1,args=(s,u)) for u,s in zip(unif_samples,sqrt_s_array**2)]
                    
    def getSamples(self):
        return self.samples
    
    def getTransformedSamples(self):
        return self.transform_callback(self.samples)

