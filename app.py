import streamlit as st
from pathlib import Path

st.set_page_config(page_title="ODU", page_icon="🧳", layout="wide")
st.title("🧳 ODU")
st.write("Upload inputs and generate outputs here.")

# Ensure folders exist
base = Path(__file__).parent
in_dir = base / "data" / "input"
out_dir = base / "data" / "output"
in_dir.mkdir(parents=True, exist_ok=True)
out_dir.mkdir(parents=True, exist_ok=True)

# Upload
uploaded = st.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded:
    dest = in_dir / uploaded.name
    dest.write_bytes(uploaded.read())
    st.success(f"Saved to: {dest}")

# Process / generate
if st.button("Generate Output"):
    # TODO: replace with your real logic
    (out_dir / "result.txt").write_text("Hello from ODU!")
    st.success(f"Output saved to: {out_dir/'result.txt'}")

# Download
result = out_dir / "result.txt"
st.download_button(
    "Download result.txt",
    data=result.read_text() if result.exists() else "",
    file_name="result.txt",
    disabled=not result.exists(),
)
