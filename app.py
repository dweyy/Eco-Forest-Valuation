import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ================= SIDEBAR PROFIL =================
st.sidebar.markdown("## 🌿 Eco-Forest System")

st.sidebar.image("mangrove.jpg", use_container_width=True)

st.sidebar.markdown("### 👥 Anggota Kelompok")
st.sidebar.markdown("""
- Dwirani Salfatihah (10090224009)  
- Nazwa Aprilia Putri (10090224015)  
- Annisa Tri Lestari (10090224019)
""")

st.sidebar.markdown("### 👨‍🏫 Dosen Pengampu")
st.sidebar.info("Yuhka Sundaya")

st.sidebar.divider()

df = pd.read_excel("data.xlsx")
df.columns = df.columns.str.strip()

def get_value(name):
    return df[df["variabel"] == name]["nilai"].values[0]

if "carbon_price" not in st.session_state:
    st.session_state["carbon_price"] = int(get_value("carbon_price"))

st.set_page_config(
    page_title="Eco-Forest Valuation System",
    page_icon="🌿",
    layout="wide"
)

carbon_default = int(get_value("carbon_price"))

st.title("Eco-Forest Valuation")

menu = st.sidebar.selectbox(
    "Pilih Modul",
    ["Home", "TEV Calculator", "Trade-off Analysis", "PES Policy", "Evaluasi"]
)

if menu == "TEV Calculator":

    st.sidebar.header("Input Ekosistem")

    luas_input = st.sidebar.slider("Luas Mangrove", 1, 1000, 200)
    density = st.sidebar.slider("Kerapatan Vegetasi", 1, 10, 5)
    carbon_price = st.sidebar.slider("Harga Karbon", 100, 1000, 500)
    

# ================= HOME =================
if menu == "Home":
    st.title("🌿 Eco-Forest Valuation System")

    st.markdown("""
    ### 📘 Deskripsi Sistem
    Sistem ini memodelkan valuasi ekonomi ekosistem mangrove menggunakan pendekatan:

    - Total Economic Value (TEV)
    - Trade-off Analysis
    - Ecosystem Services Valuation
    - Opportunity Cost Framework
    """)

    col1, col2, col3 = st.columns(3)

    col1.metric("Model", "TEV Based")
    col2.metric("Ekosistem", "Mangrove")
    col3.metric("Pendekatan", "Economics + Ecology")

    st.divider()
    st.dataframe(df)
    st.info("Model berbasis Environmental Economics: TEV + Opportunity Cost + Ecosystem Services")
