import math

ELECTRON_MASS = 9.10938356E-31
AVOGADRO_NUMBER = 6.02214076E+23

# see https://github.com/niess/pumas/blob/d04dce6388bc0928e7bd6912d5b364df4afa1089/src/pumas.c#L9155
def bremsstrahlung(Z, A, mu, K, q):
    me = ELECTRON_MASS
    sqrte = 1.648721271
    phie_factor = mu / (me * me * sqrte)
    rem = 5.63588E-13 * me / mu

    BZ_n = (202.4 if Z == 1.0 else 182.7) * pow(Z, -1. / 3.)
    BZ_e = (446.0 if Z == 1.0 else 1429.0) * pow(Z, -2. / 3.)
    D_n = 1.54 * pow(A, 0.27)
    E = K + mu
    dcs_factor = 7.297182E-07 * rem * rem * Z / E

    delta_factor = 0.5 * mu * mu / E
    qe_max = E / (1. + 0.5 * mu * mu / (me * E))

    nu = q / E
    delta = delta_factor * nu / (1. - nu)
    Phi_e = 0.0
    Phi_n = math.log(BZ_n * (mu + delta * (D_n * sqrte - 2.)) / (D_n * (me + delta * sqrte * BZ_n)))
    if Phi_n < 0.0:
        Phi_n = 0.0
    if q < qe_max:
        Phi_e = log(BZ_e * mu / ((1. + delta * phie_factor) * (me + delta * sqrte * BZ_e)))
        if (Phi_e < 0.):
            Phi_e = 0.0
    else:
        Phi_e = 0.0

    dcs = dcs_factor * (Z * Phi_n + Phi_e) * (4. / 3. * (1. / nu - 1.) + nu)
    return 0.0 if dcs < 0.0 else dcs * 1E+03 * AVOGADRO_NUMBER * (mu + K) / A
