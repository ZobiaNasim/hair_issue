from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import streamlit as st

# Initialize client (Gemini Developer API example)
client = genai.Client(api_key="AIzaSyAl-FTx28S32bsyu7HdlVMgvo8zLnaBLxQ")

st.title("Hair Image Generator")

# Fixed category = "Hair"
category = "Hair"

# User input only for description
description = st.text_input("Describe the what you want ")

if st.button("Generate Image"):
    prompt = f"""
    Generate an image focusing on the hair of a person. 
    The face should be slightly visible but most focus should be on the hair, 
    specifically showing the issue of {description}.
    """


    with st.spinner("Generating image..."):
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            )
        )

    # Extract and display image
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            img = Image.open(BytesIO(part.inline_data.data))
            st.image(img, caption=description)
            break
    else:
        st.error("❌ No image returned—try adjusting the description.")

