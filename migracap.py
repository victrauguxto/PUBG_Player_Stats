import pandas as pd
import streamlit as st
import plotly.express as px

st.title('PUBG Analysis')


st.write("""
# Diferenças entre os servidores
Comparação entre os estilos de jogo nos servidores de PUBG
""")


df = pd.read_excel("PUBG_project.xlsx", sheet_name="GERAL")

# Obter valores únicos da coluna 'Server'
servers = ['Overview'] + df['Server'].unique().tolist()


# Obter o valor selecionado pelo usuário
server = st.sidebar.selectbox('Server', servers)

# Adiciona um separador
st.sidebar.markdown("---")

# Adiciona as informações de contato no rodapé
st.sidebar.markdown("""
#### Informações de Contato
- **Nome:** Victor Augusto
- **E-mail:** [augusto.victor446@gmail.com](mailto:augusto.victor446@gmail.com) 
- **Github:** [victrauguxto](https://github.com/victrauguxto)
- **X:** [@victrauguxto](https://x.com/victrauguxto)
""")

df['Pts_match'] = df['TotalPoints'] / df['NumberOfMatches']
df['Kills_match'] = df['Kills'] / df['NumberOfMatches']
df['Position_match'] = df['PlacePts'] / df['NumberOfMatches']
df['camp_server'] = df['CAMP'] + "-" + df['Server']


# Filtrar o DataFrame de acordo com a seleção
if server == 'Overview':
    df_filtered = df
else:
    df_filtered = df[df["Server"] == server]

# Obter valores únicos da coluna 'Camp' e o servidor associado a cada um deles
unique_camps_with_server = df_filtered.groupby('CAMP')['Server'].unique().apply(list).reset_index(name='Servers')

st.write("""
### Metodologia:
Para este estudo, foram analisados um total de 21 campeonatos de PUBG, sendo selecionados 3 campeonatos de cada servidor. As regiões das Américas foram analisadas separadamente (SA e NA) e também em conjunto como "Américas". Os campeonatos escolhidos possuem 16 participantes cada. Todas as medidas foram realizadas por partida, devido ao fato de que os campeonatos da região APAC e China possuem um maior número de partidas em comparação com os demais servidores. Essa abordagem foi adotada para garantir uma análise equilibrada e representativa de cada região.
""")


# Exibir a lista de valores únicos de 'CAMP' com o servidor associado
st.write(unique_camps_with_server)


st.write("""
### Objetivo:
O objetivo deste relatório é analisar e comparar as principais diferenças de estilo de jogo dos principais servidores do mundo em campeonatos de PUBG. A análise é baseada em dados de 21 campeonatos de 7 regiões diferentes (APAC, AM, EU, CN, KR, SA, NA), buscando identificar padrões e características distintivas de cada região. Essa análise pode auxiliar jogadores, equipes e espectadores a compreenderem melhor as nuances do cenário competitivo de PUBG e as particularidades de cada região.
""")

st.write("""
### Conceitos Importantes:
 - PPG = Points per game / Pontos por Partida
 - KPG = Kills per game / Kills por Partida
 - CPG = Position points per game / Pontos de Colocação por partida

""")

# Calcular os máximos e mínimos de pts_match por servidor
df_grouped = df_filtered.groupby(['Server'])['Pts_match'].agg(['max', 'min']).reset_index()
# Criar uma nova coluna com a diferença entre o máximo e o mínimo
df_grouped['diff'] = df_grouped['max'] - df_grouped['min']

# Agrupar o DataFrame original por 'Server' e 'CAMP' para calcular os máximos e mínimos de pts_match
df_grouped_camp = df_filtered.groupby(['Server', 'CAMP'])['Pts_match'].agg(['max', 'min']).reset_index()

# Filtrar o DataFrame `df_grouped_camp` pelo servidor selecionado
if server != 'Overview':
    df_grouped_camp = df_grouped_camp[df_grouped_camp["Server"] == server]

# Criar o gráfico de linhas com Plotly Express para 'CAMP'
fig2 = px.line(df_grouped_camp, x='CAMP', y=['max', 'min'],
               labels={'value': 'Pts_match', 'CAMP': 'CAMP'},
               title=f'Diferença média em PPG entre o primeiro e o último (por CAMP) - {server}',
               line_shape='linear')

# Criar o gráfico de linhas com Plotly Express
fig = px.line(df_grouped, x='Server', y=['max', 'min'],
              labels={'value': 'Pts_match', 'Server': 'Server'},
              title='Diferença média em pontos por partida entre o primeiro e o último',
              line_shape='linear')

# Criar o gráfico de barras com Plotly Express
fig1 = px.bar(df_grouped, x='Server', y=['min', 'max'],
              labels={'value': 'Pts_match', 'Server': 'Server'},
              title='Diferença em PPG entre o primeiro e o último')

fig4 = px.line(df_grouped, x='Server', y='diff',
               labels={'diff': 'Diferença entre Mínimo e Máximo', 'Server': 'Server'},
               title='Diferença média em PPG entre o primeiro e o último',
               line_shape="linear")

if server == 'Overview':
    st.write("""
        ##### O primeiro dado que chama atenção é a diferença entre os pontos do time que mais pontuou e o time que menos pontuou.
        """)
    st.plotly_chart(fig)
    st.write("""
            Gráfico 1: Distância entre os pontos por partida do primeiro e do último. Maior espaço entre as linhas = Maior a diferença
            """)

    st.plotly_chart(fig1)
    st.write("""
            Gráfico 2: Média da Variação de PPG entre o primeiro e o último colocado. Maior a distância das barras = Maior a diferença.
            """)
    st.plotly_chart(fig4)
    st.write("""
            Gráfico 3: Diferença média de pontos entre o primeiro e o último colocado por servidor. Maior a Linha, Maior a diferença de pontos
            """)
else:
    st.plotly_chart(fig2)


df_primeiros = df_filtered[df["Position"]==1]
df_primeiros['Time_camp'] = df_primeiros['TeamName'] + " " +df_primeiros['CAMP']


fig3 = px.bar(df_primeiros, x='Time_camp', y=['Position_match','Kills_match'],
              labels={'Time_camp':'Campeão', 'Position_match':'Pts_match'})

st.plotly_chart(fig3)




