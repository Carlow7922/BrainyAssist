import os
from pathlib import Path
from brainyassist.memory.core import MemoryCore
from brainyassist.core.config import Config

class MemorySeeder:
    def __init__(self):
        self.memory_core = MemoryCore()
        # 针对 m3e-small 的安全分片长度 (中文建议 400 字以内)
        self.chunk_size = 400 

    def split_text(self, text):
        """将长文本切分为不超过 chunk_size 的片段"""
        chunks = []
        for i in range(0, len(text), self.chunk_size):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def seed_from_file(self, file_path):
        """从指定文件读取内容并批量导入向量库"""
        path = Path(file_path)
        if not path.exists():
            print(f"❌ 文件不存在: {file_path}")
            return

        print(f"正在处理文件: {path.name} ...")
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. 文本分片
        chunks = self.split_text(content)
        print(f"文本已切分为 {len(chunks)} 个片段")

        # 2. 批量入库
        success_count = 0
        for idx, chunk in enumerate(chunks):
            try:
                self.memory_core.add_memory(
                    text=chunk, 
                    metadata={"source": path.name, "chunk_id": idx}
                )
                success_count += 1
            except Exception as e:
                print(f"片段 {idx} 导入失败: {e}")

        print(f"✅ 成功导入 {success_count}/{len(chunks)} 个片段到向量库。")

if __name__ == "__main__":
    # 快速测试脚本
    seeder = MemorySeeder()
    # 示例：如果你有某个 md 文件想导入，可以在这里修改路径
    # seeder.seed_from_file("path/to/your/document.md")
    print("MemorySeeder 准备就绪。请在 chat.py 或其他入口调用 seed_from_file。")
