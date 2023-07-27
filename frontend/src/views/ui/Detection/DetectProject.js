import React, { useState, useEffect } from "react";
import { Card, CardBody, Button, Row,Col } from "reactstrap";
import "./DetectProject.css";
import Footer from "../../../layouts/Footer";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from '../../../lib/api';

const DetectProject = () => {
  const [imageUrls, setImageUrls] = useState({});
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const user_id = location.state.user_id;
  const username = location.state.username;
  const project_id = location.state.project_id;
  const project_name = location.state.project_name;
  const password = location.state.password


  // 이전으로
  const handleBackDetectList = () => {
    navigate(`/detect/projects`, { state: { username: username, password: password, project_name: project_name } });
  };
  const handleBackMain = () => {
    navigate(`/deepfake`, { state: { username: username, password: password, project_name: project_name } });
  };
  const handleSurvey = () => {
    navigate(`/survey`, { state: { user_id: user_id, username: username, password: password, project_id: project_id, project_name: project_name } });
  };

  const handleImageClick = (imageUrl) => {
    window.open(imageUrl, "_blank");
  };


  let result;

  const fetchImageUrls = async () => {
    try {
      const response = await new Promise((resolve, reject) => {
        fastapi(
          "get",
          `/detect/${username}/${project_name}`,
          {},
          (response) => {
            resolve(response);
          },
          (error) => {
            reject(error);
          }
        );
      });
      setImageUrls(response);
      result = response['result'];
      console.log(result);
      if (result === "fake") {
        setMessage("해당 이미지는 딥페이크 합성 이미지입니다.");
      } else if (result === "real") {
        setMessage("해당 이미지는 합성되지 않은 이미지입니다.");
      } else {
        setMessage("알 수 없는 결과입니다.");
      }
      if (!response.complete) {
        navigate('/detect/loading', { state: { username: username, password: password, project_name: project_name } });
      }
    } catch (error) {
      console.log(error);
    }
  };
  useEffect(() => {
    fetchImageUrls();
  }, []);

  const imageWrapperClass = message.includes("딥페이크") ? "image-wrapper red-border" : "image-wrapper";


  return (
    <>
      <div className="generate-project-container">
        <div className="generate-container">
          <h1>AI Deepfake Detection</h1>
          <p>당신의 이미지가 딥페이크를 통해 악용되고 있는지 확인해보세요!</p>
          <div className='generate-btns'>
            <Button className='btns' color="secondary" size="lg" onClick={handleBackDetectList}>
              목록으로
            </Button>
          </div>
          <div className='generate-btns'>
            <Button className='btns' color="secondary" size="lg" onClick={handleBackMain}>
              메인으로
            </Button>
          </div>
        </div>

        <h3>폴더명: {project_name}</h3>
        <Row>
          <Col xs="12" md="6">
        <div className="image-container">
          {imageUrls.target && (
            <div className={imageWrapperClass}>
              <img
                src={imageUrls.target}
                alt="Target"
                className="image"
                onClick={() => handleImageClick(imageUrls.target)}
              />
            </div>
          )}
          <h3>{message}</h3>
        </div>
          </Col>
          <Col xs="12" md="6">
          <div className="image-container">
                <div className="image-wrapper">
                  {imageUrls.gradcam&& (
                    <img
                      src={imageUrls.gradcam}
                      alt="Gradcam"
                      className="image"
                      onClick={() => handleImageClick(imageUrls.gradcam)}
                    />
                  )}
                </div>
                <h3>GradCam 출력 결과</h3>
          </div>
          </Col>
        </Row>
      </div>
      <Button
        className="btns"
        color="primary"
        onClick={handleSurvey}
      >
        만족도 조사 하러가기!
      </Button>
      <Footer />
    </>
  );
};

export default DetectProject;
