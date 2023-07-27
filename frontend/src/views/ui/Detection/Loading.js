import {
  Card,
  CardBody,
  Button
} from "reactstrap";
import '../Generation/Loading.css'
import Footer from "../../../layouts/Footer";
import { useNavigate, useLocation } from "react-router-dom";
import React, { useState, useEffect } from "react";
import fastapi from "../../../lib/api";

const Loading = () => {
  // For Dismiss Button with Alert
  const navigate = useNavigate();
  const location = useLocation();
  const [error, setError] = useState({ detail: [] });
  const username = location.state.username
  const password = location.state.password
  const project_name = location.state.project_name

  const handleClickGenerate = () => {
    navigate("/detect", { state: location.state }); // generate 페이지로 이동
  };

  const handleClickGenerateList = () => {
    navigate("/detect/projects", { state: location.state }); // generate 페이지로 이동
  };

  const handleCheckState = async () => {
    try {
      let params = {
        username: username,
        password: password,
        project_name: project_name,
      };
      let response;

      await new Promise((resolve, reject) => {
        fastapi('post', '/detection', params,
          (json) => {
            console.log(json);
            response = json;
            resolve(); // 응답을 받았음을 알림
          },
          (json_error) => {
            setError(json_error);
            reject(json_error); // 에러 발생을 알림
          }
        );
      });

      // 도착한 응답이 있는 경우 페이지를 이동시키는 로직
      if (response) {
        navigate(`/detect/${project_name}`, { state: { username: username, password: password, project_name: project_name, result: response } });
      } else if (response["complete"] === false) {
        alert("이미지 형식이 잘못되었습니다");
        navigate('/detect/start', { state: { username: username, password: password, project_name: project_name } })
      }
    } catch (error) {
      // 에러 처리
      console.error(error);
    }
  };

  useEffect(() => {
    handleCheckState();
  }, []);


  return (
    <div>
      <div className='generate-container'>
        <h1>AI Deepfake Detection</h1>
        <p>당신의 이미지가 딥페이크를 통해 악용되고 있는지 확인해보세요!</p>
        <div className='generate-btns'>
          <Button className='btns' color="secondary" size="lg" onClick={handleClickGenerate}>
            이전으로
          </Button>
          <Button className='btns' color="secondary" size="lg" onClick={handleClickGenerateList}>
            목록으로
          </Button>
        </div>
      </div>
      <Card>
        <CardBody className="">
          <div className="video-container">
            <video autoPlay muted loop>
              <source src='/videos/loading.mp4' type='video/mp4' />
            </video>
          </div>
          <h3>모델 학습중입니다! 조금만 기다려주세요</h3>
        </CardBody>
        <Footer />
      </Card>
    </div>
  );
};

export default Loading;
