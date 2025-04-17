import streamlit as st
import os
import tempfile
import base64
from PyPDF2 import PdfReader, PdfWriter
import io
from PIL import Image
import fitz  # PyMuPDF

st.set_page_config(layout="wide", page_title="PDF Editor")

# Initialize session state variables if they don't exist
if 'pdf_pages' not in st.session_state:
    st.session_state.pdf_pages = []  # List to store PDF pages
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = tempfile.TemporaryDirectory()
if 'temp_files' not in st.session_state:
    st.session_state.temp_files = []
if 'page_rotations' not in st.session_state:
    st.session_state.page_rotations = {}
if 'reordering' not in st.session_state:
    st.session_state.reordering = False
if 'drag_source' not in st.session_state:
    st.session_state.drag_source = None
if 'uploaded_files_count' not in st.session_state:
    st.session_state.uploaded_files_count = 0

# Function to convert PDF page to image
def convert_pdf_to_image(pdf_page, scale=2.0):
    # This is using PyMuPDF (fitz) to render the page
    pix = pdf_page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    img_data = pix.tobytes("ppm")
    img = Image.open(io.BytesIO(img_data))
    return img

# Function to display a PDF page
def display_page(page_num):
    if 0 <= page_num < len(st.session_state.pdf_pages):
        # Create a temporary file for the current page PDF
        temp_file = os.path.join(st.session_state.temp_dir.name, f"page_{page_num}.pdf")
        
        # Create a single page PDF
        writer = PdfWriter()
        writer.add_page(st.session_state.pdf_pages[page_num])
        
        # Apply rotation if any
        if page_num in st.session_state.page_rotations:
            writer.pages[0].rotate(st.session_state.page_rotations[page_num])
        
        with open(temp_file, "wb") as f:
            writer.write(f)
        
        return temp_file
    return None

# Function to create a download link for a PDF
def create_download_link(pdf_bytes, filename="edited_document.pdf"):
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download Edited PDF</a>'
    return href

# Function to merge all pages into a single PDF
def merge_pages():
    writer = PdfWriter()
    for i, page in enumerate(st.session_state.pdf_pages):
        writer.add_page(page)
        # Apply rotation if any
        if i in st.session_state.page_rotations:
            writer.pages[len(writer.pages) - 1].rotate(st.session_state.page_rotations[i])
    
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

# Function to swap pages during reordering
def swap_pages(idx1, idx2):
    if 0 <= idx1 < len(st.session_state.pdf_pages) and 0 <= idx2 < len(st.session_state.pdf_pages):
        # Swap pages
        st.session_state.pdf_pages[idx1], st.session_state.pdf_pages[idx2] = st.session_state.pdf_pages[idx2], st.session_state.pdf_pages[idx1]
        
        # Swap rotations
        rot1 = st.session_state.page_rotations.get(idx1, 0)
        rot2 = st.session_state.page_rotations.get(idx2, 0)
        
        if rot1 != 0:
            st.session_state.page_rotations[idx2] = rot1
        elif idx2 in st.session_state.page_rotations:
            del st.session_state.page_rotations[idx2]
            
        if rot2 != 0:
            st.session_state.page_rotations[idx1] = rot2
        elif idx1 in st.session_state.page_rotations:
            del st.session_state.page_rotations[idx1]

# Main application layout
st.title("PDF Editor")

