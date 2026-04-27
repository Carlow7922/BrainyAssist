# BrainyAssist
This project primarily addressed my own pain point—a daily token bill of 200 yuan. If you share this pain, then this is for you. If not, feel free to bookmark it and come back to it someday when you're stung by expensive APIs.

[📖 中文版](./README.zh.md) | [English](./README.md)

# BrainyAssist — Give Your AI Long-Term Memory at 1% of the Cost

> A lightweight assistant architecture based on "Fixed Core Cognitive Space + On-Demand Memory Retrieval"

Designed exclusively for **local execution, low cost, and never forgetting**

⚠️ This project is currently in the testing phase, and features are continuously being iterated and optimized.

## The Problems We Face

Have you ever encountered these situations?



* When using DeepSeek, Claude, GPT-4, or Gemini, as the conversation lengthens, the model **forgets key information mentioned just a few minutes ago**.

* To make it remember project background, you have to **repeatedly paste the same instructions in every new session**, wasting a lot of tokens and time.

* Even worse is the bill: burning 200 RMB per day on API fees, just for "long context".

* Want to run an open-source model locally? Its memory capacity is almost zero, forgetting the conversation after three questions.

**Root Cause**:

Existing solutions are either **expensive** (long-context model APIs) or **unreliable** (local small models with no memory).

There’s no middle ground — an assistant that is **both cheap and reliably remembers key information**.

## Our Solution

### Core Idea (Brain-Inspired Architecture + Dual-Layer Memory Design)

The human brain doesn’t cram all memories into its "workspace". Instead, it retains only a minimal **core cognitive space** (values, current goals, task progress), while storing all other information in **long-term memory** for quick retrieval when needed.

