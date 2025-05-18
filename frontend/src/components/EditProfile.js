import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./EditProfile.css";

function EditProfile() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    hobby: "",
    subj: "",
    interests: ""
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  useEffect(() => {
    const userEmail = localStorage.getItem("userEmail");
    if (!userEmail) {
      navigate("/login");
      return;
    }

    fetch(`http://localhost:5000/api/user/user-info?email=${encodeURIComponent(userEmail)}`)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const user = data.data;
          setFormData({
            email: user.email || userEmail,
            hobby: user.hobby || "",
            subj: user.subj || "",
            interests: user.interests ? user.interests.join(", ") : ""
          });
        } else {
          setError(data.message || "Không thể tải thông tin.");
        }
      })
      .catch(() => setError("Lỗi kết nối API"))
      .finally(() => setLoading(false));
  }, [navigate]);

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError("");

    // Prepare payload
    const payload = {
      email: formData.email,
      preferences: {
        hobby: formData.hobby,
        subj: formData.subj,
        interests: formData.interests.split(",").map(i => i.trim()).filter(Boolean),
      }
    };

    try {
      const res = await fetch("http://localhost:5000/api/user/update-profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        navigate("/profile");
      } else {
        setError(data.message || "Cập nhật thất bại");
      }
    } catch {
      setError("Lỗi kết nối API");
    }
  };

  if (loading) return <p>Đang tải...</p>;
  
  return (
    <div className="edit-profile-wrapper">
      <h2>Chỉnh sửa thông tin cá nhân</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit} className="edit-profile-form">
        <div className="form-group">
          <label>Email:</label>
          <input type="email" name="email" value={formData.email} disabled />
        </div>
        <div className="form-group">
          <label>Sở thích:</label>
          <input type="text" name="hobby" value={formData.hobby} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Môn học yêu thích:</label>
          <input type="text" name="subj" value={formData.subj} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Sở thích khác:</label>
          <input type="text" name="interests" value={formData.interests} onChange={handleChange} placeholder="Ngăn cách bởi dấu phẩy" />
        </div>
        <div className="button-group">
          <button type="submit" className="save-btn">Lưu</button>
          <button type="button" className="cancel-btn" onClick={() => navigate("/profile")}>Hủy</button>
        </div>
      </form>
    </div>
  );
}

export default EditProfile;
