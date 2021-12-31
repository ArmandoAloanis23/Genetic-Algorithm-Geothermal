#IJCN
import pandas as pd
import numpy as np
from pyXSteam.XSteam import XSteam
steamT = XSteam(XSteam.UNIT_SYSTEM_MKS)

# Lingkungan
m0 = None
P0 = 0.85 #bara
T0 = 23 + 273.15 #degC
h0 = steamT.h_pt(P0,T0-273.15)
s0 = steamT.s_pt(P0,T0-273.15)
E0 = None

# Kondisi Sumur
Xwh = 0.695
mflow = 163.3*1000/3600
Psumur = 15.7
Tsumur = steamT.tsat_p(Psumur)
hfsumur = steamT.hL_p(Psumur)
hgsumur = steamT.hV_p(Psumur)
hsumur = hfsumur + Xwh*(hgsumur-hfsumur)
sfsumur = steamT.sL_p(Psumur)
sgsumur = steamT.sV_p(Psumur)
ssumur = sfsumur + Xwh*(sgsumur-sfsumur)

# 1-Sumur ke Separator
m1 = mflow
P1 = 10.8
T1 = steamT.tsat_p(P1)
hf1 = steamT.hL_p(P1)
hg1 = steamT.hV_p(P1)
X1 = (hsumur-hf1)/(hg1-hf1)
h1 = hsumur
sf1 = steamT.sL_p(P1)
sg1 = steamT.sV_p(P1)
s1 = sf1 + X1*(sg1-sf1)
E1 = m1*((h1-h0)-T0*(s1-s0))

# 2-Separator ke Demister
h2 = h1
P2 = 10.6
T2 = steamT.tsat_p(P2)
hf2 = steamT.hL_p(P2)
hg2 = steamT.hV_p(P2)
m2 = 32.2
h2 = steamT.hV_p(P2)
s2 = steamT.sV_p(P2)
E2 = m2*((h2-h0)-T0*(s2-s0))

# 3-Demister Outlet
m3 = m2
P3 = 8.5
T3 = steamT.tsat_p(P3)
h3 = steamT.hV_p(P3)
s3 = steamT.sV_p(P3)
E3 = m3*((h3-h0)-T0*(s3-s0))

# 4-Demister to Turbin
m_4 = m3/2
Le_MCV = 0.31
Ri_MCV = 0.22
m4a = (1-Le_MCV)*m_4
m4b = (1-Ri_MCV)*m_4
P4 = P3
T4 = steamT.tsat_p(P4)
h4 = steamT.hV_p(P4)
s4 = steamT.sV_p(P4)
m4 = m4a + m4b
E4 = m4*((h4-h0)-T0*(s4-s0))
W = 13000

# 5-Turbin ke Condenser
P5 = 0.125
T5 = 50
m5 = m4
s5=s4
sf5 = steamT.sL_p(P5)
sg5 = steamT.sV_p(P5)
X5 = (s5-sf5)/(sg5-sf5)
hf5 = steamT.hL_p(P5)
hg5 = steamT.hV_p(P5)
h5 = hf5 + X5*(hg5-hf5)
E5 = m5*((h5-h0)-T0*(s5-s0))
eff = W/(m5*(h2-h5))
print(eff)

# 6-Condenser to Cooling Tower
P6 = None
T6 = 47
m6 = (3541*steamT.rhoL_t(T6))/3600
h6 = steamT.hL_t(T6)
s6 = steamT.sL_t(T6)
E6 = m6*((h6-h0)-T0*(s6-s0))

# 7-Cooling Tower to Condenser
P7 = None
T7 = 28
m7 = 900.4
h7 = steamT.hL_t(T7)
s7 = steamT.sL_t(T7)
E7 = m7*((h7-h0)-T0*(s7-s0))

# 8-Condenser to Inter Condenser
P8 = None
T8 = T6
m8 = 0.025*m5
h8 = steamT.hL_t(T8)+X5*(steamT.hV_t(T8)-steamT.hL_t(T8))
s8 = steamT.sL_t(T8)+X5*(steamT.sV_t(T8)-steamT.sL_t(T8))
E8 = m8*((h8-h0)-T0*(s8-s0))

