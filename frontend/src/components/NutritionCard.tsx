import React from 'react';
import { type NutritionData } from '../store/chatStore';
import Avatar from './Avatar';
import '../styles/nutrition-card.css';

interface NutritionCardProps {
  nutritionData: NutritionData;
  onEdit?: () => void;
  onDelete?: () => void;
}

const NutritionCard: React.FC<NutritionCardProps> = ({ 
  nutritionData, 
  onEdit, 
  onDelete 
}) => {
  const getMealTypeLabel = (mealType: string) => {
    // 新的餐次类型映射，支持中文枚举值
    const labels: { [key: string]: string } = {
      '早餐': '早餐',
      '上午加餐': '上午加餐',
      '午餐': '午餐',
      '下午加餐': '下午加餐',
      '晚餐': '晚餐',
      '夜宵': '夜宵',
      // 保持向后兼容英文值
      'breakfast': '早餐',
      'lunch': '午餐', 
      'dinner': '晚餐',
      'snack': '零食'
    };
    return labels[mealType] || '餐点';
  };

  const getMealIcon = (mealType: string) => {
    // 新的餐次类型图标映射
    const icons: { [key: string]: string } = {
      '早餐': '🌅',
      '上午加餐': '☕',
      '午餐': '🌞',
      '下午加餐': '🍎',
      '晚餐': '🌙',
      '夜宵': '🌃',
      // 保持向后兼容英文值
      'breakfast': '🌅',
      'lunch': '🌞',
      'dinner': '🌙',
      'snack': '🍪'
    };
    return icons[mealType] || '🍽️';
  };

  return (
    <div className="nutrition-card-wrapper">
      <Avatar type="health" size="medium" />
      <div className="nutrition-card">
        <div className="nutrition-header">
          <div className="meal-info">
            <span className="meal-icon">{getMealIcon(nutritionData.meal_type)}</span>
            <span className="meal-type">{getMealTypeLabel(nutritionData.meal_type)}+1</span>
          </div>
        </div>
      
      <div className="food-section">
        <div className="food-item">
          <span className="food-icon">🥤</span>
          <span className="food-name">1杯{nutritionData.food_name}</span>
        </div>
        
        <div className="calories-section">
          <span className="calories-icon">🔥</span>
          <span className="calories-value">{nutritionData.calories} kcal</span>
        </div>
      </div>

      <div className="nutrition-details">
        <div className="nutrition-item">
          <span className="nutrition-icon">🌾</span>
          <span className="nutrition-value">{nutritionData.carbs}g</span>
        </div>
        <div className="nutrition-divider"></div>
        <div className="nutrition-item">
          <span className="nutrition-icon">🥩</span>
          <span className="nutrition-value">{nutritionData.protein}g</span>
        </div>
        <div className="nutrition-divider"></div>
        <div className="nutrition-item">
          <span className="nutrition-icon">🥑</span>
          <span className="nutrition-value">{nutritionData.fat}g</span>
        </div>
      </div>

      <div className="card-actions">
        <button 
          className="action-button delete-button"
          onClick={onDelete}
        >
          删除记录
        </button>
        <button 
          className="action-button edit-button"
          onClick={onEdit}
        >
          修改记录
        </button>
      </div>
      </div>
    </div>
  );
};

export default NutritionCard;