<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader  # Updated import
from langchain_chroma import Chroma  # Updated import
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, 
            template_folder="../frontend/templates", 
            static_folder="../frontend/static")

# Initialize components once
def initialize_llm():
    return ChatGroq(
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
    )

def create_vector_db():
    loader = DirectoryLoader("./content", glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')  # Updated class
    vector_db = Chroma.from_documents(texts, embeddings, persist_directory='./chroma_db')
    vector_db.persist()
    return vector_db

def setup_qa_chain(vector_db, llm):
    retriever = vector_db.as_retriever()
    prompt_template = """You are a compassionate mental health chatbot. Respond thoughtfully to the following question:
    {context}
    User: {question}
    Chatbot: """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )

print("Initializing Chatbot...")
llm = initialize_llm()
db_path = "./chroma_db"

if not os.path.exists(db_path):
    vector_db = create_vector_db()
else:
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')  # Updated class
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)

qa_chain = setup_qa_chain(vector_db, llm)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input.strip():
        return jsonify({'response': 'Please provide a valid input'})
    
    try:
        response = qa_chain.run(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f"Error processing request: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
=======
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from model.chatbot_model import chatbot_response  # Import chatbot function

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        bot_response = chatbot_response(user_input)
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 95295d86547b39ce8334c91993909f312c4be340
