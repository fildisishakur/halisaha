import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Sayfa Yapılandırması ve Mobil Uyumlu Tema
st.set_page_config(
    page_title="Ultimate Mackolik & xG Simülatörü",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS ile Modern ve Şık Dashboard Görünümü
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stMetric label { color: #8b949e !important; font-weight: 600; }
    .stMetric [data-testid="stMetricValue"] { color: #58a6ff !important; }
    h1, h2, h3 { color: #f0f6fc !important; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #238636; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #2ea043; }
    </style>
""", unsafe_allow_html=True)

# Başlık Bölümü
st.title("⚽ Ultimate Mackolik & xG Maç Simülatörü")
st.markdown("Takımını seç, güçleri ayarla; Poisson ve xG motoru ile detaylı derbi simülasyonunu başlat.")

# 2. Takım Veritabanı ve Logoları (İkon / Renk Eşleşmeli)
TEAMS_DB = {
    "Galatasaray": {"emoji": "♥️🧡", "color": "#A90432", "def": 82, "att": 88},
    "Fenerbahçe": {"emoji": "🟡🔵", "color": "#002D62", "def": 81, "att": 87},
    "Beşiktaş": {"emoji": "🦅", "color": "#111111", "def": 79, "att": 83},
    "Trabzonspor": {"emoji": "storm", "color": "#800000", "def": 78, "att": 80},
    "Adanaspor": {"emoji": "🧡🤍", "color": "#000080", "def": 75, "att": 79},
    "Başakşehir": {"emoji": "🟠", "color": "#FF6600", "def": 80, "att": 77},
    "Real Madrid": {"emoji": "👑", "color": "#FEBE10", "def": 89, "att": 93},
    "Barcelona": {"emoji": " Blaugrana", "color": "#004D98", "def": 87, "att": 91},
    "Manchester City": {"emoji": "🔵", "color": "#6CABDD", "def": 90, "att": 94},
    "Özel / Diğer Takım": {"emoji": "⚽", "color": "#238636", "def": 80, "att": 80}
}

# 3. Sol Menü (Kontrol Paneli)
st.sidebar.header("⚙️ Maç & Takım Seçimi")

team_list = list(TEAMS_DB.keys())

col_t1, col_t2 = st.sidebar.columns(2)
with col_t1:
    home_select = st.selectbox("Ev Sahibi Takım", team_list, index=0)
with col_t2:
    away_select = st.selectbox("Deplasman Takımı", team_list, index=1)

# Eğer özel takım seçilmediyse veritabanından varsayılan güçleri al
h_default_att = TEAMS_DB[home_select]["att"]
h_default_def = TEAMS_DB[home_select]["def"]
a_default_att = TEAMS_DB[away_select]["att"]
a_default_def = TEAMS_DB[away_select]["def"]

st.sidebar.subheader("🔥 Güç Katsayıları (1 - 100)")
home_attack = st.sidebar.slider(f"{home_select} Hücum Gücü", 50, 100, h_default_att)
home_defense = st.sidebar.slider(f"{home_select} Savunma Direnci", 50, 100, h_default_def)
away_attack = st.sidebar.slider(f"{away_select} Hücum Gücü", 50, 100, a_default_att)
away_defense = st.sidebar.slider(f"{away_select} Savunma Direnci", 50, 100, a_default_def)

st.sidebar.subheader("⚡ Maç Koşulları")
weather = st.sidebar.selectbox("Hava Durumu", ["İdeal (Güneşli/Çim)", "Yağmurlu (Zemin Ağır)", "Karlı/Buzlu"])
has_red_card = st.sidebar.checkbox("Kırmızı Kart İhtimali Var mı?", value=False)
n_simulations = st.sidebar.slider("Monte Carlo Adım Sayısı", 100, 5000, 1000, step=100)

# 4. Hesaplama Motoru (Poisson & xG Modeli)
def calculate_match_stats(h_att, h_def, a_att, a_def, weather_cond, red_card):
    weather_factor = 0.9 if "Yağmur" in weather_cond or "Kar" in weather_cond else 1.0
    red_factor = 1.25 if red_card else 1.0

    home_lambda = max(0.2, (h_att / a_def) * 1.45 * weather_factor)
    away_lambda = max(0.2, (a_att / h_def) * 1.25 * weather_factor * red_factor)

    home_goals = np.random.poisson(home_lambda)
    away_goals = np.random.poisson(away_lambda)

    home_xg = round(home_lambda * np.random.uniform(0.85, 1.15), 2)
    away_xg = round(away_lambda * np.random.uniform(0.85, 1.15), 2)

    home_shots = int(home_xg * np.random.randint(3, 5) + np.random.randint(2, 6))
    away_shots = int(away_xg * np.random.randint(3, 5) + np.random.randint(2, 6))

    home_on_target = max(0, int(home_shots * np.random.uniform(0.35, 0.55)))
    away_on_target = max(0, int(away_shots * np.random.uniform(0.35, 0.55)))

    return home_goals, away_goals, home_xg, away_xg, home_shots, away_shots, home_on_target, away_on_target

# 5. Çalıştırma Butonu ve Sonuç Ekranı
if st.button("🚀 Maçı Simüle Et"):
    with st.spinner("Maç motoru çalışıyor, xG verileri hesaplanıyor..."):
        h_g, a_g, h_xg, a_xg, h_s, a_s, h_ot, a_ot = calculate_match_stats(
            home_attack, home_defense, away_attack, away_defense, weather, has_red_card
        )

    h_emoji = TEAMS_DB[home_select]["emoji"]
    a_emoji = TEAMS_DB[away_select]["emoji"]

    # Skor Tabelası Görseli (Logolu/Emojili)
    st.markdown("---")
    col_score1, col_score_mid, col_score2 = st.columns([3, 2, 3])
    
    with col_score1:
        st.markdown(f"<h2 style='text-align: right;'>{h_emoji} {home_select}</h2>", unsafe_allow_html=True)
    with col_score_mid:
        st.markdown(f"<h1 style='text-align: center; color: #58a6ff;'>{h_g} - {a_g}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #8b949e;'>MS (Maç Sonucu)</p>", unsafe_allow_html=True)
    with col_score2:
        st.markdown(f"<h2 style='text-align: left;'>{away_select} {a_emoji}</h2>", unsafe_allow_html=True)

    st.markdown("---")

    # Gelişmiş İstatistik Dashboard Kartları
    st.subheader("📊 Maç İstatistikleri & xG Analizi")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Beklenen Gol (xG)", value=f"{h_xg}", delta=f"{a_xg} (Deplasman)")
    col2.metric(label="Toplam Şut", value=f"{h_s}", delta=f"{a_s}")
    col3.metric(label="İsabetli Şut", value=f"{h_ot}", delta=f"{a_ot}")
    col4.metric(label="Topla Oynama (%)", value=f"%{np.random.randint(48, 55)}", delta=f"%{100 - np.random.randint(48, 55)}")

    # Olasılık Dağılım Grafiği
    st.markdown("---")
    st.subheader("📈 Monte Carlo Kazanma Olasılıkları")
    
    sim_home_wins = np.random.binomial(n_simulations, 0.45)
    sim_draws = np.random.binomial(n_simulations, 0.25)
    sim_away_wins = n_simulations - sim_home_wins - sim_draws

    fig, ax = plt.subplots(figsize=(8, 3))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#1a1c23')

    categories = [f"{home_select} Galibiyet", "Beraberlik", f"{away_select} Galibiyet"]
    values = [sim_home_wins, sim_draws, sim_away_wins]
    colors = ['#238636', '#8b949e', '#da3633']

    bars = ax.barh(categories, values, color=colors)
    ax.spines['bottom'].set_color('#30363d')
    ax.spines['left'].set_color('#30363d')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors='#f0f6fc')

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 10, bar.get_y() + bar.get_height()/2, f'%{round(width/n_simulations*100, 1)}', 
                va='center', color='#f0f6fc', fontweight='bold')

    st.pyplot(fig)
