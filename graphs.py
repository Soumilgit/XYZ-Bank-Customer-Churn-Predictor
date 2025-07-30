import streamlit as st
import utils as ut
from PIL import Image
import base64
import numpy as np

ut.apply_sidebar_styles()

def apply_transparent_styles():
    st.markdown("""
    <style>
        .graph-container {
            background-color: transparent !important;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }
        .graph-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }
        .stImage > img {
            background-color: transparent !important;
        }
        @media (max-width: 768px) {
            .graph-col {
                width: 100% !important;
            }
        }
        .stDeprecationWarning {
            display: none;
        }
        
        /* Dark mode image adjustments - exclude sidebar specifically */
        @media (prefers-color-scheme: dark) {
            img:not([src*="sidebar.jpeg"]):not([alt*="sidebar"]) {
                filter: invert(1) hue-rotate(180deg);
                background-color: black !important;
            }
            
            /* Explicitly ensure sidebar image stays normal */
            [data-testid="stSidebar"] img,
            [src*="sidebar.jpeg"] {
                filter: none !important;
                background-color: transparent !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def process_image(image_path, dark_mode=False, custom_width=None):
    """Process image to ensure proper display in both light and dark modes"""
    try:
        if "sidebar.jpeg" in image_path:
            return Image.open(image_path)
            
        img = Image.open(image_path)
        
        if dark_mode:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            data = np.array(img)
            red, green, blue, alpha = data.T

            data[..., :3] = 255 - data[..., :3]
            white_areas = (red == 255) & (green == 255) & (blue == 255)
            data[..., :-1][white_areas.T] = (0, 0, 0)
            
            img = Image.fromarray(data)
        
        base_width = custom_width if custom_width else 900 
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
        
        return img
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

def display_image(image_path, title):
    try:
        dark_mode = st.get_option("theme.base") == "dark" if st.get_option("theme.base") else False
        if "output-5.png" in image_path:
            adjacent_img_path = "output-4.png" 
            adjacent_img = Image.open(adjacent_img_path)
            custom_width = adjacent_img.size[0]  
            
            img = process_image(image_path, dark_mode, custom_width)
        else:
            img = process_image(image_path, dark_mode)
            
        if img:
            st.markdown(f'<div class="graph-title">{title}</div>', unsafe_allow_html=True)
            st.image(img, use_container_width=True)
    except FileNotFoundError:
        st.error(f"Image not found: {image_path}")

def main():
    ut.apply_sidebar_styles()
    apply_transparent_styles()
    
    st.title("Customer Analytics Visualizations")
    st.markdown("Key insights from customer data")
    images = [
        {"path": "output-1.png", "title": "Age Distribution"},
        {"path": "output-2.png", "title": "Credit Score vs Age"},
        {"path": "output-3.png", "title": "Balance Distribution by Churn"},
        {"path": "output-4.png", "title": "Credit Score Distribution by Churn"},
        {"path": "output-5.png", "title": "Importance vs Features"},
        {"path": "output.png", "title": "Distribution of Churn"}
    ]
    
    col1, col2 = st.columns(2)
    
    for i, img in enumerate(images):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            display_image(img["path"], img["title"])
    
    st.markdown("---")
    st.caption("All visualizations are based on XYZ Bank customer data")

if __name__ == "__main__":
    main()