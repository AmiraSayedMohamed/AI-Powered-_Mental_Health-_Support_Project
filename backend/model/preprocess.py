# file to generate the embeddings and store them in the ChromaDB directory.# backend/model/preprocess.py
import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load PDFs from the directory
loader = DirectoryLoader("backend/model/content", glob='*.pdf', loader_cls=PyPDFLoader)
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Generate embeddings
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# Create and persist ChromaDB
DB_PATH = "backend/model/chroma_db"
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

vector_db = Chroma.from_documents(texts, embeddings, persist_directory=DB_PATH)
vector_db.persist()
print(f"✅ ChromaDB embeddings generated and stored in '{DB_PATH}'.")