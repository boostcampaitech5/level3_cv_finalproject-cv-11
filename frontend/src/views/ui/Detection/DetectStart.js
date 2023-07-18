import React, { useState } from "react";
import { Alert, Card, CardBody, Button } from "reactstrap";
import "./DetectStart.css";
import Footer from "../../../layouts/Footer";
import Image from "../../../assets/images/snow2.JPG";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from "../../../lib/api";

const DetectStart = () => {
  const [selectedImages, setSelectedImages] = useState(null);
  const [selectedTargetImage, setSelectedTargetImage] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state.username
  const password = location.state.password

  // 메인 페이지로 이동
  const handleBackDetect = () => {
    navigate("/detect");
  };

  // 이미지 파일들을 선택하여 userState 객체로 변환
  const handleFolderUpload = (event) => {
    const files = Array.from(event.target.files);
    const imageFiles = files.filter((file) => file.type.startsWith('image/'));

    if (event.target.id === "real-images-input") {
      setSelectedImages(imageFiles);
    } else if (event.target.id === "target-image-input") {
      setSelectedTargetImage(imageFiles);
    }
  };

  // 이미지 파일들을 서버로 전송 후 모델 학습 페이지로 이동
  const handleFolderSubmit = async (username, project_name) => {
    const formData = new FormData();
    selectedImages.forEach((image, index) => {
      formData.append('real_file', image, `${index}`); //0 ~14
    });
    selectedTargetImage.forEach((image, index) => {
      formData.append('target_file', image, 'target_file'); //0 ~14
    });

    //("/generate/{username}/{project_name}/upload"
    const url = `/detect/${username}/${project_name}/upload`;
    // const params = formData;
    await fastapi("formdata", url, formData);
    try {
      navigate('/detect/loading', { state: { username: username, password: password, project_name: project_name } });
    } catch (error) {
      console.log(error);
    }
  };

  // 탐지하기 -> 탐지프로젝트 생성 -> return project_name
  const handleDetectStart = async (username) => {
    await fastapi(
      "post",
      `/detect/${username}/start`,
      {},
      (response) => {
        const { project_name } = response;
        handleFolderSubmit(username, project_name);
      },
      (error) => {
        console.log(error);
      }
    );
  };

  // 이미지 폴더 선택 창 띄우기
  const handleClickFolderUploadButton = (event) => {
    const folderInputId = event.target.getAttribute("data-files-input");
    const folderInput = document.getElementById(folderInputId);
    if (folderInput) {
      folderInput.click();
    }
    event.preventDefault();
  };

  // 전송 버튼 클릭
  const handleUploadButtonClick = () => {
    handleDetectStart(username);
  };

  return (
    <div>
      <div className="generate-start-container">
        <h1>AI Deepfake Detection</h1>
        <h2>탐지하기</h2>
        <p>당신의 이미지가 딥페이크를 통해 악용되고 있는지 확인해보세요!</p>
        <div className="generate-back-btns">
          <Button
            className="btns"
            color="secondary"
            size="lg"
            onClick={handleBackDetect}
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
                    onClick={handleClickFolderUploadButton}
                    data-files-input="real-images-input"
                  >
                    이미지 폴더 업로드
                  </Button>
                  <input
                    id="real-images-input"
                    type="file"
                    multiple
                    accept="image/jpg, image/jpeg, image/png"
                    onChange={handleFolderUpload}
                    style={{ display: "none" }}
                  />
                  <Button
                    className="btns2"
                    color="primary"
                    size="lg"
                    onClick={handleClickFolderUploadButton}
                    data-files-input="target-image-input"
                  >
                    target 이미지
                  </Button>
                  <input
                    id="target-image-input"
                    type="file"
                    accept="image/jpg, image/jpeg, image/png"
                    onChange={handleFolderUpload}
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

export default DetectStart;
