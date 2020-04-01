import numpy as np

avogadro = 6.0221412927 * 10**(23)
sec_in_year = 365 * 24 * 60 * 60

# Natural abundance of isotopes;
# Wedepohl, K.H. Handbook of Geochemistry, Springer-Verlag, Berlin (1978).
X_40K = 1.171 * 10**(-4)
X_238U = 0.99275 
X_235U = 0.00725
X_232Th = 1.0

# Decay energy sums (MeV/decay series)
# Ekstrom, L.P., Firestone, R.B. World Wide Web Table of Radioactive Isotopes, database
# version 2 (1999).
Sum_DS_A_238U = 42.87
Sum_DS_A_235U = 34.03
Sum_DS_A_232Th = 35.95

Sum_DS_B_238U = 6.0935
Sum_DS_B_235U = 10.4470
Sum_DS_B_232Th = 2.8408
Sum_DS_B_40K = 1.1760

Sum_DS_G_238U = 1.7034
Sum_DS_G_235U = 0.5500
Sum_DS_G_232Th = 2.2447
Sum_DS_G_40K = 0.1566

# Relative stopping power ratio's
# Aitken, M.K. Thermoluminescence Dating, Academic Press, Orlando, Florida (1985).
S_alpha = 1.89
S_beta = 1.25
S_gamma = 1.14

# Decay constant of isotopes (/yr)
# Pilson, M.E.Q. An Introduction to the Chemistry of the Sea, Cambridge University Press (2012).
lambda_238U = 1.55 * 10**(-10)
lambda_235U = 9.85 * 10**(-10)
lambda_232Th = 0.693 / (1.405 * 10**10)
lambda_40K = 5.428 * 10**(-10)

# Atomic weight of isotopes
AW_238U = 238.029
AW_235U = 235.029
AW_232Th = 232.028
AW_40K = 39.098


def calculate_Phi_at_z(Phi_0, sediment_thickness, depth):
    """
    Three different zones: shelf, margin, abyss;
    
    LaRowe, Douglas E., Ewa Burwicz, Sandra Arndt, Andrew W. Dale, and Jan P. Amend. 
    Temperature and volume of global marine sediments. Geology 45, 275-278 (2017).
    
    Hantschel, Thomas, and Armin I. Kauerauf. Fundamentals of basin and petroleum systems 
    modeling. Springer Science & Business Media, (2009).
    """
    # shelf
    if depth < 200:
        c_0 = .5e-3
        
    # margin
    elif depth >= 200 and depth <= 3500:
     c_0 = 1.7e-3
     
    # abyssal
    elif depth > 3500:
        c_0 = .85e-3

    Phi_z = Phi_0 * np.exp(-c_0 * sediment_thickness)
    
    return Phi_z


def calculate_production(U, Th, K, G_H2_alpha, G_H2_gamma, G_H2_beta, Rho_grain, Phi):
    """
    Blair, C. C., D'Hondt, S., Spivack, A. J., Kingsley, R. H. Radiolytic hydrogen and
    microbial respiration in subsurface sediments. Astrobiology 7, 951-970 (2007).
    """
    # ppm
    U_238 = X_238U * (U)
    # ppb
    U_235 = X_235U * (U) * 1000
    # ppm
    Th_232 = X_232Th * (Th) 
    #ppm
    K_40 = X_40K * (K)

    # Activities in decay/s/g_sed           
    Act_238U  = (lambda_238U  * U_238  * 10**(-6) * avogadro) / (sec_in_year * AW_238U)
    Act_235U  = (lambda_235U  * U_235  * 10**(-9) * avogadro) / (sec_in_year * AW_235U) 
    Act_232Th = (lambda_232Th * Th_232 * 10**(-6) * avogadro) / (sec_in_year * AW_232Th) 
    Act_40K   = (lambda_40K   * K_40   * 10**(-6) * avogadro) / (sec_in_year * AW_40K)

    P_H2_alpha = (Act_238U * Sum_DS_A_238U + Act_235U * Sum_DS_A_235U + Act_232Th * \
        Sum_DS_A_232Th) * Rho_grain * (1 - Phi) * G_H2_alpha
        
    P_H2_beta =  (Act_238U * Sum_DS_B_238U + Act_235U * Sum_DS_B_235U + Act_232Th * \
        Sum_DS_B_232Th + Act_40K * Sum_DS_B_40K) * Rho_grain * (1 - Phi)* G_H2_beta
        
    P_H2_gamma = (Act_238U * Sum_DS_G_238U + Act_235U * Sum_DS_G_235U + Act_232Th * \
        Sum_DS_G_232Th + Act_40K * Sum_DS_G_40K) * Rho_grain * (1 - Phi)* G_H2_gamma

    # Hydrogen production rate by water radiolysis (fct( alpha, beta & gamma radiation)
    # molecules H2 / s / cm3_sed
    P_H2_sed = P_H2_alpha + P_H2_beta + P_H2_gamma 
    
    # mol H2 / yr / cm3_sed
    P_H2_sed = P_H2_sed * sec_in_year / avogadro 

    return P_H2_sed
