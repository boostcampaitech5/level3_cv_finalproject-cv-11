import React, { useState, useEffect } from "react";
import { Row, Col, Card, CardBody, Button } from "reactstrap";
import "./GenerateProject.css";
import Footer from "../../../layouts/Footer";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from '../../../lib/api';
import Arrow from '../../../assets/images/arrow.png'

const GenerateProject = () => {
  const [imageUrls, setImageUrls] = useState({});
  const navigate = useNavigate();
  const location = useLocation();
  const user_id = location.state.user_id;
  const username = location.state.username;
  const project_id = location.state.project_id;
  const project_name = location.state.project_name;
  const password = location.state.password;


  // 이전으로
  const handleBackGenerateList = () => {
    navigate(`/generate/projects`, { state: { user_id: user_id, username: username, password: password } });
  };
  const handleBackMain = () => {
    navigate(`/deepfake`, { state: { user_id: user_id, username: username, password: password } });
  };
  const handleSurvey = () => {
    navigate(`/survey`, { state: { user_id: user_id, username: username, password: password, project_id: project_id, project_name: project_name } });
  };

  useEffect(() => {
    fetchImageUrls();
  }, []);

  const handleImageClick = (imageUrl) => {
    window.open(imageUrl, "_blank");
  };

  const fetchImageUrls = async () => {
    try {
      fastapi(
        "get",
        `/generate/${username}/${project_name}`,
        {},
        (response) => {
          setImageUrls(response);
          if (!response.complete) {
            navigate('/generate/loading', { state: { user_id: user_id, username: username, password: password, project_id: project_id, project_name: project_name } });
          }
        },
        (error) => {
          console.log(error);
        }
      );
    } catch (error) {
      console.log(error);
    }
  };

  const handleDownloadOutput = async () => {
    if (imageUrls.output) {
      try {
        const response = await fetch(imageUrls.output);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "output.jpeg");
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.log(error);
      }
    }
  };

  return (
    <>
      <div className="generate-project-container">
        <div className="generate-container">
          <h1>AI Deepfake Detection</h1>
          <p>1. 딥페이크를 통해서 타인과 '나'의 얼굴을 바꿔보세요</p>
          <div className='generate-btns'>
            <Button className='btns' color="secondary" size="lg" onClick={handleBackGenerateList}>
              목록으로
            </Button>
            <Button className='btns' color="secondary" size="lg" onClick={handleBackMain}>
              메인으로
            </Button>
          </div>
        </div>

        <h3>폴더 이름: {project_name}</h3>
        <Row>
          <Col xs="12" md="6">
            <div className="image-container">
              <h3>배경이미지</h3>
              {imageUrls.source && (
                <div className="image-wrapper">
                  <img
                    src={imageUrls.source}
                    alt="Source"
                    className="image"
                    onClick={() => handleImageClick(imageUrls.source)}
                  />
                </div>
              )}
            </div>
            <div className="image-container">
              <h3>대상이미지</h3>
              <div className="image-wrapper">
                {imageUrls.target && (
                  <img
                    src={imageUrls.target}
                    alt="Target"
                    className="image"
                    onClick={() => handleImageClick(imageUrls.target)}
                  />
                )}
              </div>
            </div>
          </Col>
          <Col xs="12" md="1" className="image-arrow">
            <img className='arrow' src={Arrow} alt='arrow' />
          </Col>
          <Col xs="12" md="5">
            <div className="image-container2">
              <h3>결과 이미지</h3>
              <div className="image-wrapper">
                {imageUrls.output && (
                  <div>
                    <img
                      src={imageUrls.output}
                      alt="Output"
                      className="image"
                      onClick={() => handleImageClick(imageUrls.output)}
                    />
                  </div>
                )}
              </div>
            </div>
          </Col>
        </Row>
        <Button
          className="btns"
          color="primary"
          onClick={handleDownloadOutput}
        >
          결과 이미지 다운로드
        </Button>
        <Button
          className="btns"
          color="primary"
          onClick={handleSurvey}
        >
          만족도 조사 하러가기!
        </Button>
        <Footer />
      </div>
    </>
  );
};

export default GenerateProject;