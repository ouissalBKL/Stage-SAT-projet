from langchain.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

embeddingModel = OllamaEmbeddings(
    base_url="http://localhost:11434", model="nomic-embed-text"
)

dbVector = Chroma(persist_directory="/dbVector", embedding_function=embeddingModel)


def search_similarity(question, k=2):
    contexte = dbVector.similarity_search(question, k=k)
    return "\n".join(doc.page_content for doc in contexte)
