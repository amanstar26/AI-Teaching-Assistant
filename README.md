# 🎓 AI Teaching Assistant

An AI-powered Teaching Assistant built with **Streamlit**, **RAG (Retrieval-Augmented Generation)**, **FAISS**, **Sentence Transformers**, and **Ollama Model**. The application allows users to upload PDF documents, ask questions, generate question papers, create flashcards, build study plans, and generate PowerPoint presentations from study material.

### Home Page

![Home](assets/home.jpeg)

> **⚡ Offline Support**
>
> The application automatically downloads the embedding model (`BAAI/bge-small-en-v1.5`) during the first run and stores it locally in the `models/` directory.
>
> After the initial download, the application works **completely offline** for embedding generation. No internet connection is required unless you choose to download a different embedding model.
>
> **Note:** Since the project uses **Ollama**, the `qwen2.5:1.5b` model must also be downloaded once using:
>
> ```bash
> ollama pull qwen2.5:1.5b
> ```
>
> Once both models are available locally, the application can run entirely offline.

---

## ✨ Features

- 📄 Upload and analyze PDF documents
- 🔍 Semantic search using FAISS vector database
- 🤖 AI-powered question answering with Ollama Model
- 📝 Generate question papers from uploaded content
- 🧠 Generate flashcards for quick revision
- 📅 Create personalized study plans
- 📊 Generate PowerPoint presentations from study material
- 🖼️ OCR support for image-based PDFs
- 💾 Local embedding model caching for offline reuse

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Ollama
- Sentence Transformers
- FAISS
- LangChain Text Splitters
- PyMuPDF
- RapidOCR
- ReportLab
- Python-PPTX

---

## 📂 Project Structure

```
AI-Teaching-Assistant/
│
├── generators/
│   ├── ppt_gen.py
│   ├── qp.py
│   └── study_plan.py
│
├── models/              # Created automatically on first run
├── uploads/             # Stores uploaded PDFs
├── vector_store/        # Stores FAISS index
│
├── app.py
├── embedding_model.py
├── pdf_processor.py
├── rag_engine.py
├── vector_store.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/amanstar26/AI-Teaching-Assistant.git
```

```bash
cd AI-Teaching-Assistant
```

---

## 2. Create a Virtual Environment (Recommended)

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Ollama

Download and install Ollama from:

https://ollama.com/download

Verify the installation:

```bash
ollama --version
```

---

## 💡 Choosing an Ollama Model

This project is configured to use **Qwen2.5:1.5B** by default because it provides a good balance between performance and hardware requirements. It runs well on most modern laptops and desktop computers.

If your system has more RAM and a more powerful CPU/GPU, you can use larger models for improved response quality. Simply pull the desired model with Ollama and update the model name in `rag_engine.py`.

### Recommended Models

| Model | Recommended Hardware | Notes |
|--------|----------------------|-------|
| `qwen2.5:1.5b` | 8 GB+ RAM | Default model. Fast and lightweight. |
| `qwen2.5:3b` | 16 GB+ RAM | Better reasoning while remaining efficient. |
| `qwen2.5:7b` | 16–32 GB+ RAM | Higher-quality responses with moderate hardware. |
| `gemma3:4b` | 16 GB+ RAM | Good balance of speed and quality. |
| `gemma3:12b` | 32 GB+ RAM | Stronger reasoning and content generation. |
| `llama3.1:8b` | 16–32 GB+ RAM | Excellent general-purpose model. |
| `mistral:7b` | 16 GB+ RAM | Fast and capable for RAG applications. |

### Example

Download another model:

```bash
ollama pull gemma3:4b
```

Then change the model name in `rag_engine.py`:

```python
response = ollama.chat(
    model="gemma3:4b",
    messages=messages
)
```

> **Note:** Larger models generally produce higher-quality responses but require more system memory and computational resources. Choose the model that best matches your hardware.

## 5. Download the Qwen2.5 Model

Pull the model from Ollama:

```bash
ollama pull qwen2.5:1.5b
```

Verify it is installed:

```bash
ollama list
```

---

## 6. Start Ollama

Make sure the Ollama service is running.

You can test the model using:

```bash
ollama run qwen2.5:1.5b
```

Type `/bye` or press `Ctrl+C` to exit.

---

## 7. Run the Application

```bash
streamlit run app.py
```

The application will automatically:

- Download the embedding model (first run only)
- Create the `models/` folder if it does not exist
- Save the embedding model locally for future offline use
- Create FAISS indexes after processing PDFs

---

## 📚 How It Works

1. Upload a PDF document.
2. Text is extracted using PyMuPDF.
3. OCR is applied to image-based pages.
4. The text is split into chunks.
5. Sentence Transformers generate embeddings.
6. Embeddings are stored in a FAISS vector database.
7. Relevant chunks are retrieved based on user queries.
8. Google Gemini generates context-aware responses.

---

## 📷 Screenshots

> Add screenshots of your application here.

Example:

```
assets/
├── home.jpeg
└── question_paper.jpeg
```

---

## 📦 Requirements

- Python 3.10 or above
- Ollama installed
- Qwen2.5 1.5B model (`qwen2.5:1.5b`)
- Internet connection (only required on the first run to download the embedding model)

---

## 🔮 Future Improvements

- Support for DOCX and TXT files
- Multi-document chat
- Conversation history
- Quiz generation
- Audio summaries
- Multi-language support
- Cloud deployment

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Aman Patel**

If you found this project useful, consider giving it a ⭐ on GitHub.