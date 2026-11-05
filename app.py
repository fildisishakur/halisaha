import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Sayfa Yapılandırması
st.set_page_config(
    page_title="Global 2026/27 Pro xG Simülatörü",
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

st.title("⚽ 2026/2027 Sezonu Eksiksiz Global xG Simülatörü")
st.markdown("Güncel kadrolar, yerel ligler, avrupa kulvarları (UCL, UEL, UECL), üstel güç katsayıları ve 100.000 Monte Carlo simülasyonu.")

# 2. 2026-2027 GÜNCEL VE EKSİKSİZ KÜRESEL VERİTABANI
GLOBAL_TEAMS = {
    # --- TRENDYOL SÜPER LİG (2026/27) ---
    "Galatasaray": {"league": "Trendyol Süper Lig", "emoji": "🦁", "g_atilan": 2.45, "g_yenilen": 0.70, "kadro_degeri": 240.0},
    "Fenerbahçe": {"league": "Trendyol Süper Lig", "emoji": "🟡🔵", "g_atilan": 2.40, "g_yenilen": 0.75, "kadro_degeri": 230.0},
    "Beşiktaş": {"league": "Trendyol Süper Lig", "emoji": "🦅", "g_atilan": 1.90, "g_yenilen": 1.00, "kadro_degeri": 155.0},
    "Trabzonspor": {"league": "Trendyol Süper Lig", "emoji": "🌊", "g_atilan": 1.80, "g_yenilen": 1.10, "kadro_degeri": 120.0},
    "İstanbul Başakşehir": {"league": "Trendyol Süper Lig", "emoji": "🟠", "g_atilan": 1.70, "g_yenilen": 1.05, "kadro_degeri": 70.0},
    "Göztepe": {"league": "Trendyol Süper Lig", "emoji": "🟡🔴", "g_atilan": 1.60, "g_yenilen": 1.08, "kadro_degeri": 50.0},
    "Samsunspor": {"league": "Trendyol Süper Lig", "emoji": "🔴⚪", "g_atilan": 1.55, "g_yenilen": 1.15, "kadro_degeri": 45.0},
    "Eyüpspor": {"league": "Trendyol Süper Lig", "emoji": "🟣🟡", "g_atilan": 1.45, "g_yenilen": 1.35, "kadro_degeri": 45.0},
    "Kocaelispor": {"league": "Trendyol Süper Lig", "emoji": "🟢⚫", "g_atilan": 1.40, "g_yenilen": 1.30, "kadro_degeri": 35.0},
    "Çaykur Rizespor": {"league": "Trendyol Süper Lig", "emoji": "🟢🔵", "g_atilan": 1.38, "g_yenilen": 1.35, "kadro_degeri": 36.0},
    "Konyaspor": {"league": "Trendyol Süper Lig", "emoji": "🟢⚪", "g_atilan": 1.35, "g_yenilen": 1.32, "kadro_degeri": 38.0},
    "Alanyaspor": {"league": "Trendyol Süper Lig", "emoji": "🍊", "g_atilan": 1.32, "g_yenilen": 1.38, "kadro_degeri": 33.0},
    "Antalyaspor": {"league": "Trendyol Süper Lig", "emoji": "🦂", "g_atilan": 1.30, "g_yenilen": 1.40, "kadro_degeri": 34.0},
    "Kasımpaşa": {"league": "Trendyol Süper Lig", "emoji": "🔵⚪", "g_atilan": 1.40, "g_yenilen": 1.42, "kadro_degeri": 36.0},
    "Sivasspor": {"league": "Trendyol Süper Lig", "emoji": "🔴⚪", "g_atilan": 1.28, "g_yenilen": 1.38, "kadro_degeri": 28.0},
    "Gaziantep FK": {"league": "Trendyol Süper Lig", "emoji": "🔴⚫", "g_atilan": 1.25, "g_yenilen": 1.40, "kadro_degeri": 30.0},
    "Kayserispor": {"league": "Trendyol Süper Lig", "emoji": "🟡🔴", "g_atilan": 1.22, "g_yenilen": 1.45, "kadro_degeri": 29.0},
    "Bodrum FK": {"league": "Trendyol Süper Lig", "emoji": "💚🤍", "g_atilan": 1.15, "g_yenilen": 1.45, "kadro_degeri": 30.0},

    # --- TFF 1. LİG (2026/27) ---
    "Bursaspor": {"league": "TFF 1. Lig", "emoji": "💚🤍", "g_atilan": 1.50, "g_yenilen": 1.10, "kadro_degeri": 20.0},
    "Ankaragücü": {"league": "TFF 1. Lig", "emoji": "🟡🔵", "g_atilan": 1.65, "g_yenilen": 1.05, "kadro_degeri": 35.0},
    "Iğdır FK": {"league": "TFF 1. Lig", "emoji": "🟢⚪", "g_atilan": 1.40, "g_yenilen": 1.15, "kadro_degeri": 16.0},
    "Bandırmaspor": {"league": "TFF 1. Lig", "emoji": "🔴🟢", "g_atilan": 1.42, "g_yenilen": 1.18, "kadro_degeri": 17.0},
    "Sakaryaspor": {"league": "TFF 1. Lig", "emoji": "🟢⚫", "g_atilan": 1.45, "g_yenilen": 1.20, "kadro_degeri": 18.0},
    "Ankara Keçiörengücü": {"league": "TFF 1. Lig", "emoji": "🟣⚪", "g_atilan": 1.35, "g_yenilen": 1.20, "kadro_degeri": 13.0},
    "Fatih Karagümrük": {"league": "TFF 1. Lig", "emoji": "🔴⚫", "g_atilan": 1.50, "g_yenilen": 1.20, "kadro_degeri": 22.0},
    "Gençlerbirliği": {"league": "TFF 1. Lig", "emoji": "🔴⚫", "g_atilan": 1.38, "g_yenilen": 1.22, "kadro_degeri": 21.0},
    "Amed SK": {"league": "TFF 1. Lig", "emoji": "🟢🔴", "g_atilan": 1.40, "g_yenilen": 1.25, "kadro_degeri": 19.0},
    "Erzurumspor FK": {"league": "TFF 1. Lig", "emoji": "🔵⚪", "g_atilan": 1.30, "g_yenilen": 1.25, "kadro_degeri": 15.0},
    "Ümraniyespor": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.32, "g_yenilen": 1.28, "kadro_degeri": 16.0},
    "Pendikspor": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.35, "g_yenilen": 1.30, "kadro_degeri": 20.0},
    "Çorum FK": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.30, "g_yenilen": 1.30, "kadro_degeri": 17.0},
    "Boluspor": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.28, "g_yenilen": 1.32, "kadro_degeri": 14.0},
    "Manisa FK": {"league": "TFF 1. Lig", "emoji": "⚫⚪", "g_atilan": 1.25, "g_yenilen": 1.35, "kadro_degeri": 15.0},
    "Esenler Erokspor": {"league": "TFF 1. Lig", "emoji": "🟡🟢", "g_atilan": 1.32, "g_yenilen": 1.28, "kadro_degeri": 16.0},
    "Şanlıurfaspor": {"league": "TFF 1. Lig", "emoji": "🟡🟢", "g_atilan": 1.20, "g_yenilen": 1.40, "kadro_degeri": 12.0},
    "İstanbulspor": {"league": "TFF 1. Lig", "emoji": "🟡⬛", "g_atilan": 1.22, "g_yenilen": 1.40, "kadro_degeri": 16.0},
    "Batman Petrolspor": {"league": "TFF 1. Lig", "emoji": "🔴⚪", "g_atilan": 1.45, "g_yenilen": 1.25, "kadro_degeri": 14.0},

    # --- AVRUPA KUPALARI ÇİFT KULVAR (2026/27) ---
    "Galatasaray (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "🦁⭐", "g_atilan": 2.10, "g_yenilen": 0.95, "kadro_degeri": 240.0},
    "Fenerbahçe (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "🟡🔵⭐", "g_atilan": 2.05, "g_yenilen": 1.00, "kadro_degeri": 230.0},
    "Beşiktaş (UEL)": {"league": "UEFA Avrupa Ligi", "emoji": "🦅🇪🇺", "g_atilan": 1.75, "g_yenilen": 1.15, "kadro_degeri": 155.0},
    "Trabzonspor (UECL)": {"league": "Konferans Ligi", "emoji": "🌊🇪🇺", "g_atilan": 1.80, "g_yenilen": 1.10, "kadro_degeri": 120.0},
    
    "Real Madrid (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "👑⭐", "g_atilan": 2.40, "g_yenilen": 0.85, "kadro_degeri": 1360.0},
    "Barcelona (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "🔵🔴⭐", "g_atilan": 2.45, "g_yenilen": 1.00, "kadro_degeri": 980.0},
    "Manchester City (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "🔵⭐", "g_atilan": 2.50, "g_yenilen": 0.90, "kadro_degeri": 1310.0},
    "Arsenal (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "🔴⭐", "g_atilan": 2.20, "g_yenilen": 0.75, "kadro_degeri": 1190.0},
    "Liverpool (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "🔴⭐", "g_atilan": 2.35, "g_yenilen": 0.95, "kadro_degeri": 1000.0},
    "Inter Milan (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "⚫🔵⭐", "g_atilan": 2.05, "g_yenilen": 0.70, "kadro_degeri": 700.0},
    "Bayern Munich (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "🔴⭐", "g_atilan": 2.65, "g_yenilen": 0.95, "kadro_degeri": 960.0},
    "Paris Saint-Germain (UCL)": {"league": "Şampiyonlar Ligi", "emoji": "🗼⭐", "g_atilan": 2.45, "g_yenilen": 0.88, "kadro_degeri": 910.0},

    # --- PREMIER LEAGUE (2026/27 - Tam Kadro) ---
    "Manchester City": {"league": "Premier League", "emoji": "🔵", "g_atilan": 2.65, "g_yenilen": 0.85, "kadro_degeri": 1310.0},
    "Arsenal": {"league": "Premier League", "emoji": "🔴", "g_atilan": 2.30, "g_yenilen": 0.70, "kadro_degeri": 1190.0},
    "Liverpool": {"league": "Premier League", "emoji": "🔴", "g_atilan": 2.45, "g_yenilen": 0.90, "kadro_degeri": 1000.0},
    "Chelsea": {"league": "Premier League", "emoji": "🔵", "g_atilan": 2.10, "g_yenilen": 1.10, "kadro_degeri": 980.0},
    "Manchester United": {"league": "Premier League", "emoji": "🔴", "g_atilan": 1.75, "g_yenilen": 1.30, "kadro_degeri": 870.0},
    "Tottenham Hotspur": {"league": "Premier League", "emoji": "⚪", "g_atilan": 2.05, "g_yenilen": 1.35, "kadro_degeri": 800.0},
    "Aston Villa": {"league": "Premier League", "emoji": "🦁", "g_atilan": 1.85, "g_yenilen": 1.20, "kadro_degeri": 640.0},
    "Newcastle United": {"league": "Premier League", "emoji": "⚫⚪", "g_atilan": 1.90, "g_yenilen": 1.25, "kadro_degeri": 650.0},
    "Brighton": {"league": "Premier League", "emoji": "🔵⚪", "g_atilan": 1.70, "g_yenilen": 1.35, "kadro_degeri": 480.0},
    "West Ham United": {"league": "Premier League", "emoji": "⚒️", "g_atilan": 1.50, "g_yenilen": 1.50, "kadro_degeri": 410.0},
    "Crystal Palace": {"league": "Premier League", "emoji": "🦅", "g_atilan": 1.40, "g_yenilen": 1.40, "kadro_degeri": 380.0},
    "Fulham": {"league": "Premier League", "emoji": "⚪⬛", "g_atilan": 1.45, "g_yenilen": 1.45, "kadro_degeri": 340.0},
    "Everton": {"league": "Premier League", "emoji": "💙", "g_atilan": 1.30, "g_yenilen": 1.40, "kadro_degeri": 330.0},
    "Brentford": {"league": "Premier League", "emoji": "🐝", "g_atilan": 1.55, "g_yenilen": 1.60, "kadro_degeri": 350.0},
    "Bournemouth": {"league": "Premier League", "emoji": "🍒", "g_atilan": 1.50, "g_yenilen": 1.55, "kadro_degeri": 320.0},
    "Nottingham Forest": {"league": "Premier League", "emoji": "🌳", "g_atilan": 1.35, "g_yenilen": 1.45, "kadro_degeri": 310.0},
    "Wolverhampton": {"league": "Premier League", "emoji": "🐺", "g_atilan": 1.30, "g_yenilen": 1.65, "kadro_degeri": 290.0},
    "Leicester City": {"league": "Premier League", "emoji": "🦊", "g_atilan": 1.25, "g_yenilen": 1.70, "kadro_degeri": 260.0},
    "Ipswich Town": {"league": "Premier League", "emoji": "🚜", "g_atilan": 1.15, "g_yenilen": 1.80, "kadro_degeri": 140.0},
    "Southampton": {"league": "Premier League", "emoji": "🔴⚪", "g_atilan": 1.10, "g_yenilen": 1.85, "kadro_degeri": 210.0},

    # --- LA LIGA (2026/27 - Tam Kadro) ---
    "Real Madrid": {"league": "La Liga", "emoji": "👑", "g_atilan": 2.50, "g_yenilen": 0.80, "kadro_degeri": 1360.0},
    "Barcelona": {"league": "La Liga", "emoji": "🔵🔴", "g_atilan": 2.55, "g_yenilen": 0.95, "kadro_degeri": 980.0},
    "Atletico Madrid": {"league": "La Liga", "emoji": "🔴⚪", "g_atilan": 1.95, "g_yenilen": 0.85, "kadro_degeri": 540.0},
    "Real Sociedad": {"league": "La Liga", "emoji": "🔵⚪", "g_atilan": 1.50, "g_yenilen": 1.10, "kadro_degeri": 420.0},
    "Athletic Bilbao": {"league": "La Liga", "emoji": "🔴⚪", "g_atilan": 1.60, "g_yenilen": 1.05, "kadro_degeri": 360.0},
    "Villarreal": {"league": "La Liga", "emoji": "🟡", "g_atilan": 1.75, "g_yenilen": 1.40, "kadro_degeri": 280.0},
    "Real Betis": {"league": "La Liga", "emoji": "🟢💚", "g_atilan": 1.55, "g_yenilen": 1.30, "kadro_degeri": 220.0},
    "Sevilla": {"league": "La Liga", "emoji": "⚪🔴", "g_atilan": 1.35, "g_yenilen": 1.50, "kadro_degeri": 200.0},
    "Valencia": {"league": "La Liga", "emoji": "🦇", "g_atilan": 1.25, "g_yenilen": 1.35, "kadro_degeri": 180.0},
    "Girona": {"league": "La Liga", "emoji": "🔴⚪", "g_atilan": 1.65, "g_yenilen": 1.30, "kadro_degeri": 210.0},
    "Celta Vigo": {"league": "La Liga", "emoji": "Sky", "g_atilan": 1.38, "g_yenilen": 1.40, "kadro_degeri": 110.0},
    "Osasuna": {"league": "La Liga", "emoji": "🔴", "g_atilan": 1.30, "g_yenilen": 1.35, "kadro_degeri": 120.0},
    "Mallorca": {"league": "La Liga", "emoji": "🔴⚫", "g_atilan": 1.20, "g_yenilen": 1.30, "kadro_degeri": 90.0},
    "Getafe": {"league": "La Liga", "emoji": "🔵", "g_atilan": 1.10, "g_yenilen": 1.20, "kadro_degeri": 95.0},
    "Rayo Vallecano": {"league": "La Liga", "emoji": "⚡", "g_atilan": 1.32, "g_yenilen": 1.38, "kadro_degeri": 85.0},
    "Alaves": {"league": "La Liga", "emoji": "🔵⚪", "g_atilan": 1.18, "g_yenilen": 1.35, "kadro_degeri": 75.0},
    "Las Palmas": {"league": "La Liga", "emoji": "🟡", "g_atilan": 1.25, "g_yenilen": 1.50, "kadro_degeri": 80.0},
    "Valladolid": {"league": "La Liga", "emoji": "🟣⚪", "g_atilan": 1.05, "g_yenilen": 1.60, "kadro_degeri": 70.0},
    "Leganes": {"league": "La Liga", "emoji": "🥒", "g_atilan": 1.10, "g_yenilen": 1.40, "kadro_degeri": 65.0},
    "Espanyol": {"league": "La Liga", "emoji": "🔵⚪", "g_atilan": 1.20, "g_yenilen": 1.45, "kadro_degeri": 85.0},

    # --- SERIE A (2026/27 - Tam Kadro) ---
    "Inter Milan": {"league": "Serie A", "emoji": "⚫🔵", "g_atilan": 2.15, "g_yenilen": 0.65, "kadro_degeri": 700.0},
    "Juventus": {"league": "Serie A", "emoji": "⚪⚫", "g_atilan": 1.80, "g_yenilen": 0.75, "kadro_degeri": 620.0},
    "AC Milan": {"league": "Serie A", "emoji": "🔴⚫", "g_atilan": 1.95, "g_yenilen": 1.00, "kadro_degeri": 570.0},
    "Napoli": {"league": "Serie A", "emoji": "🔵", "g_atilan": 1.90, "g_yenilen": 0.95, "kadro_degeri": 510.0},
    "Atalanta": {"league": "Serie A", "emoji": "🔵⚫", "g_atilan": 2.00, "g_yenilen": 1.15, "kadro_degeri": 430.0},
    "AS Roma": {"league": "Serie A", "emoji": "🐺", "g_atilan": 1.75, "g_yenilen": 1.10, "kadro_degeri": 330.0},
    "Lazio": {"league": "Serie A", "emoji": "🦅", "g_atilan": 1.65, "g_yenilen": 1.20, "kadro_degeri": 270.0},
    "Fiorentina": {"league": "Serie A", "emoji": "💜", "g_atilan": 1.60, "g_yenilen": 1.25, "kadro_degeri": 250.0},
    "Bologna": {"league": "Serie A", "emoji": "🔴🔵", "g_atilan": 1.55, "g_yenilen": 1.20, "kadro_degeri": 240.0},
    "Torino": {"league": "Serie A", "emoji": "🐂", "g_atilan": 1.35, "g_yenilen": 1.30, "kadro_degeri": 180.0},
    "Udinese": {"league": "Serie A", "emoji": "⚪⚫", "g_atilan": 1.30, "g_yenilen": 1.35, "kadro_degeri": 120.0},
    "Monza": {"league": "Serie A", "emoji": "🔴⚪", "g_atilan": 1.20, "g_yenilen": 1.40, "kadro_degeri": 110.0},
    "Genoa": {"league": "Serie A", "emoji": "🔴🔵", "g_atilan": 1.25, "g_yenilen": 1.38, "kadro_degeri": 115.0},
    "Lecce": {"league": "Serie A", "emoji": "🟡🔴", "g_atilan": 1.10, "g_yenilen": 1.45, "kadro_degeri": 80.0},
    "Empoli": {"league": "Serie A", "emoji": "🔵⚪", "g_atilan": 1.12, "g_yenilen": 1.38, "kadro_degeri": 75.0},
    "Verona": {"league": "Serie A", "emoji": "🟡🔵", "g_atilan": 1.18, "g_yenilen": 1.48, "kadro_degeri": 70.0},
    "Cagliari": {"league": "Serie A", "emoji": "🔴🔵", "g_atilan": 1.20, "g_yenilen": 1.45, "kadro_degeri": 85.0},
    "Parma": {"league": "Serie A", "emoji": "🟡🔵", "g_atilan": 1.30, "g_yenilen": 1.42, "kadro_degeri": 100.0},
    "Como": {"league": "Serie A", "emoji": "🔵⚪", "g_atilan": 1.25, "g_yenilen": 1.40, "kadro_degeri": 95.0},
    "Venezia": {"league": "Serie A", "emoji": "🟢🟠⚫", "g_atilan": 1.10, "g_yenilen": 1.55, "kadro_degeri": 65.0},

    # --- BUNDESLIGA (2026/27 - Tam Kadro) ---
    "Bayern Munich": {"league": "Bundesliga", "emoji": "🔴", "g_atilan": 2.80, "g_yenilen": 0.90, "kadro_degeri": 960.0},
    "Bayer Leverkusen": {"league": "Bundesliga", "emoji": "💊", "g_atilan": 2.40, "g_yenilen": 0.85, "kadro_degeri": 650.0},
    "Borussia Dortmund": {"league": "Bundesliga", "emoji": "🟡⚫", "g_atilan": 2.15, "g_yenilen": 1.20, "kadro_degeri": 490.0},
    "RB Leipzig": {"league": "Bundesliga", "emoji": "🔴", "g_atilan": 2.05, "g_yenilen": 1.25, "kadro_degeri": 440.0},
    "Eintracht Frankfurt": {"league": "Bundesliga", "emoji": "🦅", "g_atilan": 1.80, "g_yenilen": 1.30, "kadro_degeri": 240.0},
    "Stuttgart": {"league": "Bundesliga", "emoji": "⚪🔴", "g_atilan": 1.85, "g_yenilen": 1.35, "kadro_degeri": 220.0},
    "Werder Bremen": {"league": "Bundesliga", "emoji": "🟢⚪", "g_atilan": 1.40, "g_yenilen": 1.45, "kadro_degeri": 110.0},
    "Freiburg": {"league": "Bundesliga", "emoji": "⚫🔴", "g_atilan": 1.45, "g_yenilen": 1.38, "kadro_degeri": 160.0},
    "Hoffenheim": {"league": "Bundesliga", "emoji": "🔵", "g_atilan": 1.50, "g_yenilen": 1.50, "kadro_degeri": 150.0},
    "Wolfsburg": {"league": "Bundesliga", "emoji": "🟢", "g_atilan": 1.38, "g_yenilen": 1.42, "kadro_degeri": 170.0},
    "Mainz 05": {"league": "Bundesliga", "emoji": "🔴⚪", "g_atilan": 1.35, "g_yenilen": 1.40, "kadro_degeri": 100.0},
    "Augsburg": {"league": "Bundesliga", "emoji": "🔴🟢", "g_atilan": 1.30, "g_yenilen": 1.48, "kadro_degeri": 90.0},
    "Borussia Mönchengladbach": {"league": "Bundesliga", "emoji": "⚫⚪", "g_atilan": 1.42, "g_yenilen": 1.50, "kadro_degeri": 130.0},
    "Union Berlin": {"league": "Bundesliga", "emoji": "🔴", "g_atilan": 1.15, "g_yenilen": 1.30, "kadro_degeri": 110.0},
    "Bochum": {"league": "Bundesliga", "emoji": "🔵⚪", "g_atilan": 1.18, "g_yenilen": 1.60, "kadro_degeri": 65.0},
    "Heidenheim": {"league": "Bundesliga", "emoji": "🔴🔵", "g_atilan": 1.25, "g_yenilen": 1.45, "kadro_degeri": 55.0},
    "St. Pauli": {"league": "Bundesliga", "emoji": "🟤⚪", "g_atilan": 1.10, "g_yenilen": 1.40, "kadro_degeri": 50.0},
    "Holstein Kiel": {"league": "Bundesliga", "emoji": "🔵⚪", "g_atilan": 1.12, "g_yenilen": 1.70, "kadro_degeri": 45.0},

    # --- LIGUE 1 (2026/27 - Tam Kadro) ---
    "Paris Saint-Germain": {"league": "Ligue 1", "emoji": "🗼", "g_atilan": 2.60, "g_yenilen": 0.80, "kadro_degeri": 910.0},
    "Monaco": {"league": "Ligue 1", "emoji": "🔴⚪", "g_atilan": 2.05, "g_yenilen": 1.20, "kadro_degeri": 370.0},
    "Marseille": {"league": "Ligue 1", "emoji": "⚪🔵", "g_atilan": 1.90, "g_yenilen": 1.15, "kadro_degeri": 310.0},
    "Lille": {"league": "Ligue 1", "emoji": "🔴⚪", "g_atilan": 1.75, "g_yenilen": 1.10, "kadro_degeri": 260.0},
    "Lyon": {"league": "Ligue 1", "emoji": "🔴🔵", "g_atilan": 1.70, "g_yenilen": 1.30, "kadro_degeri": 240.0},
    "Nice": {"league": "Ligue 1", "emoji": "🔴⚫", "g_atilan": 1.55, "g_yenilen": 1.20, "kadro_degeri": 210.0},
    "Lens": {"league": "Ligue 1", "emoji": "🟡🔴", "g_atilan": 1.45, "g_yenilen": 1.25, "kadro_degeri": 180.0},
    "Rennes": {"league": "Ligue 1", "emoji": "🔴⚫", "g_atilan": 1.50, "g_yenilen": 1.35, "kadro_degeri": 170.0},
    "Strasbourg": {"league": "Ligue 1", "emoji": "🔵⚪", "g_atilan": 1.38, "g_yenilen": 1.42, "kadro_degeri": 110.0},
    "Brest": {"league": "Ligue 1", "emoji": "🔴⚪", "g_atilan": 1.40, "g_yenilen": 1.38, "kadro_degeri": 105.0},
    "Reims": {"league": "Ligue 1", "emoji": "🔴⚪", "g_atilan": 1.32, "g_yenilen": 1.38, "kadro_degeri": 95.0},
    "Toulouse": {"league": "Ligue 1", "emoji": "🟣⚪", "g_atilan": 1.30, "g_yenilen": 1.35, "kadro_degeri": 90.0},
    "Montpellier": {"league": "Ligue 1", "emoji": "🟠🔵", "g_atilan": 1.25, "g_yenilen": 1.50, "kadro_degeri": 80.0},
    "Nantes": {"league": "Ligue 1", "emoji": "🟡🟢", "g_atilan": 1.20, "g_yenilen": 1.45, "kadro_degeri": 75.0},
    "Auxerre": {"league": "Ligue 1", "emoji": "🔵⚪", "g_atilan": 1.22, "g_yenilen": 1.48, "kadro_degeri": 65.0},
    "Saint-Etienne": {"league": "Ligue 1", "emoji": "💚", "g_atilan": 1.18, "g_yenilen": 1.50, "kadro_degeri": 70.0},
    "Angers": {"league": "Ligue 1", "emoji": "⚫⚪", "g_atilan": 1.10, "g_yenilen": 1.55, "kadro_degeri": 50.0},
    "Le Havre": {"league": "Ligue 1", "emoji": "Sky", "g_atilan": 1.12, "g_yenilen": 1.52, "kadro_degeri": 55.0}
}

