// src/components/ChatInput.js
import React from 'react';

function ChatInput({ userMessage, setUserMessage, handleSendMessage }) {
  return (
    <div className="input-area">
      <input
        type="text"
        value={userMessage}
        onChange={(e) => setUserMessage(e.target.value)}
        placeholder="Nhập tin nhắn..."
      />
      <button onClick={handleSendMessage}>Gửi</button>
    </div>
  );
}

export default ChatInput;
