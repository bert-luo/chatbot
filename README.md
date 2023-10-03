# Metaphor x OpenAI Chatbot

## 1. Overview 
This short project aims to be a chatbot that references and cites real evidence when answering user queries. 

Upon a user query, Metaphor API is used to retrieve web pages with content most likely to be helpful in answering the user. 

Next, the web page contents are processed, embedded using OpenAI, and finally stored in a vector database (cassandra/astra db). 

Lastly, the database is queried using the initial user query and the question is answered using OpenAI's LLM

## 2. Instructions

## 3. Closing Remarks



