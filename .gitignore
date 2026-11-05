import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Sayfa Yapılandırması
st.set_page_config(page_title="Ultimate Mackolik Simülatör", page_icon="⚽", layout="wide")

st.title("⚽ Ultimate Mackolik & Maç Simülasyon Paneli")
st.markdown("Takım güçlerini ayarla, **100.000 Monte Carlo Simülasyonu** ile maçın tüm ihtimallerini anında ekrana dök.")

# 2. Sol Menü (Kontrol Paneli)
st.sidebar.header("⚙️ Maç & Takım Parametreleri")

home_team = st.sidebar.text_input("Ev Sahibi Takım", "Trabzonspor")
away_team = st.sidebar.text_input("Deplasman Takımı", "Freiburg")

st.sidebar.subheader("Güç Katsayıları")
home_attack = st.sidebar.slider(f"{home_team} Hücum Gücü", 0.8, 1.8, 1.28, 0.01)
home_defense = st.sidebar.slider(f"{home_team} Savunma Zafiyeti", 0.6, 1.3, 0.88, 0.01)
away_attack = st.sidebar.slider(f"{away_team} Hücum Gücü", 0.8, 1.8, 1.18, 0.01)
away_defense = st.sidebar.slider(f"{away_team} Savunma Zafiyeti", 0.6, 1.3, 0.85, 0.01)

# Ekstra Modüller
st.sidebar.subheader("Maç Koşulları")
weather_condition = st.sidebar.selectbox("Hava / Zemin Durumu", ["Normal İdeal Zemin", "Yağışlı / Ağır Zemin", "Sıcak & Nemli"])
has_red_card = st.sidebar.checkbox("Kırmızı Kart Senaryosunu Dahil Et", value=True)
has_penalties = st.sidebar.checkbox("Penaltı Modülünü Dahil Et", value=True)

n_simulations = st.sidebar.slider("Simülasyon Sayısı", 10000, 200000, 100000, 10000)

# 3. Çalıştırma Butonu
if st.sidebar.button("🚀 Simülasyonu Başlat", type="primary"):
    with st.spinner(f"{n_simulations:,} maç simüle ediliyor..."):
        np.random.seed(42)
        
        # Zemin Faktörü
        weather_factor = 0.98 if weather_condition == "Normal İdeal Zemin" else 0.92
        
        # Temel Parametreler
        avg_home, avg_away = 1.55, 1.15
        home_adv = 1.18
        
        base_h_lambda = (home_attack * away_defense * avg_home) * home_adv * weather_factor
        base_a_lambda = (away_attack * home_defense * avg_away) / (home_adv * 0.92) * weather_factor
        
        # Kırmızı Kart Etkisi
        if has_red_card:
            h_red = np.random.binomial(1, 0.10, n_simulations)
            a_red = np.random.binomial(1, 0.12, n_simulations)
            base_h_lambda = np.where(h_red == 1, base_h_lambda * 0.72, base_h_lambda)
            base_h_lambda = np.where(a_red == 1, base_h_lambda * 1.18, base_h_lambda)
            base_a_lambda = np.where(a_red == 1, base_a_lambda * 0.72, base_a_lambda)
            base_a_lambda = np.where(h_red == 1, base_a_lambda * 1.18, base_a_lambda)
            
        # Penaltı Etkisi
        h_pen = np.random.binomial(1, 0.26 * 0.65, n_simulations) if has_penalties else np.zeros(n_simulations)
        a_pen = np.random.binomial(1, 0.26 * 0.60, n_simulations) if has_penalties else np.zeros(n_simulations)
        
        # Poisson Simülasyonu
        home_goals = np.random.poisson(base_h_lambda, n_simulations) + h_pen
        away_goals = np.random.poisson(base_a_lambda, n_simulations) + a_pen
        
        # İstatistikler
        h_wins = np.sum(home_goals > away_goals)
        draws = np.sum(home_goals == away_goals)
        a_wins = np.sum(home_goals < away_goals)
        
        h_win_pct = (h_wins / n_simulations) * 100
        draw_pct = (draws / n_simulations) * 100
        a_win_pct = (a_wins / n_simulations) * 100
        
        total_goals = home_goals + away_goals
        over_2_5 = np.sum(total_goals > 2.5) / n_simulations * 100
        btts = np.sum((home_goals > 0) & (away_goals > 0)) / n_simulations * 100
        
        # Arayüz Üst Metrik Kartları (Mackolik Tarzı)
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric(f"{home_team} Kazanır", f"%{h_win_pct:.1f}")
        col2.metric("Beraberlik", f"%{draw_pct:.1f}")
        col3.metric(f"{away_team} Kazanır", f"%{a_win_pct:.1f}")
        col4.metric("2.5 Gol Üst", f"%{over_2_5:.1f}")
        col5.metric("KG Var", f"%{btts:.1f}")
        
        st.markdown("---")
        
        # Grafikler
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Skor Dağılımı
        score_pairs = list(zip(home_goals, away_goals))
        unique_scores, counts = np.unique(score_pairs, axis=0, return_counts=True)
        sorted_indices = np.argsort(-counts)
        
        top_labels, top_pcts = [], []
        for i in range(5):
            idx = sorted_indices[i]
            t_s, f_s = unique_scores[idx]
            pct = (counts[idx] / n_simulations) * 100
            top_labels.append(f"{home_team[:3].upper()} {t_s}-{f_s} {away_team[:3].upper()}")
            top_pcts.append(pct)
            
        bars = ax1.bar(top_labels, top_pcts, color=['#751B24', '#e65c00', '#1a334d', '#2d862d', '#cc3333'], edgecolor='black', alpha=0.9)
        ax1.set_title("En Muhtemel 5 Maç Skoru", fontsize=11, fontweight='bold')
        ax1.set_ylabel("İhtimal (%)")
        ax1.grid(axis='y', linestyle='--', alpha=0.6)
        
        for bar in bars:
            yval = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f"%{yval:.1f}", ha='center', va='bottom', fontsize=9, fontweight='bold')
            
        # Gol Frekansı
        ax2.hist([home_goals, away_goals], bins=np.arange(-0.5, 6.5, 1), label=[home_team, away_team], color=['#751B24', '#1a334d'], alpha=0.8, edgecolor='black', density=True)
        ax2.set_title("Atılan Gol Frekans Dağılımı", fontsize=11, fontweight='bold')
        ax2.set_xlabel("Gol Sayısı")
        ax2.set_ylabel("Yoğunluk")
        ax2.legend()
        ax2.grid(axis='y', linestyle='--', alpha=0.6)
        
        st.pyplot(fig)
else:
    st.info("👈 Sol menüden takımları belirleyip **'Simülasyonu Başlat'** butonuna basman yeterli!")
