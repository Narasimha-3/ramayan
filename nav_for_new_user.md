# Navigating the whole-POC branch

This branch is the RamayanaGPT research workspace: one snapshot commit ("Add whole POC"), followed by commits that removed hardcoded API keys and added this guide. There is no README, requirements file or launch script, so this file explains what is here and how the pieces connect.

- Project overview and design documents: the `main` branch (`README.md`, `docs/`).
- The finished, runnable system: the `deploy` branch, a Docker-based MCP server built from `cooking/` and the data in this branch.

## Before you open anything

- **Kanda numbers.** `Parts/` folders, chunk IDs and the code use part numbers 1–7: 1 Bala, 2 Ayodhya, 3 Aranya, 4 Kishkindha, 5 Sundara, 6 Yuddha, 7 Uttara. `KGs/` and `chunks/` use kanda names (`balakanda`, …). A sarga is called a canto in the text and a chapter in most of the code.
- **Paths.** `cooking/gg.py` and several notebooks use absolute Windows paths (`C:\Users\…\Ramayan\…`, `D:\Ramayan\…`), and some relative paths use backslashes (`chunks\ramayan.json`). Fix them before running anything on macOS or Linux.
- **Environment.** The notebooks ran Python 3.12.5. The code uses the LlamaIndex 0.10 API (`ServiceContext`, `KnowledgeGraphIndex`); `deploy` pins `llama-index-core==0.10.68.post1`. Every index uses `BAAI/bge-small-en-v1.5` embeddings (384 dimensions).
- **API key.** The Gemini helpers read the key from the `GOOGLE_API_KEY` environment variable. `cooking/gemini.py` creates a client when it is imported, so the app needs the variable set, but any non-empty value will do: the app makes no Gemini call.
- **Big files.** `KGs/` is about 250 MB of JSON, and `ramayan.json` and several index files are 20–60 MB each. Inspect them with a script rather than an editor.

## How the pieces connect

```text
Parts/                     verses: Sanskrit + English, one file per verse or verse range
  │  chunking: full_ramayan_prompt_pipeline.ipynb (kandas 1-4, 6), summarize_verses.ipynb (kanda 5; kanda 7 from an unsaved variant)
  │  rewrite: Gemini 1.5 Pro, narrator's perspective
  ▼
chunks/                    2,244 rewritten chunks, plus chunk ID → original verses
  ├─ triplets_generator.ipynb → *_triplets.json → triplet_parser.ipynb → parsed_*_triplets.json
  │     └─ kg_train.ipynb, updateKG.ipynb → KGs/<kanda>/          the 7 knowledge graphs
  └─ build_main_Rag.ipynb → ramayana_512_index/                   plain RAG index
                                  │
cooking/   app.py + gg.py (FastAPI), gui.py + script.py (Streamlit): loads KGs/, ramayana_512_index/, chunks/chunked_verses.json
                                  │
deploy branch   ramayana_engine.py + ramayana_mcp.py: the same data served over MCP
```

### Chunk IDs

The chunk files, the KG and RAG nodes and the verse map share a chunk ID `<part>_<chapter>_<n>`, for example `2_12_3` = Ayodhya, canto 12, chunk 3. The KG build itself pairs triplets with chunks by list position, not by this ID.

- Kandas 1–4 and 6: `n` starts at 1, and each window of about 15 verses overlaps the previous one by about 4.
- Kandas 5 and 7: `n` starts at 0, groups don't overlap, and chapters are stored in string order (`1`, `10`, `100`, …). Sundara groups hold up to 12 verses. Uttara groups hold 12 verse files whatever their length, so about half span more than 12 verses (`7_1_0` covers verses 1–24).
- KG nodes store `r_id = <chapter>_<n>` without the part; the code adds it (`f"{part}_{r_id}"`). The RAG index stores the full ID as its `r_id`.
- `chunks/chunked_verses.json` maps each ID to the original verses. It lacks 12 Bala IDs (`1_1_0`, `1_1_10` … `1_1_20`) that `KGs/balakanda` uses; deploy's `chunks/chunked_verses_may26.json` adds them. IDs `1_1_1` … `1_1_9` each belong to two Bala nodes (two chunkings of canto 1), and both verse maps return only the older, wider window's verses for them.

## Directories

