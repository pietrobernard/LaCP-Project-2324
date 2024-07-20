import numpy as np
from lcpalib import const

pc = const.PhysConst().get()
beam_r = pc['beam']['R']

# BEAM
class BeamGeometry(object):
    def __init__(self):
        # particle positions in transverse plane
        self.X = np.array([])
        self.Y = np.array([])
        # particle energies
        self.E = None
    
    def assign(self, N, E):
        # getting the particle positions across the circle
        radial_pos = np.random.uniform(0, beam_r, N)
        radial_theta = np.random.uniform(0, 2*np.pi, N)
        # calculating X and Y
        self.X = np.cos(radial_theta)*radial_pos
        self.Y = np.sin(radial_theta)*radial_pos
        # assigning energies
        self.E = E
    
    def generate_positions(self, N, E):
        found = 0
        while found<N:
            px = np.random.uniform(-beam_r, beam_r, N)
            py = np.random.uniform(-beam_r, beam_r, N)
            filt = px**2 + py**2 <= beam_r
            px = px[filt]
            py = py[filt]
            # getting space left
            diff = N - found
            plen = len(px)
            # truncating
            px = px[:min(plen,diff)]
            py = py[:min(plen,diff)]
            # adding
            self.X = np.append(self.X, px)
            self.Y = np.append(self.Y, py)
            # updating counter
            found = len(self.X)
        # assigning energy
        print(found)
        self.E = E
    
    def get(self):
        return np.array([self.X, self.Y, self.E]).T


"""
class Beam(object):
    def __init__(self):
        self.X = []
        self.Y = []
        self.Z = []
    
    def __circ_mask(self, X, Y):
        return X**2 + Y**2 - beam_r**2
    
    def PrepareXY(self, N):
        X_beam = np.random.uniform(-beam_r,beam_r,N)
        Y_beam = np.random.uniform(-beam_r,beam_r,N)
        mask = np.argwhere(self.__circ_mask(X_beam, Y_beam)<=0)
        self.X = X_beam[mask]
        self.Y = Y_beam[mask]
        return self.X.shape[0]
    
    def setEnergies(self, Z):
        self.Z = Z
    
    def get(self):
        h = {'X':self.X, 'Y':self.Y, 'Z':self.Z}
        return h
"""