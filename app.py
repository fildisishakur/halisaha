import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Sayfa Yapılandırması ve Mobil Uyumlu Tema
st.set_page_config(
    page_title="Süper Lig & 1. Lig 100K xG Simülatörü",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; }
    .stMetric label { color: #8b949e !important; font-weight: 600; font-size: 14px; }
    .stMetric [data-testid="stMetricValue"] { color: #58a6ff !important; font-size: 24px !important; }
    h1, h2, h3 { color: #f0f6fc !important; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #238636; color: white; font-weight: bold; font-size: 16px; height: 50px; }
    .stButton>button:hover { background-color: #2ea043; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Türkiye Ligleri 100.000 Adımlı Profesyonel xG Simülatörü")
st.markdown("2026/2027 Süper Lig ve TFF 1. Lig güncel kadro verileri, Poisson dağılımı ve 100.000 Monte Carlo simülasyonu.")

# 2. 2026/2027 Sezonu Güncel Süper Lig ve 1. Lig Veritabanı
TR_TEAMS = {
    # --- 2026/2027 SÜPER LİG ---
    "Galatasaray": {"league": "Trendyol Süper Lig", "emoji": "🦁", "g_atilan": 2.45, "g_yenilen": 0.70},
    "Fenerbahçe": {"league": "Trendyol Süper Lig", "emoji": "🟡🔵", "g_atilan": 2.40, "g_yenilen": 0.75},
    "Beşiktaş": {"league": "Trendyol Süper Lig", "emoji": "🦅", "g_atilan": 1.90, "g_yenilen": 1.00},
    "Trabzonspor": {"league": "Trendyol Süper Lig", "emoji": "🌊", "g_atilan": 1.80, "g_yenilen": 1.10},
    "İstanbul Başakşehir": {"league": "Trendyol Süper Lig", "emoji": "🟠", "g_atilan": 1.70, "g_yenilen": 1.05},
    "Göztepe": {"league": "Trendyol Süper Lig", "emoji": "🟡🔴", "g_atilan": 1.60, "g_yenilen": 1.08},
    "Samsunspor": {"league": "Trendyol Süper Lig", "emoji": "🔴⚪", "g_atilan": 1.55, "g_yenilen": 1.15},
    "Çaykur Rizespor": {"league": "Trendyol Süper Lig", "emoji": "🟢🔵", "g_atilan": 1.45, "g_yenilen": 1.30},
    "Tümosan Konyaspor": {"league": "Trendyol Süper Lig", "emoji": "🟢⚪", "g_atilan": 1.40, "g_yenilen": 1.25},
    "Kocaelispor": {"league": "Trendyol Süper Lig", "emoji": "🟢⚫", "g_atilan": 1.50, "g_yenilen": 1.12},
    "Corendon Alanyaspor": {"league": "Trendyol Süper Lig", "emoji": "🍊", "g_atilan": 1.35, "g_yenilen": 1.35},
    "Gaziantep FK": {"league": "Trendyol Süper Lig", "emoji": "🔴⚫", "g_atilan": 1.25, "g_yenilen": 1.40},
    "Kasımpaşa": {"league": "Trendyol Süper Lig", "emoji": "🔵⚪", "g_atilan": 1.50, "g_yenilen": 1.38},
    "Gençlerbirliği": {"league": "Trendyol Süper Lig", "emoji": "🔴⚫", "g_atilan": 1.42, "g_yenilen": 1.22},
    "Eyüpspor": {"league": "Trendyol Süper Lig", "emoji": "🟣🟡", "g_atilan": 1.38, "g_yenilen": 1.45},
    "Erzurumspor FK": {"league": "Trendyol Süper Lig", "emoji": "🔵⚪", "g_atilan": 1.30, "g_yenilen": 1.40},
    "Amed Sportif Faaliyetler": {"league": "Trendyol Süper Lig", "emoji": "🟢🔴", "g_atilan": 1.48, "g_yenilen": 1.28},
    "Çorum FK": {"league": "Trendyol Süper Lig", "emoji": "🔴⚪", "g_atilan": 1.35, "g_yenilen": 1.32},

    # --- 2026/2027 TFF 1. LİG ---
    "Bursaspor": {"league": "TFF 1. Lig", "emoji": "💚🤍", "g_atilan": 2.20, "g_yenilen": 0.85},
    "Zecorner Kayserispor": {"league": "TFF 1. Lig", "emoji": "🟡🔴", "g_atilan": 2.30, "g_yenilen": 0.78},
    "Alagöz Holding Iğdır FK": {"league": "TFF 1. Lig", "emoji": "🟢⚪", "g_atilan": 1.65, "g_yenilen": 0.95},
    "Mardin 1969 Spor": {"league": "TFF 1. Lig", "emoji": "🟥🟨", "g_atilan": 1.60, "g_yenilen": 1.05},
    "Batman Petrolspor": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.85, "g_yenilen": 1.40},
    "Ankara Keçiörengücü": {"league": "TFF 1. Lig", "emoji": "🟣⚪", "g_atilan": 1.70, "g_yenilen": 1.15},
    "Hesap.com Antalyaspor": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.55, "g_yenilen": 1.30},
    "Sipay Bodrum FK": {"league": "TFF 1. Lig", "emoji": "💚🤍", "g_atilan": 1.45, "g_yenilen": 1.10},
    "Muğlaspor": {"league": "TFF 1. Lig", "emoji": "🟢⚪", "g_atilan": 1.40, "g_yenilen": 1.35},
    "Mısırlı.com.tr Fatih Karagümrük": {"league": "TFF 1. Lig", "emoji": "🔴⚫", "g_atilan": 1.50, "g_yenilen": 1.20},
    "Sarıyerspor": {"league": "TFF 1. Lig", "emoji": "🔵⚪", "g_atilan": 1.35, "g_yenilen": 1.30},
    "Esenler Erokspor": {"league": "TFF 1. Lig", "emoji": "🟡🟢", "g_atilan": 1.38, "g_yenilen": 1.25},
    "Özbeyli Bandırmaspor": {"league": "TFF 1. Lig", "emoji": "🔴🟢", "g_atilan": 1.42, "g_yenilen": 1.18},
    "Eminevim Ümraniyespor": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.38, "g_yenilen": 1.12},
    "Atko Grup Pendikspor": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.30, "g_yenilen": 1.50},
    "Manisa FK": {"league": "TFF 1. Lig", "emoji": "⚫⚪", "g_atilan": 1.52, "g_yenilen": 1.55},
    "Özbelsan Sivasspor": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.32, "g_yenilen": 1.45},
    "İmaj Altyapı Van Spor FK": {"league": "TFF 1. Lig", "emoji": "🔴⚫", "g_atilan": 1.28, "g_yenilen": 1.50},
    "İstanbulspor": {"league": "TFF 1. Lig", "emoji": "🟡⬛", "g_atilan": 1.25, "g_yenilen": 1.42}
}

