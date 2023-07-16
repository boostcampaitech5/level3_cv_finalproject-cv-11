import React, { useState } from "react";
import { Card, CardBody, Button } from "reactstrap";
import "./GenerateStart.css";
import Footer from "../../layouts/Footer";
import Image from "../../assets/images/snow2.JPG";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from "../../lib/api";
import qs from "qs";

const GenerateStart = () => {
  const [visible, setVisible] = useState(true);
  const [error, setError] = useState({ detail: [] });

  const [selectedSourceImage, setSelectedSourceImage] = useState(null);
  const [selectedTargetImage, setSelectedTargetImage] = useState(null);
  const navigate = useNavigate();
  const username = 'test';

  // 메인 페이지로 이동
  const handleBackGenerate = () => {
    navigate("/generate");
  };

  // 소스, 타겟 이미지 -> selectedImage로 변환
  const handleImageUpload = (event) => {
    const files = Array.from(event.target.files);
    const image = files[0];

    if (event.target.id === "source-image-input") {
      setSelectedSourceImage(URL.createObjectURL(image));
    } else if (event.target.id === "target-image-input") {
      setSelectedTargetImage(URL.createObjectURL(image));
    }
  };

  // 이미지 서버로 전송 후 모델 학습 페이지로 이동
  const handleImageSubmit = async (username, project_name) => {
    const formData = new FormData();
    formData.append("source", selectedSourceImage);
    formData.append("target", selectedTargetImage);

    //("/generate/{username}/{project_name}/upload"
    const url = `/generate/${username}/${project_name}/upload`;
    const params = formData;
    await fastapi("post", url, params);
    try {
      navigate(`/generate/loading`);
    } catch (error) {
      console.log(error);
    }
  };

  // 생성하기 -> 생성프로젝트 생성
  const handleGenerateStart = async (username) => {
    await fastapi(
      "post",
      `/generate/${username}/start`,
      {},
      (response) => {
        const { project_name } = response;
        handleImageSubmit(username, project_name);
      },
      (error) => {
        console.log(error);
      }
    );
  };

  const handleClickUploadButton = (event) => {
    const fileInputId = event.target.getAttribute("data-file-input");
    const fileInput = document.getElementById(fileInputId);
    if (fileInput) {
      fileInput.click();
    }
    event.preventDefault();
  };

  const handleUploadButtonClick = () => {
    handleGenerateStart(username);
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
                    data-file-input="source-image-input"
                  >
                    source 업로드 - 대상이미지
                  </Button>
                  <input
                    id="source-image-input"
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    style={{ display: "none" }}
                  />

                  <Button
                    className="btns2"
                    color="primary"
                    size="lg"
                    onClick={handleClickUploadButton}
                    data-file-input="target-image-input"
                  >
                    target 업로드 - 배경이미지
                  </Button>
                  <input
                    id="target-image-input"
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
