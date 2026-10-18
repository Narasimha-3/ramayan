# RamayanaGPT

RamayanaGPT answers questions about Valmiki's Ramayana using only the original text. The verses are rewritten as short plain-English passages and turned into seven knowledge graphs, one per kanda. Each answer is built from graph triplets plus the passages they came from, so it can be checked against the source verses.

General LLMs and QA systems give imprecise, unverifiable answers on this text: they learn from paraphrased or modernised retellings (for example biased blogs), they lose context between passages that are far apart, and they don't keep relationships and events intact.

## Branches

The three branches have no shared history. `main` keeps the 2024 prototype's commits; `whole-POC` and `deploy` each start from a single snapshot commit.

| Branch | What is in it | Start here |
| --- | --- | --- |
| `main` | This overview, the project documents in [`docs/`](docs/), and the first prototype from August 2024 (the files at the root). | this file |
| [`whole-POC`](https://github.com/Narasimha-3/ramayan/tree/whole-POC) | The full research workspace: the verse corpus, the text-preparation and triplet notebooks, the seven kanda knowledge graphs, the RAG index, a FastAPI + Streamlit query app, and experiments. About 20,000 files. | [`nav_for_new_user.md`](https://github.com/Narasimha-3/ramayan/blob/whole-POC/nav_for_new_user.md) |
| [`deploy`](https://github.com/Narasimha-3/ramayan/tree/deploy) | The final retrieval engine packaged as a Docker-based MCP server, so Claude Desktop or another MCP client can query the Ramayana. The same files are published as [Narasimha-3/Ramayanam](https://github.com/Narasimha-3/Ramayanam). | [`README.md`](https://github.com/Narasimha-3/ramayan/blob/deploy/README.md) |

To fetch only one branch:

```bash
git clone --branch deploy --single-branch https://github.com/Narasimha-3/ramayan.git
```

`whole-POC` checks out to about 430 MB and `deploy` to about 320 MB, mostly knowledge-graph and index files.

## How it works

This follows the project documents in [`docs/`](docs/). Where the code turned out different, the figures below come from the data on `whole-POC`, and its `nav_for_new_user.md` has the details.

### 1. Preparing the text

- Input: the Valmiki Ramayana as Sanskrit verses with an English translation.
- Each canto is cut into windows of about 12–16 verses. Gemini 1.5 Pro rewrites each window as a shorter summary in formal English, from a narrator's perspective, removing toxicity and perspective anomalies so that LLMs read it more reliably.
- The result is called the modified Ramayan: 2,244 chunks, each capped at 1024 tokens and about 200 tokens on average.

### 2. Building the knowledge graphs

- The extraction prompt allows three kinds of triplet (character–character, character–event, character–canto) and lists the kinship relations to use, for example `('rama', 'is_son_of', 'dasaratha')`.
- The prompt asks Gemini 1.5 Pro for at most 30 `(node, edge, node)` triplets per chunk; the saved replies average 15–18, and a few go over.
- The triplets go into one LlamaIndex `KnowledgeGraphIndex` per kanda, seven in all, saved as JSON under `KGs/<kanda>/`. The pipeline diagram names Neo4j as the graph database; the saved graphs don't use it.
- The index links each triplet's subject and object, as keywords, to the chunk the triplet came from. Each triplet is also embedded with BAAI/bge-small-en-v1.5, so retrieval can match triplets by similarity as well as by keyword.
- The documents give one graph per kanda as the way to avoid memory overload and duplication. The saved graphs still repeat many triplets, and both query apps load all seven at once.

### 3. Answering a question

```text
query → optional RAG refinement → knowledge graph traversal → triplets + linked chunks → LLM → answer
```

- The kanda graphs do the main retrieval: triplets around the entities or relations in the query. The documents describe 1-hop traversal; no code sets the depth, and the saved query outputs show depth 2.
- Plain RAG over the rewritten text (`ramayana_512_index/`) adds extra context.
- Chunk IDs lead back to the original verses, so an answer can cite both the passage and the verses. A few Bala IDs are exceptions; `nav_for_new_user.md` lists them.

The `deploy` branch stops before the LLM step. A stop-word keyword extractor stands in for the LLM in the graph lookup, and the MCP server returns the triplets, chapter summaries and passages, each passage tagged with a chunk ID such as `2_12_3` (Ayodhya Kanda, chapter 12, chunk 3). The MCP client's own model writes the answer.

## What was tried

The first design chained a MiniRAG (rough chunks), a MainRAG (chunks refined using the query and context) and the knowledge graph (used only for entity resolution and relations between characters), then sent everything to the LLM. It behaved like a search engine returning similar paragraphs, could not connect events spread across the epic (for example Rama in Ayodhya Kanda and in Yuddha Kanda), and used little of the graph. The final design puts the graph first.

The overview document's own assessment:

| Idea | What worked | What didn't |
| --- | --- | --- |
| Story as a knowledge graph | Tracks relationships, traits and resolutions | Graphs are large and not memory-efficient unless split |
| MiniRAG + MainRAG | Layered chunking looked promising | Could not connect logic or events across paragraphs |
| Triplet metadata | Maps each triplet back to its source | The same triplet in several chunks causes collisions |
| Final graph-first pipeline | Clean 1-hop traversal with optional context | The RAG step adds complexity, sometimes for minor gains |
| Multi-hop traversal | | Added noise; 1-hop already finds most of what is needed |
| Extra context from MainRAG | | Often redundant when the triplets are clean |
| Full text in graph metadata | | High memory use and collisions from duplicate chunks |

## Example answers

Compared with Perplexity.ai in March 2025, from [`docs/ramayan_problem_overview.pdf`](docs/ramayan_problem_overview.pdf):

| Question | Perplexity.ai | RamayanaGPT |
| --- | --- | --- |
| Why did Rama kill Vali secretly? | Some sources show bias | `(Rama, explains_to, Vali)` and `(Vali, accepts, explanation)`, with the supporting chunk from Kishkindha Kanda |
| Why did Dasaratha send Rama to the jungle willingly? | False positives; tried to fit an answer | `(Kikeyi, aided, dasratha)`, `(Kikeyi, received, two wishes)` and `(dasaratha, crumbled on, Rama's exile)` |
| Who cursed Ravana and why? | Mentions a curse but not its origin | Traces it to the Vedavati incident: `(Ravana, misbehaved_with, Vedavati)` and `(Vedavati, cursed, Ravana)` |
| Was Hanuman aware of his powers? | Vague or mixed | `(Hanuman, forgets_powers, due_to_curse)` and `(Jambavan, reminds, Hanuman)`, with chunk evidence |

## Open problems

From the overview document:

- **Memory:** the graphs repeat many triplets, which makes them hard to keep in memory for fast traversal.
- **Triplet-to-chunk collisions:** the same triplet appears in several paragraphs, so it is hard to pick the most relevant chunk.
- **Context switching:** questions that span several characters across kandas lose the core narrative.
- **Hallucination:** above about 10k prompt tokens the LLM sometimes ignores "strictly answer from provided context".

Not yet built: chunk relevance scoring with a cross-attention model; a small model that weights retrieval across the seven graphs, since sometimes the whole answer sits in one or two kandas; retrieval confidence scores to abstain or fall back; a graph view of the reasoning path.

## Documents

| File | Contents |
| --- | --- |
| [`ramayan_problem_overview.pdf`](docs/ramayan_problem_overview.pdf) | Five-page write-up: problem, both approaches, what worked and what didn't, sample answers, open problems |
| [`ramayan_pipeline.pdf`](docs/ramayan_pipeline.pdf) | Stage 1 diagram: raw text → chunks → triplets |
| [`Knowledge_graph_ramayan_pipeline.pdf`](docs/Knowledge_graph_ramayan_pipeline.pdf) | Stage 1 and Stage 2 diagram, with the tool used at each step |
| [`ramayan_initial_draft_poster.pdf`](docs/ramayan_initial_draft_poster.pdf) | First poster: the MiniRAG + MainRAG + knowledge graph ("Enhanced RAG") design |
| [`ramayan_final_draft_poster.pdf`](docs/ramayan_final_draft_poster.pdf) | Final poster: the knowledge-graph RAG architecture and retrieval flow |

## The 2024 prototype (files at the root of `main`)

The first version, as committed in August 2024. The only later change: `gemini.py` reads the Gemini key from `GOOGLE_API_KEY` instead of a hardcoded key (October 2026). It is plain RAG over an English translation, with no knowledge graph yet, and a Streamlit chat UI that also accepts questions in other languages.

| File | Role |
| --- | --- |
| `story.txt` | OCR text of the English translation by Hari Prasad Shastri (Shanti Sadan, London), all three volumes. This prototype indexes it. |
| `poetic.pdf` | An English verse translation of the Ramayana; its title page reads "The Rámáyan of Válmíki, translated into English verse by Ralph T. H. Griffith" (Project Gutenberg eBook #24869). No code reads it. |
| `test.ipynb` | Builds the vector index from `story.txt` (hardcoded as `D:\Ramayanam\story.txt`) into `store_embd/`, then tries queries, the API and translation. Cell 0 sets no embedding model; the saved index uses BAAI/bge-small-en-v1.5, which cell 2 sets, so apply cell 2's settings before rebuilding. |
| `store_embd/` | The saved LlamaIndex vector index of `story.txt` (4,737 chunks). |
| `ramayan_api.py` | FastAPI app. `POST /post?post=<question>` answers from `store_embd/` using BAAI/bge-small-en-v1.5 embeddings. |
| `custom_llm.py`, `gemini.py` | A LlamaIndex `CustomLLM` that sends prompts to Gemini 1.5 Pro. The API key is read from `GOOGLE_API_KEY`. |
| `utils.py` | Calls the API at `127.0.0.1:8000`. Detects the question's language (langid), translates it to English and translates the answer back (deep-translator). |
| `gui.py`, `frontend.py` | Streamlit chat UI with a navigation bar. Each question goes to the API twice, as typed and translated to English. The answer shown comes from the translated call; the "Nodes" page shows the source chunks of the as-typed call. |
| `translator.py` | Unfinished translation test (its imports are missing). |
| `pyproject.toml`, `poetry.lock` | Poetry environment: Python 3.12, llama-index 0.10.65. `requirements.txt` is an older, partial list. |
| `__pycache__/` | Compiled Python files. |

To run it the way the code expects (not re-tested since 2024), install once and then start the API and the UI in two terminals, both from the repository root:

```bash
poetry install --no-root

# terminal 1
export GOOGLE_API_KEY=<your key>
poetry run uvicorn ramayan_api:app --port 8000   # utils.py calls this address

# terminal 2
poetry run streamlit run gui.py
```

## Tools

Used in the code: LlamaIndex 0.10 (RAG and knowledge-graph indexes), Gemini 1.5 Pro (rewriting and triplet extraction), BAAI/bge-small-en-v1.5 embeddings, FastAPI and Streamlit, langid and deep-translator (2024 prototype), and FastMCP with Docker (`deploy`). The posters also list OCR tools and Neo4j.

## People

Malisetty Lakshmi Narasimha, Jupalli Sriram (final poster), Bhogalapalli Sahishnu (initial poster). Professors: Saketha Nath Jagarlapudi, Ramakrishna Upadrasta.
