import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# App Title
st.set_page_config(page_title="🔐 Secure Data Vault", page_icon="🔐")
st.markdown("<h1 style='text-align: center; color: teal;'>🔐 Secure Data Encryption App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Made by <strong style='color: magenta;'>Asad Shabir</strong></p>", unsafe_allow_html=True)

# Setup state
if "vault" not in st.session_state:
    st.session_state.vault = {}

# Fernet Key
key = Fernet.generate_key()
cipher = Fernet(key)

# Functions
def hash_pass(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_text(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_text(enc, passkey):
    stored = st.session_state.vault.get(enc)
    if not stored:
        return None
    if stored["passkey"] == hash_pass(passkey):
        return cipher.decrypt(enc.encode()).decode()
    return None

# UI
tab1, tab2 = st.tabs(["🔒 Store Data", "🔓 Retrieve Data"])

with tab1:
    st.subheader("Save Your Secret")
    secret = st.text_area("Enter data:")
    passkey = st.text_input("Set a passkey:", type="password")
    if st.button("Encrypt & Store"):
        if secret and passkey:
            encrypted = encrypt_text(secret)
            st.session_state.vault[encrypted] = {"passkey": hash_pass(passkey)}
            st.success("✅ Data Encrypted & Stored!")
            st.code(encrypted)

with tab2:
    st.subheader("Get Back Your Data")
    enc_input = st.text_area("Paste encrypted text:")
    pass_input = st.text_input("Enter passkey:", type="password")
    if st.button("Decrypt"):
        result = decrypt_text(enc_input, pass_input)
        if result:
            st.success("🎉 Decrypted Successfully!")
            st.code(result)
        else:
            st.error("❌ Failed! Check encrypted text or passkey.")
