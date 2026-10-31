from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

WARNA_BIRU = "#206D80"
WARNA_ORANYE = "#D18936"


def cari_folder_data():
    """Mencari folder 'data' tanpa bergantung pada posisi terminal."""
    lokasi_file = Path(__file__).resolve()
    kandidat = [
        lokasi_file.parent.parent / "data",  # dashboard/dashboard.py
        lokasi_file.parent / "data",         # dashboard.py di folder utama
        lokasi_file.parent,                  # CSV satu folder dengan dashboard.py
        Path.cwd() / "data",                 # saat dijalankan dari folder proyek
    ]
    for folder in kandidat:
        if (folder / "day.csv").is_file() and (folder / "hour.csv").is_file():
            return folder
    return None


@st.cache_data
def baca_dataset(folder_data):
    """Membaca CSV sekali dan mengubah kolom tanggal menjadi datetime."""
    day = pd.read_csv(Path(folder_data) / "day.csv")
    hour = pd.read_csv(Path(folder_data) / "hour.csv")
    day["dteday"] = pd.to_datetime(day["dteday"])
    hour["dteday"] = pd.to_datetime(hour["dteday"])
    return day, hour


def rapikan_grafik(ax):
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def format_angka(nilai):
    return f"{nilai:,.0f}".replace(",", ".")


# 1. Judul dan pembacaan data
st.title("🚲 Dashboard Penyewaan Sepeda")
st.write("Analisis penggunaan sepeda berdasarkan catatan harian dan per jam, 1 Januari 2011–31 Desember 2012.")
st.caption("Data digunakan untuk membandingkan pola waktu penyewaan, bukan untuk menghitung pelanggan unik.")

folder_data = cari_folder_data()
if folder_data is None:
    st.error("File day.csv dan hour.csv tidak ditemukan.")
    st.write("Pastikan kedua file berada dalam folder **data** seperti contoh berikut:")
    st.code("proyek/\n├── dashboard/\n│   └── dashboard.py\n└── data/\n    ├── day.csv\n    └── hour.csv", language="text")
    st.stop()

try:
    day, hour = baca_dataset(str(folder_data))
except (OSError, ValueError, KeyError) as error:
    st.error(f"Data gagal dibaca: {error}")
    st.stop()

kolom_day = {"dteday", "cnt", "registered", "season"}
kolom_hour = {"dteday", "cnt", "hr", "workingday"}
if not kolom_day.issubset(day.columns) or not kolom_hour.issubset(hour.columns):
    st.error("Kolom pada CSV tidak sesuai dengan dataset Bike Sharing yang digunakan.")
    st.stop()

# 2. Filter tahun
st.sidebar.header("Filter")
tahun_dipilih = st.sidebar.selectbox("Pilih tahun pengamatan", ["Semua tahun", "2011", "2012"])
if tahun_dipilih != "Semua tahun":
    tahun = int(tahun_dipilih)
    day = day.loc[day["dteday"].dt.year == tahun].copy()
    hour = hour.loc[hour["dteday"].dt.year == tahun].copy()

if day.empty or hour.empty:
    st.warning("Tidak ada data pada tahun yang dipilih.")
    st.stop()

# 3. Indikator utama
jumlah_sewa = int(day["cnt"].sum())
rata_sewa = day["cnt"].mean()
persen_registered = day["registered"].sum() / jumlah_sewa * 100 if jumlah_sewa else 0

k1, k2, k3 = st.columns(3)
k1.metric("Total penyewaan", format_angka(jumlah_sewa))
k2.metric("Rata-rata penyewaan per hari", format_angka(rata_sewa))
k3.metric("Pengguna terdaftar", f"{persen_registered:.1f}%")
st.caption("Jumlah penyewaan tidak sama dengan jumlah pelanggan unik.")

# 4. Analisis yang menjawab pertanyaan bisnis
tab_tren, tab_jam, tab_binning, tab_data = st.tabs(
    ["Pertanyaan 1: bulan & musim", "Pertanyaan 2: jam sibuk", "Binning (lanjutan)", "Data"]
)

