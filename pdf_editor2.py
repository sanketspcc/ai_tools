import streamlit as st
import fitz
from PIL import Image
import io
import base64
from streamlit.components.v1 import html

st.set_page_config(page_title="PDF Editor", layout="wide")
st.title("📄 Interactive PDF Editor")

# Function to delete pages based on user input
def get_remaining_pages(images):
    delete_flags = [False] * len(images)
    cols_per_row = 4
    cols = st.columns(cols_per_row)
    for i, img in enumerate(images):
        col = cols[i % cols_per_row]
        col.image(img, caption=f"Page {i + 1}", use_container_width=True)
        if col.checkbox(f"Delete Page {i + 1}", key=f"delete_{i}"):
            delete_flags[i] = True
    return [i for i in range(len(images)) if not delete_flags[i]]

# Function to reorder pages using drag and drop (HTML and JavaScript)
def reorder_pages_with_drag_and_drop(images):
    # Generate HTML content with draggable elements
    draggable_images = ""
    for i, img in enumerate(images):
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format="PNG")
        img_byte_array.seek(0)  # Ensure the pointer is at the beginning of the BytesIO object
        img_base64 = base64.b64encode(img_byte_array.read()).decode("utf-8")  # Proper base64 encoding
        
        draggable_images += f"""
        <div id="page_{i}" class="draggable" style="width: 150px; padding: 5px; border: 1px solid #ccc; margin: 5px; cursor: move;">
            <img src="data:image/png;base64,{img_base64}" width="100%" />
            <div>Page {i + 1}</div>
        </div>
        """

    html_code = f"""
    <html>
    <head>
        <script>
            const dragItems = document.querySelectorAll('.draggable');
            dragItems.forEach(item => {{
                item.addEventListener('dragstart', (e) => {{
                    e.dataTransfer.setData('text/plain', item.id);
                    item.style.opacity = '0.4';
                }});
                item.addEventListener('dragend', () => {{
                    item.style.opacity = '1';
                }});
                item.addEventListener('dragover', (e) => {{
                    e.preventDefault();
                    item.style.border = '2px solid #000';
                }});
                item.addEventListener('dragleave', () => {{
                    item.style.border = '1px solid #ccc';
                }});
                item.addEventListener('drop', (e) => {{
                    e.preventDefault();
                    const draggedItemId = e.dataTransfer.getData('text/plain');
                    const draggedItem = document.getElementById(draggedItemId);
                    const dropTarget = e.target.closest('.draggable');
                    const parent = dropTarget.parentNode;
                    if (draggedItem !== dropTarget) {{
                        parent.insertBefore(draggedItem, dropTarget);
                    }}
                    item.style.border = '1px solid #ccc';

                    // Send the updated order back to Streamlit
                    const pageOrder = [];
                    document.querySelectorAll('.draggable').forEach((el, index) => {{
                        pageOrder.push(el.id.replace('page_', ''));
                    }});

                    // Send the order back to Streamlit using a custom event
                    window.parent.postMessage({{
                        type: 'page_order',
                        order: pageOrder
                    }}, '*');
                }});
            }});
        </script>
        <style>
            .draggable {{
                display: inline-block;
                width: 150px;
                padding: 5px;
                border: 1px solid #ccc;
                margin: 5px;
                cursor: move;
            }}
        </style>
    </head>
    <body>
        <div id="container" style="display: flex; flex-wrap: wrap; justify-content: start;">
            {draggable_images}
        </div>
    </body>
    </html>
    """
    html(html_code)

# Upload multiple PDFs
uploaded_files = st.file_uploader("Upload PDFs to merge and edit", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    merged_pdf = fitz.open()

    # Merge uploaded PDFs
    for uploaded_file in uploaded_files:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
            merged_pdf.insert_pdf(pdf)

    # Convert PDF pages to images for preview
    images = []
    for page in merged_pdf:
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)

    # Delete and reorder pages
    st.subheader("📌 Pages Preview and Management")
    remaining_pages = get_remaining_pages(images)

    if not remaining_pages:
        st.warning("No pages remain after deletion. Please select fewer pages to delete.")
    else:
        reorder_pages_with_drag_and_drop(images)

        # Handle the page order update when the user finishes drag-and-drop
        if "page_order" not in st.session_state:
            st.session_state.page_order = [i for i in remaining_pages]

        # Listen for the page order update from JavaScript
        page_order = st.experimental_get_query_params().get("page_order", None)
        if page_order:
            st.session_state.page_order = [int(i) for i in page_order[0].split(',')]

        if st.button("✅ Apply Changes & Download PDF"):
            # Use the updated order from session state
            new_order = st.session_state.page_order
            edited_pdf = fitz.open()
            for i in new_order:
                edited_pdf.insert_pdf(merged_pdf, from_page=i, to_page=i)

            original_file_name = uploaded_files[0].name
            original_base_name = original_file_name.rsplit(".", 1)[0]
            output_file_name = f"modified_{original_base_name}.pdf"

            edited_pdf.save(output_file_name)
            edited_pdf.close()

            with open(output_file_name, "rb") as f:
                st.download_button(
                    "📥 Download Modified PDF", f, file_name=output_file_name, mime="application/pdf"
                )
