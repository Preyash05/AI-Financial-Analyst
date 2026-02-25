# AI Financial Analyst (RAG Chatbot)

This is a Retrieval-Augmented Generation (RAG) application that acts as an AI financial analyst. It is designed to read, process, and answer complex questions based on Nvidia's SEC 10-K financial report.

## Tech Stack
* **Language:** Python
* **Frontend:** Streamlit
* **LLM:** Google Gemini 2.5 Flash
* **Orchestration:** LangChain
* **Vector Database:** ChromaDB

## How It Works
1. **Document Loading:** The app reads a massive 130-page PDF (Nvidia's SEC 10-K).
2. **Chunking & Embedding:** It splits the text into smaller, manageable chunks and converts them into vector embeddings using Google's embedding model.
3. **Storage:** The embeddings are saved locally in a ChromaDB vector database.
4. **Retrieval & Generation:** When a user asks a question, the app searches the database for the most relevant financial text, sends that context to the Gemini LLM, and generates an accurate, fact-based answer.

## How to Run Locally
1. Clone this repository.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory and add your API key: `GOOGLE_API_KEY="your_api_key_here"`.
4. Place your target PDF inside the `data/` folder and update the file path in `app.py`.
5. Start the application by running: 
   ```bash
   streamlit run app.py