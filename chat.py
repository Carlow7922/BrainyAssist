import sys
import os
from pathlib import Path

# 确保能正确导入 brainyassist 包
root = Path(__file__).parent.absolute()
sys.path.append(str(root))

try:
    from brainyassist.ai.client import AIClient
    from brainyassist.memory.seed import MemorySeeder
except ImportError as e:
    print(f"导入失败: {e}")
    sys.exit(1)

def main():
    client = AIClient()
    seeder = MemorySeeder()
    
    print("--- BrainyAssist 交互对话模式 ---")
    print("指令集:")
    print("  /seed <文件路径>  - 将指定文件导入向量库 (例如: /seed C:/docs/note.md)")
    print("  quit / exit       - 退出对话\n")

    while True:
        try:
            user_input = input("您: ").strip()
            
            if not user_input:
                continue
                
            # 处理 /seed 指令
            if user_input.startswith("/seed "):
                file_path = user_input[6:].strip().strip('"').strip("'")
                print(f"🚀 正在尝试导入: {file_path} ...")
                seeder.seed_from_file(file_path)
                print("导入操作完成。您可以继续对话或询问关于该文件的内容。\n")
                continue

            if user_input.lower() in ['quit', 'exit']:
                print("对话结束，再见！")
                break

            # 调用 AI 客户端获取回复
            response = client.chat(user_input)
            print(f"AI: {response}\n")
            
        except KeyboardInterrupt:
            print("\n对话被中断，再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
