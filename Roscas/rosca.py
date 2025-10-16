import numpy as np

# =================== Análise força e torque em parafuso de potência ===================

# Variáveis do parafuso
lamb = 10 # ° - ângulo de avanço do parfuso
L = 1 # mm - avanço
d_p = 4 # mm - diâmetro primitivo do parafuso de potência
mi = 0.15 # adm - coeficiente de atrito parafuso-rosca
alpha = 14.5 # ° - se a rosca for ACME
alpha = 0 # ° - se a rosca for quadrada

lamb = lamb*np.pi/180 #transformando alpha em rad
alpha = alpha*np.pi/180 #transformando alpha em rad

# Variáveis do colar
mi_c = 0.4 # coeficiente de atrito do colar
d_c = 2 # mm - diâmetro médio do colar

# ----------------------------------------

P = 1000 # N - carga aplicada no parafuso

# ----------------------------------------

# Torque do colar
T_c = mi_c*P*d_c/2

# Função do ângulo de avanço lamb
F_up = P * (mi*np.cos(lamb) + np.sin(lamb)) / (np.cos(lamb) - mi*np.sin(lamb))
F_down = P * (mi*np.cos(lamb) + np.sin(lamb)) / (np.cos(lamb) - mi*np.sin(lamb))

T_up = F_up * d_p/2 + T_c
T_down = F_down * d_p/2 + T_c

# Em função do avanço L

T_u = P*d_p/2 * (mi*np.pi*d_p + L*np.cos(alpha))/(np.pi*d_p*np.cos(alpha) - mi*L)
T_d = P*d_p/2 * (mi*np.pi*d_p - L*np.cos(alpha))/(np.pi*d_p*np.cos(alpha) + mi*L)

T_up = T_c + T_u
T_down = T_c + T_d

# Check se parafuso é autotravante
if mi >= L/(np.pi*d_p)*np.cos(alpha*np.pi/180):
    print('Parafuso autotravante')
else:
    print('Parafuso não autotravante')
    
# Calculando a eficiência do parafuso de potência

e = (1-mi*np.tan(lamb)) / (1-mi*(1/np.tan(lamb)))

# ------------------- PARAFUSOS DE FIXAÇÃO -------------------

# =================== Tensões em parafusos ===================

type = 'ISO'

F = 577.27e3 # N - força normal aplicada na rosca
d_nominal = 8 # mm - diâmetro nominal da rosca
passo = 1 # mm - passo da rosca

N = 3 # número de filetes por polegadas

# === carregamento sob tração ===

x1 = 0.649519
x2 = 1.226869

d_p = d_nominal - x1/N # mm - diâmetro primitivo da rosca UNS
d_r = d_nominal - x2/N # mm - diâmetro menor da rosca UNS

d_p = d_nominal - x1*passo # mm - diâmetro primitivo da rosca ISO
d_r = d_nominal - x2*passo # mm - diâmetro menor da rosca ISO
print(f'Dp é: {d_p:.2f}')
print(f'Dr é: {d_r:.2f}')

A_t = np.pi/4 * ( (d_p + d_r)/2 )**2 # mm²
print(f'Área transversal é: {A_t:.2f}')

sigma_n = F/(A_t*1e-6)
print(sigma_n)


# === carregamento sob cisalhamento ===

w_i = {
    'UNS'      : 0.80,
    'ISO'      : 0.80,
    'Quadrada' : 0.50,
    'Acme'     : 0.77,
    'Botareu'  : 0.90,
}

w_o = {
    'UNS'      : 0.88,
    'ISO'      : 0.88,
    'Quadrada' : 0.50,
    'Acme'     : 0.63,
    'Botareu'  : 0.83,
}

# Rasgamento de parafuso
A_s = np.pi*d_r*w_i[type]*passo

