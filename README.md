# 🏥 AI健康聊天机器人

> 基于大模型的智能健康行为识别与营养追踪系统

[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-blue.svg)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12-green.svg)](https://www.python.org/)

## 📋 项目概述

这是一个全栈AI驱动的健康聊天机器人H5应用，通过OpenRouter API集成真实的大语言模型，具备智能健康行为识别和营养追踪功能。系统能够实时分析用户的饮食行为，提供个性化的营养信息和健康建议。

### ✨ 核心特性

🤖 **智能对话系统**
- 基于OpenRouter的实时流式聊天
- 支持Markdown格式回复
- 持久化聊天历史记录

🍎 **健康行为识别**
- AI驱动的饮食行为智能识别
- 结构化营养数据提取
- 基于时间的餐次自动分类

📊 **营养追踪系统**
- 实时营养成分分析（热量、蛋白质、碳水、脂肪）
- 交互式营养信息卡片
- 支持中文餐次分类（早餐/午餐/晚餐/加餐/夜宵）

🎨 **现代化界面**
- 响应式移动端适配
- 流畅的动画交互效果
- 多类型头像系统（用户/AI/健康）
- 实时思考动画反馈

## 🏗️ 技术架构

### 前端技术栈
- **框架**: React 18.2 + TypeScript
- **构建工具**: Vite 5.0
- **状态管理**: Zustand 5.0
- **样式系统**: TailwindCSS 4.1 + 模块化CSS
- **动画库**: Framer Motion 12.19
- **Markdown渲染**: React Markdown 10.1

### 后端技术栈
- **框架**: FastAPI 0.104 + Uvicorn
- **数据库**: SQLite + aiosqlite (异步操作)
- **AI集成**: OpenAI SDK + OpenRouter API
- **数据验证**: Pydantic 2.5
- **时区处理**: PyTZ

### 核心功能模块

#### 🔄 双阶段流式处理
1. **健康行为检测阶段**
   - 用户输入 → 保存到数据库
   - AI分析健康行为 → 结构化数据提取
   - 前端显示思考动画 → 营养卡片展示

2. **智能对话阶段**
   - 获取对话历史 → 构建上下文
   - 调用大模型API → 流式响应输出
   - 实时渲染回复 → 保存完整对话

#### 📱 核心组件架构
```
src/
├── components/
│   ├── ChatContainer.tsx      # 主聊天界面容器
│   ├── MessageList.tsx        # 消息列表组件
│   ├── ChatInput.tsx          # 输入界面组件
│   ├── MessageBubble.tsx      # 消息气泡组件
│   ├── StreamingMessage.tsx   # 流式消息组件
│   ├── Avatar.tsx             # 多类型头像组件
│   ├── HealthBehaviorAnimation.tsx  # 健康行为分析动画
│   └── NutritionCard.tsx      # 营养信息卡片
├── services/
│   └── chatService.ts         # API通信服务
├── store/
│   └── chatStore.ts           # Zustand状态管理
└── styles/                    # 模块化样式文件
```

## 🚀 快速开始

### 环境要求
- Node.js 16+ 
- Python 3.10+
- OpenRouter API密钥

### 1. 克隆项目
```bash
git clone <repository-url>
cd AI健康小程序
```

### 2. 后端设置
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加你的 OpenRouter API 密钥
```

### 3. 前端设置
```bash
cd frontend

# 安装依赖
npm install
```

### 4. 启动应用

#### 方式一：使用启动脚本（推荐）
```bash
chmod +x start_demo.sh
./start_demo.sh
```

#### 方式二：分别启动
```bash
# 终端1 - 启动后端
cd backend
python main.py

# 终端2 - 启动前端
cd frontend
npm run dev
```

### 5. 访问应用
- 🌐 前端界面: http://localhost:5173
- 🔧 后端API: http://localhost:8000
- 📚 API文档: http://localhost:8000/docs

## ⚙️ 配置说明

### 环境变量配置 (backend/.env)
```bash
# OpenRouter API配置
OPENROUTER_API_KEY=your-openrouter-api-key-here

# 模型配置
DEFAULT_MODEL=openai/gpt-4o-mini              # 主对话模型
HEALTH_DETECTION_MODEL=openai/gpt-4o-mini     # 健康行为检测模型(需支持结构化输出)
```

### 健康行为检测配置
系统支持以下餐次类型的自动识别和分类：

| 餐次类型 | 时间范围 | 图标 |
|---------|---------|------|
| 早餐 | 06:00-09:00 | 🌅 |
| 上午加餐 | 09:00-11:00 | ☕ |
| 午餐 | 11:00-14:00 | 🌞 |
| 下午加餐 | 14:00-17:00 | 🍎 |
| 晚餐 | 17:00-21:00 | 🌙 |
| 夜宵 | 21:00-06:00 | 🌃 |

## 🗄️ 数据库结构

### SQLite表结构
```sql
CREATE TABLE messages (
    id TEXT PRIMARY KEY,                    -- UUID消息ID
    session_id TEXT,                        -- 会话ID
    content TEXT,                           -- 消息内容
    is_user BOOLEAN,                        -- 是否为用户消息
    timestamp DATETIME,                     -- 时间戳
    health_behavior_data TEXT               -- 健康行为数据(JSON)
);
```

### 健康行为数据结构
```typescript
interface HealthBehaviorData {
  type: 'relevant' | 'unrelevant';
  nutrition_data?: {
    food_name: string;        // 食物名称
    calories: number;         // 热量(千卡)
    protein: number;          // 蛋白质(克)
    carbs: number;           // 碳水化合物(克)
    fat: number;             // 脂肪(克)
    meal_type: string;       // 餐次类型
  } | null;
}
```

## 🌟 功能演示

### 智能健康行为识别
当用户输入涉及饮食的内容时，系统会：

1. **显示思考动画**
   - 3阶段动态文本："正在理解问题..." → "正在解析行为..." → "正在生成结果..."
   - 脉冲式动画效果配合动态点点点

2. **营养数据提取**
   - AI分析食物类型和营养成分
   - 基于中国食物营养数据库进行估算
   - 自动判断餐次类型

3. **信息卡片展示**
   - 精美的营养信息卡片
   - 包含热量、蛋白质、碳水、脂肪数据
   - 支持编辑和删除操作

### 实时流式对话
- **无延迟响应**: 移除人为延迟，实现真正的实时体验
- **一致性布局**: 流式渲染期间保持头像和布局一致
- **Markdown支持**: 支持格式化文本、代码块等

## 📁 项目结构

```
AI健康小程序/
├── 📁 backend/                 # 后端服务
│   ├── main.py                # FastAPI应用主入口
│   ├── database.py            # 数据库操作模块
│   ├── openrouter_service.py  # OpenRouter API服务
│   ├── health_behavior_service.py    # 健康行为检测服务
│   ├── health_behavior_schema.py     # 结构化数据模式
│   ├── models.py              # Pydantic数据模型
│   ├── config.py              # 配置管理
│   └── requirements.txt       # Python依赖
├── 📁 frontend/               # 前端应用
│   ├── 📁 src/
│   │   ├── 📁 components/     # React组件
│   │   ├── 📁 services/       # API服务
│   │   ├── 📁 store/          # 状态管理
│   │   └── 📁 styles/         # 样式文件
│   ├── package.json           # Node.js依赖
│   └── vite.config.ts         # Vite配置
├── start_demo.sh              # 一键启动脚本
├── CLAUDE.md                  # 开发文档
└── README.md                  # 项目说明
```

## 🛠️ 开发命令

### 前端开发
```bash
cd frontend
npm run dev      # 开发服务器
npm run build    # 生产构建
npm run lint     # 代码检查
npm run preview  # 预览构建结果
```

### 后端开发
```bash
cd backend
python main.py                    # 启动开发服务器
pip install -r requirements.txt   # 安装依赖
```

## 🔧 API接口

### 聊天接口
- `POST /api/chat/stream` - 流式聊天（主要接口）
- `POST /api/chat` - 非流式聊天
- `GET /api/chat/history/{session_id}` - 获取聊天历史
- `DELETE /api/chat/history/{session_id}` - 清除聊天历史

### 系统接口
- `GET /api/health` - 健康检查
- `GET /api/config` - 配置状态检查

### 接口示例

#### 流式聊天请求
```bash
curl -X POST "http://localhost:8000/api/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我刚吃了一个苹果",
    "session_id": "uuid-session-id"
  }'