# 3. Gelişmiş Lig Güç Katsayıları
LEAGUE_MULTIPLIERS = {
    "Şampiyonlar Ligi": 1.65,
    "Premier League": 1.55,
    "La Liga": 1.45,
    "Bundesliga": 1.35,
    "Serie A": 1.35,
    "Ligue 1": 1.25,
    "UEFA Avrupa Ligi": 1.30,
    "Konferans Ligi": 1.15,
    "Trendyol Süper Lig": 1.05,
    "TFF 1. Lig": 0.55
}

# Sol Menü
st.sidebar.header("⚙️ Maç & Lig Seçimi")
selected_league = st.sidebar.selectbox(
    "Lig / Kulvar Filtrele", 
    ["Tümü", "Şampiyonlar Ligi", "UEFA Avrupa Ligi", "Konferans Ligi", "Trendyol Süper Lig", "Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1", "TFF 1. Lig"]
)

if selected_league == "Tümü":
    filtered_teams = list(GLOBAL_TEAMS.keys())
else:
    filtered_teams = [t for t, data in GLOBAL_TEAMS.items() if data["league"] == selected_league]

col_t1, col_t2 = st.sidebar.columns(2)
with col_t1:
    home_team = st.selectbox("Ev Sahibi Takım", filtered_teams, index=0)
