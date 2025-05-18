import React, { useState } from "react";
import { useNavigate } from "react-router-dom";  // Import useNavigate
import axios from "axios";

const Login = ({ onLogin }) => {  // Bỏ onToggleToRegister khỏi props
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();  // Khởi tạo navigate

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://localhost:5000/api/auth/login", {
        email,
        password,
      });

      if (response.data.success) {
        localStorage.setItem("userEmail", email);
        onLogin(response.data.user);
      } else {
        alert("Đăng nhập thất bại!");
      }
    } catch (error) {
      console.error("Lỗi kết nối API:", error);
      alert("Đăng nhập thất bại! Đã xảy ra lỗi.");
    }
  };

  const handleToggleToRegister = () => {
    navigate("/register");  // Điều hướng sang trang đăng ký
  };

  return (
    <div className="container">
      <h2>Đăng Nhập</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Mật khẩu"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Đăng Nhập</button>


        <button type="button" className="toggle-btn" onClick={handleToggleToRegister}>
          Đăng Ký
        </button>
      </form>
    </div>
  );
};

export default Login;