```

#### 响应格式
```json
// 健康行为检测结果
data: {"type": "health_behavior", "data": {"type": "relevant", "nutrition_data": {...}}}

// 聊天内容流
data: {"type": "chat", "content": "苹果是很好的", "done": false}
data: {"type": "chat", "content": "水果选择！", "done": false}
data: {"type": "chat", "content": "", "done": true}
```

## 🎯 核心特色

### 1. 智能化程度高
- 基于大语言模型的自然语言理解
- 结构化输出确保数据一致性
- 上下文感知的智能对话

### 2. 用户体验优秀
- 3阶段思考动画提供清晰反馈
- 流式渲染带来实时交互感
- 响应式设计适配各种设备

### 3. 架构设计合理
- 前后端分离，职责清晰
- 模块化组件，易于维护
- 异步处理，性能优秀

### 4. 数据可靠性强
- SQLite持久化存储
- 完整的错误处理机制
- API密钥安全管理

## 🔮 未来扩展

- [ ] 添加更多营养分析维度（维生素、矿物质等）
- [ ] 支持图片识别分析食物
- [ ] 个人健康档案和趋势分析
- [ ] 多语言支持
- [ ] 移动App版本开发
- [ ] 集成更多健康数据源

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [OpenRouter](https://openrouter.ai/) - 提供AI模型API服务
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Python Web框架
- [React](https://reactjs.org/) - 用户界面构建库
- [Vite](https://vitejs.dev/) - 下一代前端构建工具
- [Zustand](https://github.com/pmndrs/zustand) - 轻量级状态管理库

---

💡 **提示**: 如果你觉得这个项目有帮助，请给它一个⭐星标！

📧 **联系**: 如有问题或建议，欢迎提交Issue或直接联系开发者。