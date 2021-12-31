#IJCN
import numpy as np
import random
from pyXSteam.XSteam import XSteam
steamT = XSteam(XSteam.UNIT_SYSTEM_MKS)


def objective_function(pop):
    fitness = np.zeros(pop.shape[0])
    for i in range(pop.shape[0]):
        x = pop[i]
        #IJCN
        # Lingkungan
        m0 = None
        P0 = 0.85 #bara
        T0 = 23 + 273.15 #K
        h0 = steamT.h_pt(P0,T0-273.15) #degC untuk T
        s0 = steamT.s_pt(P0,T0-273.15) #degC untuk T
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
        P1 = x[0]
        nT1 = np.frompyfunc(steamT.tsat_p, 1, 1)
        T1 = nT1(x[0])
        nhf1 = np.frompyfunc(steamT.hL_p, 1, 1)
        hf1 = nhf1(x[0])
        nhg1 = np.frompyfunc(steamT.hV_p, 1, 1)
        hg1 = nhg1(x[0])
        X1 = (hsumur-hf1)/(hg1-hf1)
        h1 = hf1 + X1*(hg1-hf1)
        sf1 = steamT.sL_p(P1)
        sg1 = steamT.sV_p(P1)
        s1 = sf1 + X1*(sg1-sf1)
        E1 = m1*((h1-h0)-T0*(s1-s0))

        # 2-Separator ke Demister
        P2 = P1
        nT2 = np.frompyfunc(steamT.tsat_p, 1, 1)
        T2 = nT2(P2)
        m2 = m1*X1
        nh2 = np.frompyfunc(steamT.hV_p, 1, 1)
        h2 = nh2(P2)
        ns2 = np.frompyfunc(steamT.sV_p, 1, 1)
        s2 = ns2(P2)
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
        m4 = m4a + m4b
        T4 = steamT.tsat_p(P4)
        h4 = steamT.hV_p(P4)
        s4 = steamT.sV_p(P4)
        E4 = m4*((h4-h0)-T0*(s4-s0))

        # 5-Turbin ke Condenser
        P5 = 0.125
        T5 = 50
        m5 = m4
        s5 = s4
        sf5 = steamT.sL_p(P5)
        sg5 = steamT.sV_p(P5)
        X5 = (s4-sf5)/(sg5-sf5)
        hf5 = steamT.hL_p(P5)
        hg5 = steamT.hV_p(P5)
        h5 = hf5 + X5*(hg5-hf5)
        E5 = m5*((h5-h0)-T0*(s5-s0))
        W = m5*0.8451*(h2-h5) #0.8451

        # 6-Condenser to Cooling Tower
        P6 = None
        T6 = 47
        m6 = (3541*steamT.rhoL_t(T6))/3600
        h6 = steamT.hL_t(T6)
        s6 = steamT.sL_t(T6)
        E6 = m6*((h6-h0)-T0*(s6-s0))

        # 7-Cooling Tower to Condenser
        P7 = None
        T7 = x[1]#28
        m7 = 900.4
        nh7 = np.frompyfunc(steamT.hL_t, 1, 1)
        h7 = nh7(x[1])
        ns7 = np.frompyfunc(steamT.sL_t, 1, 1)
        s7 = ns7(x[1])
        #h7 = steamT.hL_t(T7)
        #s7 = steamT.sL_t(T7)
        E7 = m7*((h7-h0)-T0*(s7-s0))

        # 8-Condenser to Inter Condenser
        P8 = None
        T8 = T6
        m8 = 0.025*m5
        h8 = steamT.hL_t(T8)+X5*(steamT.hV_t(T8)-steamT.hL_t(T8))
        s8 = steamT.sL_t(T8)+X5*(steamT.sV_t(T8)-steamT.sL_t(T8))
        E8 = m8*((h8-h0)-T0*(s8-s0))

        # 9 - Demister to Inter Condenser
        P9 = P3+0.1
        T9 = steamT.tsat_p(P9)
        h9 = steamT.hV_p(P9)
        s9 = steamT.sV_p(P9)
        m9 = (m3-m4)/2
        E9 = m9*((h9-h0)-T0*(s9-s0))

        # 10 - Demister to After Condenser
        P10 = P3
        m10 = (m3-m4)/2
        T10 = steamT.tsat_p(P10)
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
        nh17 = np.frompyfunc(steamT.hL_t, 1, 1)
        h17 = nh17(T17)
        ns17 = np.frompyfunc(steamT.sL_t, 1, 1)
        s17 = ns17(T17)
        m17 = 20.229
        E17 = m17*((h17-h0)-T0*(s17-s0))

        # 18 - Cooling Tower to After Condenser
        P18 = None
        T18 = T7
        nh18 = np.frompyfunc(steamT.hL_t, 1, 1)
        h18 = nh18(T18)
        ns18 = np.frompyfunc(steamT.sL_t, 1, 1)
        s18 = ns18(T18)
        m18 = 20.229
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
        nh21 = np.frompyfunc(steamT.hL_t, 1, 1)
        h21 = nh21(T21)
        ns21 = np.frompyfunc(steamT.sL_t, 1, 1)
        s21 = ns21(T21)
        E21 = m21*((h21-h0)-T0*(s21-s0))

        # 22 - Separator to Injection Well
        m22 = m1*(1-X1)
        P22 = P1
        nT22 = np.frompyfunc(steamT.tsat_p, 1, 1)
        T22 = nT22(P22)
        nh22 = np.frompyfunc(steamT.hL_p, 1, 1)
        h22 = nh22(P22)
        ns22 = np.frompyfunc(steamT.sL_p, 1, 1)
        s22 = ns22(P22)
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
        # fitness[i] = (W/Exin_pp*100)
        fitness[i] = W
    return fitness

