# app_ui.py  – Streamlit front‑end for fastapi‑llama‑backend
import requests
import streamlit as st

# ── Config ────────────────────────────────────────────────────────────────
API_BASE = "http://127.0.0.1:8000"
DEFAULT_TOKEN = "token_alice"           # demo token

# ── Page setup ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LLaMA‑4 Prompt UI",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for subtle style tweaks ────────────────────────────────────
st.markdown(
    """
    <style>
    html, body, [class*="css"]  { font-family: "Inter", sans-serif; }
    .stTextArea textarea        { font-size: 0.95rem; line-height: 1.4; }
    .result-box                 { background: #f7f9fc; border-radius: 0.75rem; padding: 1rem 1.2rem; }
    .history-item               { background: #fafafa; border-radius: 0.5rem; padding: 0.7rem 1rem; }
    .history-item + .history-item { margin-top: 0.6rem; }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar (token + history) ─────────────────────────────────────────────
st.sidebar.header("🔐 Authentication")
token = st.sidebar.text_input(
    "Bearer Token",
    value=st.session_state.get("token", DEFAULT_TOKEN),
    help="Use the demo token or paste one you got from /login/",
)
st.session_state["token"] = token

show_hist = st.sidebar.checkbox("Show history", value=True)
clear_hist = st.sidebar.button("🗑️ Clear history")

HEADERS = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# ── Main UI ───────────────────────────────────────────────────────────────
st.title("🦙 LLaMA‑4 Chat PP-Playground ")

with st.form("prompt_form"):
    prompt = st.text_area("Type your prompt here 👇", height=140)
    submitted = st.form_submit_button("✨ Generate")

if submitted:
    if not prompt.strip():
        st.warning("Please type a prompt first.")
    else:
        with st.spinner("Contacting LLaMA‑4…"):
            resp = requests.post(f"{API_BASE}/prompt/", headers=HEADERS, json={"prompt": prompt})

        if resp.ok:
            answer = resp.json()["response"]
            st.balloons()
            st.markdown("#### 🧠 Model Response")
            st.markdown(f'<div class="result-box">{answer}</div>', unsafe_allow_html=True)
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")

# ── History section ──────────────────────────────────────────────────────
if show_hist:
    st.markdown("### 📜 Prompt History")
    hist_resp = requests.get(f"{API_BASE}/history/", headers=HEADERS)
    if hist_resp.ok:
        history = hist_resp.json()["history"]
        if not history:
            st.info("No history yet. Start chatting!")
        else:
            if clear_hist:
                st.warning("History clearing not implemented in backend.")
            else:
                for item in reversed(history):
                    st.markdown(f"user's Input: {item['prompt']}")
                    st.markdown(f"LLaMA's Output: {item['response']}")
                    st.markdown("---")

    else:
        st.error(f"Could not load history ({hist_resp.status_code})")

# ── Footer note ──────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown(
    "Made with ❤️ using **FastAPI**, **Replicate LLaMA‑4**, and **Streamlit**."
)
