import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="DSS Laptop SAW",
    page_icon="💻",
    layout="wide"
)

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("dataset_laptop.csv")

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("⚙️ DSS Configuration")

w_harga = st.sidebar.slider("Bobot Harga", 0.0, 1.0, 0.30)
w_ram = st.sidebar.slider("Bobot RAM", 0.0, 1.0, 0.20)
w_cpu = st.sidebar.slider("Bobot CPU", 0.0, 1.0, 0.25)
w_battery = st.sidebar.slider("Bobot Battery", 0.0, 1.0, 0.15)
w_berat = st.sidebar.slider("Bobot Berat", 0.0, 1.0, 0.10)

total = w_harga + w_ram + w_cpu + w_battery + w_berat

if total == 0:
    total = 1

w_harga /= total
w_ram /= total
w_cpu /= total
w_battery /= total
w_berat /= total

# ==========================
# NORMALISASI SAW
# ==========================

norm = pd.DataFrame()

# Cost
norm["Harga"] = df["Harga"].min() / df["Harga"]
norm["Berat"] = df["Berat"].min() / df["Berat"]

# Benefit
norm["RAM"] = df["RAM"] / df["RAM"].max()
norm["CPU_Score"] = df["CPU_Score"] / df["CPU_Score"].max()
norm["Battery_Hour"] = df["Battery_Hour"] / df["Battery_Hour"].max()

# ==========================
# HITUNG SKOR SAW
# ==========================

df["Skor_SAW"] = (
    norm["Harga"] * w_harga +
    norm["RAM"] * w_ram +
    norm["CPU_Score"] * w_cpu +
    norm["Battery_Hour"] * w_battery +
    norm["Berat"] * w_berat
)

ranking = df.sort_values(
    by="Skor_SAW",
    ascending=False
).reset_index(drop=True)

ranking["Ranking"] = ranking.index + 1

best = ranking.iloc[0]

# ==========================
# HEADER
# ==========================

st.title("💻 DSS Pemilihan Laptop")
st.subheader("Metode SAW (Simple Additive Weighting)")

# ==========================
# KPI
# ==========================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Jumlah Laptop", len(ranking))
c2.metric("Laptop Terbaik", best["Laptop"])
c3.metric("RAM Maksimum", f"{ranking['RAM'].max()} GB")
c4.metric("Harga Termurah", f"Rp {ranking['Harga'].min():,}")

# ==========================
# TOP 10
# ==========================

st.subheader("🏆 Top 10 Laptop")

top10 = ranking.head(10)

fig = px.bar(
    top10,
    x="Laptop",
    y="Skor_SAW",
    color="Skor_SAW",
    title="Top 10 Ranking Laptop"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# RANKING
# ==========================

st.subheader("📊 Hasil Ranking")

st.dataframe(
    ranking[
        [
            "Ranking",
            "Laptop",
            "Harga",
            "RAM",
            "CPU_Score",
            "Battery_Hour",
            "Berat",
            "Skor_SAW"
        ]
    ],
    use_container_width=True
)

# ==========================
# VISUALISASI
# ==========================

col1, col2 = st.columns(2)

with col1:
    fig2 = px.histogram(
        ranking,
        x="Harga",
        title="Distribusi Harga"
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.histogram(
        ranking,
        x="RAM",
        title="Distribusi RAM"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ==========================
# KESIMPULAN
# ==========================

st.subheader("📄 Kesimpulan")

st.success(
    f"Laptop terbaik adalah {best['Laptop']} dengan skor SAW {best['Skor_SAW']:.4f}"
)
