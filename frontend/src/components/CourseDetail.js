// src/components/CourseDetail.js
import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

function CourseDetail() {
  const { courseId } = useParams();
  const navigate = useNavigate();

  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!courseId) {
      setError("Không có ID khóa học.");
      setLoading(false);
      return;
    }

    async function fetchCourse() {
      setLoading(true);
      try {
        const resCourse = await fetch(
          `http://localhost:5000/api/course/detail/${courseId}`
        );

        if (!resCourse.ok) throw new Error("Không tìm thấy khóa học");

        const courseData = await resCourse.json();

        if (!courseData.success) {
          throw new Error(courseData.message || "Lỗi khi lấy dữ liệu khóa học");
        }

        setCourse(courseData.data);
      } catch (err) {
        setError(err.message || "Lỗi khi lấy dữ liệu");
        setCourse(null);
      } finally {
        setLoading(false);
      }
    }

    fetchCourse();
  }, [courseId]);

  const handleBackToProfile = () => {
    navigate("/profile");
  };

  if (loading) return <p>Đang tải dữ liệu khóa học...</p>;
  if (error)
    return (
      <div>
        <p style={{ color: "red" }}>{error}</p>
        <button onClick={handleBackToProfile}>Quay lại trang cá nhân</button>
      </div>
    );

  if (!course)
    return (
      <div>
        <p>Không tìm thấy khóa học.</p>
        <button onClick={handleBackToProfile}>Quay lại trang cá nhân</button>
      </div>
    );

  return (
    <div className="course-detail">
      <h2>{course.name}</h2>
      <p>
        <strong>Mô tả:</strong> {course.description || "Chưa có mô tả"}
      </p>
      <p>
        <strong>Danh mục:</strong> {course.category || "-"}
      </p>
      <p>
        <strong>Độ khó:</strong> {course.difficulty || "-"}
      </p>
      <p>
        <strong>Thời lượng:</strong> {course.duration || "-"}
      </p>
      <p>
        <strong>Hình thức:</strong> {course.format || "-"}
      </p>
      <p>
        <strong>Nhà cung cấp:</strong> {course.provider || "-"}
      </p>
      <button onClick={handleBackToProfile}>Quay lại trang cá nhân</button>
    </div>
  );
}

export default CourseDetail;
