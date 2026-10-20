from fastapi import FastAPI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage
from custom_llm import OurLLM
from llama_index.core import ServiceContext, set_global_service_context
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core import get_response_synthesizer
from llama_index.core.response_synthesizers import BaseSynthesizer

llmR = OurLLM()
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
set_global_service_context(ServiceContext.from_defaults(llm=llmR, embed_model=embed_model, chunk_size=1024, context_window = 2048, num_output=256))


storage_context = StorageContext.from_defaults(persist_dir="balakanda_recursive_test")
index = load_index_from_storage(storage_context)


from llama_index.llms.openai import OpenAI
from llama_index.core import PromptTemplate

first_answer = ""
node_s = 0

class RAGStringQueryEngine(CustomQueryEngine):
    """RAG String Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OurLLM


    def custom_query(self, query_str: str):
        global first_answer
        global node_s
        nodes = self.retriever.retrieve(query_str)
        nodes = nodes[-3:]
        # print nodes to a log file
        with open("log.txt", "w") as f:
            for n in nodes:
                f.write("number: " + str(n.metadata["r_id"]) + "\n")
                # f.write("canto_summary: " + str(n.metadata["canto_summary"]) + "\n")
                f.write("gpt paragraph used: \n" + n.node.get_content())
                f.write("\n\n")
            f.write("\n")
        with open("log_big.txt", "a") as f:
            for n in nodes:
                f.write("number: " + str(n.metadata["r_id"]) + "\n")
                f.write("canto_summary: " + str(n.metadata["canto_summary"]) + "\n")
                f.write("gpt paragraph used: \n" + n.node.get_content())
                f.write("\n\n")
            f.write("\n")
        context_str = "\n\n".join([n.node.get_content() for n in nodes])
        # context_str = "\n\n".join([(str(n.metadata["r_id"]) + " ") for n in nodes])
        next = PromptTemplate(
                    "previous answer: {first_answer}\n"
                    "-----------------------------------\n"
                    "Additional context: {context_str}\n"
                    "-----------------------------------\n"
                    "Query: {query_str}\n"
                    "-----------------------------------\n"
                    "use the previou answer and additional and \n"
                    "Give new answer only if additional context has any new information relavant to query"
                    "It is highly recommended to not use anything but the text you are provided with.\n"
                    "If there is no good new answer, just give back the previous answer as a response.\n"
                    "-----------------------------------"
                )
        qa_prompt = PromptTemplate(
                        "Context information is below.\n"
                        "---------------------\n"
                        "{context_str}\n"
                        "---------------------\n"
                        "Given the context information and not prior knowledge, "
                        "answer the query.\n"
                        "Query: {query_str}\n"
                        "Answer: "
                    )
        if(node_s == 0):
            response = self.llm.complete(
                qa_prompt.format(context_str=context_str, query_str=query_str)
            )
        else:
            response = self.llm.complete(
                next.format(query_str=query_str, first_answer=first_answer, context_str=context_str)
            )

        return str(response)

class Ramayan():
    def __init__(self):
        self.default_nodes = 3
        self.base_retriever = index.as_retriever(similarity_top_k=self.default_nodes)
        self.query_engine = RAGStringQueryEngine(
            retriever=self.base_retriever,
            response_synthesizer=get_response_synthesizer(),
            llm=llmR,
        )
        self.question = ""
        self.curr_response = ""
    
    def reinitialize(self):
        self.default_nodes += 3
        self.base_retriever = index.as_retriever(similarity_top_k=self.default_nodes)
        self.query_engine = RAGStringQueryEngine(
            retriever=self.base_retriever,
            response_synthesizer=get_response_synthesizer(),
            llm=llmR,
        )
    
    def answer(self, query_str):
        with open("log_big.txt", "w") as f:
            f.write("")
        global first_answer
        global node_s
        node_s = 0
        first_answer = ""
        self.question = query_str
        response = self.query_engine.query(query_str)
        self.curr_response = response
        from IPython.display import display, Markdown, Latex
        with open("samples.txt", "a") as f:
            f.write("Query: \n" + query_str + "\n")
            f.write("Answer: \n" + response.response + "\n\n")
        display(Markdown(response.response))

    def get_better(self):
        global first_answer
        global node_s
        node_s += 1
        first_answer = self.curr_response.response
        self.reinitialize()
        response = self.query_engine.query(self.question)
        self.curr_response = response
        from IPython.display import display, Markdown, Latex
        with open("samples.txt", "a") as f:
            f.write("Query: \n" + self.question + "\n")
            f.write("Answer: \n" + response.response + "\n\n")
        display(Markdown(response.response))

agent = Ramayan()
app = FastAPI()

@app.post("/post")
async def ramayan(post: str):
    global agent
    # from IPython.display import display
    response = agent.answer(post)#query_engine.query(post)
    print("Response at api", response)
    from fastapi.responses import JSONResponse
    x = JSONResponse(content={"response": response})
    # display(response)
    print(x)
    return x