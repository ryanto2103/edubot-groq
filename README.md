# EduBot-Groq

Chatbot asisten belajar berbasis Streamlit dan xAI Groq API.

## Fitur

- 10 mata pelajaran (Matematika, Fisika, Kimia, Biologi, Sejarah, Bahasa Indonesia, Bahasa Inggris, Pemrograman, Ekonomi, Umum)
- Pilihan tingkat pendidikan: SD, SMP, SMA, Kuliah
- Tiga gaya jawaban: Santai, Formal, Singkat
- Sapaan personal berdasarkan nama siswa
- Streaming respon real-time
- UI putih bersih, tanpa dekorasi berlebihan

## Instalasi

```bash
git clone https://github.com/username/edubot.git
cd edubot
pip install -r requirements_groq.txt
streamlit run edubot_groq.py
```

## Penggunaan

1. Buka aplikasi di browser (`http://localhost:8501`)
2. Masukkan Groq API Key di sidebar — daftar di [console.groq.com](https://console.groq.com)
3. Pilih mata pelajaran, tingkat pendidikan, dan gaya jawaban
4. Mulai bertanya

## File

```
edubot_groq.py          # Aplikasi utama
requirements_groq.txt   # Dependensi
README.md               # Dokumentasi ini
```

## Dependensi

```
streamlit>=1.35.0
groq>=0.9.0
```

## Model yang Didukung

| Model | Keterangan |
|---|---|
| llama-3.3-70b-versatile | Ringan, cepat, hemat (default) |
| groq-3 | Paling canggih |
| mixtral-8x7b-32768 | Cepat |
| llama-3.3-70b-versatile-fast | Paling cepat |
