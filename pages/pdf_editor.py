import streamlit as st
import fitz
from PIL import Image
import io
from streamlit_sortables import sort_items

st.set_page_config(page_title="PDF Editor", layout="wide",initial_sidebar_state="collapsed")

st.title("📄 Interactive PDF Editor")

# Function to merge uploaded PDFs
def merge_pdfs(uploaded_files):
    merged_pdf = fitz.open()
    for uploaded_file in uploaded_files:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
            merged_pdf.insert_pdf(pdf)
    return merged_pdf

# Function to delete selected pages
def delete_pages(images):
    delete_flags = [False] * len(images)
    cols_per_row = 4
    cols = st.columns(cols_per_row)
    for i, img in enumerate(images):
        col = cols[i % cols_per_row]
        col.image(img, caption=f"Page {i + 1}", use_container_width=True)
        if col.checkbox(f"Delete Page {i + 1}", key=f"delete_{i}"):
            delete_flags[i] = True
    return [i for i in range(len(images)) if not delete_flags[i]]

# Function to reorder pages
def reorder_pages(remaining_pages):
    st.subheader("🔄 Reorder Pages")
    page_labels = [f"Page {i + 1}" for i in remaining_pages]
    reordered_items = sort_items(page_labels)
    reordered_indices = [remaining_pages[page_labels.index(item)] for item in reordered_items]
    return reordered_indices

# Function to create new PDF with updated pages
def create_updated_pdf(pdf, page_order):
    updated_pdf = fitz.open()
    for i in page_order:
        updated_pdf.insert_pdf(pdf, from_page=i, to_page=i)
    return updated_pdf

# Main function to handle PDF state
uploaded_files = st.file_uploader("Upload PDFs to merge and edit", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    pdf = merge_pdfs(uploaded_files)
    images = [Image.open(io.BytesIO(page.get_pixmap().tobytes("png"))) for page in pdf]

    st.subheader("📌 Pages Preview and Management")
    remaining_pages = delete_pages(images)
    
    if not remaining_pages:
        st.warning("No pages remain after deletion. Please select fewer pages to delete.")
    else:
        new_order = reorder_pages(remaining_pages)

        if st.button("✅ Apply Changes & Download PDF"):
            edited_pdf = create_updated_pdf(pdf, new_order)

            original_file_name = uploaded_files[0].name
            output_file_name = f"modified_{original_file_name.rsplit('.', 1)[0]}.pdf"
            
            edited_pdf.save(output_file_name)
            edited_pdf.close()

            with open(output_file_name, "rb") as f:
                st.download_button(
                    "📅 Download Modified PDF", f, file_name=output_file_name, mime="application/pdf"
                )
