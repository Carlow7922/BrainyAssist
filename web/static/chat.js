document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // 辅助函数：创建并添加消息气泡
    function appendMessage(role, text) {
        const wrapper = document.createElement('div');
        wrapper.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'} message-fade-in`;

        const bubble = document.createElement('div');
        bubble.className = role === 'user' 
            ? 'bg-indigo-600 text-white p-3 rounded-lg max-w-[80%] shadow-md' 
            : 'bg-slate-800 text-slate-100 p-3 rounded-lg max-w-[80%] border border-slate-700 shadow-sm';
        
        bubble.innerText = text;
        wrapper.appendChild(bubble);
        chatContainer.appendChild(wrapper);
        
        // 自动滚动到底部
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function handleSend() {
        const text = userInput.value.trim();
        if (!text) return;

        // 1. 显示用户消息
        appendMessage('user', text);
        userInput.value = '';

        // 2. 处理 /seed 指令 (简单前端模拟，实际可通过 API 扩展)
        if (text.startsWith('/seed')) {
            appendMessage('ai', '检测到 /seed 指令。由于当前界面仅支持文本，请通过 API 或后端直接导入文件，或等待后续管理面板更新。');
            return;
        }

        // 3. 调用后端 API
        try {
            // 使用 FormData 因为后端定义为 Form(...)
            const formData = new FormData();
            formData.append('prompt', text);

            const response = await fetch('/chat', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('网络响应错误');

            const data = await response.json();
            appendMessage('ai', data.reply);
        } catch (error) {
            appendMessage('ai', `❌ 错误: ${error.message}`);
        }
    }

    // 绑定点击事件
    sendBtn.addEventListener('click', handleSend);

    // 绑定回车键
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
});
