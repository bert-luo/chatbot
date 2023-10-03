from flask import Flask, request, jsonify
from flask_cors import CORS

from metaphor_python import Metaphor 
import openai

from langchain.schema.document import Document
import html2text

from db import VectorDB
from creds.settings import METAPHOR_API_KEY, OPENAI_API_KEY

app = Flask(__name__)
CORS(app)

VDB = VectorDB()

metaphor = Metaphor(METAPHOR_API_KEY)
openai.api_key = OPENAI_API_KEY


def process_contents(contents, batch_size=500): 
    """clean and batch the html website text"""
    h = html2text.HTML2Text()
    text = h.handle(contents)

    lines = text.split('\n')
    groups = []
    start = 0
    while start < len(lines):
        end = start + batch_size
        doc_lines = lines[start:end]
        doc_text = '\n'.join(doc_lines)
        groups.append(doc_text)
        start += int(batch_size*0.9)
    return groups

def fetch_documents(query, num_docs=10): 
    """
    based on user query, find docs using metaphor and upload them to vector database
    """
    QUERY_INTRO = """
    credible websites or documents that would be helpful 
    in answering the following question:\n
    """
    fetch_query = QUERY_INTRO + query
    search_response = metaphor.search(
        fetch_query, num_results=num_docs, use_autoprompt=False
    )
    contents_result = search_response.get_contents()

    vstore_docs = []
    for result in contents_result.contents: 
        text_batches = process_contents(result.extract)
        for text_chunk in text_batches:
            vstore_doc = Document(
                page_content=text_chunk,
                metadata={
                    'title': result.title, 
                    'source': result.url
                }, 
            )
            vstore_docs.append(vstore_doc)
    VDB.add_docs(vstore_docs)
    

@app.route("/")
def test():
    print('flask works')
    return {'question': 'tell me about amoebas', 'answer': '\nAmoebas are single-celled organisms that can take different shapes. They are known for their ability to change the shape of their cell membrane by extending and retracting their pseudopods. \n', 'sources': 'trust me bro 44'}

@app.route("/answer", methods=["GET"])
def chat_completion():
    """
    sends answer and referenced URL 
    """
    try:
        params = request.args
        query = params.get('query')
        print('query: ', query, type(query))
        fetch_documents(query, num_docs=5)
        print('successfully fetched docs')
        answer_object = VDB.query(query) 
        print('retrieved answer')
        return answer_object
    except Exception as e: 
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)