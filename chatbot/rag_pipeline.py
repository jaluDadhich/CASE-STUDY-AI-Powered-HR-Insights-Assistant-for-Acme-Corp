import os
from dotenv import load_dotenv
os.environ["TRANSFORMERS_NO_TF"] = "1"

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Paths
POLICY_PATH = os.path.abspath("acme_hr_policy.txt")
VECTOR_STORE_DIR = os.path.abspath("vector_store")
VECTOR_STORE_INDEX = os.path.join(VECTOR_STORE_DIR, "faiss_index")

# OpenAI API Key must be in environment variable OPENAI_API_KEY

# Embedder - using OpenAI embeddings
embedder = OpenAIEmbeddings()

# Load and chunk document
def load_and_split_doc():
    loader = TextLoader(POLICY_PATH, encoding="utf-8")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(documents)
    return chunks

# Create or load FAISS vector store
def get_vector_store():
    if os.path.exists(VECTOR_STORE_INDEX):
        vectordb = FAISS.load_local(VECTOR_STORE_INDEX, embedder, allow_dangerous_deserialization=True)
    else:
        os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
        chunks = load_and_split_doc()
        vectordb = FAISS.from_documents(chunks, embedder)
        vectordb.save_local(VECTOR_STORE_INDEX)
    return vectordb

# LLM: Use OpenAI GPT-3.5-Turbo
def get_llm():
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)

# Build QA chain with injected prompt in question
def get_hr_answer(question: str) -> str:
    vectordb = get_vector_store()
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()

    # Custom summarizing prompt injected directly into question
    def build_prompt(context: str, question: str) -> str:
        return (
            "You are a helpful HR assistant. Based on the following context, answer the employee's question clearly, completely, and in your own words.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer:"
        )

    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = build_prompt(context, question)
    result = llm.invoke(prompt)
    return result.content if hasattr(result, 'content') else str(result)
