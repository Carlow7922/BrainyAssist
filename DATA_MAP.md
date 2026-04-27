# BrainyAssist 项目文件索引 (DATA_MAP.md)

## 🚀 版本与功能路线图 (Agile Roadmap)
**当前版本：v0.4.0 (WebUI 可视化版) 🛠️ 迭代中**

- [x] **v0.1.0**：基础架构搭建 $\rightarrow$ API 链路打通 $\rightarrow$ 交互对话验证。
- [x] **v0.2.0**：认知空间与自动记忆 $\rightarrow$ 实时注入 $\rightarrow$ 带时间戳的自动固化。
- [x] **v0.3.0**：**语义记忆增强** $\rightarrow$ `m3e-small` + `ChromaDB` $\rightarrow$ 语义检索注入。
- [>] **v0.4.0**：**可视化闭环**
    - [x] **Sprint 1: API 骨架搭建** $\rightarrow$ FastAPI 后端 $\rightarrow$ 接口定义 $\rightarrow$ 端口配置 $\checkmark$
    - [x] **Sprint 2: 交互界面实现** $\rightarrow$ HTML/CSS/JS 聊天界面 $\rightarrow$ 实时对话交互 $\checkmark$
    - [ ] **Sprint 3: 记忆管理面板** $\rightarrow$ `MEMORY.md` 编辑 $\rightarrow$ 记忆日志查看。

---

## 📂 项目文件结构

### 项目根目录: `BrainyAssist/`
- `.env` : 环境变量配置文件。
- `test_connection.py` : 连通性测试脚本。
- `chat.py` : 交互式对话脚本。
- `DATA_MAP.md` : 本文件，记录项目结构、版本进度及功能。

### 核心源码包: `brainyassist/`
- `__init__.py` : 包初始化。

#### 1. 核心配置层 `brainyassist/core/`
- `config.py` : 全局配置中心。

#### 2. AI 通信层 `brainyassist/ai/`
- `client.py` : AI 客户端。实现认知注入、向量检索与自动固化。

#### 3. 记忆模块 `brainyassist/memory/`
- `core.py` : 向量记忆核心。集成 `m3e-small` 与 `ChromaDB`。
- `seed.py` : 知识库导入工具。

### Web 界面层 `web/`
- `app.py` : **FastAPI 后端服务器**。处理 API 请求与静态资源分发。
- `static/` : 存放 CSS 和 JS 脚本。
- `templates/` : 存放 HTML 模板文件。

### 数据存储目录: `data/`
- `cognitive_space/` : 核心认知空间。
- `sessionsMemory.md` : 会话记忆库。
- `memory/` : ChromaDB 本地向量存储目录。
- `MEMORY.md` : 用户手动维护的压缩索引层。
