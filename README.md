# 🧑‍🍳 GenAI Sous-Chef

A smart, Gemini-powered culinary assistant that takes ingredients from your pantry (or a photo of them) and cooks up delicious recipes — complete with structured outputs, nutritional info, and even visual recipe cards. Designed as a capstone GenAI project for the Google x Kaggle 5-Day GenAI course.

---

## 🌟 What Can It Do?

GenAI Sous-Chef can:

- ✅ Accept ingredients as text or photo  
- ✅ Understand your pantry via image understanding (Gemini Vision)  
- ✅ Generate step-by-step recipes using Gemini 1.5 Pro  
- ✅ Output structured JSON for downstream use (shopping list, meal planning, etc.)  
- ✅ Generate visual recipe cards with image captions  
- ✅ Rate the recipe or give alternate options using few-shot prompts  
- ✅ Ground recipes to real nutritional guidelines (optional RAG)  
- ✅ Cache context for longer interactions  
- ✅ Log inputs/outputs with MLOps-style observability  

---

## ✨ GenAI Capabilities Demonstrated

This project demonstrates 12+ GenAI capabilities:

- [x] Structured Output / JSON Mode  
- [x] Few-shot Prompting  
- [x] Document Understanding  
- [x] Image Understanding (Gemini Vision)  
- [x] Function Calling  
- [x] Long Context Window  
- [x] Context Caching  
- [x] Grounding  
- [x] Embeddings (for recipe similarity or tags)  
- [x] Retrieval Augmented Generation (optional for nutrition grounding)  
- [x] Vector Search (planned)  
- [x] MLOps-style Logging  

---

## 🏗️ Project Structure

TBD

## 🚀 Quickstart

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/genai-sous-chef.git
    cd genai-sous-chef
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Google API Key (for Gemini access):

    You can either export it as an environment variable:

    ```bash
    export GOOGLE_API_KEY="your_api_key_here"
    ```

    Or create a `.env` file in the project root directory with:

    ```env
    GOOGLE_API_KEY=your_api_key_here
    ```

4. Run the notebook demo:

    Launch Jupyter and open the notebook:

    ```bash
    jupyter notebook notebooks/demo_genai_sous_chef.ipynb
    ```

    Follow the instructions to generate recipes using either text or image input.

## 📜 License

MIT License — free to use, remix, and make delicious AI creations 🍲
