# 集成测试指南

## 测试目标
验证大模型结构化输出集成是否正常工作，确保前后端协同正确。

## 测试步骤

### 1. 后端测试

#### 启动后端服务
```bash
cd backend
python main.py
```

#### 测试健康行为检测API
```bash
# 测试relevant情况
curl -X POST "http://localhost:8000/api/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我刚吃了一碗白米饭",
    "session_id": "test-session"
  }'

# 测试unrelevant情况  
curl -X POST "http://localhost:8000/api/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "今天天气真好",
    "session_id": "test-session"
  }'
```

#### 运行专用测试脚本
```bash
cd backend
python test_health_detection.py
```

### 2. 前端测试

#### 启动前端服务
```bash
cd frontend
npm run dev
```

#### 手动测试用例

**测试用例1: 健康相关输入**
- 输入: "刚吃了一个苹果"
- 期望行为:
  1. 立即显示"正在思考中..."动画
  2. 2-4秒后动画消失，显示营养统计卡片
  3. 继续显示AI流式回答

**测试用例2: 非健康相关输入**  
- 输入: "今天天气怎么样"
- 期望行为:
  1. 立即显示"正在思考中..."动画
  2. 2-4秒后动画消失，无营养卡片
  3. 直接显示AI流式回答

**测试用例3: 带时间信息的输入**
- 输入: "早上喝了一杯牛奶"
- 期望行为:
  1. 营养卡片中meal_type显示为"早餐"
  2. 营养数据符合牛奶的典型数值

### 3. 数据持久化测试

1. 输入包含食物的消息
2. 刷新页面
3. 确认营养卡片重新显示

### 4. 错误处理测试

#### API密钥错误测试
1. 临时设置错误的OPENROUTER_API_KEY
2. 发送消息
3. 确认fallback机制正常工作

#### 网络错误测试
1. 断开网络连接
2. 发送消息  
3. 确认错误提示正确显示

## 预期结果

### 成功指标
- ✅ 健康行为检测准确性 > 80%
- ✅ 动画时机正确（立即显示，LLM响应后隐藏）
- ✅ 营养数据格式正确
- ✅ 餐次类型判断合理
- ✅ 数据持久化正常
- ✅ 错误处理完善
- ✅ 用户体验流畅

### 常见问题排查

**问题1: 动画一直显示不消失**
- 检查health_behavior响应是否正确返回
- 查看浏览器控制台错误

**问题2: 营养卡片不显示**  
- 确认后端返回type为'relevant'
- 检查nutrition_data字段完整性

**问题3: LLM响应错误**
- 验证OpenRouter API密钥配置
- 检查模型是否支持结构化输出

**问题4: 时间判断不准确**
- 确认北京时区配置正确
- 验证时间格式传递

## 性能指标

- 健康行为检测响应时间: < 5秒
- 前端动画流畅性: 60fps
- 数据库查询延迟: < 100ms
- 整体用户体验: 无明显卡顿