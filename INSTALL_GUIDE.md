# 🖥️ Panduan Instalasi per Sistem Operasi

## 📌 Daftar Isi
1. [Windows](#windows)
2. [macOS](#macos)
3. [Linux (Ubuntu/Debian)](#linux-ubuntudebian)
4. [Verifikasi Instalasi](#verifikasi-instalasi)

---

## Windows

### Prasyarat
1. **Python 3.8+**
   - Download dari: https://www.python.org/downloads/
   - ✅ Centang "Add Python to PATH" saat instalasi
   
2. **Git (Opsional)**
   - Download dari: https://git-scm.com/download/win

### Langkah Instalasi

#### Opsi 1: Menggunakan Command Prompt

1. **Buka Command Prompt**
   - Tekan `Win + R`
   - Ketik `cmd` dan Enter

2. **Navigasi ke folder project**
   ```cmd
   cd C:\path\to\your\project
   ```

3. **Buat Virtual Environment**
   ```cmd
   python -m venv venv
   ```

4. **Aktifkan Virtual Environment**
   ```cmd
   venv\Scripts\activate
   ```
   ✅ Anda akan melihat `(venv)` di awal command prompt

5. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

6. **Jalankan Aplikasi**
   ```cmd
   streamlit run elearning_recommendation_app.py
   ```

#### Opsi 2: Menggunakan PowerShell

1. **Buka PowerShell**
   - Tekan `Win + X`
   - Pilih "Windows PowerShell" atau "Terminal"

2. **Navigasi ke folder project**
   ```powershell
   cd C:\path\to\your\project
   ```

3. **Buat Virtual Environment**
   ```powershell
   python -m venv venv
   ```

4. **Aktifkan Virtual Environment**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   ⚠️ Jika muncul error "cannot be loaded because running scripts is disabled":
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

5. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

6. **Jalankan Aplikasi**
   ```powershell
   streamlit run elearning_recommendation_app.py
   ```

### Troubleshooting Windows

**Problem: Python tidak ditemukan**
```cmd
'python' is not recognized as an internal or external command
```
**Solution:**
1. Reinstall Python dan centang "Add to PATH"
2. Atau gunakan `py` instead of `python`
   ```cmd
   py -m venv venv
   ```

**Problem: pip tidak ditemukan**
```cmd
'pip' is not recognized...
```
**Solution:**
```cmd
python -m ensurepip --default-pip
```

**Problem: Port sudah digunakan**
**Solution:**
```cmd
streamlit run elearning_recommendation_app.py --server.port 8502
```

---

## macOS

### Prasyarat
1. **Python 3.8+**
   - Biasanya sudah terinstall
   - Cek versi: `python3 --version`
   - Jika belum ada, install via Homebrew:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     brew install python
     ```

2. **pip**
   - Biasanya sudah include dengan Python
   - Jika belum ada:
     ```bash
     python3 -m ensurepip --upgrade
     ```

### Langkah Instalasi

1. **Buka Terminal**
   - Tekan `Cmd + Space`
   - Ketik "Terminal" dan Enter

2. **Navigasi ke folder project**
   ```bash
   cd /path/to/your/project
   ```

3. **Buat Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

4. **Aktifkan Virtual Environment**
   ```bash
   source venv/bin/activate
   ```
   ✅ Anda akan melihat `(venv)` di awal terminal prompt

5. **Upgrade pip**
   ```bash
   pip install --upgrade pip
   ```

6. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

7. **Jalankan Aplikasi**
   ```bash
   streamlit run elearning_recommendation_app.py
   ```

### Troubleshooting macOS

**Problem: Permission denied**
```bash
PermissionError: [Errno 13] Permission denied
```
**Solution:**
```bash
sudo chown -R $USER /path/to/project
```

**Problem: SSL Certificate Error**
```bash
[SSL: CERTIFICATE_VERIFY_FAILED]
```
**Solution:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

**Problem: Command not found**
**Solution:**
```bash
# Tambahkan Python ke PATH
echo 'export PATH="/usr/local/opt/python/libexec/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Linux (Ubuntu/Debian)

### Prasyarat

1. **Update sistem**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Install Python 3 dan pip**
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```

3. **Install dependencies sistem (opsional)**
   ```bash
   sudo apt install build-essential libssl-dev libffi-dev python3-dev -y
   ```

### Langkah Instalasi

1. **Buka Terminal**
   - Tekan `Ctrl + Alt + T`

2. **Navigasi ke folder project**
   ```bash
   cd /path/to/your/project
   ```

3. **Buat Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

4. **Aktifkan Virtual Environment**
   ```bash
   source venv/bin/activate
   ```
   ✅ Anda akan melihat `(venv)` di awal terminal prompt

5. **Upgrade pip**
   ```bash
   pip install --upgrade pip
   ```

6. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

7. **Jalankan Aplikasi**
   ```bash
   streamlit run elearning_recommendation_app.py
   ```

### Troubleshooting Linux

**Problem: Module 'tkinter' not found**
```bash
pip install tk
```
Atau:
```bash
sudo apt-get install python3-tk
```

**Problem: Permission error saat install**
**Solution:**
```bash
pip install --user -r requirements.txt
```

**Problem: Port already in use**
```bash
# Cari process yang menggunakan port
sudo lsof -i :8501

# Kill process
sudo kill -9 <PID>

# Atau gunakan port lain
streamlit run elearning_recommendation_app.py --server.port 8502
```

---

## Verifikasi Instalasi

### 1. Cek Versi Python
```bash
python --version    # Windows
python3 --version   # macOS/Linux
```
✅ Output: `Python 3.8.x` atau lebih tinggi

### 2. Cek pip
```bash
pip --version
```
✅ Output: `pip 23.x.x from ...`

### 3. Cek Dependencies
```bash
pip list
```
✅ Harus muncul:
- streamlit
- pandas
- numpy
- plotly
- scikit-learn

### 4. Test Import
```bash
python -c "import streamlit; import pandas; import numpy; import plotly; import sklearn; print('All imports successful!')"
```
✅ Output: `All imports successful!`

### 5. Test Aplikasi
```bash
streamlit run elearning_recommendation_app.py
```
✅ Browser otomatis terbuka ke `http://localhost:8501`

---

## 🌐 Akses dari Jaringan Lokal

Untuk mengakses aplikasi dari komputer lain di jaringan yang sama:

### 1. Cari IP Address Anda

**Windows:**
```cmd
ipconfig
```
Cari "IPv4 Address"

**macOS/Linux:**
```bash
ifconfig
# atau
ip addr show
```
Cari "inet" address

### 2. Jalankan dengan Network Access

```bash
streamlit run elearning_recommendation_app.py --server.address 0.0.0.0
```

### 3. Akses dari Komputer Lain

Buka browser dan masukkan:
```
http://[IP-ADDRESS]:8501
```
Contoh: `http://192.168.1.100:8501`

---

## 📦 Instalasi Alternatif menggunakan Conda

Jika Anda menggunakan Anaconda/Miniconda:

### 1. Buat Environment
```bash
conda create -n elearning python=3.9
```

### 2. Aktifkan Environment
```bash
conda activate elearning
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
```bash
streamlit run elearning_recommendation_app.py
```

---

## 🐳 Instalasi menggunakan Docker (Advanced)

### 1. Buat Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "elearning_recommendation_app.py", "--server.address", "0.0.0.0"]
```

### 2. Build Image
```bash
docker build -t elearning-app .
```

### 3. Run Container
```bash
docker run -p 8501:8501 elearning-app
```

---

## 💡 Tips & Best Practices

### 1. Gunakan Virtual Environment
✅ **SELALU** gunakan virtual environment untuk menghindari konflik dependencies

### 2. Update Dependencies Secara Berkala
```bash
pip install --upgrade -r requirements.txt
```

### 3. Freeze Dependencies
Jika Anda memodifikasi project:
```bash
pip freeze > requirements.txt
```

### 4. Backup Project
```bash
# Menggunakan git
git init
git add .
git commit -m "Initial commit"
```

### 5. Monitor Resource Usage
```bash
# Windows
tasklist | findstr python

# macOS/Linux
top -p $(pgrep -f streamlit)
```

---

## 🆘 Bantuan Lebih Lanjut

Jika masih mengalami masalah:

1. **Cek dokumentasi resmi:**
   - Streamlit: https://docs.streamlit.io/
   - Python: https://docs.python.org/

2. **Cari error message di:**
   - Stack Overflow: https://stackoverflow.com/
   - GitHub Issues: https://github.com/streamlit/streamlit/issues

3. **Contact developer:**
   - Email: [your-email]
   - GitHub: [your-github]

---

**Happy Coding! 🚀**
