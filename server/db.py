# Vector support using Langchain, Apache Cassandra (Astra DB is built using
# Cassandra), and OpenAI (to generate embeddings)
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

# These are used to authenticate with Astra DB
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Support for dataset retrieval with Hugging Face
from datasets import load_dataset
from creds.settings import ASTRA_DB_SECURE_BUNDLE_PATH, ASTRA_DB_TOKEN_JSON_PATH, ASTRA_DB_KEYSPACE, OPENAI_API_KEY

import json


cloud_config= {
  "secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH
}
with open(ASTRA_DB_TOKEN_JSON_PATH) as f:
    secrets = json.load(f)
ASTRA_DB_APPLICATION_TOKEN = secrets["token"] 

auth_provider=PlainTextAuthProvider("token", ASTRA_DB_APPLICATION_TOKEN)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
astraSession = cluster.connect()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
big_llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo-16k-0613')

myEmbedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

myCassandraVStore = Cassandra(
    embedding=myEmbedding,
    session=astraSession,
    keyspace=ASTRA_DB_KEYSPACE,
    table_name="metaphor_docs",
)


class VectorDB(object): 
    def __new__(cls):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(VectorDB, cls).__new__(cls)
        return cls.instance
    
    def __init__(self): 
        self.vstore = myCassandraVStore
        self.vectorIndex = VectorStoreIndexWrapper(vectorstore=self.vstore)
        self.vstore.clear()

    def add_docs(self, vstore_docs): 
        """Insert langchain Documents into the vectorstore"""
        self.vstore.add_documents(vstore_docs) 
    
    def query(self, query_text, verbose=True): 
        """Answer a question by querying the vectorstore"""
        if verbose: 
            for doc, score in self.vstore.similarity_search_with_score(query_text, k=3):
                print("  %0.4f \"%s ...\"" % (score, doc.metadata))
        answer = self.vectorIndex.query_with_sources(query_text, llm=big_llm)
        print("response: ", answer)
        return answer