# ================= TEV =================
elif menu == "TEV Calculator":

    st.header("Modul 1: TEV")

    st.dataframe(df)
    st.info("""
Model TEV terdiri dari:
- Direct Use Value (perikanan, kayu, wisata)
- Indirect Use Value (perlindungan pesisir, karbon)
- Option Value (15%)
- Existence Value (25%)

Referensi: MEA (2005), Tietenberg (Environmental Economics)
""")

    # ================= BASE VALUE =================
    fisheries_base = get_value("fisheries_value")
    timber_base = get_value("timber_value")
    ecotourism_base = get_value("ecotourism_value")
    coastal_base = get_value("coastal_protection")
    carbon_seq = get_value("carbon_sequestration")

    # ================= MODEL EKONOMI INTERAKTIF =================

    scale_factor = luas_input * (density / 5)

    provisioning = (fisheries_base + timber_base + ecotourism_base) * scale_factor
    regulating = (coastal_base + (carbon_seq * carbon_price * luas_input)) * scale_factor
    cultural = ecotourism_base * scale_factor
    supporting = carbon_seq * luas_input * density

    direct_use = provisioning
    indirect_use = regulating

    option_value = 0.15 * (direct_use + indirect_use)
    existence_value = 0.25 * (direct_use + indirect_use)

    tev_total = direct_use + indirect_use + option_value + existence_value

    st.subheader("🧮 Kalkulator Total Economic Value (TEV)")
    st.caption("Input parameter → hasil valuasi ekonomi ekosistem")

    st.write("Direct Use Value:", direct_use)
    st.write("Indirect Use Value:", indirect_use)
    st.write("Option Value (15%):", option_value)
    st.write("Existence Value (25%):", existence_value)

    st.success(f"TOTAL ECONOMIC VALUE (TEV): {tev_total}")
    st.metric("Nilai Ekonomi per Hektar", tev_total / luas_input)
    st.metric("Nilai Karbon Ekosistem", carbon_seq * luas_input * carbon_price)
    st.subheader("📘 Landasan Teori")

    st.markdown("""
Model ini menggunakan pendekatan:
- MEA (2005)
- Tietenberg Environmental Economics

Klasifikasi:
- Provisioning Services
- Regulating Services
- Option Value
- Existence Value
""")
    st.subheader("📌 Interpretasi Ekonomi")

    st.info("""
Ekosistem mangrove tidak hanya bernilai dari hasil eksploitasi langsung,
tetapi juga dari fungsi ekologis yang tidak dipasarkan.

Hal ini menunjukkan adanya market failure berupa eksternalitas positif.
""")
    
    st.subheader("📥 Parameter Ekosistem (Base Data)")

    st.write("Fisheries Base:", fisheries_base)
    st.write("Timber Base:", timber_base)
    st.write("Ecotourism Base:", ecotourism_base)
    st.write("Coastal Protection:", coastal_base)
    st.write("Carbon Sequestration:", carbon_seq)
    st.write("Luas Input:", luas_input)
    st.write("Harga Karbon:", carbon_price)
    st.write("Density Index:", density)

    data_chart = {
    "Kategori": [
        "Provisioning",
        "Regulating",
        "Option Value",
        "Existence Value"
    ],
    "Nilai": [
        provisioning,
        regulating,
        option_value,
        existence_value
    ]
}

    fig = px.pie(
        data_chart,
        names="Kategori",
        values="Nilai",
        title="Komposisi TEV"
    )

    st.plotly_chart(fig, use_container_width=True, key="pie_tev")
    st.caption("Model: Total Economic Value (TEV) berbasis Ecosystem Service Valuation – Tietenberg Framework")
    st.info("""
Kalkulator ini menggunakan pendekatan:
- Ecosystem Service Valuation
- Ecological scaling function (luas × density)
- Carbon pricing model
- TEV framework (MEA 2005)
""")

