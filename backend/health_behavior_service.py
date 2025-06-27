import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import pytz
from openai import OpenAI
from .health_behavior_schema import HEALTH_BEHAVIOR_SCHEMA, HEALTH_BEHAVIOR_PROMPT_TEMPLATE, SYSTEM_PROMPT
from .config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, HEALTH_DETECTION_MODEL

# 设置日志
logger = logging.getLogger(__name__)

class HealthBehaviorService:
    """健康行为检测服务 - 使用大模型结构化输出"""
    
    def __init__(self):
        # 初始化OpenAI客户端，配置为使用OpenRouter
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL
        )
        
        # 配置使用的模型（支持结构化输出的模型）
        self.model = HEALTH_DETECTION_MODEL
        
        # 北京时区
        self.beijing_tz = pytz.timezone('Asia/Shanghai')
    
    async def detect_health_behavior(self, user_input: str) -> Dict[str, Any]:
        """
        使用大模型检测用户输入是否涉及健康行为
        返回结构化的检测结果
        """
        try:
            # 获取当前北京时间
            current_time = datetime.now(self.beijing_tz)
            time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            # 构建提示词
            prompt = HEALTH_BEHAVIOR_PROMPT_TEMPLATE.format(
                current_time=time_str,
                user_input=user_input
            )
            
            logger.info(f"开始健康行为检测，用户输入: {user_input[:50]}...")
            
            # 调用大模型进行结构化输出
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "health_behavior_analysis",
                        "strict": True,
                        "schema": HEALTH_BEHAVIOR_SCHEMA
                    }
                },
                temperature=0.1,  # 降低随机性，提高一致性
                max_tokens=1000   # 控制输出长度
            )
            
            # 解析结构化响应
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            logger.info(f"健康行为检测完成，类型: {result.get('type')}")
            
            # 验证结果完整性
            self._validate_result(result)
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
            return self._get_fallback_result()
            
        except Exception as e:
            logger.error(f"健康行为检测失败: {e}")
            return self._get_fallback_result()
    
    def _validate_result(self, result: Dict[str, Any]) -> None:
        """验证检测结果的完整性"""
        if result.get('type') not in ['relevant', 'unrelevant']:
            raise ValueError("Invalid type value")
        
        if result.get('type') == 'relevant':
            nutrition_data = result.get('nutrition_data')
            if not nutrition_data:
                raise ValueError("Missing nutrition_data for relevant type")
            
            required_fields = ['food_name', 'calories', 'protein', 'carbs', 'fat', 'meal_type']
            for field in required_fields:
                if field not in nutrition_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # 验证meal_type是否在允许的值范围内
            valid_meal_types = ["早餐", "上午加餐", "午餐", "下午加餐", "晚餐", "夜宵"]
            if nutrition_data['meal_type'] not in valid_meal_types:
                raise ValueError("Invalid meal_type value")
    
    def _get_fallback_result(self) -> Dict[str, Any]:
        """
        在LLM调用失败时返回fallback结果
        默认返回unrelevant，让用户流程继续
        """
        logger.warning("使用fallback结果：unrelevant")
        return {
            "type": "unrelevant",
            "nutrition_data": None
        }
    
    def format_result_for_api(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        将检测结果格式化为API响应格式
        保持与现有前端期望的数据结构一致
        """
        # 新的结构化输出已经是正确的格式，直接返回
        return result
    
    def _get_current_meal_type_hint(self) -> str:
        """
        根据当前时间获取推荐的餐次类型（用于调试）
        """
        current_time = datetime.now(self.beijing_tz)
        hour = current_time.hour
        
        if 6 <= hour < 9:
            return "早餐"
        elif 9 <= hour < 11:
            return "上午加餐"
        elif 11 <= hour < 14:
            return "午餐"
        elif 14 <= hour < 17:
            return "下午加餐"
        elif 17 <= hour < 21:
            return "晚餐"
        else:
            return "夜宵"

# 为了保持向后兼容，保留一些数据类（如果其他地方仍在使用）
class NutritionData:
    """营养数据结构 - 保持向后兼容"""
    def __init__(self, food_name: str, calories: float, protein: float, 
                 carbs: float, fat: float, meal_type: str):
        self.food_name = food_name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.meal_type = meal_type

class HealthBehaviorResult:
    """健康行为检测结果 - 保持向后兼容"""
    def __init__(self, type: str, nutrition_data: Optional[Dict] = None, 
                 confidence: float = 0.0, detected_keywords: list = None):
        self.type = type
        self.nutrition_data = nutrition_data
        self.confidence = confidence
        self.detected_keywords = detected_keywords or []