import streamlit as st
from cryptography.fernet import Fernet
import os

# ---------- Save/load encryption key ----------
KEY_FILE = "secret.key"

def save_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    return save_key()

cipher = Fernet(load_key())

# ---------- Encrypt/Decrypt ----------
def encrypt_text(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(token):
    try:
        return cipher.decrypt(token.encode()).decode()
    except Exception:
        return None

# ---------- Streamlit App ----------
st.set_page_config(page_title="Secure Vault 🔐", page_icon="🔒", layout="centered")

# Header
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🔐 Secure Data Encryption App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>✨ Made by <strong style='color: #FF5722;'>Asad Shabir</strong></p>", unsafe_allow_html=True)

# Custom Menu
menu = st.selectbox("📁 Choose an option:", ["🏠 Home", "🔒 Encrypt Data", "🔓 Decrypt Data"])

# Home
if menu == "🏠 Home":
    st.success("Welcome! Use this app to securely encrypt and decrypt your sensitive data.")
    st.info("🔐 Your data is encrypted using Fernet encryption and stored only temporarily in memory.")

# Encrypt Section
elif menu == "🔒 Encrypt Data":
    st.subheader("🔒 Store Your Secret")
    secret_text = st.text_area("Enter text to encrypt:")
    
    if st.button("Encrypt 🔐"):
        if secret_text:
            encrypted = encrypt_text(secret_text)
            st.success("✅ Encrypted Text:")
            st.code(encrypted, language="text")
        else:
            st.warning("⚠️ Please enter some text.")

# Decrypt Section
elif menu == "🔓 Decrypt Data":
    st.subheader("🔓 Get Back Your Secret")
    enc_input = st.text_area("Paste encrypted text here:")

    if st.button("Decrypt 🔓"):
        if enc_input:
            result = decrypt_text(enc_input)
            if result:
                st.success("✅ Decrypted Text:")
                st.code(result, language="text")
            else:
                st.error("❌ Failed! Check encrypted text.")
        else:
            st.warning("⚠️ Please provide encrypted input.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>🔐 End-to-End Encryption | Streamlit UI | 💻 Python Project</p>", unsafe_allow_html=True)
