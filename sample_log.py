from datetime import datetime, timedelta
import random

# Tipos de logs
log_levels = ['INFO', 'ERROR', 'WARN', 'ALERT']
log_types = ['APPLICATION', 'ACCESS', 'AUTHENTICATION', 'DATABASE', 'SYSTEM',
             'NETWORK', 'PERFORMANCE', 'DEPLOYMENT', 'MONITORING']
users = ['jose.silva', 'ana.moura', 'maria.souza', 'carlos.lima', 'admin.bot']
ips = ['192.168.1.12', '10.0.0.1', '172.16.0.5', '192.168.1.100', '10.10.10.10']
services = ['checkout-api', 'user-service', 'inventory-db', 'payment-gateway']

# Probabilidade de aparecer cada tipo de log (ajustado para maior realismo)
log_type_probabilities = {
    'APPLICATION': 0.1,
    'ACCESS': 0.1,
    'AUTHENTICATION': 0.1,
    'DATABASE': 0.2,
    'SYSTEM': 0.05,
    'NETWORK': 0.1,
    'PERFORMANCE': 0.1,
    'DEPLOYMENT': 0.05,
    'MONITORING': 0.2
}

# Probabilidade de aparecer cada nível de log (ajustado)
log_level_probabilities = {
    'INFO': 0.7,
    'ERROR': 0.1,
    'WARN': 0.15,
    'ALERT': 0.05
}

# Probabilidade de cada usuário realizar um login (mais alto valor significa mais login)
user_login_prob = {
    'jose.silva': 0.3,
    'ana.moura': 0.1,
    'maria.souza': 0.25,
    'carlos.lima': 0.2,
    'admin.bot': 0.15
}

# Geração de logs
start_time = datetime(2025, 4, 26, 9, 0, 0)
logs = []

for i in range(10000):  # Gerando 10.000 logs
    timestamp = start_time + timedelta(seconds=i*5)
    
    # Escolher o tipo de log baseado nas probabilidades
    log_type = random.choices(log_types, weights=[log_type_probabilities[t] for t in log_types], k=1)[0]
    
    # Escolher o nível de log baseado nas probabilidades
    log_level = random.choices(log_levels, weights=[log_level_probabilities[l] for l in log_levels], k=1)[0]

    # Gerar a mensagem do log de acordo com o tipo
    if log_type == 'ACCESS' and random.random() < sum(user_login_prob.values()):  # Ajuste de probabilidade total
        usuario = random.choices(users, weights=[user_login_prob[user] for user in users], k=1)[0]
        message = f'Login attempt for user: "{usuario}" from IP: {random.choice(ips)}'
    elif log_type == 'AUTHENTICATION':
        message = f'Login {"success" if random.random() > 0.5 else "failed"} for user: "{random.choice(users)}"'
    elif log_type == 'DATABASE':
        # Tempo de execução da query com distribuição assimétrica (maior chance de ser baixo)
        execution_time = random.choices([random.randint(50, 500), random.randint(500, 1500), random.randint(1500, 3000)],
                                        weights=[0.7, 0.2, 0.1])[0]
        message = f'Query executed: SELECT * FROM table_{random.randint(1,10)} (execution time {execution_time}ms)'
    elif log_type == 'SYSTEM':
        message = f'System load at {random.randint(10, 95)}%'
    elif log_type == 'NETWORK':
        message = f'Incoming requests: {random.randint(100, 2000)} per minute'
    elif log_type == 'PERFORMANCE':
        message = f'API response time: {random.randint(100, 800)}ms'
    elif log_type == 'DEPLOYMENT':
        message = f'Version {random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)} deployed by user: "{random.choice(users)}"'
    elif log_type == 'MONITORING':
        message = f'Service Health Check {"PASSED" if random.random() > 0.2 else "FAILED"} for service: {random.choice(services)}'
    else:  # APPLICATION
        message = f'Application event: {random.choice(["Started", "Stopped", "Crashed", "Recovered"])}'

    # Adicionar o log gerado na lista
    logs.append(f'[{timestamp.strftime("%Y-%m-%d %H:%M:%S")}] [{log_level}] [{log_type}] - {message}')

# Salvar o arquivo
file_name = 'logs_exemplo.txt'
with open(file_name, 'w') as f:
    for log in logs:
        f.write(log + '\n')

print(f'Arquivo {file_name} criado com sucesso!')
