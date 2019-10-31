import pandas as pd
import numpy as np

# http://www.oecd-nea.org/dbdata/data/mass-evals2003/mass.mas03
df = pd.read_fwf(
    'mass.mas03',
    usecols=(2, 3, 11),
    names=tuple('NZE'),
    widths=(1,3,5,5,5,1,3,4,1,13,11,11,9,1,2,11,9,1,3,1,12,11,1),
    header=39, index_col=False
)

# drop predicted values and convert to MeV
df['E_known'] = 1 - pd.isnull(df.E)
df.E = pd.to_numeric(df.E, errors='coerce')

def gathers(name, orelse):
    data = {(data.N, data.Z): data[name] for i, data in df.iterrows()}
    return np.vectorize(lambda n, z: data.get((n,z), orelse))

aV, aS, aC, aA, delta0 = 15750, 17800, 711, 23700, 11180  # MeV

@np.vectorize
def binding_per_nucleon(N, Z):
    A = Z + N
    sgn = 0 if A % 2 else (-1 if Z % 2 else +1)
    return ( aV - aS / A**(1/3)
                - aC * Z*(Z-1) / A**(4/3)
                - aA * (A-2*Z)**2/A**2
                + delta0 * sgn/A**(3/2)
    )