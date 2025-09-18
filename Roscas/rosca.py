import numpy as np



# =================== Tensões em parafusos ===================

type = 'ISO'

F = 577.27e3 # N - força normal aplicada na rosca
d_nominal = 100 # mm - diâmetro nominal da rosca
passo = 3 # mm - passo da rosca

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