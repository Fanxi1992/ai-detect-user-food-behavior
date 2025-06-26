import React from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

interface StreamingMessageProps {
  content: string;
}

const StreamingMessage: React.FC<StreamingMessageProps> = ({ content }) => {
  if (!content) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="message-bubble ai-message streaming"
    >
      <div className="message-content">
        <ReactMarkdown>{content}</ReactMarkdown>
        <span className="cursor-blink">|</span>
      </div>
    </motion.div>
  );
};

export default StreamingMessage;