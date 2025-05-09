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
    visualize = st.checkbox("Visualize Tree")

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

if st.button("Run Huffman Coding", use_container_width=True):
    if not text:
        st.error("Input is empty!")
    else:

        # counter
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
            verification_placeholder.success("✓ Verified: Decoding Matches Original")
        else:
            verification_placeholder.error("✗ Decoding Failed!")

        # Main output panels
        col1, col2 = st.columns([1, 2], gap="large")
        
        with col1:  # Left panel for Text outputs
            with st.container():
                st.subheader("Original Text")
                st.write(f'```\n{text[:200]}{"..." if len(text) > 200 else ""}\n```')
                
            with st.container():
                st.subheader("Encoded Text")
                st.code(encoded)

        with col2:  # Right panel Visual outputs
            if visualize and root:
                try:
                    with st.container():
                        st.subheader("Huffman Tree Visualization")
                        img_path = visualize_huffman_tree(root, view=False, input_text=text)
                        st.image(img_path, use_column_width=True)
                except Exception as e:
                    st.error(f"Visualization Error: {str(e)}")
            
            with st.container():
                st.subheader("Huffman Codes")
                codes_df = pd.DataFrame(
                    [(k, repr(str(k)), v) for k, v in codes.items()],
                    columns=["ASCII", "Character", "Code"]
                )
                st.dataframe(codes_df, height=300, hide_index=True)

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