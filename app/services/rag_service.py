
import os
from groq import Groq
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class RagService:
    def __init__(self):
        self.groq_client = Groq(api_key=os.get('GROQ_API_KEY'))
        self.embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
        self.vector_store = None
        
    
    def initialize(self):
        loader = TextLoader("data/medhive.txt")
        document = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap = 200
        )
        
        text = text_splitter.split_documents(document)
        
        self.vector_store = FAISS.from_documents(text, self.embeddings)
        
        
    def get_context(self, question: str, k: int = 3) -> str:
        
        docs = self.vector_store.similarity_search(question, k=k)
        return "\n\n".join([doc.page_content for doc in docs])
        
        
    def generate_response(self, question: str, context: str) -> str:
        """Generate a response using the Groq API with the provided context."""
        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f""
                            f"{context}"
                        )
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
        
rag_service = RagService()