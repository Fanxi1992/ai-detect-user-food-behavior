import React from 'react';
import { NutritionData } from '../store/chatStore';
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
    const labels = {
      breakfast: '早餐',
      lunch: '午餐', 
      dinner: '晚餐',
      snack: '零食'
    };
    return labels[mealType as keyof typeof labels] || '餐点';
  };

  const getMealIcon = (mealType: string) => {
    const icons = {
      breakfast: '🌅',
      lunch: '🌞',
      dinner: '🌙',
      snack: '🍪'
    };
    return icons[mealType as keyof typeof icons] || '🍽️';
  };

  return (
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
  );
};

export default NutritionCard;