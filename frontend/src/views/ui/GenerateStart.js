import React, { useState } from "react";
import { Card, CardBody, Button } from "reactstrap";
import "./GenerateStart.css";
import Footer from "../../layouts/Footer";
import Image from "../../assets/images/snow2.JPG";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const GenerateStart = () => {
  const [visible, setVisible] = useState(true);
  const [selectedImage, setSelectedImage] = useState([]); // Change variable name to `selectedImage`
  const navigate = useNavigate();

  // 메인 페이지로 이동
  const handleBackGenerate = async () => {
    navigate("/generate");
  };

  // 소스, 타겟 이미지 업로드
  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files); // 업로드된 파일들 가져오기
    const images = files.map((file) => URL.createObjectURL(file)); // 선택된 이미지들 업데이트
    setSelectedImage(images); // Change variable name to `selectedImage`
  };

  // 전송하기 버튼 : 프로젝트 생성, 이미지 input
  const handleClickUploadButton = () => {
    const fileInput = document.getElementById("image-input");
    fileInput.click();
  };

  // 생성하기 -> 생성프로젝트 생성
  const handleGenerateStart = async () => {
    try {
      const response = await axios.post("/generate/start"); // fastapi - 생성프로젝트생성
      const username = response.data.username;
      const project_name = response.data.project_name;
      navigate(`/generate/${project_name}/upload`, {
        state: { username, project_name },
      }); // 생성하기-이미지 업로드 페이지로 이동
    } catch (error) {
      console.log(error);
    }
  };

  // 서버로 이미지 전송
  const handleSendImages = async () => {
    try {
      const formData = new FormData();
      selectedImage.forEach((image, index) => {
        formData.append(`image${index}`, image);
      });

      const { state } = navigate(); // 현재 경로의 상태 가져오기
      const { username, project_name } = state; // state에서 username과 project_name 가져오기

      await axios.post(`/generate/${project_name}/upload`, formData); // project_name 변수 적용
      navigate(`/generate/${project_name}/loading`); // 모델 학습 페이지로 이동
    } catch (error) {
      console.log(error);
    }
  };

  const handleUploadButtonClick = () => {
    handleGenerateStart(); // 프로젝트 생성을 위해 handleGenerateStart 호출
    handleSendImages(); // 이미지를 서버로 전송하기 위해 handleSendImages 호출
  };

  return (
    <div>
      <div className="generate-start-container">
        <h1>AI Deepfake Detection</h1>
        <h2>생성하기</h2>
        <p>딥페이크를 통해서 타인과 '나'의 얼굴을 바꿔보세요</p>
        <div className="generate-back-btns">
          <Button
            className="btns"
            color="secondary"
            size="lg"
            onClick={handleBackGenerate}
          >
            이전으로
          </Button>
        </div>
      </div>
      <Card>
        <CardBody className="">
          <div className="mt-3">
            <h3>생성하기</h3>
            <div className="box-container2">
              <div className="box2">
                <img src={Image} alt="이미지 유의사항" />
                <div>
                  <Button
                    className="btns2"
                    color="primary"
                    size="lg"
                    onClick={handleClickUploadButton}
                  >
                    source 업로드 - 대상이미지
                  </Button>
                  <input
                    id="image-input"
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    style={{ display: "none" }}
                  />
                </div>
                <div>
                  <Button
                    className="btns2"
                    color="primary"
                    size="lg"
                    onClick={handleClickUploadButton}
                  >
                    target 업로드 - 배경이미지
                  </Button>
                  <input
                    id="image-input"
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    style={{ display: "none" }}
                  />
                </div>
                <Button
                  className="btns2"
                  color="success"
                  size="lg"
                  onClick={handleUploadButtonClick}
                >
                  전송하기
                </Button>
              </div>
            </div>
          </div>
        </CardBody>
        <Footer />
      </Card>
    </div>
  );
};

export default GenerateStart;

