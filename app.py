import streamlit as st
import pandas as pd

# 1. Konfigurasi halaman dasar
st.set_page_config(page_title="Sistem Deteksi Dini Transaksi E-Commerce", layout="wide")

# 2. Injeksi CSS kustom (Aman tanpa benturan f-string)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FFB7B2 0%, #C7CEEA 100%);
    }
    .main-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .title-box {
        font-weight: bold;
        color: #4A0E4E;
        border-bottom: 2px solid #FFB7B2;
        padding-bottom: 8px;
        margin-bottom: 15px;
        font-size: 14px;
        text-transform: uppercase;
    }
    .stNumberInput label, .stSelectbox label {
        color: #4A0E4E !important;
        font-weight: 600 !important;
    }
    div.stButton > button:first-child {
        background: linear-gradient(to right, #FFB7B2, #9B5DE5);
        color: white;
        border: none;
        padding: 8px 35px;
        font-weight: bold;
        border-radius: 20px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 3. HEADER PANEL NAVIGASI UTAMA
st.markdown("""
<div style="background: rgba(255, 255, 255, 0.85); padding: 15px 20px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; backdrop-filter: blur(5px); box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
    <span style="font-weight: bold; color: #4A0E4E; line-height: 1.2;">
        <span style="font-size: 11px; color: #666;">SISTEM PENDUKUNG KEPUTUSAN</span><br>
        <span style="font-size: 16px; font-weight: 800;">SISTEM DETEKSI DINI PERILAKU TRANSAKSI PELANGGAN E-COMMERCE</span>
    </span>
    <span style="font-size: 12px; font-weight: 600; color: #4A0E4E; background: rgba(255,183,178,0.4); padding: 5px 12px; border-radius: 15px;">Admin Panel</span>
</div>
""", unsafe_allow_html=True)

# 4. CONTAINER FORM INPUT UTAMA
st.markdown('<div class="main-box"><div class="title-box">Form Input Aktivitas Pengunjung Sesi</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    admin_page = st.number_input("Administrative Page", min_value=0, value=2)
    page_values = st.number_input("Page Values", min_value=0.0, value=45.20)
with col2:
    info_page = st.number_input("Informational Page", min_value=0, value=1)
    special_day = st.number_input("Special Day (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.0)
with col3:
    prod_page = st.number_input("Product Related Page", min_value=0, value=15)
    prod_duration = st.number_input("Product Duration (Detik)", min_value=0, value=240)

col_extra1, col_extra2, col_extra3 = st.columns(3)
with col_extra1:
    bounce_rate = st.number_input("Bounce Rate", min_value=0.0, max_value=1.0, value=0.01)
with col_extra2:
    exit_rate = st.number_input("Exit Rate", min_value=0.0, max_value=1.0, value=0.02)
with col_extra3:
    bulan = st.selectbox("Bulan Kunjungan", ['Feb', 'Mar', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Tombol Eksekusi
tombol_klik = st.button("Proses Prediksi")
st.markdown('</div>', unsafe_allow_html=True) # Tutup main-box input

# 5. CONTAINER LOGIKA OUTPUT HASIL EVALUASI DIKLIK
if tombol_klik:
    st.markdown('<div class="main-box"><div class="title-box">Output Evaluasi & Tindakan Strategis</div>', unsafe_allow_html=True)
    
    # Aturan keputusan bisnis dinamis berbasis input user
    if page_values > 0.0:
        status, solusi, warna = "POTENSIAL MEMBELI", "Berikan Promo Flash", "green"
        rekomendasi_detail = "Sesi Potensial Membeli: Dorong konversi dengan memunculkan pop-up kupon diskon 10% atau opsi gratis ongkos kirim secara real-time sebelum pengunjung meninggalkan halaman."
    else:
        status, solusi, warna = "HANYA BROWSING", "Retargeting Iklan", "red"
        rekomendasi_detail = "Sesi Hanya Browsing: Minimalkan alokasi biaya pemasaran langsung pada sesi aktif ini, melainkan simpan log aktivitas untuk penargetan ulang (retargeting) di media sosial."

    # Render komponen tabel HTML
    html_tabel = f"""
    <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 15px;">
        <thead>
            <tr style="background-color: #FFF0F0; border-bottom: 2px solid #FFB7B2; color: #4A0E4E;">
                <th style="padding: 12px; border: 1px solid #eee;">Sesi ID</th>
                <th style="padding: 12px; border: 1px solid #eee;">Product Duration</th>
                <th style="padding: 12px; border: 1px solid #eee;">Page Values</th>
                <th style="padding: 12px; border: 1px solid #eee;">Bounce Rate</th>
                <th style="padding: 12px; border: 1px solid #eee;">Prediksi Niat Beli</th>
                <th style="padding: 12px; border: 1px solid #eee;">Tindakan / Solusi</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 12px; border: 1px solid #eee; font-weight: 600; color: #555;">SIM-001</td>
                <td style="padding: 12px; border: 1px solid #eee;">{prod_duration} Detik</td>
                <td style="padding: 12px; border: 1px solid #eee;">{page_values:.2f}</td>
                <td style="padding: 12px; border: 1px solid #eee;">{bounce_rate:.2f}</td>
                <td style="padding: 12px; border: 1px solid #eee; font-weight: bold; color: {warna}; font-size: 13px;">{status}</td>
                <td style="padding: 12px; border: 1px solid #eee; font-weight: bold; color: #4A0E4E;">{solusi}</td>
            </tr>
        </tbody>
    </table>
    
    <div style="background: rgba(255, 183, 178, 0.15); border-left: 4px solid #9B5DE5; border-radius: 4px; padding: 15px; font-size: 12px; line-height: 1.6;">
        <div style="font-weight: bold; color: #4A0E4E; margin-bottom: 5px;">Rekomendasi Intervensi Bisnis Otomatis:</div>
        <p style="margin: 0; color: #444;">{rekomendasi_detail}</p>
    </div>
    """
    st.markdown(html_tabel, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Tutup main-box output
