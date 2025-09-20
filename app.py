# app.py — ODU (no tabs, no icon)
from pathlib import Path
import pandas as pd
import streamlit as st

# --- Paths ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
for d in (INPUT_DIR, OUTPUT_DIR, ASSETS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# --- Page header (no emoji icon) ---
st.set_page_config(page_title="ODU", page_icon=None, layout="wide")
st.title("ODU")
st.caption("Upload inputs and generate outputs here.")

# --- Upload section (no tabs) ---
st.subheader("Upload")
uploads = st.file_uploader(
    "Upload CSV/Excel (multiple allowed)",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True,
)
if uploads:
    saved = []
    for u in uploads:
        p = INPUT_DIR / u.name
        with open(p, "wb") as f:
            f.write(u.getbuffer())
        saved.append(p.name)
    st.success("Saved: " + ", ".join(saved))

    # Example processing: write *_processed.xlsx to output/
    rows = []
    for name in saved:
        in_path = INPUT_DIR / name
        if name.lower().endswith(".csv"):
            df = pd.read_csv(in_path, low_memory=False)
        else:
            df = pd.read_excel(in_path)
        out_path = OUTPUT_DIR / (in_path.stem + "_processed.xlsx")
        df.to_excel(out_path, index=False)
        rows.append({
            "file": name,
            "rows": df.shape[0],
            "columns": df.shape[1],
            "output": out_path.name
        })
    st.dataframe(pd.DataFrame(rows))

# --- Outputs list ---
st.subheader("Outputs")
outs = sorted(OUTPUT_DIR.glob("*"))
if not outs:
    st.info("No outputs yet.")
else:
    for p in outs:
        c1, c2 = st.columns([4, 2])
        c1.write(p.name)
        c2.download_button("Download", p.read_bytes(), file_name=p.name)
