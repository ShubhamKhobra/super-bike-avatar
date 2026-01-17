# Image Editor with Gemini Nano Banana

A Streamlit web application that allows you to upload images and apply AI-powered edits using Google's Gemini Nano (Banana) model.

## Features

- 🖼️ Upload images in various formats (JPG, JPEG, PNG, WebP)
- ✏️ Describe edits using natural language
- 🤖 AI-powered image editing using Google Gemini API
- 📥 Download edited images
- 🎨 Multiple Gemini model options

## Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

## Setup

1. Get your Google Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the API key

2. Create a `.env` file in the project directory:
   ```bash
   touch .env
   ```

3. Add your API key to the `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual API key.

4. Run the Streamlit app:

```bash
streamlit run app.py
```

5. Open your browser and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

6. Upload an image and describe the edits you want!

## Usage

1. **Upload an Image**: Click on the file uploader and select an image
2. **Enter Edit Instructions**: Describe what edits you want (e.g., "Make colors more vibrant", "Add a sunset sky")
3. **Apply Edits**: Click the "Apply Edits" button
4. **Download**: Once processed, download your edited image

## Example Prompts

- "Make the colors more vibrant and add a warm filter"
- "Remove the background and make it transparent"
- "Apply a vintage film look"
- "Enhance the contrast and brightness"
- "Add a dramatic sunset sky in the background"
- "Convert to black and white with high contrast"

## Environment Variables

The application uses a `.env` file to store the API key securely. Create a `.env` file in the project root with:

```
GEMINI_API_KEY=your_api_key_here
```

**Important**: Never commit your `.env` file to version control. It should be listed in `.gitignore`.

## Notes

- The Gemini API may return text descriptions or image data depending on the model used
- Some models may require specific formatting for image editing
- Make sure you have sufficient API quota for image processing
- The API key is loaded from the `.env` file at startup

## Requirements

- Python 3.8+
- Google Gemini API key
- Internet connection

## License

This project is open source and available for personal and commercial use.

# super-bike-avatar
