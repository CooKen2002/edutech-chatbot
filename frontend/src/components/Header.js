// src/components/Header.js
import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Header({ user, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    if (onLogout) onLogout();
    navigate("/login");
  };

  return (
    <header className="app-header">
      <div className="header-container">
        <Link to="/" className="logo">
          EdTechChat
        </Link>
        <nav className="nav-links">
          <Link to="/">Trang chủ</Link>
          <Link to="/profile">Trang cá nhân</Link>
          <Link to="/courses">Khóa học</Link>
        </nav>
        <div className="user-actions">
          {user ? (
            <>
              <span className="user-name">Xin chào, {user.name || user.email}</span>
              <button className="logout-btn" onClick={handleLogout}>
                Đăng xuất
              </button>
            </>
          ) : (
            <Link to="/login" className="login-link">Đăng nhập</Link>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;
