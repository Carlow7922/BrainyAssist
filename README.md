# BrainyAssist
This project primarily addressed my own pain point—a daily token bill of 200 yuan. If you share this pain, then this is for you. If not, feel free to bookmark it and come back to it someday when you're stung by expensive APIs.

[📖 中文版](./README.zh.md) | [English](./README.md)

# BrainyAssist — Give Your AI Long-Term Memory at 1% of the Cost

> A lightweight assistant architecture based on **fixed core context + on‑demand memory retrieval**  
> Designed for **local execution, low cost, and never forgetting what matters**

## The Problem We Face

Have you ever run into these?

- You chat with DeepSeek, Claude, GPT‑4, or Gemini — after a few turns, the model **forgets key information from minutes ago**.
- To keep it on track, you have to **re‑paste the same project background** every new session, wasting tokens and time.
- Worse, the bill: you burn ¥200 (≈ $28) a day, just because you need “long context”.
- You try a local open‑source model — but it has almost no memory and forgets after three questions.

**Root cause**  
Existing solutions are either **expensive** (long‑context API models) or **stupid** (local small models with no memory).  
There is no middle ground: a cheap assistant that reliably remembers important information.

## Our Solution

### Core Idea (inspired by brain architecture)

The human brain does not cram all memories into working memory. It keeps only a minimal **core cognitive space** (values, current goal, task progress) and stores everything else in **long‑term memory**, retrieved only when needed.

We engineer this mechanism:

| Component | Role | Token cost |
| :--- | :--- | :--- |
| **Temporary Core Cognitive Space** | Fixed state injected every turn (project name, current task, tool descriptions) | Constant ~500 tokens |
| **External Memory (Vector retrieval)** | Retrieve top‑3‑5 relevant memories based on user query | ~2000 tokens |
| **LLM Inference** | Generate answer using core context + retrieved memories | Normal generation length |

**Result**  
Token consumption per request stays **almost constant**, no matter how long the conversation runs. No more context ballooning.

### Where does this idea come from?

- Neuroscience distinction between **working memory vs. long‑term memory**
- Your proven MVP: [BrainDecoupledLLM-MVP](https://github.com/Carlow7922/BrainDecoupledLLM-MVP/tree/main)
- Borrows from RAG and fixed system prompts, but reorganizes them into a **brain‑inspired modular architecture**

### Feasibility analysis

- ✅ MVP already proves that “fixed core + external retrieval” enables multi‑turn retention.
- ✅ Vector databases (Chroma, LanceDB) are mature — handle millions of memories on a single machine.
- ✅ Local models (Llama 3 8B, Qwen 2.5 7B) run comfortably on consumer GPUs (RTX 3060), completely offline, no API bills.
- ✅ Even with cheap APIs (Doubao Pro, SiliconFlow free tier), per‑request cost can be **< $0.001**.

### Implementation sketch (simple, runnable)

1. **Initialisation**: create `core_state.txt` — write your fixed cognitive context (e.g., “Project: BrainyAssist, current task: implement memory retrieval”).
2. **Each conversation turn**:
   - Load `core_state.txt` as system prompt.
   - Retrieve relevant memories from vector DB using user’s input.
   - Build prompt: (core context + retrieved memories + user question) → send to LLM.
   - Show LLM’s answer to user.
   - (Optionally) use automatic rules or a manual trigger to store new knowledge into memory.
3. **Memory management**:
   - Write: only store facts, decisions, conclusions (1‑2 sentences), ignore chit‑chat.
   - Retrieve: compute embeddings (local or API), return top‑K.

> Full core logic is ~200 lines of Python, depending on `chromadb`, `requests`, and an embedding model.

## Why This Project Matters

### 1. Drastic cost reduction

| Method | Total tokens over 50 turns | Estimated cost |
| :--- | :--- | :--- |
| Gemini / Claude long context | > 2 million | $6 – $30 |
| **BrainyAssist (local Llama)** | ~140k | **$0** (completely free) |
| **BrainyAssist (cheap API)** | ~140k | < $0.10 |

### 2. Truly local & private

- All memories and conversations stay on your own machine.
- Can work with Ollama, llama.cpp, or any local inference engine — **no API key required**.
- No data leakage, no corporate collection.

### 3. Low hardware barrier

- **Minimum**: 4GB RAM + 2‑core CPU (using Qwen 1.5B or a quantised 2‑3B model).
- **Recommended**: RTX 3060 12GB VRAM (running Llama 3 8B or Qwen 2.5 7B).

## Quick Start (for yourself — and you can adapt)

> At this stage, the project is mainly built to solve the author’s own pain, while open‑sourced for anyone who shares the same pain.

```bash
# 1. Clone
git clone https://github.com/Carlow7922/BrainyAssist.git
cd BrainyAssist

# 2. Install dependencies
pip install chromadb sentence-transformers requests

# 3. Configure your core_state.txt (example in config/core_state.example.txt)

# 4. Run the chat script
python chat.py --model local      # use local Ollama
# or
python chat.py --model api --endpoint https://api.deepseek.com --key YOUR_KEY
```

Detailed usage: [USAGE.md](./USAGE.md)

## Status & Roadmap

- ✅ MVP proven (non‑forgetting capability) — see [BrainDecoupledLLM-MVP](https://github.com/Carlow7922/BrainDecoupledLLM-MVP/tree/main)
- 🔨 In development: fully automatic memory writing (based on conversation importance scoring)
- 📅 Future plans:
  - One‑click installer (PyInstaller → .exe)
  - Support more local inference engines (llama.cpp, Ollama)
  - Optional GUI

## Who Is This For?

- Developers / researchers burning high API costs daily.
- Anyone who needs a **long‑term project memory** but doesn’t want to pay huge bills.
- Tech explorers interested in brain‑inspired, modular AI architectures.
- Privacy‑conscious users who want a fully offline assistant with memory.

## Who Is This NOT For?

- People who need to process 1M token documents in one go (use Gemini or similar specialised tools).
- Users unwilling to write a single line of config or touch the command line (please wait for our one‑click installer).

## FAQ

**Q: Why not just use LangChain’s ConversationBufferMemory?**  
A: LangChain’s buffer still pushes the whole history into the context, making cost grow linearly with turns. We use **fixed core + on‑demand retrieval** — constant cost.

**Q: How accurate is memory retrieval?**  
A: We currently use `sentence-transformers/all-MiniLM-L6-v2` for embeddings. For factual queries, recall is >90%. A reranker will be added later.

**Q: Can I use this commercially?**  
A: Yes, the code is MIT licensed. For consulting support, open an Issue.

---

**One last sentence**  
This project first and foremost solves my own pain — ¥200 of token bills every day. If you suffer from the same pain, this README is for you. If not, bookmark it; come back when the expensive APIs start hurting.

**Stars are not the goal — saving money is.**  
(Of course, if it saves you money, a star would be nice 😊)
