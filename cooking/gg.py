from llama_index.core import StorageContext, load_index_from_storage, PromptTemplate
from custom_llm import OurLLM
from gemini import ramayandata
from llama_index.core import ServiceContext, set_global_service_context
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import json
from llama_index.core.indices.knowledge_graph.retrievers import KGTableRetriever
from llama_index.core.llms.mock import MockLLM
    
llmR = OurLLM()
mock_llm = MockLLM(max_tokens=2560)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
set_global_service_context(ServiceContext.from_defaults(llm=llmR, embed_model=embed_model, chunk_size=512, context_window = 12000, num_output=512))

RAG = load_index_from_storage(StorageContext.from_defaults(persist_dir=r"C:\Users\M LAKSHMI NARASIMHA\OneDrive\Desktop\Ramayan\ramayana_512_index"))

qa_prompt = PromptTemplate(
    "Optional context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Question is below.\n"
    "---------------------\n"
    "{query_str}\n"
    "Given the optional context information and the question, please\n"
    "write three other variants of the same question. These questions are used for RAG retrieval.\n"
    "Use context only if it is relavant in some sense, also the new questions should not change the meaning of old question\n"
    "and should be in the same language as the original question.\n"
    "The questions should try to include main important keywords for better retrieval.\n"
    "Try to include different words in new questions that mean same as the orginal question\n"
    "Just give questions in the output, do not add any other text, also let all the questions be in a single line, one after the other, don't number them.\n"
)

with open(r"C:\Users\M LAKSHMI NARASIMHA\OneDrive\Desktop\Ramayan\chunks\chunked_verses.json", "r", encoding="utf-8") as f:
    verses = json.load(f)

# with open("ramayana_log_temp.txt", "r") as f:
#     lines = f.readlines()
#     previous_str = ""
#     for line in lines:
#         if line.strip() == "":
#             continue
#         previous_str += line.strip() + "\n"

# qa_prompt_2 = PromptTemplate(
#     "Optional context information is below.\n"
#     "---------------------\n"
#     "{context_str}\n"
#     "---------------------\n"
#     "previous question and answer is below.\n"
#     "{previous_str}\n"
#     "---------------------\n"
#     "Question is below.\n"
#     "---------------------\n"
#     "{query_str}\n"
#     "Given the optional context information and the question, please\n"
#     "write three other variants of the same question. These questions are used for RAG retrieval.\n"
#     "Use context only if it is relavant in some sense, also the new questions should not change the meaning of old question\n"
#     "and should be in the same language as the original question.\n"
#     "The questions should try to include main important keywords for better retrieval.\n"
#     "Try to include different words in new questions that mean same as the orginal question\n"
#     "Just give questions in the output, do not add any other text, also let all the questions be in a single line, one after the other, don't number them.\n"
#     "Also only use context from previous question and answer if the current question completely depends on previous question, otherwise don't use it at all.\n"
# )

query_engine_rag = RAG.as_query_engine(response_mode="tree_summarize", similarity_top_k=5)
query_engine_rag.update_prompts(
    {"response_synthesizer:summary_template": qa_prompt}
)

balakanda = load_index_from_storage(StorageContext.from_defaults(persist_dir=r"C:\Users\M LAKSHMI NARASIMHA\OneDrive\Desktop\Ramayan\KGs\balakanda"))
query_engine_balakanda = balakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=5,
    verbose=True)
query_engine_balakanda2 = balakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=15,
    verbose=True)

ayodhyakanda = load_index_from_storage(StorageContext.from_defaults(persist_dir=r"C:\Users\M LAKSHMI NARASIMHA\OneDrive\Desktop\Ramayan\KGs\ayodhyakanda"))
query_engine_ayodhyakanda = ayodhyakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=5,
    verbose=True)
query_engine_ayodhyakanda2 = ayodhyakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=15,
    verbose=True)

aranyakanda = load_index_from_storage(StorageContext.from_defaults(persist_dir=r"C:\Users\M LAKSHMI NARASIMHA\OneDrive\Desktop\Ramayan\KGs\aranyakanda"))
query_engine_aranyakanda = aranyakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=5,
    verbose=True)
