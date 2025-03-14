import streamlit as st
import requests
from retrieval import RAGRetriever
from llm_response import LLMGenerator
from PIL import Image
from io import BytesIO
import asyncio
import sys

# ✅ Fix asyncio event loop issue (for Windows users)
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ✅ Set Google Colab API URL (replace with updated Ngrok URL)
COLAB_API_URL = "https://72bd-34-125-142-72.ngrok-free.app/generate_image"  # Update with actual Ngrok URL

# ✅ Initialize AI Components
retriever = RAGRetriever()
llm = LLMGenerator()

st.title("AI-Powered Knowledge Assistant")

query = st.text_input("Ask me anything:")

if st.button("Generate Response"):
    if not query.strip():
        st.warning("Please enter a valid query.")
        st.stop()

    with st.spinner("Retrieving information..."):
        retrieved_docs = retriever.retrieve(query)
    
    if not retrieved_docs:
        st.error("No relevant information found.")
        st.stop()

    with st.spinner("Generating response..."):
        # ✅ Ensure the retrieved context is properly formatted
        context = "\n".join(retrieved_docs)
        prompt = f"Context:\n{context}\n\nBased on this, answer the question: {query}"
        response = llm.generate_response(prompt)

    st.write("### Response:")
    st.write(response)

    with st.spinner("Generating image..."):
        # ✅ Improve image generation prompt
        enhanced_prompt = f"An artistic illustration of: {response}"

        try:
            response_img = requests.post(COLAB_API_URL, json={"prompt": enhanced_prompt})
            if response_img.status_code == 200:
                image = Image.open(BytesIO(response_img.content))
                st.image(image, caption="Generated Image", use_column_width=True)
            else:
                st.error(f"Failed to generate image: {response_img.status_code} - {response_img.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to Colab API: {e}")
