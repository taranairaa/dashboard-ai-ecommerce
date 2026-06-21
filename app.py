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

# 4. CONTAINER FORM INPUT UTAMA (TOP 5 FEATURE IMPORTANCE)
st.markdown('<div class="main-box"><div class="title-box">Form Input Aktivitas Pengunjung Sesi (Top 5 Variabel Utama)</div>', unsafe_allow_html=True)

# Membagi form menjadi 2 baris agar layout tetap seimbang dan rapi
row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    page_values = st.number_input("Page Values", min_value=0.0, value=45.20, help="Nilai rata-rata halaman yang berkontribusi pada transaksi")
with row1_col2:
    prod_duration = st.number_input("Product Related Duration (Detik)", min_value=0, value=240, help="Total durasi pengunjung di halaman produk")
with row1_col3:
    admin_page = st.number_input("Administrative Page", min_value=0, value=2, help="Jumlah halaman administratif/akun yang dibuka")

row2_col1, row2_col2, row2_col3 = st.columns(3)
with row2_col1:
    exit_rate = st.number_input("Exit Rate", min_value=0.0, max_value=1.0, value=0.02, help="Persentase pengunjung keluar dari halaman ini")
with row2_col2:
    bounce_rate = st.number_input("Bounce Rate", min_value=0.0, max_value=1.0, value=0.01, help="Persentase pengunjung langsung kabur setelah 1 halaman")
with row2_col3:
    # Bulan kunjungan dipertahankan sebagai pelengkap konteks waktu bisnis
    bulan = st.selectbox("Bulan Kunjungan", ['Feb', 'Mar', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Tombol Eksekusi
tombol_klik = st.button("Proses Prediksi")
st.markdown('</div>', unsafe_allow_html=True) # Tutup main-box input


# 5. CONTAINER LOGIKA OUTPUT HASIL EVALUASI (SINKRON TOP 5 GRAFIK BAB 4)
if tombol_klik:
    st.markdown('<div class="main-box"><div class="title-box">Output Evaluasi & Tindakan Strategis</div>', unsafe_allow_html=True)
    
    # --- PERHITUNGAN MATEMATIS BERDASARKAN BOBOT ASLI GRAFIK ---
    # 1. PageValues (Bobot: 65%) -> Maksimal kontribusi penuh jika nilai >= 100
    page_val_score = min(page_values / 100.0, 1.0) * 0.65
    
    # 2. ProductRelated_Duration (Bobot: 10%) -> Dinormalisasi dibagi 600 detik (10 menit)
    duration_score = min(prod_duration / 600.0, 1.0) * 0.10
    
    # 3. Administrative (Bobot: 4%) -> Dinormalisasi dibagi maksimal 10 halaman
    admin_score = min(admin_page / 10.0, 1.0) * 0.04
    
    # * Tambahan konstanta Informational (Bobot: 2%) diset default memberikan kontribusi pasif kecil
    info_passive_score = 0.01 
    
    # 4. Bounce Rates (Bobot: 7%) & Exit Rates (Bobot: 12%) -> Sifatnya penalti negatif
    rate_penalty = (bounce_rate * 0.07) + (exit_rate * 0.12)
    
    # Akumulasi hasil skor akhir matematika
    skor_total = (page_val_score + duration_score + admin_score + info_passive_score) - rate_penalty
    skor_akhir_persen = max(min(skor_total * 100, 100.0), 0.0)

    # Penentuan Klasifikasi Niat Beli Berdasarkan Threshold Standar 50%
    if skor_akhir_persen >= 50.0:
        status, solusi, warna = "POTENSIAL MEMBELI", "Berikan Promo Flash", "green"
        rekomendasi_detail = f"Sesi Potensial Membeli (Probabilitas Konversi: {skor_akhir_persen:.1f}%): Dorong transaksi dengan memunculkan pop-up kupon diskon langsung atau opsi gratis ongkos kirim real-time sebelum sesi berakhir."
    else:
        status, solusi, warna = "HANYA BROWSING", "Retargeting Iklan", "red"
        rekomendasi_detail = f"Sesi Hanya Browsing (Probabilitas Konversi: {skor_akhir_persen:.1f}%): Pengunjung minim niat beli belanja saat ini. Batasi intervensi biaya langsung, gunakan log aktivitas untuk retargeting pasca-sesi."

    # Render Tabel Informasi Hasil Simulasi
    html_tabel = f"""
    <div style="margin-bottom: 15px; background: #f9f9f9; padding: 12px; border-radius: 5px; border-left: 5px solid #9B5DE5;">
        <span style="font-weight: bold; color: #4A0E4E;">📊 Hasil Analisis Probabilitas (Top 5 Feature Importance Model): {skor_akhir_persen:.1f}%</span>
    </div>
    
    <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 15px;">
        <thead>
            <tr style="background-color: #FFF0F0; border-bottom: 2px solid #FFB7B2; color: #4A0E4E;">
                <th style="padding: 12px; border: 1px solid #eee;">Sesi ID</th>
                <th style="padding: 12px; border: 1px solid #eee;">Product Related Duration</th>
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