query_engine_aranyakanda2 = aranyakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=15,
    verbose=True)

kishkindhakanda = load_index_from_storage(StorageContext.from_defaults(persist_dir=r"C:\Users\M LAKSHMI NARASIMHA\OneDrive\Desktop\Ramayan\KGs\kishkindhakanda"))
query_engine_kishkindhakanda = kishkindhakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=5,
    verbose=True)
query_engine_kishkindhakanda2 = kishkindhakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=15,
    verbose=True)

sundarakanda = load_index_from_storage(StorageContext.from_defaults(persist_dir=r"C:\Users\M LAKSHMI NARASIMHA\OneDrive\Desktop\Ramayan\KGs\sundarakanda"))
query_engine_sundarakanda = sundarakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=5,
    verbose=True)
query_engine_sundarakanda2 = sundarakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=15,
    verbose=True)

yuddhakanda = load_index_from_storage(StorageContext.from_defaults(persist_dir=r"C:\Users\M LAKSHMI NARASIMHA\OneDrive\Desktop\Ramayan\KGs\yuddhakanda"))
query_engine_yuddhakanda = yuddhakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=5,
    verbose=True)
query_engine_yuddhakanda2 = yuddhakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=15,
    verbose=True)

uttarakanda = load_index_from_storage(StorageContext.from_defaults(persist_dir=r"C:\Users\M LAKSHMI NARASIMHA\OneDrive\Desktop\Ramayan\KGs\uttarakanda"))
query_engine_uttarakanda = uttarakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=5,
    verbose=True)
query_engine_uttarakanda2 = uttarakanda.as_query_engine(
    include_text=True, 
    response_mode="tree_summarize",
    embedding_mode="hybrid",
    similarity_top_k=15,
    verbose=True)
# query_engine_balakanda.retriever.switch1()

def log_data(data, data_type = 1):
    if data_type == 1:
        with open("chunks_retrieved.txt", "w", encoding="utf-8") as f:
            f.write(data)   
    elif data_type == 2:
        with open("query_variants.txt", "w", encoding="utf-8") as f:
            f.write(data)
    elif data_type == 3:
        with open("log.txt", "w", encoding="utf-8") as f:
            f.write(data)
    elif data_type == 4:
        with open("ramayana_log.txt", "a", encoding="utf-8") as f:
            f.write(data)
    elif data_type == 5:
        with open("ramayana_log_temp.txt", "w", encoding="utf-8") as f:
            f.write(data)
    elif data_type == 6:
        with open("verses_retrieved.txt", "w", encoding="utf-8") as f:
            f.write(data)

    

def question_variants(query):
    response = query_engine_rag.query(query)
    return query + response.response

def post_process(nodes, kg = True, part = 1):
    lol = {}
    data = """"""
    verses_ = """"""

    if kg:
        for node in nodes[:-1]:
            id = node.metadata['r_id'].split("_")[0]
            if id not in lol:
                lol[id] = []
                lol[id].append(node.metadata['canto_summary'])
            lol[id].append(node.text)
            p_r_id = str(part) + "_" + node.metadata['r_id']
            try:
                verses_ += f"{verses[p_r_id]}\n" + "---------------------------\n"
            except:
                print(f"{p_r_id} not found in 12 chunk verses")
        for key, value in lol.items():
            if value[0] != 'No summary available':
                data += f"chapter summary: {value[0]}\n"
            for i in value[1:]:
                data += f"content: {i}\n"
            data += "\n"
            data += "------------------------\n"
        data += "Following are the knowledge graph triplets used to retrieve above context:\n"
        for triplet in nodes[-1].metadata['kg_rel_texts']:
            data += f"{triplet}\n"
        data += "------------------------\n"
    else:
        for node in nodes:
            id = node.metadata['r_id'].split("_")[0]
            if id not in lol:
                lol[id] = []
                lol[id].append(node.metadata['canto_summary'])
            lol[id].append(node.text)
        for key, value in lol.items():
            if value[0] != 'No summary available':
                data += f"chapter summary: {value[0]}\n"
            for i in value[1:]:
                data += f"content: {i}\n"
            data += "\n"
            data += "------------------------\n"

    return data, verses_
        