elif menu == "Trade-off Analysis":
    st.header("Modul 2: Trade-off Analysis")
    st.sidebar.subheader("Parameter Trade-off")

    # ================= INPUT PARAMETER =================
    conversion_rate = st.sidebar.slider("Tingkat Konversi Lahan (%)", 0, 100, 50)
    discount_factor = st.sidebar.slider("Discount Factor", 0.0, 1.0, 0.95)
    time_adjustment = discount_factor  # simplifikasi PV proxy

    carbon_price = st.sidebar.slider( 
    "Harga Karbon (USD/ton)", 100, 1000, 
    st.session_state.get("carbon_price", 500) 
    )

    # ================= ECOLOGICAL STATE =================
    remaining_forest = 100 - conversion_rate
    ecological_health = ((remaining_forest / 100) ** 2)

    # ================= DATA INPUT =================
    fisheries = get_value("fisheries_value")
    timber = get_value("timber_value")
    ecotourism = get_value("ecotourism_value")
    coastal = get_value("coastal_protection")
    carbon_seq = get_value("carbon_sequestration")
    luas = get_value("luas_mangrove")

    # ================= ECONOMIC VALUE =================
    carbon_value = carbon_seq * carbon_price * luas

    mangrove_benefit = (
    fisheries + timber + ecotourism + coastal + carbon_value
) * ecological_health * time_adjustment

    private_gain = get_value("aquaculture_cost") * (conversion_rate / 100)

    environmental_damage = (1 - ecological_health) * 500000  # proxy ecological cost

    aquaculture_benefit = private_gain - environmental_damage
    net_benefit_mangrove = mangrove_benefit
    net_benefit_conversion = aquaculture_benefit
    max_value = mangrove_benefit / max(ecological_health, 0.01)

    tradeoff = net_benefit_mangrove - net_benefit_conversion

    loss_if_convert = mangrove_benefit - aquaculture_benefit
    opportunity_cost = mangrove_benefit

    # ================= POLICY SCENARIO =================
    tev_no_regulation = mangrove_benefit

    pes_rate = 1000  # bisa juga dijadikan slider nanti
    pes_payment = ecological_health * pes_rate * luas

    tev_regulation = mangrove_benefit * (1 + (1 - ecological_health) * 0.3) + pes_payment
    damage_reduction = mangrove_benefit * (1 - ecological_health) * 0.25
    tev_regulation += damage_reduction

    # ================= OUTPUT =================
    st.subheader("Hasil Trade-off")
    st.write("Sisa Hutan (%):", remaining_forest)
    st.write("Kesehatan Ekosistem:", ecological_health)

    st.write("Nilai Mangrove:", mangrove_benefit)
    st.write("Nilai Aquaculture:", aquaculture_benefit)
    st.success(f"Kerugian Ekosistem: {loss_if_convert}")

    st.write("Opportunity Cost:", opportunity_cost)
    st.success(f"Net Trade-off: {tradeoff}")

    # ================= SAVE TO SESSION STATE =================
    st.session_state["conversion_rate"] = conversion_rate
    st.session_state["ecological_health"] = ecological_health
    st.session_state["luas"] = luas
    st.session_state["mangrove_benefit"] = mangrove_benefit

    # ================= POLICY COMPARISON =================
    st.subheader("📊 Perbandingan Skenario Kebijakan")

    st.write("TEV Tanpa Regulasi:", tev_no_regulation)
    st.write("TEV Dengan Regulasi:", tev_regulation)

    if tev_regulation > tev_no_regulation:
        st.success("Regulasi meningkatkan nilai ekonomi total dengan menekan degradasi ekosistem.")
    else:
        st.warning("Tanpa regulasi lebih tinggi jangka pendek, tetapi tidak sustainable.")

    fig_policy = go.Figure()
    fig_policy.update_layout(yaxis_range=[0, max(tev_no_regulation, tev_regulation) * 1.2])

    fig_policy.add_trace(go.Bar(
        name="No Regulation",
        x=["TEV Scenario"],
        y=[tev_no_regulation]
    ))

    fig_policy.add_trace(go.Bar(
        name="Regulation",
        x=["TEV Scenario"],
        y=[tev_regulation]
    ))

    fig_policy.update_layout(
        title="Comparison: Regulation vs No Regulation",
        barmode='group'
    )

    st.plotly_chart(fig_policy, use_container_width=True, key="policy_comparison")

    # ================= DEGRADATION CURVE =================
    import numpy as np

    x = np.linspace(0, 100, 100)

    ecological_curve = max_value * ((100 - x) / 100) ** 2
    aquaculture_curve = (x / 100) ** 1.2 * max_value

    diff = np.abs(ecological_curve - aquaculture_curve)
    break_even_point = x[np.argmin(diff)]

    st.subheader("📍 Break-even Point")
    st.info(f"Titik keseimbangan terjadi pada konversi sekitar {break_even_point:.2f}%")

    # ===== CHART =====
    fig_curve = go.Figure()

    fig_curve.add_trace(go.Scatter(
        x=x,
        y=ecological_curve,
        mode="lines",
        name="Ecological Health"
    ))

    fig_curve.add_trace(go.Scatter(
        x=x,
        y=aquaculture_curve,
        mode="lines",
        name="Opportunity Value"
    ))

    fig_curve.update_layout(
        title="Ecological Degradation Curve",
        xaxis_title="Konversi Lahan (%)",
        yaxis_title="Kesehatan Ekosistem" )

    st.plotly_chart(fig_curve, use_container_width=True, key="degradation_curve")

    # ================= INTERPRETASI =================
    st.subheader("📌 Interpretasi Ekonomi")

    st.info("""
Model menunjukkan hubungan non-linear antara intensitas konversi lahan dan penurunan kualitas ekosistem,
yang berdampak pada penurunan Total Economic Value melalui mekanisme ecological degradation function.
""") 
    st.info("""
Break-even point menunjukkan kondisi dimana
marginal benefit konversi = marginal cost kehilangan ekosistem.
""")

    if mangrove_benefit > aquaculture_benefit:
        st.success("Konservasi lebih optimal secara ekonomi jangka panjang karena adanya positive externality.")
    else:
        st.warning("Konversi memberikan keuntungan jangka pendek namun meningkatkan risiko ecological loss.")