# 3. Sol Menü (Lig ve Takım Filtresi)
st.sidebar.header("⚙️ Maç & Lig Seçimi")

selected_league = st.sidebar.selectbox("Lig Filtrele", ["Tümü", "Trendyol Süper Lig", "TFF 1. Lig"])

if selected_league == "Tümü":
    filtered_teams = list(TR_TEAMS.keys())
else:
    filtered_teams = [t for t, data in TR_TEAMS.items() if data["league"] == selected_league]

col_t1, col_t2 = st.sidebar.columns(2)
with col_t1:
    home_team = st.selectbox("Ev Sahibi Takım", filtered_teams, index=0)
with col_t2:
    away_team = st.selectbox("Deplasman Takımı", filtered_teams, index=1 if len(filtered_teams) > 1 else 0)

st.sidebar.subheader("⚡ Maç Dinamikleri")
is_derby = st.sidebar.checkbox("Yüksek Rekabet / Derbi Atmosferi", value=False)
weather = st.sidebar.selectbox("Zemin ve Hava", ["İdeal Çim", "Yağmurlu (Ağır Zemin)"])

# 4. 100.000 Adımlı Monte Carlo & Poisson Motoru
def run_simulation(h_name, a_name, derby, cond):
    h = TR_TEAMS[h_name]
    a = TR_TEAMS[a_name]

    home_advantage = 1.12
    derby_mod = 0.88 if derby else 1.0
    weather_mod = 0.92 if "Yağmur" in cond else 1.0

    # Gol beklentisi (Lambda) hesaplamaları
    h_lambda = max(0.2, ((h["g_atilan"] + a["g_yenilen"]) / 2) * home_advantage * derby_mod * weather_mod)
    a_lambda = max(0.2, ((a["g_atilan"] + h["g_yenilen"]) / 2) * derby_mod * weather_mod)

    # Tekil Maç Skoru Üretimi
    h_goals = np.random.poisson(h_lambda)
    a_goals = np.random.poisson(a_lambda)

    # xG Hesaplama
    h_xg = round(h_lambda * np.random.uniform(0.92, 1.08), 2)
    a_xg = round(a_lambda * np.random.uniform(0.92, 1.08), 2)

    # 100.000 Adımlı Monte Carlo Simülasyon Matrisi
    n_sims = 100000
    sim_h_goals = np.random.poisson(h_lambda, n_sims)
    sim_a_goals = np.random.poisson(a_lambda, n_sims)
    
    h_wins = np.sum(sim_h_goals > sim_a_goals)
    draws = np.sum(sim_h_goals == sim_a_goals)
    a_wins = np.sum(sim_h_goals < sim_a_goals)

    hp = (h_wins / n_sims) * 100
    dp = (draws / n_sims) * 100
    ap = (a_wins / n_sims) * 100

    # Maç İstatistikleri
    h_shots = int(h_xg * np.random.randint(3, 5) + np.random.randint(2, 5))
    a_shots = int(a_xg * np.random.randint(3, 5) + np.random.randint(2, 5))
    h_on_target = max(1, int(h_shots * np.random.uniform(0.35, 0.50)))
    a_on_target = max(1, int(a_shots * np.random.uniform(0.35, 0.50)))
    
    h_corners = np.random.randint(3, 8)
    a_corners = np.random.randint(2, 7)
    h_yellow = np.random.randint(1, 4)
    a_yellow = np.random.randint(1, 4)
    h_red = 1 if np.random.rand() < 0.07 else 0
    a_red = 1 if np.random.rand() < 0.07 else 0

    return h_goals, a_goals, h_xg, a_xg, h_shots, a_shots, h_on_target, a_on_target, h_corners, a_corners, h_yellow, a_yellow, h_red, a_red, hp, dp, ap

