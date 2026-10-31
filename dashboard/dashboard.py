from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title='Bike Sharing | Dashboard', page_icon='🚲', layout='wide')

WARNA = '#176B80'
WARNA_2 = '#C17A25'
FOLDER_DATA = Path(__file__).resolve().parent.parent / 'data'

@st.cache_data
def ambil_data():
    harian = pd.read_csv('day.csv', parse_dates=['dteday'])
    jam = pd.read_csv('hour.csv', parse_dates=['dteday'])
    return harian, jam

st.title('🚲 Pola Penyewaan Sepeda')
st.caption('Analisis data penyewaan sepeda 2011–2012')
st.write('Dashboard ini memperlihatkan pola harian, jam sibuk, dan hasil pengelompokan jam. Semua angka berasal dari dataset yang disertakan dalam proyek.')

try:
    day, hour = ambil_data()
except FileNotFoundError:
    st.error('File data/day.csv dan data/hour.csv belum ditemukan. Periksa struktur folder proyek.')
    st.stop()

pilihan_tahun = st.sidebar.selectbox('Tahun', ['2011–2012', 2011, 2012])
if pilihan_tahun != '2011–2012':
    day = day[day['dteday'].dt.year == pilihan_tahun].copy()
    hour = hour[hour['dteday'].dt.year == pilihan_tahun].copy()

if day.empty or hour.empty:
    st.warning('Tidak ada catatan untuk tahun yang dipilih.')
    st.stop()

jumlah_total = int(day['cnt'].sum())
rata_harian = float(day['cnt'].mean())
anggota_terdaftar = float(day['registered'].sum() / day['cnt'].sum() * 100)
k1, k2, k3 = st.columns(3)
k1.metric('Total penyewaan', f'{jumlah_total:,}'.replace(',', '.'))
k2.metric('Rata-rata per hari', f'{rata_harian:,.0f}'.replace(',', '.'))
k3.metric('Porsi registered', f'{anggota_terdaftar:.1f}%')

st.sidebar.caption('Pilih tahun untuk memperbarui semua grafik di bawah.')
tab_bulan, tab_jam, tab_kelompok = st.tabs(['Bulanan dan musim', 'Jam sibuk', 'Pengelompokan jam'])

with tab_bulan:
    st.subheader('Perubahan menurut bulan')
    day['bulan_tahun'] = day['dteday'].dt.strftime('%Y-%m')
    bulanan = day.groupby('bulan_tahun')['cnt'].mean().sort_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(bulanan.index, bulanan.values, color=WARNA, marker='o', linewidth=2, markersize=4)
    ax.set_title('Rata-rata penyewaan per hari menurut bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Penyewaan per hari (rata-rata)')
    ax.tick_params(axis='x', rotation=60)
    ax.grid(axis='y', alpha=0.2)
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.write(f'Bulan tertinggi: **{bulanan.idxmax()}** dengan rata-rata **{bulanan.max():,.1f} penyewaan/hari**.')

    nama_musim = {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'}
    day['nama_musim'] = day['season'].map(nama_musim)
    musim = day.groupby('nama_musim')['cnt'].mean().reindex(['Semi', 'Panas', 'Gugur', 'Dingin'])
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(musim.index, musim.values, color=['#9DBFC6', '#65A6AF', WARNA, '#C5D8D9'])
    ax.set_ylim(0, musim.max() * 1.2)
    ax.set_ylabel('Penyewaan per hari (rata-rata)')
    ax.set_title('Rata-rata penyewaan menurut musim')
    ax.bar_label(bars, fmt='%.0f', padding=3)
    ax.grid(axis='y', alpha=0.2)
    ax.set_axisbelow(True)
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with tab_jam:
    st.subheader('Jam yang paling ramai')
    hour['jenis_hari'] = hour['workingday'].map({1: 'Hari kerja', 0: 'Bukan hari kerja'})
    rataan_jam = hour.groupby(['hr','jenis_hari'])['cnt'].mean().unstack().reindex(range(24))
    fig, ax = plt.subplots(figsize=(10, 4))
    for jenis, warna in [('Hari kerja', WARNA), ('Bukan hari kerja', WARNA_2)]:
        ax.plot(rataan_jam.index, rataan_jam[jenis], label=jenis, linewidth=2,
                marker='o', markersize=3, color=warna)
    ax.set_title('Rata-rata penyewaan per catatan jam')
    ax.set_xlabel('Jam (00–23)')
    ax.set_ylabel('Penyewaan per catatan jam (rata-rata)')
    ax.set_xticks(range(0,24,2))
    ax.set_ylim(bottom=0)
    ax.grid(axis='y', alpha=0.2)
    ax.legend(frameon=False)
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    col_kerja, col_libur = st.columns(2)
    for col, jenis in [(col_kerja, 'Hari kerja'), (col_libur, 'Bukan hari kerja')]:
        jam_puncak = int(rataan_jam[jenis].idxmax())
        col.metric(f'Puncak · {jenis}', f'{jam_puncak:02d}.00')
        col.caption(f'Rata-rata {rataan_jam[jenis].max():,.1f} penyewaan per catatan jam')

with tab_kelompok:
    st.subheader('Analisis lanjutan: binning waktu')
    st.write('Pembagian jam menggunakan aturan manual: dini hari 00–05, pagi 06–09, siang 10–15, sore 16–19, dan malam 20–23. Tidak menggunakan machine learning.')
    hour['jenis_hari'] = hour['workingday'].map({1: 'Hari kerja', 0: 'Bukan hari kerja'})
    urutan = ['Dini hari', 'Pagi', 'Siang', 'Sore', 'Malam']
    hour['kelompok'] = pd.cut(hour['hr'], bins=[-1,5,9,15,19,23],labels=urutan)
    hasil = hour.groupby(['kelompok','jenis_hari'], observed=True)['cnt'].mean().unstack().reindex(urutan)
    st.dataframe(hasil.round(1), use_container_width=True)
    fig, ax = plt.subplots(figsize=(9, 4))
    hasil[['Hari kerja', 'Bukan hari kerja']].plot(kind='bar', ax=ax, color=[WARNA, WARNA_2])
    ax.set_ylim(0, hasil.max().max() * 1.2)
    ax.set_title('Rata-rata penyewaan menurut kelompok waktu')
    ax.set_xlabel('Kelompok waktu')
    ax.set_ylabel('Penyewaan per catatan jam (rata-rata)')
    ax.tick_params(axis='x', rotation=0)
    ax.legend(title='Jenis hari', frameon=False)
    ax.grid(axis='y', alpha=0.2)
    ax.set_axisbelow(True)
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption('Kelompok memiliki panjang waktu berbeda. Rata-rata per catatan jam dipakai agar perbandingan tidak tergantung jumlah jam dalam kelompok.')

st.divider()
st.caption('Catatan: angka adalah jumlah penyewaan, bukan pelanggan unik. Beberapa tanggal memiliki kurang dari 24 catatan jam. Analisis ini bersifat deskriptif dan tidak membuktikan sebab-akibat.')
