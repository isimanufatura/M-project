import numpy as np

w_i = {
    'UNS'      : 0.80,
    'ISO'      : 0.80,
    'Quadrada' : 0.50,
    'Acme'     : 0.77,
    'Botareu'  : 0.90,
}

type = 'ISO'

passo = 1 # mm - passo da rosca
d = 6 # mm - diâmetro_nominal da rosca

# Alumínio 6351-T6

sigma_e = 283e6 # Pa
f_a = 0.9 # fator limite de aplicação da pré-carga

tau_e = 200e6 # Pa

# Tensão axial

# === carregamento sob tração ===

x1 = 0.649519
x2 = 1.226869

d_p = d - x1*passo # mm - diâmetro primitivo da rosca ISO
d_r = d - x2*passo # mm - diâmetro menor da rosca ISO
#print(f'Dp é: {d_p:.2f}')
#print(f'Dr é: {d_r:.2f}')

A_t = np.pi/4 * ( (d_p + d_r)/2 )**2 # mm²
print(f'Área transversal é: {A_t:.2f}')

#sigma_n = F/(A_t*1e-6)
#print(sigma_n)

# Tensão de cisalhamento
A_s = np.pi*d_r*w_i[type]*passo

#tau_s_porca = F/A_s

# Tensões torcionais
T = 15e3 # Nmm
tau_tors = 16*T/(np.pi*d_r**3)
#print(tau_tors)

T = tau_e*f_a*(np.pi*(d_r*1e-3)**3)/16
#print(T)

def check_torque(d,passo,T,tau_e):
    # === carregamento sob tração ===
    
    print(f'Analisando o parafuso M{d}')

    x1 = 0.649519
    x2 = 1.226869

    d_p = d - x1*passo # mm - diâmetro primitivo da rosca ISO
    d_r = d - x2*passo # mm - diâmetro menor da rosca ISO
    print(f'Dp é: {d_p:.2f}')
    print(f'Dr é: {d_r:.2f}')

    A_t = np.pi/4 * ( (d_p + d_r)/2 )**2 # mm²
    #print(f'Área transversal é: {A_t:.2f}')
    
    # Tensões torcionais
    tau_tors = 16*T/(np.pi*(d_r*1e-3)**3)
    print(f'Tensão de cisalhamento resultante da pré-carga de {T}Nm:\n{tau_tors*1e-6:.2f} MPa')

    T = tau_e*(np.pi*(d_r*1e-3)**3)/16
    print(f'Pré-carga suportada pelo material:\n{T:.4f} Nm')
    
    F = T/(0.21*d*1e-3)
    print(f'A força de pré-carga suportada é:\n{F:.2f}')
    
d_parafusos = [3,4,5,6] # mm 
passo_parafusos = [0.5,0.7,0.8,1] # mm
T_parafusos = [2,4,9,15] #Nm
for di,pi,Ti in zip(d_parafusos,passo_parafusos,T_parafusos):
    tau_e = 200e6 # Pa
    check_torque(di,pi,Ti,tau_e)