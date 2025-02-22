import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import logging
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()  # Load environment variables from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ Error: GROQ_API_KEY is missing! Add it to the .env file.")

DB_PATH = "model/chroma_db"
if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"❌ Error: ChromaDB directory '{DB_PATH}' not found! Run preprocessing script to generate embeddings.")

def initialize_llm():
    """Initialize the language model (LLM)."""
    try:
        llm = ChatGroq(
            temperature=0,
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile"
        )
        logging.info("✅ LLM successfully initialized.")
        return llm
    except Exception as e:
        logging.error(f"❌ Error initializing LLM: {str(e)}")
        
def load_vector_db():
    """Load the vector database from ChromaDB."""
    try:
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        logging.info("✅ Vector database loaded successfully.")
        return vector_db
    except Exception as e:
        logging.error(f"❌ Error loading vector database: {str(e)}")
        raise

def create_vector_db():
    # Load PDFs from the "/content" directory
    loader = DirectoryLoader("/content", glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Generate embeddings
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Create and persist ChromaDB
    vector_db = Chroma.from_documents(texts, embeddings, persist_directory='./chroma_db')
    vector_db.persist()

    print("ChromaDB created and data saved")
    return vector_db
    
def setup_qa_chain(vector_db, llm):
    """Set up the QA chain for chatbot responses."""
    try:
        retriever = vector_db.as_retriever()
        prompt_templates = """You are a compassionate mental health chatbot. Respond thoughtfully to the following question:
        {context}
        User: {question}
        Chatbot:"""
        PROMPT = PromptTemplate(template=prompt_templates, input_variables=['context', 'question'])

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT}
        )
        logging.info("✅ QA Chain setup completed.")
        return qa_chain
    except Exception as e:
        logging.error(f"❌ Error setting up QA chain: {str(e)}")
        raise

# Initialize components
llm = initialize_llm()
vector_db = create_vector_db()
qa_chain = setup_qa_chain(vector_db, llm)

def chatbot_response(user_input):
    """Generate chatbot response."""
    if not user_input.strip():
        return "⚠️ Please provide a valid input."
    
    try:
        response = qa_chain.run(user_input)
        return response
    except Exception as e:
        logging.error(f"❌ Error generating chatbot response: {str(e)}")
        return "⚠️ Sorry, I couldn't process your request. Please try again later."
