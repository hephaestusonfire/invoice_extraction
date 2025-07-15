import streamlit as st
import httpx
import base64
import pandas as pd
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="🧾 Receipt OCR with LLaVA", layout="wide")
st.title("📸 Intelligent Receipt OCR App (LLaVA)")

uploaded_files = st.file_uploader("Upload receipt images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# === Function to encode image as base64 string ===
def encode_image(file_bytes):
    return base64.b64encode(file_bytes).decode("utf-8")

# === Function to send to LLaVA via Ollama API ===
def query_llava(image_base64):
    payload = {
        "model": "llava",
        "prompt": "Extract all receipt details in text format",
        "images": [image_base64],
        "stream": False
    }
    try:
        response = httpx.post("http://localhost:11434/api/generate", json=payload, timeout=90.0)
        response.raise_for_status()
        return response.json()["response"].strip()
    except httpx.HTTPStatusError as e:
        return f"❌ HTTP {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Error: {e}"

# === Function to extract useful lines from the response ===
def parse_lines_to_table(text):
    lines = text.splitlines()
    rows = [line for line in lines if any(c.isdigit() for c in line)]
    return pd.DataFrame({"Line Items": rows})

# === Main Execution ===
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.divider()
        st.subheader(f"📷 File: `{uploaded_file.name}`")
        
        try:
            file_bytes = uploaded_file.getvalue()  # read once
            image = Image.open(BytesIO(file_bytes))
            st.image(image, caption="Uploaded Receipt", use_column_width=True)

            with st.spinner("🧠 Querying LLaVA..."):
                encoded = encode_image(file_bytes)
                response_text = query_llava(encoded)

            if response_text.startswith("❌"):
                st.error(response_text)
            else:
                st.success("✅ Model response received!")
                st.code(response_text, language="markdown")
                
                # Parse line items
                df = parse_lines_to_table(response_text)
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                    st.download_button("💾 Download CSV", df.to_csv(index=False), file_name=f"{uploaded_file.name}_data.csv")
                else:
                    st.warning("No clear line items found in response.")

        except Exception as e:
            st.error(f"❌ Failed to process file `{uploaded_file.name}`: {e}")
else:
    st.info("Upload image receipts to begin...")
