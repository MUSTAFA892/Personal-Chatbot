from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# FAISS index file path
vectordb_file_path = "faiss_index"

def create_vector_db():
    """Loads CSV, creates FAISS index, and saves it locally."""
    try:
        # Load environment variables
        load_dotenv()
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        # Initialize HuggingFace embeddings
        sentence_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        print("Embeddings model loaded successfully!")

        # Load CSV data
        loader = CSVLoader(file_path='Data/sample.csv', source_column="prompt")
        data = loader.load()

        if not data:
            print("No data loaded. Check the CSV file format!")
            return

        print(f"Loaded {len(data)} documents from CSV.")
        print("Sample Data:", data[:3])

        # Create FAISS vector store
        vectordb = FAISS.from_documents(documents=data, embedding=sentence_embeddings)
        print("FAISS Index successfully created!")

        # Save FAISS index locally
        vectordb.save_local(vectordb_file_path)
        print(f"FAISS index saved successfully at {vectordb_file_path}")

    except Exception as e:
        print(f"Error in FAISS index creation: {e}")

def get_qa_chain():
    """Loads FAISS index, creates retriever, and builds QA chain."""
    try:
        # Ballot Load environment variables
        load_dotenv()
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        # Initialize Google Gemini LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        print("LLM initialized successfully!")

        # Initialize HuggingFace embeddings
        sentence_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        print("Embeddings model loaded successfully!")

        # Load FAISS index
        vectordb = FAISS.load_local(
            vectordb_file_path,
            sentence_embeddings,
            allow_dangerous_deserialization=True
        )
        print("FAISS index loaded successfully!")

        # Create retriever
        retriever = vectordb.as_retriever(score_threshold=0.7)

        # Define prompt template
        prompt_template = """Given the following context and a question, generate an answer based on this context only.
        In the answer, try to provide as much text as possible from the "response" section in the source document context without making changes.
        If the answer is not found in the context, state "I don't know." Do not make up an answer.

        CONTEXT: {context}

        QUESTION: {question}"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Create RetrievalQA Chain
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            input_key="query",
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

        print("QA chain created successfully!")
        return chain

    except Exception as e:
        print(f"Error loading FAISS index or creating QA chain: {e}")
        return None

if __name__ == "__main__":
    create_vector_db()