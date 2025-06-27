import React from 'react';
import '../styles/health-behavior-animation.css';

interface HealthBehaviorAnimationProps {
  onComplete?: () => void;
}

const HealthBehaviorAnimation: React.FC<HealthBehaviorAnimationProps> = ({ onComplete }) => {
  // 移除自动触发逻辑，现在等待真实的LLM响应
  // onComplete现在由父组件在收到health_behavior响应时调用

  return (
    <div className="health-behavior-animation">
      <div className="animation-container">
        <div className="detection-icon">
          <div className="pulse-ring"></div>
          <div className="pulse-ring pulse-ring-delay-1"></div>
          <div className="pulse-ring pulse-ring-delay-2"></div>
          <div className="center-icon">
            🤔
          </div>
        </div>
        <div className="detection-text">
          <h3>正在思考中...</h3>
        </div>
        <div className="loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  );
};

export default HealthBehaviorAnimation;