| Directory | What it is |
| --- | --- |
| `Parts/` | Source text: 20,019 files in `Parts/<part>/<sarga>/`, 645 sargas. Each sarga has `text.txt` (the whole canto), usually `summary.txt` (heading and summary), and one file per verse or verse range named after its marker: `12.txt`, `3-4.txt`, `19—22.txt` (em dash). Devanagari Sanskrit plus English prose, OCR'd, with noise. Nothing in this branch writes it, and its source isn't recorded. |
| `chunks/` | The final rewritten chunks. `<kanda>.json` holds records `{part, chapter, prompt_number, summary, content}`, 2,244 in all (233, 423, 248, 240, 274, 553, 273). `ramayan.json` is all seven concatenated in alphabetical file order (Aranya first), the input of the RAG index. `chunked_verses.json` maps chunk ID → original verses. Same content as `deploy`'s copies; only line endings differ. |
| `KGs/` | The seven knowledge graphs, one LlamaIndex `KnowledgeGraphIndex` per kanda, byte-identical to `deploy`'s. See [Inside a knowledge graph](#inside-a-knowledge-graph). |
| `ramayana_512_index/` | Plain vector RAG index of `chunks/ramayan.json`: 2,261 nodes, chunk size 512, metadata `canto_summary` and `r_id`. Built by `build_main_Rag.ipynb`; byte-identical to `deploy`'s. |
| `cooking/` | The query app (FastAPI backend and Streamlit chat) and its logs. See [The query app](#the-query-app-cooking). |
| `balakanda_chapter1_update/` | Output of `updateKG.ipynb`; the same data as `KGs/balakanda/`. |
| `balakanda_old/` | The older Bala KG that the canto-1 update was applied to: 217 nodes, triplet embeddings, no `graph_store.json`. |
| `mln_test/` | Toy KG built from `abc.json` by `kg_train copy.ipynb` to test retrieval. Not Ramayana data. |
| `__pycache__/` | Compiled Python 3.12 files from the authors' machine. `gg.cpython-312.pyc` is all that is left of an early root `gg.py` that queried the Yuddha KG. |

## Root files, by stage

### Text preparation

| File | What it is |
| --- | --- |
| `summarize_verses.ipynb` | Cell 0 (commented out) dumps `Parts/` into `ramayan.json`. Cell 1, `get_chunked_chapter_data`, cuts one kanda into non-overlapping verse groups. Cell 6 builds the rewrite prompt; its Gemini call is commented out, so the saved run wrote only test files. |
| `full_ramayan_prompt_pipeline.ipynb` | Reads `Parts/` directly, cuts each canto into overlapping windows and appends them to `chunked_verses.json`. It holds the same rewrite prompt and a Gemini helper, but the saved loop doesn't call them. The saved run covered kanda 6 only. |
| `ramayan.json` | `Parts/` as one file: `{part: {sarga: {summary, content, verses}}}`. Not the same file as `chunks/ramayan.json`. |
| `ramayan_chunked_test.json` | Uttara (kanda 7, despite the name) in groups of 12 verse files: the grouping behind the final Uttara chunks. |
| `ramayan_chunked_test_5.json` | Sundara (kanda 5) in groups of up to 12 verses: the grouping behind the final Sundara chunks. The 5 is the kanda number. |
| `chunked_balakanda_5_size.json` | Bala in groups of up to 5 verses. Only canto 1 was taken further, into `balakanda_chapter1.json`. |
| `balakanda_chapter1.json` | 21 rewritten chunks of Bala canto 1 with their source verses, from the groups of up to 5 verses in `chunked_balakanda_5_size.json`. Range files aren't split, so a chunk holds 1–9 verses. |
| `sundarakanda.json`, `uttarakanda.json` | Rewritten Sundara and Uttara chunks with their source verses (274 and 273 records). `chunks/` has the same records without `verses`. |
| `uttarakanda1.json`, `uttarakanda11.json` | Uttara in groups of up to 16 verses (`summarize_verses.ipynb` cells 2–3), which the final chunks don't use, and a dry run of the rewrite loop over it: one record per canto (its last chunk only) with placeholder content. |
| `gemini.py` | `google.generativeai` wrapper for `gemini-1.5-pro`: `ramayandata(prompt)` returns the reply text. |
| `custom_llm.py` | LlamaIndex `CustomLLM` (`OurLLM`) that sends every prompt to `gemini.ramayandata` and overwrites `prompt.txt` with it. |
| `prompt.txt` | The last prompt `OurLLM` sent: a knowledge-graph question-answering prompt for "Name rama's bow that belonged to indra?". |

### Triplets

| File | What it is |
| --- | --- |
| `triplets_generator.ipynb` | Fills the triplet prompt for each chunk (three triplet patterns, a list of kinship relations, snake_case, up to 20 triplets plus 10 "is in canto" ones) and sends it to Gemini. Each raw reply is appended to `<kanda>_triplets.json`. As saved it targets `balakanda_chapter1.json`. |
| `triplet_parser.ipynb` | `trippie()` (cell 1) turns one raw reply into `[head, relation, tail]` lists; cell 2 applies it to every entry and cell 4 writes `parsed_<kanda>_triplets.json`. Cells 6–12 are an unexecuted KG test. |
| `balakanda_chapter_1_triplets.json`, `ayodhyakanda_triplets.json`, `sundarakanda_triplets.json`, `uttarakanda_triplets.json` | Raw Gemini replies: a JSON list with one `{r_id: text}` object per chunk (21, 423, 274 and 273). |
| `parsed_*_triplets.json` | Parsed triplets for the same four: 345, 7,438, 4,133 and 4,839. The Ayodhya, Sundara and Uttara files equal the triplets in their KGs. |
| `ayodhyakanda.txt`, `sundarakanda.txt`, `uttarakanda.txt` | Logs of the raw Gemini replies between `jai_balayya_ew` lines, written by logging code that is now commented out in `gemini.py`. The Ayodhya and Uttara logs end with some replies from later queries. |

The triplet files for Aranya, Kishkindha and Yuddha are not in the branch; those triplets exist only inside `KGs/`.

### Knowledge graphs

| File | What it is |
| --- | --- |
| `kg_train.ipynb` | Builds one kanda's KG from a parsed triplet file and its chunk file. File names were edited for each run: as saved, it mixes Sundara inputs with a Yuddha output name and reads `5_gpt_out.json`, which isn't in the branch. Later cells drop `verses` from a chunk file and count chunk tokens. |
| `kg_train copy.ipynb` | Not a plain copy: the same build code run on the toy `abc.json`, saved to `mln_test/`, plus retriever experiments. |
| `updateKG.ipynb` | Adds Bala canto 1 (21 chunks, 345 triplets) to the existing Bala KG and saves `balakanda_chapter1_update/`. |
| `updateKG copy.ipynb` | Byte-identical copy of `updateKG.ipynb`. |
| `testKG.ipynb` | Asks the updated Bala KG one question through Gemini. Later cells, never run, build a 3-chunk Sundara test KG. |

### RAG

| File | What it is |
| --- | --- |
| `build_main_Rag.ipynb` | Builds `ramayana_512_index/` from `chunks/ramayan.json`. |
| `test_rag.ipynb` | Reloads the index, tries a prompt that rewrites the question into three search variants, and inspects a top-5 retrieval. |

### Other

| File | What it is |
| --- | --- |
| `test_app.py` | FastAPI stub: `POST /kg` returns `cooking/log.txt` as a JSON string (with its line breaks doubled), for testing the chat UI without loading the graphs. Start it from the branch root. |
| `abc.json` | Synthetic test data about a fictional city, used for `mln_test/`. |
| `tt.json`, `ttt.json` | Empty files. |
| `RAMAYAN POSTER.png`, `INITIAL ARCHITECTURE RAMAYAN.png` | One image under two names: the initial poster (MiniRAG → MainRAG → knowledge graph), the same design as `docs/ramayan_initial_draft_poster.pdf` on `main`. |

## Inside a knowledge graph

Each `KGs/<kanda>/` folder is a saved LlamaIndex `KnowledgeGraphIndex` on a `SimpleGraphStore`, which is plain JSON (no Neo4j).

| File | Contents |
| --- | --- |
| `docstore.json` | One node per chunk that went into the build (chunks are never split), with metadata such as `canto_summary` and `r_id`. A few chunks have no node; see Known gaps. |
| `graph_store.json` | `subject → [[relation, object], …]`, duplicates kept. |
| `index_store.json` | A keyword table (entity → node IDs) and `embedding_dict`, a 384-dimension embedding for every triplet string. The triplet embeddings live here. |
| `default__vector_store.json`, `image__vector_store.json` | Empty. |

How a graph was built (`kg_train.ipynb`): one LlamaIndex `Document` per chunk, `Settings.llm = None` so no LLM runs during the build, then `upsert_triplet_and_node(triplet, node, include_embeddings=True)` for every pre-generated triplet. Triplets and chunk nodes are paired by list position, so the triplet file and the chunk file must be in the same order. The 217 Bala nodes inherited from `balakanda_old` were built by a variant that wasn't saved (other text templates, no `canto` key).

| Kanda | Nodes | Triplet entries (unique) |
| --- | --- | --- |
| Bala | 238 | 345 (286) in the graph, 3,934 embedded |
| Ayodhya | 423 | 7,438 (4,898) |
| Aranya | 240 | 3,883 (2,791) |
| Kishkindha | 240 | 4,347 (3,090) |
| Sundara | 274 | 4,133 (2,902) |
| Yuddha | 552 | 9,721 (6,994) |
| Uttara | 273 | 4,839 (4,137) |

`KGs/balakanda` is the odd one. It is the canto-1 update applied to `balakanda_old`, which had no `graph_store.json`, so its graph holds only the canto-1 triplets. The other 3,648 Bala triplets exist only in `embedding_dict`, so they surface only through the similarity search, not graph traversal. The keyword table still holds the old entities, so question keywords still reach the old Bala chunks; only their triplets are missing from the graph. Its `r_id`s `1_1` … `1_9` also appear twice, once from each chunking of canto 1.

Querying, as in `cooking/gg.py` and `deploy`: `as_query_engine(include_text=True, embedding_mode="hybrid", …)`. Keywords taken from the question select graph entries, the triplet embeddings are searched by similarity, and the linked chunk nodes come back, with the triplets in `nodes[-1].metadata["kg_rel_texts"]`. In `testKG.ipynb` the root `OurLLM` sends the keyword prompt to Gemini. The build notebooks set `Settings.llm = None`, so their query cells fall back to LlamaIndex's MockLLM. In `cooking/` and `deploy` the keywords are the question's own words.

## The query app (`cooking/`)

| File | Role |
| --- | --- |
| `app.py` | FastAPI backend. `POST /kg?item=<question>` returns `gg.ramayana(item)`. `POST /kg_mini` takes `"<kanda>: <question>"` and queries that kanda's graph alone. |
| `gg.py` | When imported, loads `ramayana_512_index`, `chunks/chunked_verses.json` and the seven KGs from absolute Windows paths (lines 15, 34, 71, 85, 99, 113, 127, 141, 155). `ramayana(q)` takes 5 RAG chunks plus hybrid retrieval from each kanda graph (10 chunks and up to 30 triplets per kanda in the saved log). It builds a context of chapter summaries, chunk text and triplets, writes the original verses of the graph chunks to `verses_retrieved.txt` (they are not put in the prompt), and returns the assembled question-answering prompt. |
| `custom_llm.py`, `gemini.py` | `OurLLM` calls `ramayandata`, which here returns the part of its prompt between the first two dashed lines instead of calling Gemini (the model call is commented out). For the keyword step that part is the question, so the keywords are the question's words. |
| `gui.py`, `script.py` | Streamlit chat with pages QA, Chunks, Query Variants and Verses. Posts to `http://127.0.0.1:8000/kg`, or to `/kg_mini` for `kanda: question` input. |
| `hanuman.ipynb` | Retrieval probe on the Bala KG. |
| `debug.ipynb` | Scratch cells, never run: calls to `ramayana()`, to the API and to Gemini. |
| `query_variants.txt`, `verses_retrieved.txt`, `ramayana_log.txt` | Overwritten by every `ramayana()` call: the query, the original verses of the chunks retrieved from the graphs, and the assembled context. |
| `log.txt` | One full assembled prompt from an older run. Shown on the Chunks page and served by `test_app.py`. |
| `ramayana_log_qa.txt` | 210 question and answer pairs from an earlier setup in which the model was still called. |
| `prompt.txt`, `keywords.txt` | The last keyword-extraction prompt and one list of extracted keywords. |
| `__pycache__/` | Compiled Python 3.12 files. |

What it does today: for a plain question the QA page shows the assembled prompt (about 97 KB for "Who is father of dasaratha ?"), and for `kanda: question` it shows that kanda's retrieved context. It never shows a model answer: the final `ramayandata(prompt)` call in `gg.py` is commented out, and `ramayandata` in `cooking/gemini.py` no longer calls Gemini either. The context puts the RAG block first, then the seven kanda blocks.

Running it. No launch command is recorded; these follow from the code:

```bash
cd cooking
# first point the paths in gg.py at ../ramayana_512_index, ../chunks/chunked_verses.json and ../KGs/<kanda>
export GOOGLE_API_KEY=placeholder   # any non-empty value, see "API key" above
uvicorn app:app --host 127.0.0.1 --port 8000
streamlit run gui.py                 # in a second shell, also from cooking/
```

The imports need fastapi, streamlit, streamlit-navigation-bar, requests, llama-index-core 0.10, llama-index-embeddings-huggingface and google-genai; the launch command also needs uvicorn. To run the finished system instead, use the `deploy` branch (`docker compose up -d --build`; see its README).

## From cooking/ to deploy

`ramayana_engine.py` on `deploy` keeps the core of `gg.py`: the same embeddings, KGs and RAG index, hybrid KG engines and a reworked `post_process`. What changed:

- Paths come from `RAMAYAN_DATA_DIR` instead of Windows paths.
- `OurLLM` became a stop-word keyword extractor: no Gemini, no keys.
- Retrieval is wider: 10 RAG chunks instead of 5, KG `similarity_top_k` 10 instead of 5, and up to 100 triplets per kanda (cooking used LlamaIndex's default of 30), reranked by similarity to the question down to 10. The sizes are tool arguments with a minimum of 10.
- Every chunk is labelled with its ID, and the original verses are fetched on request (`get_original_verses`) from `chunks/chunked_verses_may26.json`.
- The KG sections come first and the RAG results follow as additional information.
- FastAPI and Streamlit are replaced by an MCP server with three tools.

## Where the code differs from the project documents

| The documents say | The code and data |
| --- | --- |
| Neo4j graph database | LlamaIndex `SimpleGraphStore` JSON; Neo4j appears only as an unused import in `triplet_parser.ipynb` |
| 1-hop traversal | No depth is set; saved query outputs show depth 2 |
| 20–30 triplets per chunk | The prompt asks for at most 30; the files average 15–18, and a few chunks go over (up to 44) |
| 1024-token chunks | 1024 is the rewrite cap; chunks average about 200 tokens (max 712) |
| Triplet embeddings in a vector database, with the chunk in metadata | Embeddings are in `index_store.json` (`embedding_dict`); the link to the chunk is the keyword table plus the node's `r_id` |
| KG first, RAG second | `cooking/gg.py` puts the RAG block first; `deploy` puts the KG first |

## Known gaps

- Referenced but missing: `5_gpt_out.json` and `chunks/sundarakanda1.json` (`kg_train.ipynb`), a root `ayodhyakanda.json` (`triplet_parser.ipynb`), and the root `gg.py` that `testKG.ipynb` imports (only its `.pyc` is left). Also missing, though nothing names them: the triplet files behind the Aranya, Kishkindha, Yuddha and original Bala graphs.
- Not saved: the code that wrote the rewritten `content` for kandas 1–4 and 6, merged the appended JSON fragments into `chunks/chunked_verses.json`, and built `chunks/ramayan.json`.
- `Parts/` has splitting errors: misread range names where the start isn't below the end (for example `830—32.txt` and `8—5.txt`); garbled markers such as `(36--38)` that never became files, so 286 verse numbers have no file of their own; and 7 sargas where a repeated marker overwrote a verse file (an OCR misread, an interpolated canto numbered from 1, or an in-text list read as verse numbers). `text.txt` still holds each full canto.
- Some chunk IDs in `chunks/` have no node in their KG: Bala `48_1` and `73_2`–`77_3`, Aranya `73_3`–`75_3`, Yuddha `119_4`.
- Notebook outputs show prints from a locally modified LlamaIndex that isn't included, so retrieval with stock LlamaIndex may differ.
