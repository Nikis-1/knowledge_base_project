
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai 

from .pdf_loader import load_text_from_file, split_into_chunks 

embedding_model_name = "models/text-embedding-004"
llm_model_name = "gemini-2.0-flash"

try:
    genai.configure(api_key="Your_GEMINI_API_KEY")
    print("Gemini client successfully initialized.")
except Exception:
    print("FATAL ERROR: Gemini client failed to initialize (Key missing or invalid).")


class VectorStoreMultiPDF: 
    """
    Manages loading, embedding, and querying MULTIPLE PDF documents.
    """
    def __init__(self):
        self.chunk_stores = {}    
        self.embedding_stores = {} 

    def load_pdf(self, file_path, filename): 
        """Loads PDF, splits into chunks, and embeds the chunks, storing by filename."""
        print(f"\n Loading PDF: {filename} from {file_path}")
        text = load_text_from_file(file_path)
        self.chunks = split_into_chunks(text)

        if not self.chunks:
            print("Skipping embedding: No content found in PDF.")
            return

        print(f"Splitting into {len(self.chunks)} chunks...")
        print("Generating embeddings...")

        try:
            
            response = genai.embed_content(
                model=embedding_model_name,
                content=self.chunks, 
                task_type="RETRIEVAL_DOCUMENT"
            )
            
            doc_embeddings = np.array(response.get("embedding", []))

            self.chunk_stores[filename] = self.chunks 
            self.embedding_stores[filename] = doc_embeddings
            
            print(f"Embedded {len(doc_embeddings)} chunks for file: {filename}")

        except Exception as e:
            print(f"Embedding failed: {e}")

    def _synthesize_answer(self, question, context):
        """Generate answer using the GenerativeModel class."""
        
        prompt = (
            "You are a helpful assistant. Synthesize a concise answer "
            "to the user's question based ONLY on the following CONTEXTS. "
            "Combine information from all relevant contexts. "
            "If the answer is not present, state that you cannot find the information.\n\n"
            f"---CONTEXTS---\n{context}\n\n"
            f"---QUESTION---\n{question}"
        )

        try:
            model = genai.GenerativeModel(llm_model_name) 
            
            response = model.generate_content(prompt) 

            return response.text.strip()

        except Exception as e:
            print(f"LLM generation failed: {e}")
            return "Failed to generate answer using LLM."

    def query(self, question):
        """Retrieves best matching chunk(s) across ALL loaded documents."""
        if not self.embedding_stores:
            return "No documents loaded. Please upload a PDF first."

        query_response = genai.embed_content(
            model=embedding_model_name,
            content=[question], 
            task_type="RETRIEVAL_QUERY"
        )
        query_vector = np.array(query_response.get("embedding", []))

        best_score = -1.0
        best_chunks = []
        
        for filename, doc_embeddings in self.embedding_stores.items():
            
            similarities = cosine_similarity(query_vector.reshape(1, -1), doc_embeddings).flatten()
            
            top_indices = similarities.argsort()[-3:][::-1]
            current_highest_score = similarities[top_indices[0]]
            
            if current_highest_score > best_score:
                best_score = current_highest_score
                
                doc_chunks = self.chunk_stores[filename]
                retrieved_chunks = [doc_chunks[i] for i in top_indices]
                best_chunks = retrieved_chunks
                
        
        print(f"Highest similarity score across all documents: {best_score:.4f}")

        if best_score < 0.40: 
            return "Sorry, I couldn't find anything relevant in any of the uploaded documents."

        context = "\n---\n".join(best_chunks) 
        
        return self._synthesize_answer(question, context)

vector_store = VectorStoreMultiPDF()

def load_pdf_to_store(file_path, filename):
    vector_store.load_pdf(file_path, filename)

def query_pdf_store(question):
    return vector_store.query(question)

def clear_vector_store():
    """Function to clear the indexed data, called by the 'Clear Context' button."""
    vector_store.chunk_stores = {}
    vector_store.embedding_stores = {}
    print("RAG context cleared.")