# Criar o gráfico de radar
            fig = go.Figure()

            # Adicionar traços para cada jogador
            for index, row in df_top5_stats.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=row[['Kills', 'Knocks', 'Assists', 'Damage Dealt (normalized)', 'Revives']].values.tolist(),
                    theta=categories,
                    fill='toself',
                    name=row['Player'],
                    customdata=[f"Damage Dealt (normalized): {row['Damage Dealt (normalized)']:.2f}"],
                    hovertemplate='%{theta}: %{r}<br>'
                ))

            # Configurações do layout
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, df_top5_stats.iloc[:, 1:].max().max()]
                    )
                ),
                showlegend=True
            )