def ramayana(query_original):
    # query = question_variants(query_original)
    query = query_original
    log_data(query, 2)
    rag_data, rag_verses = post_process(query_engine_rag.retrieve(query), False)
    # query_engine_balakanda.retriever.switch1()
    balakanda_data, balakanda_verses = post_process(query_engine_balakanda.retrieve(query), True, 1)
    # query_engine_balakanda.retriever.switch1()
    # query_engine_ayodhyakanda.retriever.switch2()
    ayodhyakanda_data, ayodhyakanda_verses = post_process(query_engine_ayodhyakanda.retrieve(query), True, 2)
    # query_engine_ayodhyakanda.retriever.switch2()
    # query_engine_aranyakanda.retriever.switch2()
    aranyakanda_data, aranyakanda_verses = post_process(query_engine_aranyakanda.retrieve(query), True, 3)
    # query_engine_aranyakanda.retriever.switch2()
    # query_engine_kishkindhakanda.retriever.switch2()
    kishkindhakanda_data, kishkindhakanda_verses = post_process(query_engine_kishkindhakanda.retrieve(query), True, 4)
    # query_engine_kishkindhakanda.retriever.switch2()
    # query_engine_sundarakanda.retriever.switch2()
    sundarakanda_data, sundarakanda_verses = post_process(query_engine_sundarakanda.retrieve(query), True, 5)
    # query_engine_sundarakanda.retriever.switch2()
    # query_engine_yuddhakanda.retriever.switch2()
    yuddhakanda_data, yuddhakanda_verses = post_process(query_engine_yuddhakanda.retrieve(query), True, 6)
    # query_engine_yuddhakanda.retriever.switch2()
    # query_engine_uttarakanda.retriever.switch2()
    uttarakanda_data, uttarakanda_verses = post_process(query_engine_uttarakanda.retrieve(query), True, 7)
    # query_engine_uttarakanda.retriever.switch2()
    # data = rag_data + balakanda_data + ayodhyakanda_data + aranyakanda_data + kishkindhakanda_data + sundarakanda_data + yuddhakanda_data + uttarakanda_data
    data = rag_data + "------------------------\n" + "Bala Kanda" + balakanda_data + "Ayodhya Kanda" + ayodhyakanda_data + "Aranya Kanda" + aranyakanda_data + "Kishkindha Kanda" + kishkindhakanda_data  + "Sundara Kanda" + sundarakanda_data + "Yuddha Kanda" + yuddhakanda_data + "Uttara Kanda" + uttarakanda_data
    verses_ = rag_verses + "------------------------\n" + "Bala Kanda" + balakanda_verses + "Ayodhya Kanda" + ayodhyakanda_verses + "Aranya Kanda" + aranyakanda_verses + "Kishkindha Kanda" + kishkindhakanda_verses  + "Sundara Kanda" + sundarakanda_verses + "Yuddha Kanda" + yuddhakanda_verses + "Uttara Kanda" + uttarakanda_verses
    log_data(verses_, 6)
    with open("ramayana_log.txt", "w", encoding="utf-8") as f:
        f.write(data)   
    
    prompt = f"""
    You are question answering system for Ramayana.\n
    You are given the context information below. Please answer the question that follows.\n
    ---------------------\n
    {data}\n
    Answer only from the context information provided. If the answer is not present in the context, please say "I don't know".\n
    Use only relavant information from the context to answer the question.\n
    ---------------------\n
    Question: {query_original}\n
    Answer:
    """
    # response = ramayandata(prompt)

    # log_data("Prompt: \n" + prompt + "Answer: \n" + response + "\n", 3)
    # # log_data("question: " + query_original + "\n" + "Answer: " + response + "\n", 4)
    # # log_data("question: " + query_original + "\n" + "Answer: " + response + "\n", 5)
    # with open("ramayana_log_qa.txt", "a", encoding="utf-8") as f:
    #     f.write("question: " + query_original + "\n" + "Answer: " + response + "\n") 


    # return 
    return prompt