# A área pode ser multiplicada por todos, um, ou alguma fração 
# do número total de filetes de rosca engajados de acordo ao que julgar correto o 
# projetista 
# Em todo caso, devemos supor algum 
# grau de compartilhamento da carga entre os filetes de rosca a fim de calcular as 
# tensões. Um modo de proceder consiste em considerar que, uma vez que uma 
# falha completa requer que todos os filetes de rosca sejam rasgados, estas podem 
# ser consideradas como compartilhando a carga igualmente. Essa hipótese é 
# provavelmente válida desde que a porca ou parafuso (ou ambos) seja dúctil de modo 
# a permitir que cada rosca escoe à medida que o conjunto começa a falhar. 
# Contudo, se ambas as partes são frágeis (por exemplo, aços de alta resistência ou ferro 
# fundido) e o ajuste dos filetes de rosca é pobre, podemos imaginar cada filete 
# assumindo toda a carga por turnos até que haja fratura e o trabalho seja repassado 
# para o próximo filete. A realidade está novamente inserida entre esses extremos. 

tau_s_parafuso = F/A_s

# Rasgamento de porca
A_s = np.pi*d_r*w_i[type]*passo

tau_s_porca = F/A_s

# =================== Pré-carga em parafusos ===================

# NOTA: criar função de gráfico em função do aperto,
# baseado no diâmetro nominal escolhido

d_nominal = 100 # mm - diâmetro nominal da rosca
F_i = 100 # N - força de pré-carga
K_i = 0.21 # coeficiente resultante do atrito da cabeça do parafuso e filetes

T_i = K_i*F_i*d_nominal

d_nominal = 100 # mm - diâmetro nominal da rosca
T_i = 100 # Nm - torque de pré-carga
K_i = 0.21 # coeficiente resultante do atrito da cabeça do parafuso e filetes

F_i = T_i/(K_i*d_nominal)

# ==============================================================
# Tabela 15-2 Dimensões principais de roscas de parafusos métricos padrão ISO
# tupla com (passo [mm], diâmetro menor [mm], área sob-tração [mm²])
# nem precisa dessa tabela pois é possível somente informar o diâmetro nominal
# e 
rosca_grossa = {
    3   : (0.50 ,  2.39 ,   5.03) ,
    3.5 : (0.60 ,  2.76 ,   6.78) ,
    4   : (0.70 ,  3.14 ,   8.78) ,
    5   : (0.80 ,  4.02 ,  14.18) ,
    6   : (1.00 ,  4.77 ,  20.12) ,
    7   : (1.00 ,  5.77 ,  28.86) ,
    8   : (1.25 ,  6.47 ,  36.61) ,
    10  : (1.50 ,  8.16 ,  57.99) ,
    12  : (1.75 ,  9.85 ,  84.27) ,
    14  : (2.00 , 11.55 , 115.44) ,
    16  : (2.00 , 13.55 , 156.67) ,
    18  : (2.50 , 14.93 , 192.47) ,
    20  : (2.50 , 16.93 , 244.79) ,
    22  : (2.50 , 18.93 , 303.40) ,
    24  : (3.00 , 20.32 , 352.50) ,
    27  : (3.00 , 23.32 , 459.41) ,
    30  : (3.50 , 25.71 , 560.59) ,
    33  : (3.50 , 28.71 , 693.55) ,
    36  : (4.00 , 31.09 , 816.72) ,
    39  : (4.00 , 34.09 , 975.75) ,
}

rosca_fina = {
    3   : True,
    3.5 : True,
    4   : True,
    5   : True,
    6   : True,
    7   : True,
    8   : True,
    10  : True,
    12  : True,
    14  : True,
    16  : True,
    18  : True,
    20  : True,
    22  : True,
    24  : True,
    27  : True,
    30  : True,
    33  : True,
    36  : True,
    39  : True,
}

rosca_grossa = {
    3   : False,
    3.5 : False,
    4   : False,
    5   : False,
    6   : False,
    7   : False,
    8   : True,
    10  : True,
    12  : True,
    14  : True,
    16  : True,
    18  : True,
    20  : True,
    22  : True,
    24  : True,
    27  : True,
    30  : True,
    33  : True,
    36  : True,
    39  : True,
}

