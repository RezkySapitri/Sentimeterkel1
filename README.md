# 📚 Sistem Rekomendasi E-Learning Berbasis Reinforcement Learning

Aplikasi web berbasis Streamlit untuk sistem rekomendasi materi pembelajaran e-learning menggunakan algoritma Q-Learning (Reinforcement Learning).

## 👤 Informasi Peneliti
- **Nama:** Siti Rahma Alia
- **NIM:** 20230040023
- **Dosen Pengampu:** Ir. Somantri, S.T, M.Kom
- **Mata Kuliah:** Metode Penelitian

## 🎯 Tujuan Penelitian
Mengembangkan sistem rekomendasi e-learning berbasis Reinforcement Learning yang mampu:
1. Mempersonalisasi materi pembelajaran berdasarkan perilaku pengguna
2. Mengoptimalkan algoritma RL untuk meningkatkan relevansi rekomendasi
3. Meningkatkan efektivitas pembelajaran dibandingkan metode konvensional

## ✨ Fitur Utama

### 1. 📊 Eksplorasi Data
- Visualisasi distribusi data siswa
- Analisis performa akademik
- Korelasi antar variabel
- Statistik deskriptif lengkap

### 2. 🤖 Training Model Q-Learning
- Implementasi algoritma Q-Learning
- Parameter yang dapat disesuaikan (learning rate, discount factor, epsilon)
- Visualisasi training progress
- Q-Table interaktif

### 3. 🎯 Sistem Rekomendasi
- Rekomendasi materi pembelajaran adaptif
- Input data siswa secara interaktif
- Visualisasi Q-values per action
- Rencana belajar yang dipersonalisasi

### 4. 📈 Analisis Hasil
- Evaluasi policy optimal
- Heatmap Q-Table
- Metrik performa model
- Analisis konvergensi

### 5. 👤 Profil Siswa
- Detail informasi siswa individual
- Perbandingan dengan rata-rata kelas
- Radar chart performa
- Rekomendasi personal

## 🚀 Cara Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah-langkah Instalasi

1. **Clone atau Download repository**
   ```bash
   # Jika menggunakan git
   git clone <repository-url>
   cd elearning-recommendation
   
   # Atau extract file ZIP yang didownload
   ```

2. **Buat Virtual Environment (Opsional tapi Direkomendasikan)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Cara Menjalankan Aplikasi

1. **Pastikan berada di folder yang tepat**
   ```bash
   # Pastikan file elearning_recommendation_app.py ada di folder ini
   ls -l  # Linux/Mac
   dir    # Windows
   ```

2. **Jalankan Streamlit**
   ```bash
   streamlit run elearning_recommendation_app.py
   ```

3. **Akses Aplikasi**
   - Browser akan terbuka otomatis
   - Jika tidak, buka: http://localhost:8501
   - Untuk akses dari jaringan lokal: http://[IP-ADDRESS]:8501

## 📁 Struktur File

```
project/
│
├── elearning_recommendation_app.py   # File aplikasi utama
├── requirements.txt                  # Dependencies Python
├── README.md                         # Dokumentasi (file ini)
└── student_info.csv                  # Dataset (harus diupload)
```

## 📊 Format Dataset

File CSV harus memiliki kolom berikut:

| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| student_id | String | ID unik siswa |
| name | String | Nama siswa |
| gender | String | Jenis kelamin (Male/Female/Other) |
| age | Integer | Usia siswa |
| grade_level | Integer | Tingkat kelas (9-12) |
| math_score | Integer | Nilai matematika (0-100) |
| reading_score | Integer | Nilai reading (0-100) |
| writing_score | Integer | Nilai writing (0-100) |
| attendance_rate | Float | Tingkat kehadiran (0-100%) |
| parent_education | String | Pendidikan orang tua |
| study_hours | Float | Jam belajar per hari |
| internet_access | String | Akses internet (Yes/No) |
| lunch_type | String | Tipe makan siang |
| extra_activities | String | Aktivitas ekstrakurikuler (Yes/No) |
| final_result | String | Hasil akhir (Pass/Fail) |

## 🔧 Parameter Q-Learning

### Learning Rate (α)
- **Range:** 0.01 - 1.0
- **Default:** 0.1
- **Fungsi:** Menentukan seberapa cepat agent belajar dari pengalaman baru

### Discount Factor (γ)
- **Range:** 0.0 - 1.0
- **Default:** 0.9
- **Fungsi:** Menentukan pentingnya reward masa depan

### Epsilon (ε)
- **Range:** 0.0 - 1.0
- **Default:** 0.1
- **Fungsi:** Menentukan probabilitas eksplorasi vs eksploitasi

