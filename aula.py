from collections import Counter
import dash
from dash import dcc, html
import plotly.graph_objs as go
from datetime import datetime

# 1. Lendo o arquivo
with open('logs_exemplo.txt', 'r') as f:
    logs = f.readlines()

# 2. Filtrar logs por nível
erros = [linha for linha in logs if '[ERROR]' in linha]

# 3. Contar quantidade de cada nível de log
contagem_niveis = Counter()
for linha in logs:
    if '[INFO]' in linha:
        contagem_niveis['INFO'] += 1
    elif '[ERROR]' in linha:
        contagem_niveis['ERROR'] += 1
    elif '[WARN]' in linha:
        contagem_niveis['WARN'] += 1
    elif '[ALERT]' in linha:
        contagem_niveis['ALERT'] += 1

# 4. Contar quantidade de cada log_type
log_types = ['APPLICATION', 'ACCESS', 'AUTHENTICATION', 'DATABASE', 'SYSTEM',
             'NETWORK', 'PERFORMANCE', 'DEPLOYMENT', 'MONITORING']

contagem_log_types = Counter()
for linha in logs:
    for tipo in log_types:
        if f'[{tipo}]' in linha:
            contagem_log_types[tipo] += 1

# 5. Buscar tentativas de login
logins = [linha for linha in logs if '[ACCESS]' in linha]
usuarios = []
for login in logins:
    inicio = login.find('user: "') + len('user: "')
    fim = login.find('"', inicio)
    usuario = login[inicio:fim]
    usuarios.append(usuario)

contagem_usuarios = Counter(usuarios)

# 6. Buscar falhas de autenticação
falhas = [linha for linha in logs if '[AUTHENTICATION]' in linha and 'failed' in linha]

# 7. Buscar queries lentas (>1000ms)
queries_lentas = []
for linha in logs:
    if '[DATABASE]' in linha and 'execution time' in linha:
        tempo_str = linha.split('execution time ')[-1].replace('ms)', '').strip()
        try:
            tempo_ms = int(tempo_str)
            if tempo_ms > 1000:
                queries_lentas.append(linha)
        except ValueError:
            continue

# 8. Buscar falhas de monitoramento
falhas_monitoramento = [linha for linha in logs if '[MONITORING]' in linha and 'FAILED' in linha]

# ==========================================
# Criando o Dash app com Tema Noturno e Cores Pastéis
# ==========================================
app = dash.Dash(__name__)

dark_layout = {
    'paper_bgcolor': '#1e1e1e',
    'plot_bgcolor': '#1e1e1e',
    'font': {'color': 'white'}
}

app.layout = html.Div([
    html.H1("Dashboard de Logs de Sistema", style={'text-align': 'center'}),

    html.Div([
        dcc.Graph(
            id='grafico-niveis',
            figure={
                'data': [
                    go.Bar(
                        x=list(contagem_niveis.keys()),
                        y=list(contagem_niveis.values()),
                        marker={'color': ['#A8D5BA', '#FFB3B3', '#FFD59E', '#D0B3E1']}  # cores pastéis diferentes
                    )
                ],
                'layout': go.Layout(
                    title='Distribuição dos Tipos de Log (Níveis)',
                    xaxis={'title': 'Tipo de Log (Nível)'},
                    yaxis={'title': 'Quantidade'},
                    
                )
            }
        ),
        dcc.Graph(
            id='grafico-tipos-log',
            figure={
                'data': [
                    go.Bar(
                        x=list(contagem_log_types.keys()),
                        y=list(contagem_log_types.values()),
                        marker={'color': [
                            '#A8E6CF', '#DCEDC1', '#FFD3B6', '#FFAAA5', '#FF8C94', '#D5AAFF', '#B5EAD7', '#C7CEEA', '#FFDAC1'
                        ]}
                    )
                ],
                'layout': go.Layout(
                    title='Distribuição dos Tipos de Log (log_types)',
                    xaxis={'title': 'Tipo de Log (Categoria)', 'tickangle': 45},
                    yaxis={'title': 'Quantidade'},
                    
                )
            }
        )
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    html.Div([
        dcc.Graph(
            id='grafico-pizza-tipos-log',
            figure={
                'data': [
                    go.Pie(
                        labels=list(contagem_log_types.keys()),
                        values=list(contagem_log_types.values()),
                        hole=0.3,
                marker={'colors': [
                    '#A8E6CF', '#DCEDC1', '#FFD3B6', '#FFAAA5', '#FF8C94',
                    '#D5AAFF', '#B5EAD7', '#C7CEEA', '#FFDAC1'
                ]}
                    )
                ],
                'layout': go.Layout(
                    title='Proporção dos Tipos de Log (log_types)',
                    
                )
            }
        ),
        dcc.Graph(
            id='grafico-top-usuarios',
            figure={
                'data': [
                    go.Bar(
                        x=[usuario for usuario, _ in contagem_usuarios.most_common(10)],
                        y=[qtd for _, qtd in contagem_usuarios.most_common(10)],
                        marker={'color': '#AEDFF7'}
                    )
                ],
                'layout': go.Layout(
                    title='Top 10 Usuários com Mais Tentativas de Login',
                    xaxis={'title': 'Usuário'},
                    yaxis={'title': 'Quantidade de Tentativas'},
                    
                )
            }
        )
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    html.Div([
        dcc.Graph(
            id='grafico-falhas',
            figure={
                'data': [
                    go.Bar(
                        x=['Autenticação', 'Monitoramento', 'Queries Lentas'],
                        y=[len(falhas), len(falhas_monitoramento), len(queries_lentas)],
                        marker={'color': ['#FFB3B3', '#D0B3E1', '#FFD59E']}
                    )
                ],
                'layout': go.Layout(
                    title='Quantidade de Falhas por Tipo',
                    xaxis={'title': 'Tipo de Falha'},
                    yaxis={'title': 'Quantidade'},
                    
                )
            }
        ),
        dcc.Graph(
            id='grafico-histograma-tempos-queries',
            figure={
                'data': [
                    go.Histogram(
                        x=[int(linha.split('execution time ')[-1].replace('ms)', '').strip()) for linha in logs if '[DATABASE]' in linha and 'execution time' in linha],
                        nbinsx=20,
                        marker={'color': '#AEDFF7', 'line': {'color': 'white'}}
                    )
                ],
                'layout': go.Layout(
                    title='Distribuição dos Tempos de Execução das Queries (ms)',
                    xaxis={'title': 'Tempo (ms)'},
                    yaxis={'title': 'Quantidade de Queries'},
                    
                )
            }
        )
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
], style={ 'padding': '20px'})

if __name__ == '__main__':
    app.run(debug=True)
