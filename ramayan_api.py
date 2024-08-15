from fastapi import FastAPI
from llama_index.core import StorageContext, load_index_from_storage
from custom_llm import OurLLM
from llama_index.core import ServiceContext, set_global_service_context
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

llmR = OurLLM()
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

set_global_service_context(ServiceContext.from_defaults(llm=llmR, embed_model=embed_model, chunk_size=512, context_window = 2048, num_output=256))
storage_context = StorageContext.from_defaults(persist_dir="store_embd")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()

app = FastAPI()

@app.post("/post")
async def ramayan(post: str):
    response = query_engine.query(post)
    return response
