import google.genai as genai
from PIL import Image
from io import BytesIO
import streamlit as st

# ✅ Hardcode the API key directly (not using st.secrets)
client = genai.Client(api_key="AIzaSyAl-FTx28S32bsyu7HdlVMgvo8zLnaBLxQ")

st.title("Hair Image Generator")

# Fixed category = "Hair"
category = "Hair"

# User input only for description
description = st.text_input("Describe the hair issue you want shown:")

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
            config=genai.types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )

    # Extract and display image
    image_shown = False
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            img = Image.open(BytesIO(part.inline_data.data))
            st.image(img, caption=description)
            image_shown = True
            break

    if not image_shown:
        st.error("❌ No image returned — try adjusting the description.")