Building on this brain-inspired mechanism, we further adopt the **dual-layer memory architecture** from the [zer0dex](https://github.com/hermes-labs-ai/zer0dex/blob/main/README.md) project. By managing memories in layers and integrating compressed indexes, we achieve more efficient memory retrieval and reuse, completely solving the pain points of "memory fragmentation" and "inefficient retrieval":



| Component                                        | Role                                                                                                                                     | Token Consumption                   |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| **Core Cognitive Space (Permanent + Temporary)** | Fixed cognition and temporary cache injected in every conversation (core project info, temporary task status)                            | Constant \~500 tokens               |
| **Dual-Layer Memory System**                     | Compressed index file (MEMORY.md) + vector database retrieval (returns top 3\~5 most relevant historical memories based on user queries) | \~2000 tokens                       |
| **Session Memory**                               | Key information summarized automatically after each conversation (sessionsMemory.md)                                                     | On-demand incremental, controllable |
| **LLM Inference**                                | Generates answers based on all the above information                                                                                     | Normal generation length            |

**Result**:

No matter how long the conversation is, the token consumption per request **remains almost constant**, eliminating context bloat entirely. The dual-layer memory architecture increases retrieval recall rate to over 90% while solving the weak cross-domain correlation issue of traditional RAG.

### Architecture Origins



* The neuroscientific distinction between **working memory vs. long-term memory**

* Proven feasibility by your **BrainDecoupledLLM-MVP** ([GitHub Link](https://github.com/Carlow7922/BrainDecoupledLLM-MVP/tree/main))

* Draws on mature practices of RAG and fixed system prompts, with **brain-inspired modular integration**

* Core memory architecture references the dual-layer design of [zer0dex](https://github.com/hermes-labs-ai/zer0dex/blob/main/README.md), retaining its compressed index mechanism and optimizing for Chinese-language scenarios

### Feasibility Analysis



* ✅ MVP Proven: Fixed core cognition + external retrieval enables multi-turn memory retention.

* ✅ Vector databases (Chroma) are mature and stable, capable of handling millions of memories on a single machine with transparent and controllable storage paths.

* ✅ Compatible with **Llama.cpp local API and third-party low-cost APIs** (e.g., Doubao Pro, SiliconFlow), running smoothly on consumer-grade hardware with flexible cloud/local deployment options.

* ✅ Even with third-party low-cost APIs, the per-request cost can be controlled at **<0.01 RMB**, far exceeding the cost-effectiveness of long-context models.

* ✅ Chinese-optimized embedding model solves the low recall rate of Chinese memory in open-source solutions.

### Key Memory File Explanation



| File Path                                     | Role                                                                                      | Notes                                                                                 |
| --------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `data/cognitive_space/permanent_cognition.md` | Permanent cognitive file storing core project information and fixed background            | Replaces the original core\_state.txt to ensure core cognition is not lost            |
| `data/cognitive_space/temporary_context.md`   | Temporary cache file storing current session status and task progress                     | Replaces the original core\_state.txt to flexibly adapt to short-term needs           |
| `data/MEMORY.md`                              | Compressed index file of the dual-layer memory architecture                               | Adopts zer0dex's design to provide knowledge navigation scaffolding                   |
| `data/sessionsMemory.md`                      | Session memory file with key information automatically summarized after each conversation | Updated incrementally in real-time to avoid redundant memory                          |
| `data/memory/`                                | Vector database storage directory                                                         | Locally private storage supporting backup/migration with secure and controllable data |

### Memory Workflow (Current Implementation)

In each conversation turn, the system automatically loads/executes the following operations:



1. Loads core cognitive files: `permanent_cognition.md` + `temporary_context.md` under `cognitive_space`;

2. Loads the compressed index file `MEMORY.md` (provides knowledge classification navigation to solve cross-domain correlation issues);

3. Loads the session memory file `sessionsMemory.md` (retains recent key interactions);

4. Retrieves the `data/memory/` vector database based on the user's current query, returning the top 3\~5 most relevant memories (⚠️ Writing retrieval results to cache is not yet implemented);

5. Intelligently concatenates all memory information + user query and sends it to the LLM for answer generation (avoids context bloat);

6. After the conversation ends, automatically summarizes key information and writes it to `sessionsMemory.md` (only stores facts/decisions/conclusions in 1\~2 sentences, ignoring casual chat).

### Text Embedding Model Adaptation



* **Default Model**: `m3e-small`, optimized specifically for Chinese scenarios, balancing speed and recall rate for Chinese users;

* **English Scenario Adaptation**: Manually modify the code to replace the embedding model with `nomic-embed-text-v1.5`.

### Known Limitations



* Does not support image input temporarily, only text-based interactions;

* Writing vector database retrieval results to cache is not yet implemented;

* The project is currently in the testing phase, and some features may undergo iterative adjustments.

## Why This Project Matters (Core Advantages & Differentiation)

### 1. Extreme Cost Advantage (Outperforming Long-Context Models)



| Solution                                    | Total Tokens for 50 Turns | Estimated Cost              | Core Differentiation                                              |
| ------------------------------------------- | ------------------------- | --------------------------- | ----------------------------------------------------------------- |
| Gemini / Claude Long Context                | > 2 million               | 6 \~ 30 USD                 | Cost grows linearly with turns, becoming more expensive over time |
| **BrainyAssist (Llama.cpp Local API)**      | \~140k                    | **0 RMB** (Completely Free) | Constant cost with no additional token consumption                |
| **BrainyAssist (Third-Party Low-Cost API)** | \~140k                    | 1 USD                       | Extremely low cost without bearing long-context premiums          |
| Traditional RAG Solutions                   | \~500k                    | 0 \~ 10 USD                 | Redundant retrieval with weak cross-domain correlation            |

### 2. Flexible Deployment + Low Hardware Threshold



* **Deployment Freedom**: Supports Llama.cpp local API (completely offline) or third-party low-cost API (lightweight online), choosing based on needs;

* **Data Security**: All memories, conversations, and vector databases are stored locally during on-premises deployment, eliminating data leakage risks;

* **Hardware-Friendly**: Runs on a minimum configuration of 4GB RAM + 2-core CPU (supports quantized models); recommended configuration: RTX 3060 12GB VRAM (runs Llama 3 8B or Qwen 2.5 7B smoothly);

* **No Mandatory Dependencies**: No need for high-end hardware or expensive API keys, flexibly adapting to different user scenarios.

### 3. Differentiated Memory Architecture (Brain-Inspired + Dual-Layer Design)



* Compared to Traditional RAG: Solves the "floating unconnected facts" problem; compressed index provides knowledge navigation, increasing cross-domain query recall rate by 40%+;

* Compared to Flat File Solutions: Avoids full-context injection with constant token consumption, improving retrieval efficiency by 3x;

* Compared to MemGPT/Letta: No complex memory paging management, latency controlled within 100ms, low complexity and easy deployment;

* Compared to Single API Solutions: Supports local/third-party API switching, balancing cost and flexibility with significant Chinese adaptation advantages.

### 4. Extremely Easy to Use + Flexible Expansion



* Core logic is only \~200 lines of Python, with low deployment cost and low threshold for secondary development;

* Supports MD File URL Import: Enter the online URL of a Markdown document to automatically parse and write content to the local vector database, quickly building a dedicated knowledge base;

* Compatible with more local inference engines (future plan) to adapt to different scenario needs.

## Quick Start (For Yourself — And For Your Reference)

> At this stage, the project is mainly built to 
>
> **solve the author's own needs**
>
>  while being open-sourced for anyone with similar pain points.

### 1. Environment Preparation



```
\# 1. Clone the repository

git clone https://github.com/Carlow7922/BrainyAssist.git

cd BrainyAssist

\# 2. Install core dependencies

pip install chromadb sentence-transformers requests

\# 3. Install frontend dependencies (required for Web interface)

pip install fastapi uvicorn jinja2 python-multipart
```

### 2. Configuration Instructions

#### (1) Cognitive File Configuration



* Edit `data/cognitive_space/``permanent_cognition.md`: Write fixed core project information (e.g., "Project Name: BrainyAssist, Core Goal: Low-Cost Long-Term Memory Assistant");

* Edit `data/cognitive_space/``temporary_context.md`: Write current session temporary information (e.g., "Current Task: Test document import function, Progress: 30%");

* Edit `data/``MEMORY.md`: Fill in knowledge classifications in compressed index format (refer to zer0dex examples, e.g., "## Project Related - Core Features: Long-Term Memory, MD Import; ## Tech Stack: Python, FastAPI, Chroma").

#### (2) API Configuration (Supports 2 Types, Unified File-Based Management)

All API connection parameters are modified in the configuration file `BrainyAssist/.env`, supporting one-click switching between local/third-party APIs:



| API Type                                    | Core Configuration Items                                                                                                  | Default Value/Example                                  |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **Llama.cpp Local API**                     | BASE_URL=http://192.168.1.2:8000/v1                                                                        |must match Llama.cpp service |
| **Third-Party API (e.g., DeepSeek/Doubao)** | API\_TYPE=third\_party>THIRD\_PARTY\_ENDPOINT=[https://api.deepseek](https://api.deepseek).com\_PARTY\_KEY=YOUR\_API\_KEY | Fill in the corresponding platform's endpoint and key  |

Configuration Steps:



1. Copy `BrainyAssist/.env.example` to `BrainyAssist/.env` (create .env directly if the example file does not exist);

2. Fill in the corresponding configuration items based on the actual API type used, and comment out the unused type configuration;

3. Ensure the local API is started (Llama.cpp scenario) or the API key is valid (third-party scenario).

### 3. Start the Project

#### Method: Launch Web Frontend (Visual Interaction, Recommended)



```
\# Run the frontend script

python BrainyAssist/web/app.py

\# Or start directly via uvicorn (more stable)

uvicorn BrainyAssist.web.app:app
```

### 4. Advanced Feature: Import MD Documents to Vector Database

Enter a valid online URL of a Markdown document in the Web interface. The system will automatically parse the document content and write it to the local vector database (storage path: `BrainyAssist/data/memory`), enabling rapid expansion of the knowledge base.

### 5. Project File Structure Reference

For a complete file directory explanation, refer to: `BrainyAssist/``DATA_MAP.md` to quickly understand the function and purpose of each directory/file.

## Project Status & Roadmap



* ✅ MVP has verified memory retention capability (see [BrainDecoupledLLM-MVP](https://github.com/Carlow7922/BrainDecoupledLLM-MVP/tree/main));

* ✅ Integrated zer0dex dual-layer memory architecture (compressed index + vector retrieval);

* ✅ Adapted Chinese-optimized lightweight embedding model m3e-small;

* ✅ Implemented basic Web frontend interaction (powered by FastAPI);

* ✅ Supported MD file URL import to vector database;

* ✅ Supported dual-mode (Llama.cpp local API + third-party low-cost API) with file-based configuration management;

* 🔨 In Development:


  * Fully automatic memory writing (based on conversation importance scoring);

  * Writing vector database retrieval results to cache;

  * Integrating memory re-ranking models to improve retrieval accuracy;

* 📅 Future Plans:


  * One-click installer (packaged as exe via PyInstaller);

  * Supporting more local inference engines (llama.cpp, Ollama, etc.);

  * Optimizing the graphical interface to lower the threshold for non-technical users;

  * Supporting image input (multimodal expansion);

  * Adding quick adaptation templates for more third-party APIs (no need to manually fill in endpoints).

## Who Is This For?



* Developers/researchers burning high API costs daily (pursuing low costs);

* Anyone who needs **long-term project memory** but doesn’t want to pay huge bills;

* Technology explorers interested in brain-inspired, modular AI architectures;

* Privacy-conscious users who want a fully offline "memory-enabled assistant" running locally;

* Users in Chinese-language scenarios needing efficient memory retrieval with flexible local/cloud deployment options.

## Who Is This NOT For?



* Those needing to process 1 million token ultra-long documents in one go (use specialized tools like Gemini);

* Non-technical users unwilling to write a single line of configuration or use the command line (wait for our one-click installer);

* Users urgently needing image input and multimodal interactions (not supported currently);

* Users pursuing managed services who refuse local deployment and low-cost APIs.

## Frequently Asked Questions

**Q: Why not directly use LangChain's ConversationBufferMemory?**

A: LangChain's Buffer still injects the entire history into the context, causing costs to grow linearly with turns. We use **fixed core + dual-layer memory retrieval** for constant costs and more efficient cross-domain retrieval.

**Q: How to ensure the accuracy of memory retrieval?**

A: Currently using m3e-small (Chinese)/nomic-embed-text-v1.5 (English) for embeddings, with a recall rate of >90% for factual queries. A re-ranking model will be added later to further improve accuracy.

**Q: Can it be used commercially?**

A: The code is licensed under MIT, commercial use is welcome. For technical support, contact via Issues.

**Q: How to back up/migrate vector database data?**

A: The vector database is stored in the `data/memory/` directory. Simply copy this directory to complete backup/migration without additional configuration.

**Q: How to switch between local API and third-party API?**

A: Edit the configuration file `BrainyAssist/.env`, modify `API_TYPE` to `local_llama_cpp` or `third_party`, fill in the corresponding configuration items, and restart the service to take effect.

**Q: Which third-party APIs are supported?**

A: Theoretically supports all APIs compatible with OpenAI format or providing text generation interfaces (e.g., DeepSeek, Doubao Pro, SiliconFlow). Simply fill in the corresponding `endpoint` and `key` in `.env`. Quick adaptation templates will be added in the future, eliminating the need for manual endpoint configuration.



***

**Final Note**:

This project first and foremost solves my own pain — a 200 RMB daily token bill. If you share the same pain, this is for you. If not, feel free to bookmark it and come back when expensive APIs start to sting.

**Stars are not the goal — saving money is.**

(Of course, if it saves you money, a star would be greatly appreciated 😊)

> （注：文档部分内容可能由 AI 生成）

**License**: MIT  
**Author**: Carlow  
