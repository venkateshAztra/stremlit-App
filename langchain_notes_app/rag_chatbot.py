import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub  # optional

# Load .env
load_dotenv()

# Load values from .env
TEXT_FILE = os.getenv("TEXT_FILE")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL_NAME")

# Load and process document
loader = TextLoader(TEXT_FILE)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# HuggingFace Embeddings
embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
db = Chroma.from_documents(docs, embedding)
retriever = db.as_retriever()

# For now: use basic LLM placeholder — will not generate answers unless you configure HuggingFaceHub or OpenRouter model
from langchain.chains.question_answering import load_qa_chain
from langchain.llms.fake import FakeListLLM

llm = FakeListLLM(responses=["This is a placeholder response."])
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

while True:
    query = input("Ask a question (or type 'exit'): ")
    if query.lower() in ["exit", "quit"]:
        break
    answer = qa.run(query)
    print("Answer:", answer)