# Sidebar for controls and thumbnails
with st.sidebar:
    st.header("Controls")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file (You can add multiple PDFs)", type="pdf", accept_multiple_files=True, key=f"uploader_{st.session_state.uploaded_files_count}")
    
    if uploaded_file:
        # Read the PDF files - now handling multiple files
        try:
            for file in uploaded_file:
                reader = PdfReader(file)
                # Add all pages from the PDF
                for i in range(len(reader.pages)):
                    st.session_state.pdf_pages.append(reader.pages[i])
                
                st.success(f"Added PDF '{file.name}' with {len(reader.pages)} pages")
            
            # Increment the counter for the uploader key (forces a fresh uploader)
            st.session_state.uploaded_files_count += 1
            # This is a trick to clear the file uploader
            st.experimental_rerun()
            
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    
    # Only show these controls if there are pages
    if st.session_state.pdf_pages:
        st.divider()
        st.subheader("Page Operations")
        
        # Selected page for operations
        selected_page = st.number_input("Select page for operations:", 
                                        min_value=1, 
                                        max_value=len(st.session_state.pdf_pages),
                                        value=1)
        page_idx = selected_page - 1
        
        # Rotation options
        rotation_options = {
            "0°": 0,
            "90°": 90,
            "180°": 180, 
            "270°": 270
        }
        
        current_rotation = st.session_state.page_rotations.get(page_idx, 0)
        selected_rotation_key = next((k for k, v in rotation_options.items() if v == current_rotation), "0°")
        
        new_rotation = st.select_slider(
            "Set page rotation:",
            options=list(rotation_options.keys()),
            value=selected_rotation_key
        )
        
        # Update rotation if changed
        if rotation_options[new_rotation] != current_rotation:
            if rotation_options[new_rotation] == 0:
                if page_idx in st.session_state.page_rotations:
                    del st.session_state.page_rotations[page_idx]
            else:
                st.session_state.page_rotations[page_idx] = rotation_options[new_rotation]
        
        # Delete page button
        if st.button("Delete Selected Page"):
            if 0 <= page_idx < len(st.session_state.pdf_pages):
                # Remove the page and its rotation if exists
                st.session_state.pdf_pages.pop(page_idx)
                if page_idx in st.session_state.page_rotations:
                    del st.session_state.page_rotations[page_idx]
                
                # Update rotations indexes
                new_rotations = {}
                for k, v in st.session_state.page_rotations.items():
                    if k > page_idx:
                        new_rotations[k-1] = v
                    elif k < page_idx:
                        new_rotations[k] = v
                st.session_state.page_rotations = new_rotations
                
                st.success(f"Deleted page {selected_page}")
                st.experimental_rerun()
        
        # Clear all PDFs button
        if st.button("Clear All PDFs"):
            st.session_state.pdf_pages = []
            st.session_state.page_rotations = {}
            st.success("Cleared all PDFs")
            st.experimental_rerun()
        
        # Save the edited PDF
        st.divider()
        if st.button("Save PDF"):
            if st.session_state.pdf_pages:
                pdf_bytes = merge_pages()
                st.markdown(create_download_link(pdf_bytes.getvalue()), unsafe_allow_html=True)
            else:
                st.warning("No pages to save.")
        
        # Preview of all pages - for reordering
        st.divider()
        st.subheader("Page Thumbnails")
        st.caption("Drag and drop to reorder pages")
        
        # Toggle for drag mode
        st.session_state.reordering = st.checkbox("Enable drag mode", value=st.session_state.reordering)
        
        if st.session_state.reordering:
            st.info("Click on a thumbnail to select, then click on another to swap them.")
        
        # Container for thumbnails
        thumbnail_container = st.container()
        with thumbnail_container:
            # Create a grid layout for thumbnails
            cols = 2  # Number of columns in grid
            
            # Calculate number of rows needed
            num_pages = len(st.session_state.pdf_pages)
            
            # Create rows and place thumbnails
            for i in range(0, num_pages, cols):
                columns = st.columns(cols)
                
                # Add pages to this row
                for j in range(cols):
                    idx = i + j
                    if idx < num_pages:
                        with columns[j]:
                            # Create temp file for this page with rotation applied
                            temp_file = display_page(idx)
                            
                            if temp_file:
                                # Open with PyMuPDF for rendering
                                doc = fitz.open(temp_file)
                                if doc.page_count > 0:
                                    thumb_img = convert_pdf_to_image(doc[0], scale=0.5)
                                    
                                    # Display thumbnail with page number
                                    st.image(thumb_img, caption=f"Page {idx+1}", use_container_width=True)
                                    
                                    # Button for source selection in reordering mode
                                    if st.session_state.reordering:
                                        if st.session_state.drag_source is None:
                                            if st.button(f"Select", key=f"select_{idx}"):
                                                st.session_state.drag_source = idx
                                                st.experimental_rerun()
                                        elif st.session_state.drag_source == idx:
                                            if st.button(f"Cancel", key=f"cancel_{idx}"):
                                                st.session_state.drag_source = None
                                                st.experimental_rerun()
                                        else:
                                            if st.button(f"Swap with {st.session_state.drag_source+1}", key=f"target_{idx}"):
                                                swap_pages(st.session_state.drag_source, idx)
                                                st.session_state.drag_source = None
                                                st.experimental_rerun()
                                
                                # Close the document
                                doc.close()

# Main content area - show all pages
main_container = st.container()
with main_container:
    if st.session_state.pdf_pages:
        st.header(f"All Pages ({len(st.session_state.pdf_pages)} total)")
        
        # For drag mode notification
        if st.session_state.drag_source is not None:
            st.info(f"Page {st.session_state.drag_source+1} selected. Click on another page to swap.")
        
        # Display each page
        for i in range(len(st.session_state.pdf_pages)):
            st.markdown(f"### Page {i+1}")
            
            # Get temp file for this page
            temp_file = display_page(i)
            if temp_file:
                # Open with PyMuPDF for rendering
                doc = fitz.open(temp_file)
                if doc.page_count > 0:
                    page_img = convert_pdf_to_image(doc[0], scale=1.5)
                    st.image(page_img, use_container_width=True)
                
                # Show current rotation if any
                rotation = st.session_state.page_rotations.get(i, 0)
                if rotation != 0:
                    st.caption(f"Rotation: {rotation}°")
                
                # Close the document
                doc.close()
            
            st.divider()
    else:
        st.info("Upload PDF files to begin editing.")
        
        # Add instructions
        st.markdown("""
        ### Instructions:
        1. Drag and drop PDF files into the uploader in the sidebar
        2. Add multiple PDFs to merge them
        3. Use the sidebar controls to:
           - Select pages for operations
           - Set page rotation (0°, 90°, 180°, 270°)
           - Delete unwanted pages
           - Reorder pages by enabling drag mode and swapping
        4. Preview all pages in the sidebar thumbnails
        5. Save your edited PDF when done
        """)