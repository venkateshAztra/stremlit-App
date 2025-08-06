from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
import os

# Load environment variables (make sure .env contains your HuggingFace token)
load_dotenv()

def load_docs(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(docs)

def build_chain(file_path):
    docs = load_docs(file_path)

    # Sentence-transformer for embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Store vectors in Chroma DB
    vectordb = Chroma.from_documents(docs, embeddings)
    retriever = vectordb.as_retriever()

    # ✅ Correct LLM config — inside function
    llm = HuggingFaceHub(
    repo_id="google/flan-t5-base",
    task="text2text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    model_kwargs={"temperature": 0.3, "max_length": 512}
)

    # Build the RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain
