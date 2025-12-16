# 🚀 QUICK START GUIDE

## Cara Cepat Menjalankan Aplikasi

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
streamlit run elearning_recommendation_app.py
```

### 3. Upload Dataset
- Buka aplikasi di browser (otomatis terbuka)
- Klik "Upload File CSV" di sidebar kiri
- Pilih file `student_info.csv`

### 4. Mulai Training
- Pindah ke tab "Training Model"
- (Opsional) Sesuaikan parameter di sidebar:
  - Learning Rate: 0.1 (default)
  - Discount Factor: 0.9 (default)
  - Epsilon: 0.1 (default)
  - Episodes: 100 (default)
- Klik tombol "🚀 Mulai Training"
- Tunggu proses selesai (~10-30 detik)

### 5. Dapatkan Rekomendasi
- Pindah ke tab "Rekomendasi"
- Masukkan data siswa menggunakan slider dan dropdown:
  - Math Score
  - Reading Score
  - Writing Score
  - Gender
  - Grade Level
  - Internet Access
  - Extra Activities
  - Study Hours
- Klik "🎯 Dapatkan Rekomendasi"
- Lihat hasil rekomendasi materi pembelajaran

### 6. Eksplorasi Fitur Lain
- Tab "Eksplorasi Data": Visualisasi dan analisis dataset
- Tab "Analisis Hasil": Evaluasi model dan policy
- Tab "Profil Siswa": Lihat detail siswa individual

## 📝 Tips & Trik

### Untuk Hasil Training Optimal:
- Gunakan Learning Rate 0.1 untuk pembelajaran stabil
- Set Episodes minimal 100 untuk konvergensi baik
- Epsilon 0.1 untuk balance eksplorasi-eksploitasi

### Untuk Rekomendasi Akurat:
- Pastikan input data siswa sesuai dengan profil sebenarnya
- Perhatikan kategori performa yang ditampilkan
- Bandingkan Q-values untuk melihat kepercayaan model

### Untuk Analisis Mendalam:
- Lihat heatmap Q-Table untuk memahami policy
- Perhatikan grafik konvergensi training
- Bandingkan profil siswa dengan rata-rata kelas

## 🎯 Contoh Use Case

### Skenario 1: Siswa Berprestasi Rendah
```
Input:
- Math Score: 50
- Reading Score: 55
- Writing Score: 52
- Study Hours: 1.5

Output:
- Performance: Low
- Recommendation: Materi Dasar + Video Tutorial
- Study Plan: 1-2 jam/hari intensitas rendah
```

### Skenario 2: Siswa Berprestasi Tinggi
```
Input:
- Math Score: 95
- Reading Score: 92
- Writing Score: 94
- Study Hours: 4.5

Output:
- Performance: Excellent
- Recommendation: Materi Olimpiade + Research
- Study Plan: 3.5-5 jam/hari intensitas tinggi
```

## ⚠️ Common Issues

### Issue: Port already in use
**Solution:**
```bash
streamlit run elearning_recommendation_app.py --server.port 8502
```

### Issue: Module not found
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: CSV upload error
**Solution:**
- Pastikan format CSV sesuai dengan contoh
- Cek encoding file (harus UTF-8)
- Pastikan semua kolom tersedia

## 📞 Need Help?

Jika mengalami masalah:
1. Baca dokumentasi lengkap di README.md
2. Cek troubleshooting section
3. Pastikan semua dependencies terinstall
4. Restart aplikasi dan browser

---
Happy Learning! 📚✨
