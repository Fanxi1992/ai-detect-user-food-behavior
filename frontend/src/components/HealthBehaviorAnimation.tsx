import React, { useState, useEffect } from 'react';
import '../styles/health-behavior-animation.css';

interface HealthBehaviorAnimationProps {
  onComplete?: () => void;
}

const HealthBehaviorAnimation: React.FC<HealthBehaviorAnimationProps> = ({ onComplete }) => {
  const [currentPhase, setCurrentPhase] = useState(0);
  const [dots, setDots] = useState('');

  // 3个阶段的文本
  const phases = [
    '正在理解问题',
    '正在解析行为', 
    '正在生成结果'
  ];

  // 管理阶段切换
  useEffect(() => {
    const phaseTimer = setInterval(() => {
      setCurrentPhase(prev => {
        if (prev < 2) {
          return prev + 1;
        }
        return prev; // 停留在第3阶段直到外部完成
      });
    }, 1500);

    return () => clearInterval(phaseTimer);
  }, []);

  // 管理点点点动画
  useEffect(() => {
    const dotTimer = setInterval(() => {
      setDots(prev => {
        if (prev === '...') return '';
        return prev + '.';
      });
    }, 500);

    return () => clearInterval(dotTimer);
  }, []);

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
          <h3>
            {phases[currentPhase]}
            <span className="dynamic-dots">{dots}</span>
          </h3>
        </div>
      </div>
    </div>
  );
};

export default HealthBehaviorAnimation;