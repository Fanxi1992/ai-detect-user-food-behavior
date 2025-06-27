import random
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class NutritionData:
    """营养数据结构"""
    food_name: str
    calories: int  # 卡路里
    protein: float  # 蛋白质(g)
    carbs: float   # 碳水化合物(g)
    fat: float     # 脂肪(g)
    meal_type: str  # 餐次类型：breakfast, lunch, dinner, snack

@dataclass
class HealthBehaviorResult:
    """健康行为检测结果"""
    type: str  # 'relevant' 或 'unrelevant'
    nutrition_data: Optional[NutritionData] = None
    confidence: float = 0.0  # 置信度
    detected_keywords: list = None  # 检测到的关键词

class HealthBehaviorService:
    """健康行为检测服务"""
    
    def __init__(self):
        # Mock食物数据库
        self.food_database = {
            "瑞幸咖啡": {"calories": 32, "protein": 1.2, "carbs": 5.0, "fat": 1.6},
            "咖啡": {"calories": 32, "protein": 1.2, "carbs": 5.0, "fat": 1.6},
            "拿铁": {"calories": 150, "protein": 8.0, "carbs": 12.0, "fat": 8.0},
            "美式咖啡": {"calories": 15, "protein": 0.5, "carbs": 2.0, "fat": 0.2},
            "苹果": {"calories": 95, "protein": 0.5, "carbs": 25.0, "fat": 0.3},
            "香蕉": {"calories": 105, "protein": 1.3, "carbs": 27.0, "fat": 0.4},
            "米饭": {"calories": 130, "protein": 2.7, "carbs": 28.0, "fat": 0.3},
            "鸡胸肉": {"calories": 165, "protein": 31.0, "carbs": 0.0, "fat": 3.6},
            "沙拉": {"calories": 50, "protein": 2.0, "carbs": 10.0, "fat": 1.0},
            "酸奶": {"calories": 100, "protein": 6.0, "carbs": 12.0, "fat": 3.0},
        }
        
        # 健康行为关键词
        self.health_keywords = [
            "吃了", "喝了", "吃", "喝", "早餐", "午餐", "晚餐", "夜宵",
            "运动", "跑步", "散步", "睡觉", "睡眠", "喝水", "锻炼",
            "健身", "瑜伽", "游泳", "骑车"
        ]
    
    def detect_health_behavior(self, user_input: str) -> HealthBehaviorResult:
        """
        检测用户输入是否涉及健康行为
        当前使用Mock逻辑：50%概率返回relevant
        """
        # Mock逻辑：随机判断
        is_relevant = random.choice([True, False])
        
        if not is_relevant:
            return HealthBehaviorResult(
                type="unrelevant",
                confidence=0.3
            )
        
        # 如果判断为相关，生成mock营养数据
        nutrition_data = self._generate_mock_nutrition_data(user_input)
        detected_keywords = self._extract_keywords(user_input)
        
        return HealthBehaviorResult(
            type="relevant",
            nutrition_data=nutrition_data,
            confidence=0.8,
            detected_keywords=detected_keywords
        )
    
    def _extract_keywords(self, text: str) -> list:
        """提取健康相关关键词"""
        found_keywords = []
        for keyword in self.health_keywords:
            if keyword in text:
                found_keywords.append(keyword)
        return found_keywords
    
    def _generate_mock_nutrition_data(self, user_input: str) -> NutritionData:
        """根据用户输入生成mock营养数据"""
        # 简单的食物识别逻辑
        detected_food = None
        for food_name in self.food_database.keys():
            if food_name in user_input:
                detected_food = food_name
                break
        
        # 如果没有识别到具体食物，使用默认数据
        if not detected_food:
            detected_food = random.choice(list(self.food_database.keys()))
        
        food_data = self.food_database[detected_food]
        
        # 确定餐次类型
        meal_type = self._determine_meal_type(user_input)
        
        return NutritionData(
            food_name=detected_food,
            calories=food_data["calories"],
            protein=food_data["protein"],
            carbs=food_data["carbs"],
            fat=food_data["fat"],
            meal_type=meal_type
        )
    
    def _determine_meal_type(self, text: str) -> str:
        """根据文本内容判断餐次类型"""
        if any(word in text for word in ["早餐", "早上", "breakfast"]):
            return "breakfast"
        elif any(word in text for word in ["午餐", "中午", "lunch"]):
            return "lunch"
        elif any(word in text for word in ["晚餐", "晚上", "dinner"]):
            return "dinner"
        else:
            return "snack"  # 默认为零食
    
    def format_result_for_api(self, result: HealthBehaviorResult) -> Dict[str, Any]:
        """将检测结果格式化为API响应格式"""
        response = {
            "type": result.type,
            "confidence": result.confidence
        }
        
        if result.type == "relevant" and result.nutrition_data:
            nutrition = result.nutrition_data
            response["nutrition_data"] = {
                "food_name": nutrition.food_name,
                "calories": nutrition.calories,
                "protein": nutrition.protein,
                "carbs": nutrition.carbs,
                "fat": nutrition.fat,
                "meal_type": nutrition.meal_type
            }
            response["detected_keywords"] = result.detected_keywords or []
        
        return response