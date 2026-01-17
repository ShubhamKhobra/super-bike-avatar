import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.title("🚴 Kid on Superbike Generator")
st.markdown("Upload an image with a kid, and we'll generate an image of the same kid on a superbike")
# File uploader
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=['png', 'jpg', 'jpeg'],
    help="Upload an image containing a kid"
)

if uploaded_file is not None:
    # Display the uploaded image
    st.subheader("📸 Original Image")
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption="Uploaded Image", use_container_width=True)
    
    # Generate button
    if st.button("🚀 Generate Image", type="primary"):
        with st.spinner("Analyzing the image and generating... This may take a moment."):
            try:
                # Convert image to base64 for API
                img_bytes = io.BytesIO()
                original_image.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
                
                # Step 1: Use GPT-4 Vision to analyze the kid in the image
                st.info("🔍 Analyzing the image...")
                
                # Use GPT-4 Vision to describe the kid
                vision_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        "Analyze this image and provide a detailed description of the child/kid in the image. "
                                        "Include details about their appearance, clothing, age, hair color, skin tone, "
                                        "facial features, and any distinctive characteristics. Be very specific and detailed. "
                                        "Focus only on describing the child's appearance accurately."
                                    )
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=300
                )
                
                kid_description = vision_response.choices[0].message.content
                st.success("✅ Image analyzed successfully!")
                
                # Step 2: Generate image using gpt-image-1 (OpenAI's latest image model)
                st.info("🎨 Generating image...")
                
                # Prepare the image as a proper file-like object with content type
                img_bytes.seek(0)
                
                # Generate image with gpt-image-1 (OpenAI's latest image generation model)
                # Using cartoon/illustration style to work within content policies
                image_response = client.images.edit(
                    model="gpt-image-1",
                    image=("image.png", img_bytes.getvalue(), "image/png"),
                    prompt=(
                        f"Transform this photo into a fun, colorful cartoon illustration in Pixar/Disney animation style. "
                        f"The animated character should be riding an awesome, stylized superbike motorcycle. "
                        # f"Add a cool racing helmet on the character. "
                        # f"Make the scene exciting with motion lines, a vibrant sunset background, and a cool race track setting. "
                        f"Bright colors, friendly cartoon style, fun and playful mood. "
                        f"High quality digital illustration, smooth gradients, appealing character design."
                    ),
                    size="1024x1024"
                )
                
                # Extract the generated image
                if image_response.data and len(image_response.data) > 0:
                    # Check if we have base64 data or URL
                    image_data_item = image_response.data[0]
                    if hasattr(image_data_item, 'b64_json') and image_data_item.b64_json:
                        image_data = base64.b64decode(image_data_item.b64_json)
                        generated_image = Image.open(io.BytesIO(image_data))
                    elif hasattr(image_data_item, 'url') and image_data_item.url:
                        img_response = requests.get(image_data_item.url)
                        generated_image = Image.open(io.BytesIO(img_response.content))
                    else:
                        generated_image = None
                else:
                    generated_image = None
                
                if generated_image is None:
                    st.error("No image was generated. Please try again.")
                else:
                    # Display the generated image
                    st.subheader("🎨 Generated Image")
                    st.image(generated_image, caption="Kid on Superbike", use_container_width=True)
                    
                    # Option to download the image
                    img_buffer = io.BytesIO()
                    generated_image.save(img_buffer, format='PNG')
                    st.download_button(
                        label="💾 Download Generated Image",
                        data=img_buffer.getvalue(),
                        file_name="kid_on_superbike.png",
                        mime="image/png"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please make sure you have set up your OpenAI API key correctly in your .env file.")
                st.info("You need: OPENAI_API_KEY=your_api_key_here")
else:
    st.info("👆 Please upload an image file to get started.")

