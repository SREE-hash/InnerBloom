import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI as LlamaOpenAI

# Load API key from environment
llama_llm = LlamaOpenAI(
    model="mistralai/mistral-7b-instruct:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Load documents from the "data" folder
documents = SimpleDirectoryReader("data").load_data()

# Build vector index with LLM
index = VectorStoreIndex.from_documents(documents, llm=llama_llm)

# Create a query engine
query_engine = index.as_query_engine()

# Example query
response = query_engine.query("Summarize the documents in 3 bullet points.")
print(response)
