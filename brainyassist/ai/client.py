import requests
from datetime import datetime
from brainyassist.core.config import Config
from brainyassist.memory.core import MemoryCore

class AIClient:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.api_key = Config.API_KEY
        self.model_id = Config.MODEL_ID
        # 初始化向量记忆核心
        self.memory_core = MemoryCore()

    def _load_cognitive_space(self):
        """读取永久和临时认知空间的内容"""
        context = ""
        if Config.PERMANENT_COG_FILE.exists():
            with open(Config.PERMANENT_COG_FILE, 'r', encoding='utf-8') as f:
                context += f"\n[Permanent Cognition]\n{f.read()}\n"
        
        if Config.TEMPORARY_COG_FILE.exists():
            with open(Config.TEMPORARY_COG_FILE, 'r', encoding='utf-8') as f:
                context += f"\n[Temporary Context]\n{f.read()}\n"
        
        return context

    def _load_user_memory_index(self):
        """读取用户手动维护的 MEMORY.md (压缩索引层)"""
        if Config.USER_MEMORY_INDEX_FILE.exists():
            with open(Config.USER_MEMORY_INDEX_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def _save_to_session_memory(self, content):
        """将提炼后的信息加上时间戳并追加写入 sessionsMemory.md"""
        if not content or "无重要信息" in content:
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(Config.SESSIONS_MEMORY_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n[{timestamp}] - {content}")

    def _extract_important_info(self, user_input, ai_response):
        """调用 AI 提炼对话中的重要事实、决定或结论"""
        extract_prompt = (
            f"请分析以下对话，提取其中包含的重要事实、决定或结论。 "
            f"要求：\n1. 每条信息必须精简为一句话。\n2. 如果没有重要信息，请直接回复'无重要信息'。\n"
            f"对话内容：\n用户: {user_input}\nAI: {ai_response}\n\n提取结果："
        )
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model_id, "messages": [{"role": "user", "content": extract_prompt}]}
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"提炼信息时出错: {e}")
            return None

    def chat(self, prompt):
        # 1. 准备上下文注入
        # A. 认知空间 (身份/人格)
        cognitive_context = self._load_cognitive_space()
        
        # B. 用户手动索引 (地图)
        user_index = self._load_user_memory_index()
        
        # C. 向量库检索 (细节)
        related_memories = self.memory_core.query_memory(prompt, top_k=5)
        memory_details = "\n".join([f"- {m}" for m in related_memories]) if related_memories else "无相关细节记录。"

        # 2. 组装最终 Prompt
        # 结构：[认知空间] + [用户索引] + [检索细节] + [用户输入]
        context_block = ""
        if cognitive_context: context_block += f"{cognitive_context}\n"
        if user_index: context_block += f"\n[User Memory Index]\n{user_index}\n"
        context_block += f"\n[Related Memory Details]\n{memory_details}\n"
        
        full_prompt = f"{context_block}\n\nUser: {prompt}" if context_block else prompt
        
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model_id, "messages": [{"role": "user", "content": full_prompt}]}
        
        try:
            # 3. 获取 AI 回复
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]

            # 4. 自动固化记忆
            important_info = self._extract_important_info(prompt, ai_response)
            self._save_to_session_memory(important_info)

            return ai_response
        except Exception as e:
            return f"Error occurred: {e}"
