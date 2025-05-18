// src/App.js
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Chatbot from "./components/Chatbot";
import UserProfile from "./components/UserProfile";
import EditProfile from "./components/EditProfile";
import CourseDetail from "./components/CourseDetail";

const App = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
  };

  const handleRegister = (userData) => {
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  const handleUserUpdate = (updatedUser) => {
    setUser(updatedUser);
    localStorage.setItem("user", JSON.stringify(updatedUser));
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={user ? <Navigate to="/" replace /> : <Login onLogin={handleLogin} />}/>
          <Route path="/register" element={user ? <Navigate to="/" replace /> : <Register onRegister={handleRegister} />}/>
          <Route path="/" element={user ? <Chatbot user={user} onLogout={handleLogout} /> : <Navigate to="/login" replace />}/>
          <Route path="/profile" element={user ? <UserProfile user={user} onUserUpdate={handleUserUpdate} /> : <Navigate to="/login" replace />}/>
          <Route path="/profile/edit" element={<EditProfile />} />
          <Route path="/course/:courseId" element={<CourseDetail />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
