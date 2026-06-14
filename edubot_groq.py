import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="EduBot",
    page_icon=None,
    layout="centered",
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: #ffffff;
    color: #111111;
}
.stApp { background-color: #ffffff; }
.main .block-container { max-width: 720px; padding: 2rem 1.5rem 6rem 1.5rem; }
h1 { font-size: 1.4rem !important; font-weight: 600 !important; color: #111 !important; margin-bottom: 0.1rem !important; }
[data-testid="stSidebar"] { background-color: #f9f9f9 !important; border-right: 1px solid #e5e5e5 !important; }
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }
[data-testid="stSidebar"] label { font-size: 0.82rem !important; color: #555 !important; font-weight: 500 !important; }
[data-testid="stSidebar"] h3 { font-size: 0.95rem !important; font-weight: 600 !important; color: #111 !important; }
.stButton > button {
    background-color: #111 !important; color: #fff !important; border: none !important;
    border-radius: 6px !important; font-size: 0.82rem !important; font-weight: 500 !important;
    padding: 0.4rem 0.9rem !important; width: 100% !important;
}
.stButton > button:hover { background-color: #333 !important; }
[data-testid="stChatMessage"] { border-radius: 8px !important; margin-bottom: 0.5rem !important; padding: 0.75rem 1rem !important; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background-color: #f3f3f3 !important; border: 1px solid #e8e8e8 !important; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) { background-color: #ffffff !important; border: 1px solid #e8e8e8 !important; }
[data-testid="stChatMessageContent"] p { font-size: 0.9rem !important; line-height: 1.7 !important; color: #111 !important; }
[data-testid="stChatInput"] { border: 1px solid #ddd !important; border-radius: 8px !important; background-color: #fff !important; }
[data-testid="stChatInput"] textarea { font-size: 0.9rem !important; color: #111 !important; }
#MainMenu, footer, header { visibility: hidden; }
hr { border: none !important; border-top: 1px solid #e5e5e5 !important; margin: 1rem 0 !important; }
.stCaption { font-size: 0.78rem !important; color: #999 !important; }
.stAlert { border-radius: 6px !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Konfigurasi EduBot ──────────────────────────────────────────────
MATA_PELAJARAN = {
    "Matematika":       "matematika: aljabar, geometri, kalkulus, statistika, aritmatika",
    "Fisika":           "fisika: mekanika, termodinamika, listrik, optika, gelombang",
    "Kimia":            "kimia: stoikiometri, ikatan kimia, reaksi, periodik unsur",
    "Biologi":          "biologi: sel, genetika, ekosistem, evolusi, anatomi",
    "Sejarah":          "sejarah Indonesia dan dunia",
    "Bahasa Indonesia": "tata bahasa, sastra, menulis, membaca, ejaan",
    "Bahasa Inggris":   "grammar, vocabulary, reading, writing, speaking Bahasa Inggris",
    "Pemrograman":      "pemrograman: Python, JavaScript, algoritma, struktur data, web",
    "Ekonomi":          "ekonomi mikro dan makro, akuntansi dasar, bisnis",
    "Umum":             "semua mata pelajaran dan topik pendidikan umum",
}

TINGKAT = ["SD", "SMP", "SMA", "Kuliah"]

GAYA = {
    "Santai":  "Gunakan bahasa yang santai, ramah, dan mudah dipahami. Boleh pakai analogi sehari-hari.",
    "Formal":  "Gunakan bahasa yang formal dan akademis. Sistematik dan terstruktur.",
    "Singkat": "Jawab secara ringkas dan to the point. Hindari penjelasan panjang kecuali diminta.",
}

def build_system_prompt(mapel, tingkat, gaya, nama):
    topik = MATA_PELAJARAN[mapel]
    instruksi_gaya = GAYA[gaya]
    sapa = f" Nama siswa yang kamu bantu adalah {nama}." if nama.strip() else ""
    return f"""Kamu adalah EduBot, asisten belajar AI untuk pelajar Indonesia.{sapa}

Fokus bidang: {topik}.
Tingkat pendidikan siswa: {tingkat}.
Gaya komunikasi: {instruksi_gaya}

Panduan menjawab:
- Selalu jawab dalam Bahasa Indonesia (kecuali topik Bahasa Inggris).
- Sesuaikan kedalaman penjelasan dengan tingkat pendidikan siswa.
- Gunakan contoh konkret yang relevan.
- Jika ada rumus atau kode, tuliskan dengan rapi.
- Bantu siswa MEMAHAMI konsep, bukan sekadar memberi jawaban.
- Jika pertanyaan tidak terkait edukasi, arahkan kembali dengan sopan."""

# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.subheader("Pengaturan")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
    )
    st.caption("Untuk Mendapatkan API Key, Daftar di console.groq.com")

    st.markdown("---")

    nama = st.text_input("Nama kamu", placeholder="Opsional")

    mapel = st.selectbox("Mata pelajaran", list(MATA_PELAJARAN.keys()))

    tingkat = st.selectbox("Tingkat pendidikan", TINGKAT, index=2)

    gaya = st.selectbox("Gaya jawaban", list(GAYA.keys()))

    model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"],
        index=0,
    )

    st.markdown("---")

    if st.button("Reset percakapan"):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        n = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.caption(f"{n} pertanyaan dalam sesi ini")

# ── Header ───────────────────────────────────────────────────────────
st.title("EduBot")
st.caption(f"Asisten belajar · {mapel} · {tingkat} · Terintegrasikan dengan Groq")

# ── API key check ────────────────────────────────────────────────────
if not api_key:
    st.info("Masukkan Groq xAI API Key di sidebar untuk mulai belajar.")
    st.stop()

# ── Init client ──────────────────────────────────────────────────────
if "client" not in st.session_state or st.session_state.get("_last_key") != api_key:
    try:
        st.session_state.client = Groq(
            api_key=api_key,
        )
        st.session_state._last_key = api_key
        st.session_state.messages = []
    except Exception as e:
        st.error(f"Gagal membuat koneksi: {e}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Pesan sambutan ───────────────────────────────────────────────────
if not st.session_state.messages:
    sapa = f"Halo, {nama.strip()}! " if nama.strip() else "Halo! "
    with st.chat_message("assistant"):
        st.markdown(
            f"{sapa}Aku EduBot, siap bantu kamu belajar **{mapel}** untuk tingkat **{tingkat}**.\n\n"
            "Tanya apa saja — konsep, soal latihan, atau minta penjelasan ulang. Yuk mulai!"
        )

# ── Riwayat chat ─────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input ────────────────────────────────────────────────────────────
prompt = st.chat_input("Tanya sesuatu...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    system = build_system_prompt(mapel, tingkat, gaya, nama)
    api_messages = [{"role": "system", "content": system}] + st.session_state.messages

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            stream = st.session_state.client.chat.completions.create(
                model=model,
                messages=api_messages,
                temperature=0.7,
                max_tokens=1024,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

        except Exception as e:
            err = str(e)
            if "401" in err or "Unauthorized" in err:
                full_response = "API key tidak valid. Periksa kembali di console.groq.com."
            elif "429" in err:
                full_response = "Terlalu banyak permintaan. Tunggu sebentar lalu coba lagi."
            else:
                full_response = f"Terjadi kesalahan: {err}"
            placeholder.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
