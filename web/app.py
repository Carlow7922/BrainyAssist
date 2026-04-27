from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import shutil
import os
from pathlib import Path

# 导入 BrainyAssist 核心组件
from brainyassist.ai.client import AIClient
from brainyassist.memory.seed import MemorySeeder
from brainyassist.core.config import Config

app = FastAPI(title="BrainyAssist API")

# 初始化核心组件
ai_client = AIClient()
seeder = MemorySeeder()

# 配置静态文件和模板路径
app.mount("/static", StaticFiles(directory=Config.ROOT_DIR / "web" / "static"), name="static")
templates = Jinja2Templates(directory=str(Config.ROOT_DIR / "web" / "templates"))

@app.get("/")
async def read_root(request: Request):
    """返回主界面"""
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.post("/chat")
async def chat(prompt: str = Form(...)):
    """对话接口"""
    try:
        response = ai_client.chat(prompt)
        return {"status": "success", "reply": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/seed")
async def seed_file(file: UploadFile = File(...)):
    """文件导入接口"""
    try:
        temp_path = Config.DATA_DIR / f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        seeder.seed_from_file(str(temp_path))
        os.remove(temp_path)
        return {"status": "success", "message": f"File {file.filename} seeded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/index")
async def get_memory_index():
    """获取 MEMORY.md 的内容"""
    if Config.USER_MEMORY_INDEX_FILE.exists():
        with open(Config.USER_MEMORY_INDEX_FILE, 'r', encoding='utf-8') as f:
            return {"content": f.read()}
    return {"content": "No index found."}

@app.get("/memory/sessions")
async def get_session_memory():
    """获取会话记忆日志"""
    if Config.SESSIONS_MEMORY_FILE.exists():
        with open(Config.SESSIONS_MEMORY_FILE, 'r', encoding='utf-8') as f:
            return {"content": f.read()}
    return {"content": "No session memory found."}

if __name__ == "__main__":
    import uvicorn
    # 使用配置文件的端口启动
    uvicorn.run(app, host="0.0.0.0", port=Config.APP_PORT)