# ================= PES POLICY MODULE =================
elif menu == "PES Policy":
    st.header("Modul 3: Kebijakan PES")

    import numpy as np

    # ================= INPUT =================
    pes_rate = st.sidebar.slider(
        "Insentif PES (USD per hektar)",
        100,
        5000,
        1000,
        key="pes_rate"
    )

    conversion_rate = st.session_state.get("conversion_rate", 50)
    ecological_health = st.session_state.get("ecological_health", 0.5)
    luas = st.session_state.get("luas", get_value("luas_mangrove"))

    # ================= BASE VALUE =================
    fisheries = get_value("fisheries_value")
    timber = get_value("timber_value")
    ecotourism = get_value("ecotourism_value")
    coastal = get_value("coastal_protection")
    carbon_seq = get_value("carbon_sequestration")

    mangrove_benefit = (
        fisheries + timber + ecotourism + coastal + (carbon_seq * luas)
    )

    # ================= PES MODEL =================
    base_pes = pes_rate * luas
    adjusted_pes = base_pes * ecological_health

    # ================= OPPORTUNITY COST =================
    conversion_pressure = conversion_rate / 100
    ecological_risk = (1 - ecological_health)

    opportunity_cost = mangrove_benefit * conversion_pressure * ecological_risk

    # ================= NET SOCIAL VALUE =================
    net_social_value = adjusted_pes - opportunity_cost
    net_social_value = max(net_social_value, -0.3 * opportunity_cost)

    # ================= BREAK-EVEN =================
    break_even_pes_per_ha = opportunity_cost / (luas + 1e-6)
    adjusted_pes_per_ha = adjusted_pes / (luas + 1e-6)

    # ================= DECISION =================
    if adjusted_pes_per_ha >= break_even_pes_per_ha:
        decision = "PES efektif: insentif menahan konversi"
    else:
        decision = "PES tidak cukup: konversi tetap terjadi"

    # ================= OUTPUT =================
    st.subheader("📊 Hasil Ekonomi PES")
    st.write("Base PES:", base_pes)
    st.write("Adjusted PES:", adjusted_pes)
    st.write("Opportunity Cost:", opportunity_cost)
    st.success(f"Net Social Value: {net_social_value}")

    st.subheader("📌 Keputusan Kebijakan")
    st.info(decision)

    st.subheader("📍 Break-even PES Level")
    st.write("Break-even per ha:", break_even_pes_per_ha)
    st.write("Adjusted PES per ha:", adjusted_pes_per_ha)

    # ================= PES EFFECTIVENESS INDEX =================
    pes_effectiveness_index = adjusted_pes_per_ha / (break_even_pes_per_ha + 1e-6)

    st.subheader("📊 PES Effectiveness Index")
    st.write(pes_effectiveness_index)

    if pes_effectiveness_index >= 1:
        st.success("PES efektif (melewati threshold ekonomi)")
    else:
        st.warning("PES belum efektif")

    # ================= OPTIMAL PES ZONE =================
    st.subheader("🎯 Optimal PES Zone")

    lower_bound = 0.8 * break_even_pes_per_ha
    upper_bound = 1.2 * break_even_pes_per_ha

    st.write("Lower bound:", lower_bound)
    st.write("Upper bound:", upper_bound)

    if lower_bound <= pes_rate <= upper_bound:
        st.success("PES berada di zona optimal kebijakan")
    elif pes_rate < lower_bound:
        st.warning("PES terlalu rendah (tidak efektif)")
    else:
        st.info("PES terlalu tinggi (inefisien fiskal)")

    # ================= THRESHOLD CURVE =================
    st.subheader("📈 Threshold Curve PES")

    x = np.linspace(0, 5000, 100)

    # 🔥 KUNCI: PES benefit HARUS fungsi dari pes_rate
    pes_slope = (pes_rate / 5000)  # normalisasi 0–1

    pes_curve = x * pes_slope * (1 + ecological_health)

    oc_level = opportunity_cost / (luas + 1e-6)
    oc_curve = np.ones_like(x) * oc_level

    # break-even dynamic
    diff = np.abs(pes_curve - oc_curve)
    idx = np.argmin(diff)
    break_even = x[idx]

    # optimal zone
    lower_bound = 0.8 * break_even
    upper_bound = 1.2 * break_even

    fig = go.Figure()

    fig.add_trace(go.Scatter(
       x=x,
      y=pes_curve,
      mode="lines",
      name="PES Benefit Curve"
))

    fig.add_trace(go.Scatter(
      x=x,
      y=oc_curve,
      mode="lines",
      name="Opportunity Cost Threshold"
))

    fig.add_vline(
      x=break_even,
      line_dash="dash",
      line_color="red",
      annotation_text="Break-even"
)

    fig.add_vrect(
      x0=lower_bound,
      x1=upper_bound,
      fillcolor="green",
      opacity=0.15,
      line_width=0
)

    fig.update_layout(
      title="Dynamic PES Threshold Curve",
      xaxis_title="PES (USD/ha)",
      yaxis_title="Economic Value"
)

    st.plotly_chart(fig, use_container_width=True)

    st.info(f"Break-even PES: {break_even:.2f} USD/ha")
    st.info(f"Optimal Zone: {lower_bound:.0f} - {upper_bound:.0f} USD/ha")
    # ================= DEBUG =================
    with st.expander("Debug Info"):
        st.write("PES Rate:", pes_rate)
        st.write("Conversion Rate:", conversion_rate)
        st.write("Ecological Health:", ecological_health)
        st.write("Break-even:", break_even_pes_per_ha)
        st.write("Effectiveness Index:", pes_effectiveness_index)

    # ================= INTERPRETASI =================
    st.subheader("📘 Interpretasi Ekonomi")
    st.info(
        "Model PES menunjukkan kondisi optimal kebijakan berbasis threshold "
        "dimana insentif harus melampaui opportunity cost untuk menghentikan konversi lahan."
    )
