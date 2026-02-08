import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Quanto dinheiro podes ter ao sair da faculdade?",
    layout="centered"
)

st.title("🎓 Simulação de Património no Final da Faculdade")
st.write(
    "Esta simulação estima quanto dinheiro poderás ter ao terminar a faculdade, "
    "com base nas tuas **condições reais**, hábitos e escolhas financeiras."
)

# -----------------------------
# MÉDIAS DE REFERÊNCIA
# -----------------------------
MEDIAS = {
    "Alimentação": 180,
    "Lazer": 80,
    "Transportes": 60,
    "Outros": 50
}

# -----------------------------
# FUNÇÃO PIE CHART SEGURA
# -----------------------------
def plot_gastos_pie(gastos_dict):
    clean_data = {
        k: v for k, v in gastos_dict.items()
        if v is not None and not np.isnan(v) and v > 0
    }

    if len(clean_data) == 0:
        return None

    fig = px.pie(
        names=list(clean_data.keys()),
        values=list(clean_data.values()),
        hole=0.4
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>%{value:.0f}€<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20)
    )

    return fig



# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs([
    "📋 Condições",
    "💸 Gastos Mensais",
    "📊 Resultado Final"
])

# =====================================================
# TAB 1 — CONDIÇÕES
# =====================================================
with tab1:
    st.subheader("📋 Condições da Faculdade")

    anos_faculdade = st.slider(
        "Duração da faculdade (anos)",
        1, 6, 5
    )

    paga_casa = st.checkbox("Pagas renda/casa?")
    if paga_casa:
        renda = st.number_input(
            "Valor mensal da renda (€)",
            min_value=0,
            value=400
        )
    else:
        renda = 0

    recebe_ajuda_renda = st.checkbox("Recebes ajuda mensal para pagar renda?")
    if recebe_ajuda_renda:
        ajuda_pais_renda = st.number_input(
            "Ajuda mensal para renda (€)",
            min_value=0,
            value=200
        )
    else:
        ajuda_pais_renda = 0

    recebe_ajuda = st.checkbox("Recebes ajuda mensal para gastos do dia a dia?")
    if recebe_ajuda:
        ajuda_pais = st.number_input(
            "Ajuda mensal (€)",
            min_value=0,
            value=200
        )
    else:
        ajuda_pais = 0

    tem_part_time = st.checkbox("Tens part-time?")
    if tem_part_time:
        rendimento_part_time = st.number_input(
            "Rendimento mensal do part-time (€)",
            min_value=0,
            value=500
        )
    else:
        rendimento_part_time = 0

    st.success("Avança para a TAB 💸 Gastos Mensais assim que terminares de preencher esta.")

# =====================================================
# TAB 2 — GASTOS
# =====================================================
with tab2:
    st.subheader("💸 Gastos Mensais Médios")

    alimentacao = st.number_input("Alimentação (€)", 0, 400, 180)
    transportes = st.number_input("Transportes (€)", 0, 200, 60)
    lazer = st.number_input("Lazer (€)", 0, 300, 80)
    outros = st.number_input("Outros gastos (€)", 0, 300, 50)

    propinas = st.number_input(
        "Propinas mensais (€)",
        min_value=0,
        value=70
    )

    renda = max(0, renda - ajuda_pais_renda)


    gastos = {
        "Renda": renda,
        "Alimentação": alimentacao,
        "Transportes": transportes,
        "Lazer": lazer,
        "Outros": outros,
        "Propinas": propinas
    }

    st.markdown("### 📌 Avisos")
    for categoria, media in MEDIAS.items():
        valor = gastos.get(categoria, 0)
        if valor > media:
            st.warning(
                f"{categoria}: gasto acima da média ({valor}€ vs {media}€)"
            )
    st.success("Avança para a TAB 📊 Resultado Final assim que terminares de preencher esta.")



# =====================================================
# TAB 3 — RESULTADO FINAL
# =====================================================
with tab3:
    st.subheader("📊 Resultado Final")

    gastos_mensais = sum(gastos.values())
    rendimento_total = rendimento_part_time + ajuda_pais
    poupanca_mensal = rendimento_total - gastos_mensais

    meses = anos_faculdade * 12
    patrimonio_final = poupanca_mensal * meses

    st.markdown("### 🔢 O teu número mágico")

    if poupanca_mensal <= 0:
        st.error(
            f"Com estas condições, não estás a poupar mensalmente. Perdes {-poupanca_mensal} mensalmente. "
            "Pequenos ajustes fazem uma grande diferença."
        )
    else:
        st.success(
            f"👉 Poupança mensal estimada: **{poupanca_mensal:.0f}€**"
        )
        st.success(
            f"🎯 Património estimado no fim da faculdade: **{patrimonio_final:,.0f}€**"
        )

    # -----------------------------
    # PIE CHART
    # -----------------------------
    st.markdown("### 🥧 Distribuição dos Gastos")
    st.caption(
    "Este gráfico mostra para onde vai o teu dinheiro todos os meses. "
    "Pequenos desvios aqui têm impacto enorme ao longo de vários anos."
    )

    fig = plot_gastos_pie(gastos)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados suficientes para mostrar o gráfico.")


    # -----------------------------
    # SIMULAÇÃO EXTRA — PART-TIME HIPOTÉTICO
    # -----------------------------
    if not tem_part_time:
        st.markdown("### 🔁 E se tivesses um part-time de 500€?")

        poupanca_alt = (500 + ajuda_pais) - gastos_mensais
        patrimonio_alt = poupanca_alt * meses

        if poupanca_alt > 0:
            st.success(
                f"💼 Com part-time de 500€, terminarias com **{patrimonio_alt:,.0f}€**"
            )
        else:
            st.warning(
                "Mesmo com um part-time de 500€, os gastos continuam demasiado elevados."
            )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption(
    "Esta simulação é educativa. Não substitui planeamento financeiro personalizado."
)
