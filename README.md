# Metaphor x OpenAI Chatbot

## 1. Overview 

![](chatbot.png)

This short project aims to be a chatbot that references and cites real evidence when answering user queries. 

Upon a user query, Metaphor API is used to retrieve web pages with content most likely to be helpful in answering the user. 

Next, the web page contents are processed, embedded using OpenAI, and finally stored in a vector database (cassandra/astra db). 

Lastly, the database is queried using the initial user query and the question is answered using OpenAI's LLM. Both the answer as well as the sources used are displayed in the UI.

## 2. Instructions
1. Clone this repository
2. Change OpenAI key in server/creds/settings.py (sorry for the trouble)
3. Run Server

~~~
cd ../chatbot/server
. env/bin/activate
pip install requirements.txt
flask --app app run
~~~

4. Run Client (in a separate terminal)

~~~
cd ../chatbot/client
npm i
npm run start
~~~

5. Visit localhost:3000

## 3. Closing Remarks

1. Source retrieval could be improved via prompt chaining to generate a more pointed Metaphor API prompt and parameters. Even with autoprompt, it seems sometimes Metaphor isn't able to recognize the complexity behind more complex questions that are passed in e.g. How many points did Jeremy Lin score the first night of Linsanity? In this example, it not only needs to recognize key entities 'Jeremy Lin' and 'Linsanity', but also must recognize the importance of query parameters 'first night' and 'points'. An article detailing a thorough recounting of Linsanity or a press release of the specific game would've been the most useful documents, but our results are all too generic. 

2. Data extraction could be improved by featurizing the web documents more. Currently, only the text is extracted and batched into documents, but important information stored in the structure, URL, and title are largely lost. A solution to this I wasn't able to try as to insert the raw unprocessed html into the vectorestore and use a Markup-understanding LLM such as MarkupLM on huggingface to answer questions. 

3. Features I would build next would be 
    - Chat History: instead of just independent Q&A, include previous conversation and retrieved documents as context for future responses
    - Autonomous Retrieval: currently, the bot follows a fixed workflow of retrieval and response. Ideally, we would want it to somehow know when call Metaphor API for more documents. A simple but faulty solution would be to implement a threshold for the highest similarity score of a document found in the vectorstore.

In sum, the current app could use improvements in both retrieval as well as document understanding, but is able to perform well on general knowledge questions where there exists many text-rich websites on the subject, e.g. biographical facts.

Also, I acknowledge some best practices were thrown out the window for convenience sake but hopefully overall the project captured the right spirit.

