
from langchain.vectorstores import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from .vector_service import embeddingModel
# Charger .env
load_dotenv()



dbVector = Chroma(persist_directory="/dbVector", embedding_function=embeddingModel)

memory = ConversationBufferMemory(memory_key="history", return_messages=True, k=2)
llm = ChatGroq(
    base_url="https://api.groq.com",
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    api_key=os.getenv("GROQ_API_KEY"),
)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
)
