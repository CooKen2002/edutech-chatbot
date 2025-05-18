// src/components/Register.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = ({ onRegister }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate(); // Hook điều hướng

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Kiểm tra mật khẩu xác nhận
    if (password !== confirmPassword) {
      alert("Mật khẩu không khớp!");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (data.success) {
        // Lưu userEmail vào localStorage sau khi đăng ký thành công
        localStorage.setItem("userEmail", email);
        console.log("UserEmail lưu vào localStorage:", email);

        onRegister(data.user);
        navigate("/profile"); // Chuyển đến trang profile ngay sau khi đăng ký thành công
      } else {
        alert("Đăng ký thất bại!");
      }
    } catch (error) {
      console.error("Lỗi kết nối API:", error);
      alert("Đăng ký thất bại! Đã xảy ra lỗi.");
    }
  };

  const handleToggleToLogin = () => {
    navigate("/login"); // Chuyển hướng đến trang Login
  };

  return (
    <div className="container">
      <h2>Đăng Ký</h2>
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
        <input
          type="password"
          placeholder="Xác nhận mật khẩu"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
        <button type="submit">Đăng Ký</button>
        
        {/* Chuyển sang trang đăng nhập */}
        <button type="button" className="toggle-btn" onClick={handleToggleToLogin}>
          Quay lại Đăng Nhập
        </button>
      </form>
    </div>
  );
};

export default Register;
