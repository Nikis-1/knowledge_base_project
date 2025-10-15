
import os
from .vector_store import load_pdf_to_store, query_pdf_store, clear_vector_store

def main():
    print("=================================================================")
    print("Welcome to the Multi-Document RAG Test Console!")
    print("-----------------------------------------------------------------")
    print("Commands:")
    print("  UPLOAD <path/to/file> <filename.pdf> - Indexes a new document.")
    print("  CLEAR - Clears all indexed documents.")
    print("  EXIT - Quit the console.")
    print("=================================================================")

    while True:
        user_input = input("Input: ").strip()
        
        if user_input.lower() == "exit":
            print("Exiting RAG console.")
            break
        if user_input.lower() == "clear":
            clear_vector_store()
            print("Console: All knowledge base context has been cleared.")
            continue
        if user_input.lower().startswith("upload "):
            try:
                parts = user_input[7:].strip().split()
                if len(parts) < 2:
                    print("Error: Usage is 'UPLOAD <path> <filename.pdf>'")
                    continue
                    
                pdf_path = parts[0]
                filename = parts[1]
                load_pdf_to_store(pdf_path, filename) 
                
            except Exception as e:
                print(f"Error loading PDF: {e}")
            continue
        if user_input:
            answer = query_pdf_store(user_input)
            print("Answer:\n", answer)

if __name__ == "__main__":
    main()