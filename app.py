import streamlit as st
from google import genai
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini client
client = genai.Client()

# Load the logo
LOGO_PATH = "/home/ubuntu/Sh/image_on_superbike/logo.jpeg"

from PIL import ImageDraw, ImageFont

def add_logo_to_image(pil_image, logo_path, padding=10):
    """Add logo to the top left corner of the image."""
    logo = Image.open(logo_path)
    
    # Resize logo to be proportional to the image (e.g., 15% of image width)
    logo_width = int(pil_image.width * 0.15)
    logo_height = int(logo.height * (logo_width / logo.width))
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    
    # Convert logo to RGBA if it has transparency, or add alpha channel
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')
    
    # Convert main image to RGBA for proper compositing
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    
    # Paste logo at top left with padding
    pil_image.paste(logo, (padding, padding), logo)
    
    # Convert back to RGB for saving as PNG/JPEG
    return pil_image.convert('RGB')

def add_bottom_text_banner(pil_image, text, ribbon_color=(255, 215, 0), text_color=(255, 0, 0)):
    """Add a text banner at the bottom of the image with colored ribbon background."""
    # Ensure image is in RGB mode
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    
    # Create a copy to avoid modifying the original
    img = pil_image.copy()
    draw = ImageDraw.Draw(img)
    
    # Calculate font size based on image width (approximately 2.5% of width)
    font_size = max(16, int(img.width * 0.025))
    
    # Try to load a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Get text bounding box
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate ribbon dimensions
    ribbon_height = text_height + 20  # Add padding
    ribbon_y = img.height - ribbon_height
    
    # Draw yellow ribbon (full width)
    draw.rectangle(
        [(0, ribbon_y), (img.width, img.height)],
        fill=ribbon_color
    )
    
    # Calculate text position (centered)
    text_x = (img.width - text_width) // 2
    text_y = ribbon_y + (ribbon_height - text_height) // 2
    
    # Draw red text
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    return img

# Streamlit UI
st.title("🏍️ Superbike Avatar Generator")
st.markdown("Upload an image of a kid, and we'll generate a superbike avatar for them!")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=['png', 'jpg', 'jpeg'],
    help="Upload an image containing a person"
)

if uploaded_file is not None:
    # Display the uploaded image
    st.subheader("📸 Original Image")
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption="Uploaded Image", width=400)
    
    # Generate button
    if st.button("🚀 Generate Image", type="primary"):
        with st.spinner("Generating image... This may take a moment."):
            try:
                # Create the prompt
                prompt = "Put this person on a cool superbike motorcycle, maintaining their appearance. Change clothes as well."
                
                # Retry mechanism - safety filter is non-deterministic
                max_retries = 10
                generated_image = None
                
                progress_bar = st.progress(0, text="Generating...")
                
                for attempt in range(max_retries):
                    progress_bar.progress((attempt + 1) / max_retries, text=f"Attempt {attempt + 1}/{max_retries}...")
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-image",
                        contents=[prompt, original_image],
                    )
                    
                    # Check if successful
                    if response.parts:
                        for part in response.parts:
                            if part.text is not None:
                                # st.info(part.text)
                                pass
                            elif part.inline_data is not None:
                                generated_image = part.as_image()
                        if generated_image:
                            progress_bar.progress(1.0, text="Success!")
                            break
                
                progress_bar.empty()
                
                # If all retries failed
                if not generated_image:
                    st.error("⚠️ The image generation was blocked by safety filters after multiple attempts.")
                    st.info("This can happen with certain images. Please try again or use a different image.")
                    st.stop()
                
                # Display the generated image
                if generated_image:
                    st.subheader("🎨 Generated Image")
                    # Convert genai Image to PIL Image for display
                    pil_image = Image.open(io.BytesIO(generated_image.image_bytes))
                    
                    # Add logo to the top left corner
                    pil_image_with_logo = add_logo_to_image(pil_image, LOGO_PATH)
                    
                    # Add text banner at the bottom
                    banner_text = "Buy Yellow Diamond Rings to make your Super Bike Avatar"
                    final_image = add_bottom_text_banner(pil_image_with_logo, banner_text)
                    
                    st.image(final_image, caption="Your Super Bike Avatar", width=500)
                    
                    # Option to download the image with logo and banner
                    img_buffer = io.BytesIO()
                    final_image.save(img_buffer, format='PNG')
                    st.download_button(
                        label="💾 Download Generated Image",
                        data=img_buffer.getvalue(),
                        file_name="person_on_superbike.png",
                        mime="image/png"
                    )
                else:
                    st.error("No image was generated. Please try again.")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please make sure you have set up your Google Gemini API key correctly.")
else:
    st.info("👆 Please upload an image file to get started.")
