// src/components/Chatbot.js - React Component for Chatbot
import React, { useState } from "react";
import axios from "axios";
import "./Chatbot.css";
import { useNavigate } from "react-router-dom";

function Chatbot({ user, onLogout }) {
  const [messages, setMessages] = useState([
    { text: "Chào bạn! Tôi là chatbot của bạn. Bạn cần giúp gì không?", sender: "bot" }
  ]);
  const [userMessage, setUserMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSendMessage = async () => {
    if (!userMessage.trim()) return;

    const newMessage = { text: userMessage, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setUserMessage("");
    setLoading(true);

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/api/chat/`,
        { message: userMessage, email: user?.email || "unknown@example.com" },
        { headers: { "Content-Type": "application/json" } }
      );

      const botMessage = { text: response.data.response || "Không nhận được phản hồi hợp lệ từ bot.", sender: "bot" };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [...prevMessages, { text: "Đã xảy ra lỗi khi gửi tin nhắn. Vui lòng thử lại.", sender: "bot" }]);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    if (onLogout) onLogout();
    navigate("/login");
  };

  return (
    <div className="chatbot-wrapper">
      <div className="header">
        <div className="homepage"><button onClick={() => navigate("/")}>Edutech Chatbot</button></div>
        <div className="user-section">
          <div className="user-avatar">
            <img 
              src="https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp" 
              alt="Avatar" 
              onClick={() => navigate("/profile")}
            />
          </div>
          <button className="logout-button" onClick={handleLogout}>Đăng Xuất</button>
        </div>
      </div>

      <div className="main-content">
        <div className="learning-list"><h3>Tên khóa học</h3><ul><li>HTML - 80%</li><li>CSS - 60%</li><li>JavaScript - 40%</li></ul></div>

        <div className="chatbot-container">
          <div className="chat-area">
            {messages.map((message, index) => <div key={index} className={`message ${message.sender}`}><span>{message.text}</span></div>)}
            {loading && <div className="message bot"><span>Đang tải...</span></div>}
          </div>

          <div className="input-area">
            <input type="text" placeholder="Nhập tin nhắn..." value={userMessage} onChange={(e) => setUserMessage(e.target.value)} onKeyDown={(e) => e.key === "Enter" && handleSendMessage()} />
            <button onClick={handleSendMessage}>📤</button>
          </div>
        </div>

        <div className="notification"><h3>Thông báo</h3><ul><li>Bạn đã hoàn thành 80% khóa học HTML.</li><li>Có bài kiểm tra mới cho khóa JavaScript.</li></ul></div>
      </div>
    </div>
  );
}

export default Chatbot;
