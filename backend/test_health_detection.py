#!/usr/bin/env python3
"""
健康行为检测功能测试脚本
用于测试大模型结构化输出功能
"""

import asyncio
import json
from health_behavior_service import HealthBehaviorService

async def test_health_detection():
    """测试健康行为检测功能"""
    
    print("🧪 开始测试健康行为检测功能...")
    print("=" * 50)
    
    # 初始化服务
    try:
        service = HealthBehaviorService()
        print("✅ 健康行为检测服务初始化成功")
    except Exception as e:
        print(f"❌ 服务初始化失败: {e}")
        return
    
    # 测试用例
    test_cases = [
        {
            "input": "我刚吃了一碗白米饭",
            "expected_type": "relevant",
            "description": "明确的饮食行为 - 应该被识别为relevant"
        },
        {
            "input": "今天天气真好啊",
            "expected_type": "unrelevant", 
            "description": "天气话题 - 应该被识别为unrelevant"
        },
        {
            "input": "早上喝了一杯牛奶和两片面包",
            "expected_type": "relevant",
            "description": "早餐描述 - 应该被识别为relevant"
        },
        {
            "input": "什么是健康饮食？",
            "expected_type": "unrelevant",
            "description": "健康知识咨询 - 应该被识别为unrelevant"
        },
        {
            "input": "晚上吃了炒菜和米饭",
            "expected_type": "relevant",
            "description": "晚餐描述 - 应该被识别为relevant"
        }
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 测试用例 {i}/{total_count}")
        print(f"输入: {test_case['input']}")
        print(f"期望: {test_case['expected_type']}")
        print(f"描述: {test_case['description']}")
        
        try:
            # 调用检测函数
            result = service.detect_health_behavior(test_case['input'])
            
            print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 验证结果
            actual_type = result.get('type')
            if actual_type == test_case['expected_type']:
                print("✅ 测试通过")
                success_count += 1
            else:
                print(f"❌ 测试失败: 期望 {test_case['expected_type']}, 实际 {actual_type}")
            
            # 如果是relevant类型，验证营养数据
            if actual_type == 'relevant':
                nutrition_data = result.get('nutrition_data')
                if nutrition_data:
                    print("🍎 营养数据:")
                    print(f"   食物: {nutrition_data.get('food_name', 'N/A')}")
                    print(f"   热量: {nutrition_data.get('calories', 'N/A')} kcal")
                    print(f"   餐次: {nutrition_data.get('meal_type', 'N/A')}")
                else:
                    print("⚠️ 警告: relevant类型但缺少营养数据")
                    
        except Exception as e:
            print(f"❌ 测试执行失败: {e}")
        
        print("-" * 30)
    
    print(f"\n📊 测试总结:")
    print(f"总计: {total_count} 个测试用例")
    print(f"成功: {success_count} 个")
    print(f"失败: {total_count - success_count} 个")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 存在测试失败，请检查模型配置和提示词")

def test_meal_type_detection():
    """测试餐次类型识别"""
    print("\n🕐 测试餐次类型识别...")
    
    service = HealthBehaviorService()
    current_hint = service._get_current_meal_type_hint()
    print(f"当前时间建议餐次: {current_hint}")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_health_detection())
    test_meal_type_detection()