with tab_tren:
    st.markdown("**Pertanyaan bisnis 1**")
    st.subheader("Bagaimana perubahan rata-rata penyewaan sepeda harian menurut bulan dan musim selama periode 1 Januari 2011 hingga 31 Desember 2012?")
    st.caption("Grafik bulanan dan musiman di bawah menjawab pertanyaan bisnis pertama.")
    day_bulanan = day.copy()
    day_bulanan["bulan"] = day_bulanan["dteday"].dt.to_period("M").astype(str)
    rata_bulanan = day_bulanan.groupby("bulan")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(rata_bulanan.index, rata_bulanan.values, marker="o", color=WARNA_BIRU)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata penyewaan per hari")
    ax.tick_params(axis="x", rotation=60)
    rapikan_grafik(ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.write(
        f"Rata-rata penyewaan harian tertinggi terjadi pada **{rata_bulanan.idxmax()}** "
        f"yaitu sekitar **{format_angka(rata_bulanan.max())} penyewaan per hari**."
    )

    st.subheader("Perbandingan rata-rata penyewaan menurut musim")
    nama_musim = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
    day_musim = day.copy()
    day_musim["musim"] = day_musim["season"].map(nama_musim)
    rata_musim = day_musim.groupby("musim")["cnt"].mean().reindex(
        ["Semi", "Panas", "Gugur", "Dingin"]
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(rata_musim.index, rata_musim.values, color=WARNA_BIRU)
    ax.bar_label(bars, fmt="%.0f", padding=3)
    ax.set_ylabel("Rata-rata penyewaan per hari")
    ax.set_ylim(0, rata_musim.max() * 1.2)
    rapikan_grafik(ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption("Grafik membandingkan rata-rata harian, bukan total per musim.")

with tab_jam:
    st.markdown("**Pertanyaan bisnis 2**")
    st.subheader("Pada jam berapa rata-rata penyewaan sepeda tertinggi terjadi pada hari kerja dan bukan hari kerja selama periode 1 Januari 2011 hingga 31 Desember 2012?")
    st.caption("Garis pada grafik menunjukkan rata-rata penyewaan pada masing-masing jam yang tercatat.")
    jam_df = hour.copy()
    jam_df["jenis_hari"] = jam_df["workingday"].map(
        {1: "Hari kerja", 0: "Bukan hari kerja"}
    )
    rata_jam = jam_df.groupby(["hr", "jenis_hari"])["cnt"].mean().unstack()
    rata_jam = rata_jam.reindex(range(24))

    fig, ax = plt.subplots(figsize=(10, 4))
    for kategori, warna in [
        ("Hari kerja", WARNA_BIRU),
        ("Bukan hari kerja", WARNA_ORANYE),
    ]:
        ax.plot(rata_jam.index, rata_jam[kategori], marker="o", markersize=3,
                label=kategori, color=warna)
    ax.set_xlabel("Jam (0–23)")
    ax.set_ylabel("Rata-rata penyewaan per catatan jam")
    ax.set_xticks(range(0, 24, 2))
    ax.set_ylim(bottom=0)
    ax.legend()
    rapikan_grafik(ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    kiri, kanan = st.columns(2)
    for kolom, kategori in [(kiri, "Hari kerja"), (kanan, "Bukan hari kerja")]:
        jam_puncak = int(rata_jam[kategori].idxmax())
        kolom.metric(f"Jam tersibuk · {kategori}", f"{jam_puncak:02d}.00")
        kolom.caption(
            f"Rata-rata {rata_jam[kategori].max():.1f} penyewaan pada catatan jam tersebut."
        )

with tab_binning:
    st.subheader("Analisis lanjutan: pengelompokan jam (binning)")
    st.write(
        "Jam dibagi secara manual menjadi lima kelompok: dini hari (00–05), "
        "pagi (06–09), siang (10–15), sore (16–19), dan malam (20–23). "
        "Pengelompokan ini tidak menggunakan machine learning."
    )
    data_kelompok = hour.copy()
    kelompok = ["Dini hari", "Pagi", "Siang", "Sore", "Malam"]
    data_kelompok["kelompok_jam"] = pd.cut(
        data_kelompok["hr"], bins=[-1, 5, 9, 15, 19, 23], labels=kelompok
    )
    data_kelompok["jenis_hari"] = data_kelompok["workingday"].map(
        {1: "Hari kerja", 0: "Bukan hari kerja"}
    )
    tabel_kelompok = (
        data_kelompok.groupby(["kelompok_jam", "jenis_hari"], observed=True)["cnt"]
        .mean()
        .unstack()
        .reindex(kelompok)
    )

    st.dataframe(tabel_kelompok.round(1), use_container_width=True)
    fig, ax = plt.subplots(figsize=(9, 4))
    tabel_kelompok[["Hari kerja", "Bukan hari kerja"]].plot(
        kind="bar", ax=ax, color=[WARNA_BIRU, WARNA_ORANYE]
    )
    ax.set_xlabel("Kelompok waktu")
    ax.set_ylabel("Rata-rata penyewaan per catatan jam")
    ax.tick_params(axis="x", rotation=0)
    ax.legend(title="Jenis hari")
    rapikan_grafik(ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption(
        "Karena panjang kelompok jam tidak sama, digunakan rata-rata per catatan jam "
        "agar kelompok yang lebih panjang tidak otomatis tampak lebih ramai."
    )

with tab_data:
    st.subheader("Dataset")
    st.write("**Data harian**")
    st.dataframe(day.head(10), use_container_width=True)
    st.write("**Data per jam**")
    st.dataframe(hour.head(10), use_container_width=True)

    selisih_total = int(day["cnt"].sum() - hour["cnt"].sum())
    st.write(f"Selisih total penyewaan data harian dan per jam: **{format_angka(selisih_total)}**")
    st.caption("Selisih nol menunjukkan total kedua tabel konsisten untuk tahun yang dipilih.")

st.divider()
st.caption(
    "Sumber: dataset Bike Sharing (day.csv dan hour.csv). Analisis ini bersifat deskriptif. "
    "Beberapa tanggal memiliki kurang dari 24 catatan jam, sehingga rata-rata per jam "
    "dihitung dari catatan jam yang tersedia. Hasil tidak membuktikan hubungan sebab-akibat."
)
