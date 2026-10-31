# Proyek Analisis Data Bike Sharing

Proyek ini menggunakan `day.csv` dan `hour.csv` untuk melihat perubahan penyewaan sepeda dari waktu ke waktu. Data yang dianalisis adalah catatan 1 Januari 2011 sampai 31 Desember 2012. Analisis menggunakan Pandas dan Matplotlib, sedangkan dashboard dibuat dengan Streamlit.

## Pertanyaan bisnis

1. Bagaimana perubahan rata-rata penyewaan sepeda harian menurut bulan dan musim selama periode 1 Januari 2011 hingga 31 Desember 2012?
2. Pada jam berapa rata-rata penyewaan sepeda tertinggi terjadi pada hari kerja dan bukan hari kerja selama periode 1 Januari 2011 hingga 31 Desember 2012?

Pertanyaan pertama dijawab menggunakan data harian melalui grafik rata-rata penyewaan per bulan dan per musim. Pertanyaan kedua dijawab menggunakan data per jam melalui grafik yang membandingkan hari kerja dengan bukan hari kerja. Dashboard juga menyediakan filter tahun dan analisis binning sebagai analisis lanjutan tanpa machine learning.

## Struktur folder

```text
submisi-data-analyst/
├── dashboard/
│   └── dashboard.py
├── data/
│   ├── day.csv
│   └── hour.csv
├── main-data.ipynb
├── requirements.txt
├── README.md
└── url.txt
```

## Menjalankan dashboard dari VS Code (Windows)

**1.** Ekstrak ZIP, kemudian buka folder `submisi-data-analyst` melalui **File > Open Folder** di VS Code. Buka terminal di folder ini, bukan di dalam `.venv/Scripts`.

**2.** Buat lingkungan virtual Python dari terminal PowerShell:

```powershell
py -m venv .venv
```

**3.** Instal library yang tercantum dalam `requirements.txt`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**4.** Jalankan dashboard:

```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard/dashboard.py
```

Buka alamat yang muncul di terminal, biasanya `http://localhost:8501`. Perintah di atas tidak memerlukan aktivasi PowerShell sehingga tetap bisa digunakan jika kebijakan eksekusi skrip membatasi `Activate.ps1`.

Jika lingkungan virtual sudah dibuat sebelumnya di folder lain, gunakan interpreter yang sesuai atau buat ulang `.venv` di folder proyek ini. Jangan memindahkan file `dashboard.py` ke dalam folder `.venv`.

## Menjalankan dashboard di macOS / Linux

Jalankan perintah berikut dari folder proyek:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run dashboard/dashboard.py
```

## Menjalankan notebook di Google Colab

1. Buka `main-data.ipynb` melalui Google Colab.
2. Seret `day.csv` dan `hour.csv` ke panel **Files** sehingga kedua file berada di `/content/`.
3. Pilih **Runtime > Run all**.
4. Simpan notebook setelah output muncul.

Notebook juga bisa dijalankan dari folder proyek ini karena kode otomatis mencari kedua file di `data/`. File notebook dalam ZIP ini sudah dijalankan menggunakan kedua CSV asli.

## Deploy ke Streamlit Community Cloud

1. Buat repository GitHub baru, lalu unggah **isi folder proyek** (bukan berkas ZIP). Pastikan `dashboard/`, `data/`, `requirements.txt`, dan `README.md` berada langsung di root repository.
2. Masuk ke https://share.streamlit.io/ dan buat aplikasi dari repository tersebut.
3. Pilih branch yang digunakan (umumnya `main`) dan set **main file path** menjadi `dashboard/dashboard.py`.
4. Setelah aplikasi online, buka URL publik dan uji: grafik bulanan dan musiman, grafik jam sibuk, tab binning, serta filter **Semua tahun / 2011 / 2012**.
5. Tulis URL publik yang benar di `url.txt`, lalu kompres ulang folder proyek menjadi ZIP untuk submission.

Jika perubahan kode sudah diunggah ke GitHub tetapi dashboard belum berubah, periksa commit yang terhubung di Streamlit Cloud dan lakukan reboot/redeploy aplikasi bila diperlukan.

## Ringkasan hasil dari dataset

- Data harian mencakup **731 tanggal**, sedangkan data per jam berisi **17.379 baris**. Total penyewaan adalah **3.292.679**.
- **September 2012** memiliki rata-rata penyewaan harian tertinggi, sekitar **7.285,8** per hari.
- Menurut musim, rata-rata harian tertinggi adalah musim gugur, sekitar **5.644,3** per hari (gabungan dua tahun).
- Pada **hari kerja**, jam tertinggi adalah **17.00**, sekitar **525,3** penyewaan per catatan jam. Pada **bukan hari kerja**, puncaknya **13.00**, sekitar **372,7**.
- Binning dilakukan dengan `pd.cut()` untuk membuat kelompok dini hari, pagi, siang, sore, dan malam. Tidak ada algoritma machine learning yang digunakan.

## Catatan mengenai kualitas data

Tidak ditemukan nilai kosong atau duplikasi. Total data harian sesuai dengan penjumlahan data per jam pada setiap tanggal. Beberapa tanggal tidak memiliki 24 catatan jam, sehingga hasil per jam menggunakan rata-rata dari baris yang tersedia. Penjelasan dalam notebook dan dashboard bersifat deskriptif dan tidak mengklaim hubungan sebab-akibat.