# ================= MODUL 4: MANGROVE BLUE CARBON (SIDEBAR VERSION) =================
elif menu == "Evaluasi":

    st.header("🌿 Modul 4: Kasus Mangrove Blue Carbon (Indonesia)")

    import numpy as np
    import plotly.graph_objects as go

    # ================= SIDEBAR INPUT =================
    st.sidebar.subheader("Parameter Kasus Mangrove")

    luas = st.sidebar.slider("Luas Mangrove (hektar)", 1, 1000, 200)
    deforestation_rate = st.sidebar.slider("Tingkat Konversi Lahan (%)", 0, 100, 30)
    carbon_price = st.sidebar.slider("Harga Karbon (USD/ton)", 100, 1000, 500)
    ecosystem_quality = st.sidebar.slider("Kualitas Ekosistem (%)", 0, 100, 80)

    # ================= MODEL =================
    def_rate = deforestation_rate / 100
    eco_factor = ecosystem_quality / 100

    carbon_stock_per_ha = 200  # ton CO2/ha (literatur standar mangrove)

    total_carbon = carbon_stock_per_ha * luas
    carbon_value = total_carbon * carbon_price

    carbon_loss = carbon_value * def_rate
    adjusted_carbon = carbon_value * eco_factor

    net_carbon_value = adjusted_carbon - carbon_loss

    # ================= OUTPUT =================
    st.subheader("📊 Hasil Valuasi Ekosistem")

    st.write("Total Carbon Value:", carbon_value)
    st.write("Kerugian Konversi:", carbon_loss)
    st.write("Nilai Karbon Tersimpan:", adjusted_carbon)

    st.success(f"Net Ecosystem Value: {net_carbon_value:.2f} USD")

    # ================= INTERPRETASI =================
    st.subheader("📌 Interpretasi Ekonomi")

    if net_carbon_value > carbon_value * 0.7:
        st.success("Ekosistem masih stabil, fungsi karbon terjaga.")
    else:
        st.warning("Degradasi tinggi, kehilangan nilai karbon signifikan.")

    # ================= VISUALISASI =================
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Initial Carbon Value",
        x=["Scenario"],
        y=[carbon_value]
    ))

    fig.add_trace(go.Bar(
        name="Net Carbon Value",
        x=["Scenario"],
        y=[net_carbon_value]
    ))

    fig.update_layout(
        title="Mangrove Blue Carbon Economic Impact",
        barmode="group",
        xaxis_title="Scenario",
        yaxis_title="Economic Value (USD)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ================= INFO =================
    st.info(
        "Model ini menunjukkan hubungan antara luas mangrove, degradasi lahan, "
        "dan nilai ekonomi karbon dalam konteks blue carbon ecosystem."
    )