with col_t2:
    away_team = st.selectbox("Deplasman Takımı", filtered_teams, index=1 if len(filtered_teams) > 1 else 0)

st.sidebar.subheader("⚡ Maç Dinamikleri")
is_derby = st.sidebar.checkbox("Yüksek Rekabet / Derbi Atmosferi", value=False)
weather = st.sidebar.selectbox("Zemin ve Hava", ["İdeal Çim", "Yağmurlu (Ağır Zemin)"])

# 4. 100K Monte Carlo Simülasyon Motoru
def run_simulation(h_name, a_name, derby, cond):
    h = GLOBAL_TEAMS[h_name]
    a = GLOBAL_TEAMS[a_name]

    h_mult = LEAGUE_MULTIPLIERS.get(h["league"], 1.0)
    a_mult = LEAGUE_MULTIPLIERS.get(a["league"], 1.0)

    squad_ratio = (h["kadro_degeri"] ** 0.35) / (a["kadro_degeri"] ** 0.35)

    home_advantage = 1.12
    derby_mod = 0.88 if derby else 1.0
    weather_mod = 0.92 if "Yağmur" in cond else 1.0

    h_lambda = max(0.12, ((h["g_atilan"] * h_mult + a["g_yenilen"] / a_mult) / 2) * squad_ratio * home_advantage * derby_mod * weather_mod)
    a_lambda = max(0.12, ((a["g_atilan"] * a_mult + h["g_yenilen"] / h_mult) / 2) * (1 / squad_ratio) * derby_mod * weather_mod)

    n_sims = 100000
    sim_h_goals = np.random.poisson(h_lambda, n_sims)
    sim_a_goals = np.random.poisson(a_lambda, n_sims)
    
    h_goals = int(np.bincount(sim_h_goals).argmax())
    a_goals = int(np.bincount(sim_a_goals).argmax())

    h_wins = np.sum(sim_h_goals > sim_a_goals)
    draws = np.sum(sim_h_goals == sim_a_goals)
    a_wins = np.sum(sim_h_goals < sim_a_goals)

    hp = (h_wins / n_sims) * 100
    dp = (draws / n_sims) * 100
    ap = (a_wins / n_sims) * 100

    o1 = round(max(1.05, 100 / hp), 2) if hp > 0 else 10.0
    ox = round(max(1.05, 100 / dp), 2) if dp > 0 else 10.0
    o2 = round(max(1.05, 100 / ap), 2) if ap > 0 else 10.0

    h_xg = round(h_lambda, 2)
    a_xg = round(a_lambda, 2)

    h_shots = int(h_xg * 4 + 2)
    a_shots = int(a_xg * 4 + 2)
    h_on_target = max(1, int(h_shots * 0.42))
    a_on_target = max(1, int(a_shots * 0.42))
    
    h_corners = np.random.randint(4, 8)
    a_corners = np.random.randint(3, 7)

    return h_goals, a_goals, h_xg, a_xg, h_shots, a_shots, h_on_target, a_on_target, h_corners, a_corners, hp, dp, ap, o1, ox, o2

