
from flask import Flask, request, render_template, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from .vector_store import load_pdf_to_store, query_pdf_store, clear_vector_store 

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "txt"}

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "rag_search_secret") 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    status_message = None
    
    if 'indexed_files' not in session:
        session['indexed_files'] = []

    if request.method == "POST":
        if 'clear_context' in request.form:
            clear_vector_store()
            session.pop('indexed_files', None)
            status_message = "🗑️ Knowledge base cleared. Ready for new documents."
            return redirect(url_for('index')) 
        if "pdf_file" in request.files:
            files = request.files.getlist("pdf_file")
            indexed_count = 0

            clear_vector_store()
            session['indexed_files'] = []
            session.modified = True 
            
            for file in files:
                if file.filename == '':
                    continue 
                
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    
                    try:
                       
                        file.save(filepath)
                        load_pdf_to_store(filepath, filename) 
                        
                        if filename not in session['indexed_files']:
                            session['indexed_files'].append(filename)
                            session.modified = True 
                            indexed_count += 1
                            
                    except Exception as e:
                        status_message = f"Error indexing file {filename}: {e}"
                        print(status_message)
                        
            if indexed_count > 0:
                status_message = f"Successfully indexed {indexed_count} new document(s)! Ready to search."
            elif status_message is None:
                status_message = "Please select at least one valid file."
        elif "query" in request.form:
            query = request.form.get("query")
            
            if not session.get('indexed_files'):
                status_message = "Cannot search. Please upload a document first."
            elif query:
                answer = query_pdf_store(query)
                status_message = "Search Complete"
            else:
                status_message = "Please enter a query in the search box."
    return render_template("index.html", 
                           answer=answer, 
                           status=status_message,
                           indexed_files=session.get('indexed_files', []))

if __name__ == "__main__":
    app.run(debug=True)