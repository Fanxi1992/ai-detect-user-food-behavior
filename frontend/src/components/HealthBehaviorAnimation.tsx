import React from 'react';
import '../styles/health-behavior-animation.css';

interface HealthBehaviorAnimationProps {
  onComplete?: () => void;
}

const HealthBehaviorAnimation: React.FC<HealthBehaviorAnimationProps> = ({ onComplete }) => {
  // 3秒后触发完成回调
  React.useEffect(() => {
    const timer = setTimeout(() => {
      onComplete?.();
    }, 3000);

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div className="health-behavior-animation">
      <div className="animation-container">
        <div className="detection-icon">
          <div className="pulse-ring"></div>
          <div className="pulse-ring pulse-ring-delay-1"></div>
          <div className="pulse-ring pulse-ring-delay-2"></div>
          <div className="center-icon">
            🍎
          </div>
        </div>
        <div className="detection-text">
          <h3>检测到您的健康行为</h3>
          <p>正在为您进行打卡统计...</p>
          <div className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HealthBehaviorAnimation;