# 5. Dashboard Ekranı
if st.button("🚀 100.000 Adımlı Küresel Simülasyonu Başlat"):
    with st.spinner("2026/2027 güncel kadrolar işleniyor, 100.000 simülasyon koşturuluyor..."):
        h_g, a_g, h_xg, a_xg, h_s, a_s, h_ot, a_ot, h_c, a_c, hp, dp, ap, o1, ox, o2 = run_simulation(
            home_team, away_team, is_derby, weather
        )

    h_info = GLOBAL_TEAMS[home_team]
    a_info = GLOBAL_TEAMS[away_team]

    st.markdown("---")
    sc1, sc_mid, sc2 = st.columns([3, 2, 3])
    
    with sc1:
        st.markdown(f"<h2 style='text-align: right;'>{h_info['emoji']} {home_team}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: right; color: #8b949e;'>Kulvar: {h_info['league']} | Değer: €{h_info['kadro_degeri']}M</p>", unsafe_allow_html=True)
    with sc_mid:
        st.markdown(f"<h1 style='text-align: center; color: #58a6ff; font-size: 48px;'>{h_g} - {a_g}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #8b949e;'>En Olası Maç Sonucu (Mod)</p>", unsafe_allow_html=True)
    with sc2:
        st.markdown(f"<h2 style='text-align: left;'>{away_team} {a_info['emoji']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: left; color: #8b949e;'>Kulvar: {a_info['league']} | Değer: €{a_info['kadro_degeri']}M</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 Gelişmiş xG & Kalite Analizi")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Beklenen Gol (xG)", value=f"{h_xg}", delta=f"{a_xg} (Dep)")
    col2.metric(label="Toplam Şut", value=f"{h_s}", delta=f"{a_s}")
    col3.metric(label="İsabetli Şut", value=f"{h_ot}", delta=f"{a_ot}")
    col4.metric(label="Korner", value=f"{h_c}", delta=f"{a_c}")

    st.markdown("---")
    st.subheader("🎯 Hesaplanan Tahmini Bahis Oranları")
    b1, bx, b2 = st.columns(3)
    b1.metric(label="MS 1 (Ev Sahibi)", value=f"{o1}")
    bx.metric(label="MS X (Beraberlik)", value=f"{ox}")
    b2.metric(label="MS 2 (Deplasman)", value=f"{o2}")

    st.markdown("---")
    st.subheader("📈 100.000 Simülasyon Olasılık Dağılımı")

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
