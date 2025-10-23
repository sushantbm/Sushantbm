### ** Workflow**
1. **🏪 Tab 1: Bank Selection** - Choose your bank FIRST
2. **📋 Tab 2: Preprocessing** - Process documents for selected bank
6. **🤖 Tab 6: Chatbot** - Query your bank-specific analyses

This is the Streamlit project, 

First, we load financial documents—either from PDFs, URLs, or a database—into the system. These documents are then split into manageable chunks, or 'splits,' for easier processing.

Each chunk is embedded using OpenAI embeddings and stored in a vector database like Chroma or FAISS, which is our 'vectorstore.' 

When a user asks a question, that query is also embedded, and the system retrieves the most relevant chunks by comparing embeddings.

These relevant pieces are then included as context in a prompt which is sent to an OpenAI LLM, such as GPT-3.5-turbo, to generate a tailored, context-aware answer.

This entire process ensures that responses are grounded in the source documents, improving both accuracy and explainability for financial analysis use cases.

The OpenAI API key used for the embeddings and LLM calls is securely stored in our environment file to keep credentials safe


1. install the pre req :
   
pip install -r requirements.txt

2. Run Streamlit:
   
streamlit run main.py
