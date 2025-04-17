# 🧑‍🍳 GenAI Sous-Chef

A smart, Gemini-powered culinary assistant that transforms ingredients from your pantry (or a photo) into full-fledged recipes — complete with structured outputs, nutritional breakdowns, and image-guided instructions. Built using LangGraph agents and Gemini API, this project demonstrates the power of GenAI orchestration across multiple modalities.

Designed as a capstone GenAI project for the **Google x Kaggle 5-Day GenAI course**.

---

## 🌟 What Can It Do?

GenAI Sous-Chef can:

- ✅ Accept ingredients as plain text or from a pantry image  
- ✅ Use Gemini Vision to understand visual ingredients *(optional)*  
- ✅ Generate structured, step-by-step recipes using Gemini Flash  
- ✅ Visualize each cooking step using image generation  
- ✅ Compute nutrition insights using AI-generated reasoning  
- ✅ Use LangGraph agents to modularize and chain tasks  
- ✅ Display recipe + image instructions in a unified interface  
- ✅ Produce structured JSON output for integrations (shopping lists, apps, etc.)

---

## ✨ GenAI Capabilities Demonstrated

This project showcases **7 key GenAI capabilities**:

- [x] Structured Output / JSON Mode  
- [x] Few-shot Prompting  
- [x] Image Understanding (Gemini Vision)  
- [x] Function Calling (via LangGraph agent nodes)  
- [x] Agents (LangGraph task orchestration)  
- [x] Long Context Window (multi-step recipe and nutrition processing)  
- [x] Grounding (based on user-provided ingredient context)  

---

## 🏗️ Project Structure

```text
.
├── agents.py               # LangGraph pipeline definition
├── config.py               # Environment and API keys
├── main.py                 # CLI entry point for generation
├── utils.py                # Core logic for recipe gen, nutrition, visuals
├── notebooks/
│   └── sous_chef_demo.ipynb   # Step-by-step walkthrough notebook
├── data/                   # Pantry image samples (optional)
└── README.md
```

## 🚀 Quickstart

### 1. Clone the repository


```bash
git clone https://github.com/your-username/genai-sous-chef.git
cd genai-sous-chef
```

### 2. Set up the Conda environment

Create and activate the environment from `environment.yaml`:

```bash
conda env create -f environment.yaml
conda activate genai-sous-chef
```

### 3. Set up your Google API Key (for Gemini access)

You can either export it as an environment variable:

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

Or create a `.env` file in the project root directory with:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run the notebook demo

Launch Jupyter and open the notebook:

```bash
jupyter notebook notebooks/sous_chef_demo.ipynb
```

Follow the instructions to generate recipes using either text or image input.

## 🧠 Example Pipeline

1. Ingredients →
2. generate_recipe agent node (Gemini Flash) →
3. generate_images node (Gemini Image model) →
4. get_nutrition node (Gemini Flash) →
5. 📋 Combined structured output with step-wise visuals and insights

## 📜 License

MIT License — free to use, remix, and make delicious AI creations 🍲
