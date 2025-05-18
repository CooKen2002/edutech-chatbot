// src/components/UserProfile.js
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./UserProfile.css";

function UserProfile({ onEditClick, onLogout }) {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [courses, setCourses] = useState([]);
  const [loadingUser, setLoadingUser] = useState(true);
  const [loadingCourses, setLoadingCourses] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const userEmail = localStorage.getItem("userEmail");
    if (!userEmail || typeof userEmail !== "string" || userEmail.trim() === "") {
      setError("Bạn chưa đăng nhập. Vui lòng đăng nhập lại.");
      setLoadingUser(false);
      setLoadingCourses(false);
      setTimeout(() => navigate("/login"), 2000);
      return;
    }

    setError("");
    fetchUserInfo(userEmail);
    fetchUserCourses(userEmail);
  }, [navigate]);

  // Lấy thông tin user
  const fetchUserInfo = (email) => {
    setLoadingUser(true);
    fetch(`http://localhost:5000/api/user/user-info?email=${encodeURIComponent(email)}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Lỗi HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (data.success) {
          setUser(data.data);
        } else {
          setError(data.message || "Không lấy được thông tin người dùng");
          setUser(null);
        }
      })
      .catch((err) => {
        setError("Lỗi kết nối lấy thông tin người dùng");
        setUser(null);
        console.error("Fetch user info error:", err);
      })
      .finally(() => setLoadingUser(false));
  };

  // Lấy danh sách khóa học + tiến độ user
  const fetchUserCourses = (email) => {
    setLoadingCourses(true);
    fetch(`http://localhost:5000/api/user/user-progress?email=${encodeURIComponent(email)}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Lỗi HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (data.success) {
          setCourses(data.data || []);
        } else {
          setCourses([]);
        }
      })
      .catch((err) => {
        setCourses([]);
        console.error("Fetch user courses error:", err);
      })
      .finally(() => setLoadingCourses(false));
  };

  // Đăng xuất
  const handleLogout = () => {
    if (onLogout) onLogout();
    localStorage.removeItem("userEmail");
    navigate("/login");
  };

  // Tìm tiến độ khóa học đã chọn (nếu có)
  const selectedCourseProgress =
    user && user.selected_course
      ? courses.find((c) => c.name === user.selected_course)
      : null;

  if (loadingUser) return <p>Đang tải thông tin người dùng...</p>;

  if (error) return <p style={{ color: "red" }}>{error}</p>;

  if (!user) return <p>Không có dữ liệu người dùng.</p>;

  return (
    <div className="userprofile-wrapper">
      {/* Header */}
      <div className="header">
        <div className="homepage">
          <button onClick={() => navigate("/")}>Edutech Chatbot</button>
        </div>
        <div className="user-section">
          <div className="user-avatar">
            <img
              src={
                user.avatar ||
                "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp"
              }
              alt="Avatar"
              onClick={() => navigate("/profile")}
              style={{ cursor: "pointer" }}
            />
          </div>
          <button className="logout-button" onClick={handleLogout}>
            Đăng Xuất
          </button>
        </div>
      </div>

      {/* Nội dung chính */}
      <div className="profile-container">
        {/* Sidebar */}
        <aside className="profile-sidebar">
          <div className="profile-card">
            <div className="avatar-wrapper">
              <img
                src={
                  user.avatar ||
                  "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp"
                }
                alt="Avatar"
                className="avatar"
              />
            </div>
            <div className="info-row">
              <strong>Email:</strong> {user.email}
            </div>
            <div className="info-row">
              <strong>Sở thích:</strong> {user.hobby || "-"}
            </div>
            <div className="info-row">
              <strong>Môn học yêu thích:</strong> {user.subj || "-"}
            </div>
            <div className="info-row">
              <strong>Sở thích khác:</strong>{" "}
              {user.interests?.length > 0 ? user.interests.join(", ") : "-"}
            </div>
            <button
              className="edit-button"
              onClick={() => navigate("/profile/edit")}
            >
              Chỉnh sửa thông tin
            </button>
          </div>
        </aside>

        {/* Main content */}
        <main className="profile-main">
          {/* Khóa học đã chọn */}
          <h2>Khóa học đã chọn</h2>
          {user.selected_course ? (
            <div className="selected-course">
              <p>
                <strong>{user.selected_course}</strong>
              </p>
              <p>
                Tiến độ:{" "}
                {selectedCourseProgress
                  ? `${selectedCourseProgress.progress}%`
                  : "Chưa có tiến độ"}
              </p>
            </div>
          ) : (
            <p></p>
          )}

          {/* Danh sách khóa học */}
          {loadingCourses ? (
            <p>Đang tải khóa học...</p>
          ) : courses.length > 0 ? (
            <table className="course-table">
              <thead>
                <tr>
                  <th>Tên khóa học</th>
                  <th>Trạng thái</th>
                  <th>Tiến độ</th>
                </tr>
              </thead>
              <tbody>
                {courses.map((course) => (
                  <tr
                    key={course._id || course.name}
                    style={{ cursor: "pointer" }}
                    onClick={() => {
                      if (!course._id) {
                        const courseId = course._id || course.id;
                        if (!courseId) {
                          console.error("Course ID không tồn tại:", course);
                          return;
                        }
                       }
                      navigate(`/course/${course.id}`);
                    }}


                  >
                    <td>{course.name}</td>
                    <td>{course.status}</td>
                    <td>{course.progress}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Bạn chưa đăng ký khóa học nào.</p>
          )}
        </main>
      </div>
    </div>
  );
}

export default UserProfile;