# 9 - Demister to Inter Condenser
P9 = 8.6
T9 = steamT.tsat_p(P9)
m9 = (m3-m4)/2
h9 = steamT.hV_p(P9)
s9 = steamT.sV_p(P9)
E9 = m9*((h9-h0)-T0*(s9-s0))

# 10 - Demister to After Condenser
P10 = 8.5
T10 = steamT.tsat_p(P10)
m10 = (m3-m4)/2
h10 = steamT.hV_p(P10)
s10 = steamT.sV_p(P10)
E10 = m10*((h10-h0)-T0*(s10-s0))

# 11 - Inter Condenser
P11 = 0.6
T11 = None
m11 = 4.86
h11 = steamT.hL_p(P11)+X5*(steamT.hV_p(P11)-steamT.hL_p(P11))
s11 = steamT.sL_p(P11)+X5*(steamT.sV_p(P11)-steamT.sL_p(P11))
E11 = m11*((h11-h0)-T0*(s11-s0))

# 12 - Inter Condenser to Main Condenser
P12 = None
T12 = 37
m12 = 22.367
h12 = steamT.hL_t(T12)
s12 = steamT.sL_t(T12)
E12 = m12*((h12-h0)-T0*(s12-s0))

# 13 - Inter Condenser to After Condenser
P13 = 1.4
T13 = 50
m13 = 2.722
h13 = steamT.hL_t(T13)+X5*(steamT.hV_t(T13)-steamT.hL_t(T13))
s13 = steamT.sL_t(T13)+X5*(steamT.sV_t(T13)-steamT.sL_t(T13))
E13 = m13*((h13-h0)-T0*(s13-s0))

# 14 - After Condenser
P14 = 0.62
T14 = None
m14 = 6.922
h14 = steamT.hL_p(P14)+X5*(steamT.hV_p(P14)-steamT.hL_p(P14))
s14 = steamT.sL_p(P14)+X5*(steamT.sV_p(P14)-steamT.sL_p(P14))
E14 = m14*((h14-h0)-T0*(s14-s0))

# 15 - After Condenser to Main Condenser
P15 = None
T15 = 45
m15 = 26.175
h15 = steamT.hL_t(T15)
s15 = steamT.sL_t(T15)
E15 = m15*((h15-h0)-T0*(s15-s0))

# 16 - After Condenser to Exhaust
P16 = 0.78
T16 = 45
m16 = 0.976
h16 = steamT.hV_t(T16)
s16 = steamT.sV_t(T16)
E16 = m16*((h16-h0)-T0*(s16-s0))

# 17 - Cooling Tower to Inter Condenser
P17 = None
T17 = T7
m17 = 20.229
h17 = steamT.hL_t(T17)
s17 = steamT.sL_t(T17)
E17 = m17*((h17-h0)-T0*(s17-s0))

# 18 - Cooling Tower to After Condenser
P18 = None
T18 = T7
m18 = 20.229
h18 = steamT.hL_t(T18)
s18 = steamT.sL_t(T18)
E18 = m18*((h18-h0)-T0*(s18-s0))

# 19 - Udara to Cooling Tower
m19 = 2.4
P19 = 0.85 #bara
T19 = 23 #degC
h19 = steamT.h_pt(P19,T19)
s19 = steamT.s_pt(P19,T19)
E19 = m19*((h19-h0)-T0*(s19-s0))

# 20 - Udara out from Cooling Tower
m20 = 0.051*3
P20 = 0.85
T20 = None
h20 = steamT.hV_p(P20)
s20 = steamT.sV_p(P20)
E20 = m20*((h20-h0)-T0*(s20-s0))

# 21 - Cooling Tower to Settling Basin
m21 = m3
P21 = None
T21 = T7
h21 = steamT.hL_t(T21)
s21 = steamT.sL_t(T21)
E21 = m21*((h21-h0)-T0*(s21-s0))


