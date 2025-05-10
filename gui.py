import streamlit as st
from visualization import visualize_huffman_tree
from huffman_encoder import build_huffman_tree, get_huffman_codes, huffman_encode
from huffman_decoder import huffman_decode

import io
import pandas as pd
from contextlib import redirect_stdout
from collections import Counter


st.set_page_config(page_title="Huffman Coding", page_icon="📦")
st.title("📦 Huffman Coding Compression")


# Sidebar for controls and verification
with st.sidebar:
    st.header("Controls")
    input_method = st.radio("Input Method:", ("Text Input", "File Upload"))
    verbose = st.radio("Verbose Mode:", ("Off", "On"), horizontal=True)

verification_placeholder = st.empty()

# Main content area
text = ""
if input_method == "Text Input":
    with st.container():
        verification_placeholder.empty()
        text = st.text_area("Enter Text to Encode:", height=150)
else:
    uploaded_file = st.file_uploader("Upload a Text File:", type=["txt"])
    if uploaded_file:
        text = uploaded_file.getvalue().decode("utf-8")

if st.button("Run Huffman Coding", use_container_width=True) or text:
    if not text:
        st.error("Input is empty!")
    else:
        frequency = Counter(text)

        # Processing
        verbose_logs = ""
        if verbose == "On":
            f = io.StringIO()
            with redirect_stdout(f):
                root = build_huffman_tree(text, frequency, verbose=True)
                codes = get_huffman_codes(root, verbose=True)
                encoded = huffman_encode(text, codes, verbose=True)
                decoded = huffman_decode(encoded, root, verbose=True)
            verbose_logs = f.getvalue()
        else:
            root = build_huffman_tree(text, frequency, verbose=False)
            codes = get_huffman_codes(root, verbose=False)
            encoded = huffman_encode(text, codes, verbose=False)
            decoded = huffman_decode(encoded, root, verbose=False)

        if text == decoded:
            verification_placeholder.success(
                "✓ SUCCESS: Encoding and Decoding successful! Original text matches decoded text."
            )
        else:
            verification_placeholder.error(
                "✗ FAILED: Decoding failed! Original text does NOT match decoded text."
            )

        # Main output panels
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:  # Left panel for Text outputs
            with st.container():
                st.subheader("Encoded Text")
                st.code(encoded)

            with st.container():
                st.subheader("Decoded Text")
                st.write(f"```\n{text[:200]}{'...' if len(text) > 200 else ''}\n```")

        with col2:  # Right panel Visual outputs
            try:
                with st.container():
                    st.subheader("Huffman Tree Visualization")
                    # Get both path and reuse status (explicitly set format)
                    img_path, is_reused = visualize_huffman_tree(
                        root, view=False, input_text=text, format="png"
                    )

                    if img_path:
                        st.image(img_path, use_container_width=True)
                    else:
                        st.warning("Tree visualization could not be generated")
            except Exception as e:
                st.error(f"Visualization Error: {str(e)}")

        with st.container():
            st.subheader("Huffman Codes")
            codes_df = pd.DataFrame(
                [(repr(str(k)), frequency[k], v) for k, v in codes.items()],
                columns=["Character", "Frequency", "Code"],
            )
            st.dataframe(codes_df, hide_index=True)

        # Bottom panel - Stats and verbose
        with st.container():
            st.subheader("Compression Statistics")
            cols = st.columns(4)
            original_bits = len(text) * 8
            encoded_bits = len(encoded)
            saved = original_bits - encoded_bits
            ratio = (saved / original_bits) * 100 if original_bits else 0

            cols[0].metric("Original Bits", original_bits)
            cols[1].metric("Encoded Bits", encoded_bits)
            cols[2].metric("Space Saved", saved)
            cols[3].metric("Ratio", f"{ratio:.2f}%")

        if verbose == "On":
            with st.expander("Verbose Output", expanded=True):
                st.code(verbose_logs)
