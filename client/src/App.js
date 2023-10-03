import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [inputQuery, setinputQuery] = useState('');
  const [loading, setStatus] = useState(false);
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);


  const handleTextareaChange = (event) => {
    setinputQuery(event.target.value);
  };

  const handleButtonClick = () => {
    console.log("Button clicked!");
    sendRequest();
    setStatus(true);
  }; 

  function sendRequest() {
    const data = {
      'query': inputQuery
    }; 
    axios.get(`${API_BASE_URL}/answer`, {params: data})
    .then(response => {
      console.log(response.data);
      setStatus(false);
      setAnswer(response.data.answer);
      if (response.data.sources.length > 0) {
        const sourceURLs = response.data.sources.split(',');
        const sources = sourceURLs.map((url) => (
          <div>
            <a href={url}>
              {url}
            </a>
            <br/>
          </div>
        ));
        setSources(sources);
      }
      
    })
    .catch(error => {
      console.error(error);
      setStatus(false);
    });
  };

  return (
    <div className="App">
      <header className="App-header">
      Metaphor x RAG
      </header>
      
      <hr />
      <div className="form-section">
            <textarea
                rows="3"
                className="form-control"
                placeholder="Ask me anything and I'll answer and back it up with evidence!"
                value={inputQuery}
                onChange={handleTextareaChange}
            ></textarea>
            <button className="submit-button" onClick={handleButtonClick}>
                Generate Response 🤖
            </button>
            
        </div>
        
        <div className="response-section">
            {loading && <div className="loading">generating response...</div>}
            {answer.length>0 && <div className="answer">
              Sources: {sources.length===0 && 'None found'}{sources.length>0 && sources}<br/>{answer}
                </div>}
        </div>
    </div>
  );
}

export default App;
