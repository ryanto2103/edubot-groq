# EduBot-Groq

Chatbot asisten belajar berbasis Streamlit dan xAI Groq API.

## Instalasi

```bash
git clone https://github.com/username/edubot.git
cd edubot
pip install -r requirements_groq.txt
streamlit run edubot_groq.py
```

## Cara Penggunaan

1. Buka aplikasi di browser (`http://localhost:8501`)
2. Masukkan Groq API Key di sidebar — daftar di [console.groq.com](https://console.groq.com)
3. Pilih mata pelajaran, tingkat pendidikan, dan gaya jawaban
4. Mulai bertanya

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