def selection(pop, fitness, pop_size):
    next_generation = np.zeros((pop_size, pop.shape[1]))
    elite = np.argmax(fitness)
    next_generation[0] = pop[elite]
    fitness = np.delete(fitness, elite)
    pop = np.delete(pop, elite, axis=0)
    P = [f / sum(fitness) for f in fitness]
    index = list(range(pop.shape[0]))
    index_selected = np.random.choice(index, size=pop_size-1, replace=False, p=P)
    s = 0
    for j in range(pop_size - 1):
        next_generation[j + 1] = pop[index_selected[s]]
        s += 1
    return next_generation

def crossover(pop, crossover_rate):
    offspring = np.zeros((crossover_rate, pop.shape[1]))
    for i in range(int(crossover_rate / 2)):
        r1 = random.randint(0, pop.shape[0] - 1)
        r2 = random.randint(0, pop.shape[0] - 1)
        while r1 == r2:
            r1 = random.randint(0, pop.shape[0] - 1)
            r2 = random.randint(0, pop.shape[0] - 1)
        cutting_point = random.randint(1, pop.shape[1] - 1)
        offspring[2 * i, 0:cutting_point] = pop[r1, 0:cutting_point]
        offspring[2 * i, cutting_point:] = pop[r2, cutting_point:]
        offspring[2 * i +1, 0:cutting_point] = pop[r2, 0:cutting_point]
        offspring[2 * i +1, cutting_point:] = pop[r1, cutting_point:]
    return offspring

def mutation(pop, mutation_rate):
    offspring = np.zeros((mutation_rate, pop.shape[1]))
    for i in range(int(mutation_rate / 2)):
        r1 = random.randint(0, pop.shape[0] - 1)
        r2 = random.randint(0, pop.shape[0] - 1)
        while r1 == r2:
            r1 = random.randint(0, pop.shape[0] - 1)
            r2 = random.randint(0, pop.shape[0] - 1)
        cutting_point = random.randint(0, pop.shape[1] - 1)
        offspring[2 * i] = pop[r1]
        offspring[2 * i, cutting_point] = pop[r2, cutting_point]
        offspring[2 * i + 1] = pop[r2]
        offspring[2 * i + 1, cutting_point] = pop[r1, cutting_point]
    return offspring

def local_search(pop, fitness, lower_bounds, upper_bounds, step_size, rate):
    index = np.argmax(fitness)
    offspring = np.zeros((rate * 2 * pop.shape[1], pop.shape[1]))
    for r in range(rate):
        offspring1 = np.zeros((pop.shape[1], pop.shape[1]))
        for i in range(int(pop.shape[1])):
            offspring1[i] = pop[index]
            offspring1[i, i] += np.random.uniform(0, step_size)
            if offspring1[i, i] > upper_bounds[i]:
                offspring1[i, i] = upper_bounds[i]
        offspring2 = np.zeros((pop.shape[1], pop.shape[1]))
        for i in range (int(pop.shape[1])):
            offspring2[i] = pop[index]
            offspring2[i, i] += np.random.uniform(-step_size, 0)
            if offspring2[i, i] < lower_bounds[i]:
                offspring2[i, i] = lower_bounds[i]
        offspring12 = np.zeros((2 * pop.shape[1], pop.shape[1]))
        offspring12[0:pop.shape[1]] = offspring1
        offspring12[pop.shape[1]:2 * pop.shape[1]] = offspring2
        offspring[r * 2 * pop.shape[1]:r * 2 * pop.shape[1] + 2 * pop.shape[1]] = offspring12
    return offspring

# This script of genetic algorithm belongs to Sun Duy Dao
# you can check the full video in "Adaptive Re-Start Hybrid Genetic Algorithm for Global Optimization (Python Code)"
# in this link https://www.youtube.com/watch?v=mSqZqvm7YUA&t=5s