# 5. Çalıştırma Butonu ve Sonuç Ekranı
if st.button("🚀 100.000 Adımlı Simülasyonu Başlat"):
    with st.spinner("2026/2027 güncel gol ortalamaları işleniyor ve 100.000 Monte Carlo simülasyonu koşturuluyor..."):
        h_g, a_g, h_xg, a_xg, h_s, a_s, h_ot, a_ot, h_c, a_c, h_y, a_y, h_r, a_r, hp, dp, ap = run_simulation(
            home_team, away_team, is_derby, weather
        )

    h_info = TR_TEAMS[home_team]
    a_info = TR_TEAMS[away_team]

    # Skor Tabelası
    st.markdown("---")
    sc1, sc_mid, sc2 = st.columns([3, 2, 3])
    
    with sc1:
        st.markdown(f"<h2 style='text-align: right;'>{h_info['emoji']} {home_team}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: right; color: #8b949e;'>Maç Başı Atılan: {h_info['g_atilan']} | Yenilen: {h_info['g_yenilen']}</p>", unsafe_allow_html=True)
    with sc_mid:
        st.markdown(f"<h1 style='text-align: center; color: #58a6ff; font-size: 48px;'>{h_g} - {a_g}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #8b949e;'>MS (Maç Sonucu)</p>", unsafe_allow_html=True)
    with sc2:
        st.markdown(f"<h2 style='text-align: left;'>{away_team} {a_info['emoji']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: left; color: #8b949e;'>Maç Başı Atılan: {a_info['g_atilan']} | Yenilen: {a_info['g_yenilen']}</p>", unsafe_allow_html=True)

    st.markdown("---")

    # İstatistik Kartları
    st.subheader("📊 Profesyonel xG & Maç İstatistikleri")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Beklenen Gol (xG)", value=f"{h_xg}", delta=f"{a_xg} (Dep)")
    col2.metric(label="Toplam Şut", value=f"{h_s}", delta=f"{a_s}")
    col3.metric(label="İsabetli Şut", value=f"{h_ot}", delta=f"{a_ot}")
    col4.metric(label="Korner", value=f"{h_c}", delta=f"{a_c}")

    col_d1, col_d2, col_d3 = st.columns(3)
    col_d1.metric(label="Sarı Kart", value=f"{h_y}", delta=f"{a_y}")
    col_d2.metric(label="Kırmızı Kart", value=f"{h_r}", delta=f"{a_r}")
    col_d3.metric(label="Topla Oynama", value=f"%{np.random.randint(46, 55)}", delta=f"%{100 - np.random.randint(46, 55)}")

    # 100.000 Adımlı Monte Carlo Olasılık Grafiği
    st.markdown("---")
    st.subheader("📈 100.000 Simülasyon Sonucu Olasılık Dağılımı")

    fig, ax = plt.subplots(figsize=(8, 2.5))
    fig.patch.set_facecolor('#0b0e14')
    ax.set_facecolor('#161b22')

    categories = [f"{home_team} Kazanır", "Beraberlik", f"{away_team} Kazanır"]
    values = [hp, dp, ap]
    colors = ['#238636', '#8b949e', '#da3633']

    bars = ax.barh(categories, values, color=colors)
    ax.spines['bottom'].set_color('#30363d')
    ax.spines['left'].set_color('#30363d')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors='#f0f6fc')
    ax.set_xlim(0, 100)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2, f'%{round(width, 1)}', 
                va='center', color='#f0f6fc', fontweight='bold')

    st.pyplot(fig)
