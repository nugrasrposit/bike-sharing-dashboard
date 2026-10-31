# Proyek Analisis Data Bike Sharing

Proyek ini membahas pola penyewaan sepeda berdasarkan dua file: `day.csv` (harian) dan `hour.csv` (per jam). Data mencakup 1 Januari 2011 hingga 31 Desember 2012. Analisis dan dashboard memakai data yang sama, tetapi kedua file tidak digabung sebagai baris karena unit pengamatannya berbeda.

## Susunan berkas

```text
submission_bike_sharing_final/
├── dashboard/
│   └── dashboard.py
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Menjalankan notebook di Google Colab

1. Buka `notebook.ipynb` melalui Google Colab.
2. Dari panel **Files** (ikon folder), seret file `data/day.csv` dan `data/hour.csv` ke folder `/content/`. Pengguna tidak perlu menghubungkan Google Drive.
3. Klik **Runtime → Run all**.
4. Notebook juga bisa dijalankan langsung dari folder hasil ekstraksi ZIP jika `data/` tetap di lokasi yang sama. Notebook dalam ZIP sudah disertai hasil eksekusi dengan CSV asli.

## Menjalankan dashboard secara lokal

Dari folder proyek, jalankan:

```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

Browser akan menampilkan alamat lokal yang diberikan Streamlit, biasanya `http://localhost:8501`. Dashboard membaca langsung dari folder `data/`, sehingga tidak perlu mengunggah CSV lagi saat menjalankannya secara lokal.

## Cara deploy ke Streamlit Community Cloud

1. Ekstrak ZIP, lalu unggah seluruh isi folder proyek ke repositori GitHub milik Anda. Pastikan folder `data/` ikut terunggah.
2. Masuk ke https://share.streamlit.io/ dan pilih **Create app**.
3. Pilih repositori dan branch, lalu isi path berkas utama: **`dashboard/dashboard.py`**.
4. Lakukan deployment. Setelah aplikasi dapat dibuka, salin tautan publiknya ke `url.txt`, kemudian kemas ulang folder proyek menjadi ZIP untuk submission.
5. Jangan mengisi `url.txt` dengan tautan contoh atau URL lokal.

## Pertanyaan dan metode

1. Bagaimana perubahan rata-rata penyewaan sepeda per hari menurut bulan dan musim? → Analisis `day.csv` menggunakan `groupby`, tabel rata-rata, grafik garis, dan grafik batang.
2. Pada jam berapa penyewaan sepeda paling ramai, dan bagaimana perbedaannya antara hari kerja dan bukan hari kerja? → Analisis `hour.csv` menggunakan `groupby`, grafik dua garis, serta **binning manual** menggunakan `pd.cut()`.

## Temuan utama dari data asli

- Jumlah penyewaan keseluruhan: **3.292.679**, mencakup 731 hari dan 17.379 baris data per jam.
- September 2012 memiliki rata-rata harian tertinggi (**7.285,8** penyewaan/hari).
- Rata-rata harian tertinggi menurut musim adalah musim gugur (**5.644,3** penyewaan/hari).
- Hari kerja paling ramai pukul **17.00** (**525,3** penyewaan per catatan jam); bukan hari kerja pukul **13.00** (**372,7** per catatan jam).
- Melalui binning, kelompok sore (16–19) paling ramai pada hari kerja, sedangkan kelompok siang (10–15) paling ramai pada bukan hari kerja.

## Catatan kualitas data

Tidak ditemukan nilai kosong, duplikasi, angka negatif, atau perbedaan antara `cnt` dengan `casual + registered`. Nilai total harian dari `day.csv` sesuai dengan penjumlahan per jam dari `hour.csv`. Sebanyak **76 hari** memiliki kurang dari 24 baris jam; jam yang tidak tercatat tidak diisi otomatis dengan nol. Rata-rata berdasarkan `hour.csv` dibaca sebagai rata-rata per jam **yang tercatat**. Hasil hanya menggambarkan pola historis pada 2011–2012 dan tidak menyimpulkan sebab-akibat.

## Sebelum submission

- Isi nama, email, dan ID Dicoding pada bagian awal notebook.
- Pastikan notebook tetap tersimpan dengan seluruh output setelah pembaruan.
- Lakukan deployment dashboard ke Streamlit Cloud, lalu isi `url.txt` dengan tautan sebenarnya.
- Kirim satu file ZIP yang berisi seluruh folder proyek, termasuk kedua dataset asli.
