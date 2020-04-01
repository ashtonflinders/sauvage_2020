import numpy as np

def sediment_parameters(lith):
    """
    To perform the global calculation, each lithologic type is assigned a characteristic 
    set of G(H2)-values (alpha, beta, and gamma radiation), radioactive element content
    (sedimentary U, Th and K concentration) and density (Supp. Table 3, Sauvage et al. 2020). 

    Radiolytic yields for the main seafloor lithologies are obtained by averaging 
    experimentally derived yields for the respective lithologies (Supp. Table 3, Sauvage 
    et al. 2020). We assume that G(H2)-beta values equal G(H2)-gamma values.

    'U'         :   ppm
    'Th'        :   ppm
    'K'         :   ppm
    'RHO'       :   gm / cm**3
    'H2_ALPHA'  :   Molecules H2 MeV**(-1)
    'H2_BETA'   :   Molecules H2 MeV**(-1)
    'H2_GAMMA'  :   Molecules H2 MeV**(-1)
    """

    lithogenous = { 'U'         :   2.70,   \
                    'Th'        :   12,     \
                    'K'         :   20753,  \
                    'RHO'       :   2.70,   \
                    'H2_ALPHA'  :   146100, \
                    'H2_BETA'   :   2800,   \
                    'H2_GAMMA'  :   2800}

    si_ooze = {     'U'         :   1.82,   \
                    'Th'        :   10.44,  \
                    'K'         :   24790,  \
                    'RHO'       :   2.30,   \
                    'H2_ALPHA'  :   200750, \
                    'H2_BETA'   :   18250,  \
                    'H2_GAMMA'  :   18250}

    ca_ooze = {     'U'         :   0.77,   \
                    'Th'        :   0.53,   \
                    'K'         :   684,    \
                    'RHO'       :   2.70,   \
                    'H2_ALPHA'  :   62000,  \
                    'H2_BETA'   :   4800,   \
                    'H2_GAMMA'  :   4800}

    marl = {        'U'         :   1.16,   \
                    'Th'        :   9.04,   \
                    'K'         :   1100,   \
                    'RHO'       :   2.44,   \
                    'H2_ALPHA'  :   157300, \
                    'H2_BETA'   :   6200,   \
                    'H2_GAMMA'  :   6200}

    clay = {        'U'         :   2.51,   \
                    'Th'        :   11.21,  \
                    'K'         :   18748,  \
                    'RHO'       :   2.70,   \
                    'H2_ALPHA'  :   248464, \
                    'H2_BETA'   :   8455,   \
                    'H2_GAMMA'  :   8455}

    other = {       'U'         :   2.70,   \
                    'Th'        :   12,     \
                    'K'         :   20753,  \
                    'RHO'       :   2.70,   \
                    'H2_ALPHA'  :   146100, \
                    'H2_BETA'   :   2800,   \
                    'H2_GAMMA'  :   2800}


    lith_table3 = {1:lithogenous, 2:si_ooze, 3:ca_ooze, 4:marl, 5:clay, 6:other}
 
    """ Initialize parameter datasets """
    U = np.empty(lith.shape)
    U[:] = np.NAN
    Th = np.copy(U)
    K = np.copy(U)
    RHO = np.copy(U)
    H2_ALPHA = np.copy(U)
    H2_BETA = np.copy(U)
    H2_GAMMA = np.copy(U)
    H2_PRODUCTION = np.copy(U)


    for lith_i in lith_table3:
        U[lith == lith_i]        = lith_table3[lith_i]['U']
        Th[lith == lith_i]       = lith_table3[lith_i]['Th']
        K[lith == lith_i]        = lith_table3[lith_i]['K']
        RHO[lith == lith_i]      = lith_table3[lith_i]['RHO']
        H2_ALPHA[lith == lith_i] = lith_table3[lith_i]['H2_ALPHA']
        H2_BETA[lith == lith_i]  = lith_table3[lith_i]['H2_BETA']
        H2_GAMMA[lith == lith_i] = lith_table3[lith_i]['H2_GAMMA']

    return U, Th, K, RHO, H2_ALPHA, H2_BETA, H2_GAMMA

