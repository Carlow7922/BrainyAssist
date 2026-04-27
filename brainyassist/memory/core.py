import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from brainyassist.core.config import Config
from pathlib import Path

class MemoryCore:
    def __init__(self):
        # 1. 初始化嵌入模型 (m3e-small)
        # 第一次运行会自动从 HuggingFace 下载模型，约 100MB+
        self.model_name = "moka-ai/m3e-small"
        self.embedding_model = SentenceTransformer(self.model_name)
        
        # 2. 初始化 ChromaDB 客户端 (持久化存储)
        # 存储路径在 data/memory
        self.db_path = Config.ROOT_DIR / "data" / "memory"
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        
        # 3. 创建或获取集合 (Collection)
        # 我们将所有记忆存储在一个名为 'brainy_memory' 的集合中
        self.collection = self.client.get_or_create_collection(name="brainy_memory")

    def get_embedding(self, text):
        """将文本转换为向量"""
        return self.embedding_model.encode(text).tolist()

    def add_memory(self, text, metadata=None):
        """
        将记忆存入向量库
        :param text: 要存储的文本内容
        :param metadata: 附加元数据 (如日期, 来源等)
        """
        vector = self.get_embedding(text)
        # 生成唯一的 ID (简单处理：使用文本的 hash 或 随机 ID)
        import uuid
        mem_id = str(uuid.uuid4())
        
        self.collection.add(
            ids=[mem_id],
            embeddings=[vector],
            metadatas=[metadata or {}],
            documents=[text]
        )

    def query_memory(self, query_text, top_k=5):
        """
        语义检索最相关的记忆
        :param query_text: 查询文本
        :param top_k: 返回前 K 条结果
        """
        vector = self.get_embedding(query_text)
        results = self.collection.query(
            query_embeddings=[vector],
            n_results=top_k
        )
        # 返回文档内容列表
        return results['documents'][0] if results['documents'] else []

if __name__ == "__main__":
    # 基础验证测试
    print("Initializing MemoryCore...")
    try:
        mem = MemoryCore()
        print("✅ MemoryCore initialized and model loaded.")
        
        test_text = "BrainyAssist is a brain-inspired memory architecture."
        mem.add_memory(test_text, metadata={"source": "test"})
        print(f"✅ Added test memory: {test_text}")
        
        query = "What is BrainyAssist?"
        res = mem.query_memory(query)
        print(f"✅ Query result for '{query}': {res}")
    except Exception as e:
        print(f"❌ Error: {e}")