### Episodes
- **Range:** 50 - 500
- **Default:** 100
- **Fungsi:** Jumlah iterasi training

## 📖 Cara Menggunakan Aplikasi

### 1. Upload Dataset
- Klik tombol "Upload File CSV" di sidebar
- Pilih file `student_info.csv`
- Data akan otomatis diproses

### 2. Eksplorasi Data
- Tab pertama menampilkan visualisasi data
- Analisis distribusi, korelasi, dan statistik
- Pahami karakteristik dataset

### 3. Training Model
- Pindah ke tab "Training Model"
- Sesuaikan parameter jika diperlukan
- Klik tombol "Mulai Training"
- Tunggu hingga proses selesai
- Lihat grafik training progress

### 4. Mendapatkan Rekomendasi
- Pindah ke tab "Rekomendasi"
- Input data siswa (score, demografi, dll)
- Klik "Dapatkan Rekomendasi"
- Sistem akan menampilkan:
  - Kategori performa
  - Materi yang direkomendasikan
  - Rencana belajar
  - Visualisasi Q-values

### 5. Analisis Hasil
- Tab "Analisis Hasil" menampilkan:
  - Policy optimal
  - Heatmap Q-Table
  - Metrik performa
  - Grafik konvergensi

### 6. Profil Siswa
- Pilih student_id dari dropdown
- Lihat profil lengkap siswa
- Bandingkan dengan rata-rata kelas
- Dapatkan rekomendasi personal

## 🎨 Screenshot & Preview

### Dashboard Utama
```
┌─────────────────────────────────────────┐
│  📚 Sistem Rekomendasi E-Learning       │
│  Berbasis Reinforcement Learning        │
├─────────────────────────────────────────┤
│  Sidebar:                                │
│  • Upload CSV                            │
│  • Parameter Settings                    │
│                                          │
│  Tabs:                                   │
│  📊 Eksplorasi Data                      │
│  🤖 Training Model                       │
│  🎯 Rekomendasi                          │
│  📈 Analisis Hasil                       │
│  👤 Profil Siswa                         │
└─────────────────────────────────────────┘
```

## 🔬 Metodologi Penelitian

### Algoritma Q-Learning
```
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
```

Dimana:
- Q(s,a): Q-value untuk state s dan action a
- α: Learning rate
- r: Reward
- γ: Discount factor
- s': Next state
- a': Next action

### State Representation
- **State 0:** Low Performance (avg_score < 60)
- **State 1:** Medium Performance (60 ≤ avg_score < 75)
- **State 2:** High Performance (75 ≤ avg_score < 90)
- **State 3:** Excellent Performance (avg_score ≥ 90)

### Action Space
- **Action 0:** Intensitas Belajar Rendah (1-2 jam/hari)
- **Action 1:** Intensitas Belajar Sedang (2-3.5 jam/hari)
- **Action 2:** Intensitas Belajar Tinggi (3.5-5 jam/hari)

### Reward Function
```
Reward = +5  jika Pass
Reward = -5  jika Fail
```

## 🐛 Troubleshooting

### Error: ModuleNotFoundError
```bash
# Install ulang dependencies
pip install -r requirements.txt --upgrade
```

### Error: Port sudah digunakan
```bash
# Gunakan port lain
streamlit run elearning_recommendation_app.py --server.port 8502
```

### Error: File tidak ditemukan
```bash
# Pastikan file CSV ada di folder yang sama
# Atau upload melalui interface aplikasi
```

### Aplikasi loading lambat
```bash
# Kurangi jumlah episodes di parameter
# Atau gunakan dataset yang lebih kecil
```

## 📚 Referensi

Berdasarkan penelitian dari:

1. Tjahyanti (2017) - Arsitektur E-Learning dalam Standar Pendidikan
2. Pratiwi et al. (2022) - Personalisasi Belajar dalam Pembelajaran Daring
3. Andreanus & Kurniawan (2018) - Reinforcement Learning: Teori dan Penerapan
4. Waisen et al. (2025) - Sistem Rekomendasi Kurikulum Personal Berbasis CLT dan RL

## 🤝 Kontribusi

Untuk pertanyaan, saran, atau kontribusi:
- **Email:** [email-anda]
- **GitHub:** [github-profile]

## 📄 Lisensi

Proyek ini dibuat untuk keperluan penelitian akademik.

## 🙏 Acknowledgments

Terima kasih kepada:
- Ir. Somantri, S.T, M.Kom sebagai dosen pengampu
- Universitas/Institusi [Nama Institusi]
- Semua pihak yang telah mendukung penelitian ini

---

**Last Updated:** Desember 2024
**Version:** 1.0.0

Made with ❤️ using Streamlit
