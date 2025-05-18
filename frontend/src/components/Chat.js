// src/components/Chat.js
import React, { useState } from 'react';
import axios from 'axios';

const Chat = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    // Thêm tin nhắn người dùng vào lịch sử và gửi
    setChatHistory(prev => [...prev, { sender: 'user', text: message }]);

    try {
      const response = await axios.post('http://localhost:5000/api/auth/chat', { message });

      setChatHistory(prev => [
        ...prev,
        { sender: 'bot', text: response.data.response }
      ]);
      setMessage('');
    } catch (error) {
      console.error('Error while sending message:', error);
    }
  };
  
  return (
    <div className="chat-container">
      <div className="chat-box">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={message}
          onChange={e => setMessage(e.target.value)}
          placeholder="Type a message..."
          onKeyDown={e => {
            if (e.key === 'Enter') sendMessage();
          }}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
