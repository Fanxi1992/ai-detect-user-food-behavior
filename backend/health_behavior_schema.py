# 健康行为检测结构化输出Schema定义

HEALTH_BEHAVIOR_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "enum": ["relevant", "unrelevant"],
            "description": "判断用户输入是否与健康营养行为相关"
        },
        "nutrition_data": {
            "anyOf": [
                {
                    "type": "object",
                    "properties": {
                        "food_name": {
                            "type": "string",
                            "description": "所有涉及到的食物名称+数量的总体说明，如：1碗米饭、2个苹果和1个香蕉等"
                        },
                        "calories": {
                            "type": "number",
                            "description": "热量（千卡），基于常见份量估算"
                        },
                        "protein": {
                            "type": "number", 
                            "description": "蛋白质含量（克）"
                        },
                        "carbs": {
                            "type": "number",
                            "description": "碳水化合物含量（克）"
                        },
                        "fat": {
                            "type": "number",
                            "description": "脂肪含量（克）"
                        },
                        "meal_type": {
                            "type": "string",
                            "enum": ["早餐", "上午加餐", "午餐", "下午加餐", "晚餐", "夜宵"],
                            "description": "餐次类型，根据用户描述或当前时间判断"
                        }
                    },
                    "required": ["food_name", "calories", "protein", "carbs", "fat", "meal_type"],
                    "additionalProperties": False
                },
                {
                    "type": "null"
                }
            ]
        }
    },
    "required": ["type", "nutrition_data"],
    "additionalProperties": False
}

# 提示词模板
HEALTH_BEHAVIOR_PROMPT_TEMPLATE = """请分析用户的输入是否与健康营养行为相关，并按要求返回结构化数据。

当前北京时间：{current_time}

用户输入："{user_input}"

分析要求：
1. 判断用户输入是否涉及具体的饮食、营养、健康行为相关内容
   - 相关(relevant)：用户提到了具体的食物、饮品、营养补充剂、进餐行为等
   - 不相关(unrelevant)：用户询问健康知识、运动建议、一般性咨询等，但没有涉及具体的饮食行为

2. 如果相关(type: "relevant")，请提取或估算营养信息，如果是多个食物，那么计算calories、protein、carbs、fat的总量：
   - food_name: 具体的食物名称，如"白米饭"、"苹果"、"牛奶"等
   - calories: 热量(千卡)，基于中国常见食物营养数据和常规份量估算
   - protein: 蛋白质(克)，保留1位小数
   - carbs: 碳水化合物(克)，保留1位小数  
   - fat: 脂肪(克)，保留1位小数
   - meal_type: 根据用户描述或当前时间判断餐次类型
     * 如果用户明确提到是哪一餐，优先使用用户的描述
     * 如果未明确提到，根据当前时间判断：
       - 06:00-09:00: 早餐
       - 09:00-11:00: 上午加餐
       - 11:00-14:00: 午餐
       - 14:00-17:00: 下午加餐
       - 17:00-21:00: 晚餐
       - 21:00-06:00: 夜宵

3. 如果不相关(type: "unrelevant")，nutrition_data设为null

营养估算原则：
- 基于中国常见食物营养成分表
- 按照正常食用份量估算（如1碗米饭约150g，1个中等苹果约200g）
- 数值保留1位小数，确保合理性
- 如无法准确估算，给出保守的合理近似值

请严格按照JSON schema返回结构化数据。"""

SYSTEM_PROMPT = """你是一个专业的营养健康分析师，擅长从用户的日常描述中识别和分析饮食营养信息。

你的专业能力包括：
1. 准确识别用户输入中的饮食营养相关内容
2. 基于中国常见食物营养数据进行科学估算
3. 根据上下文和时间推断合理的餐次类型
4. 提供准确、实用的营养成分分析

请始终保持专业、准确、有帮助的态度，确保分析结果的科学性和实用性。"""