# 22 - Separator to Injection Well
m22 = m1*(1-X1)
P22 = P2
T22 = steamT.tsat_p(P22)
h22 = steamT.hL_p(P22)
s22 = steamT.sL_p(P22)
E22 = m22*((h22-h0)-T0*(s22-s0))

# Exergy
# Separator
Exin_sep = E1
Exout_sep = E2+E22
Exeff_sep = Exout_sep/Exin_sep*100
Exloss_sep = Exin_sep-Exout_sep
# Demister
Exin_dem = E2
Exout_dem = E3
Exeff_dem = Exout_dem/Exin_dem*100
Exloss_dem = Exin_dem-Exout_dem
# Turbine-Generator
Exin_turbgen = E4
Exout_turbgen = W+E5
Exeff_turbgen = Exout_turbgen/Exin_turbgen*100
Exloss_turbgen = Exin_turbgen-Exout_turbgen
# Condenser
Exin_cond = E5+E7+E12+E15
Exout_cond = E8+E6
Exeff_cond = Exout_cond/Exin_cond*100
Exloss_cond = Exin_cond-Exout_cond
# Inter Condenser
Exin_incond = E11 + E17
Exout_incond = E12 + E13
Exeff_incond = Exout_incond/Exin_incond*100
Exloss_incond = Exin_incond-Exout_incond
# After Condenser
Exin_afcond = E14 + E18
Exout_afcond = E15 + E16
Exeff_afcond = Exout_afcond/Exin_afcond*100
Exloss_afcond = Exin_afcond-Exout_afcond
# Cooling Tower
Exin_ct = E6+E19
Exout_ct = E7+E17+E18+E20+E21
Exeff_ct = Exout_ct/Exin_ct*100
Exloss_ct = Exin_ct-Exout_ct
# Overall Power Plant
Exin_pp = E1
Exout_pp = W
Exloss_pp = Exloss_sep + Exloss_dem + Exloss_turbgen + Exloss_cond + Exloss_incond + Exloss_afcond + Exloss_ct
Exeff_pp = W/Exin_pp*100 #W

print("Daya keluaran W", W)
print("Kualitas uap X1", X1)
print("Laju alir massa uap m2", m2)
print("Efisiensi eksergi pembangkit", Exeff_pp)

# data = pd.DataFrame({
# 'Laju Alir Massa m (kg/s)':[m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12,
# m13, m14, m15, m16, m17, m18, m19, m20, m21, m22], 'Tekanan P (bara)':[P0, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12,
# P13, P14, P15, P16, P17, P18, P19, P20, P21, P22], 'Temperatur T (degC)':[T0-273.15, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12,
# T13, T14, T15, T16, T17, T18, T19, T20, T21, T22], 'Entalpi h (kJ/kg)':[h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12,
# h13, h14, h15, h16, h17, h18, h19, h20, h21, h22], 'Entropi s (kJ/kg K)':[s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12,
# s13, s14, s15, s16, s17, s18, s19, s20, s21, s22], 'Eksergi X (kW)':[E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12,
# E13, E14, E15, E16, E17, E18, E19, E20, E21, E22]
# })

# hasil = pd.DataFrame({
# 'Eksergi masuk':[Exin_sep, Exin_dem, Exin_turbgen, Exin_cond, Exin_incond, Exin_afcond, Exin_ct, Exin_pp],
# 'Eksergi Keluar':[Exout_sep, Exout_dem, Exout_turbgen, Exout_cond, Exout_incond, Exout_afcond, Exout_ct, Exout_pp],
# 'Eksergi Loss':[Exloss_sep, Exloss_dem, Exloss_turbgen, Exloss_cond, Exloss_incond, Exloss_afcond, Exloss_ct, Exloss_pp],
# 'Efisiensi Eksergi':[Exeff_sep, Exeff_dem, Exeff_turbgen, Exeff_cond, Exeff_incond, Exeff_afcond, Exeff_ct, Exeff_pp]
# })

# data.to_excel('./data.xlsx', sheet_name='Data')
# hasil.to_excel('./hasil.xlsx', sheet_name='Hasil')