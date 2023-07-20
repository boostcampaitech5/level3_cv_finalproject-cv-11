import {
  Card,
  CardBody,
  Button
} from "reactstrap";
import './Loading.css'
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
    navigate("/generate",{state: { username: username, password: password, project_name: project_name }}); // generate 페이지로 이동
  };

  const handleClickGenerateList = () => {
    navigate("/generate/projects",{state: { username: username, password: password, project_name: project_name }}); // generate 페이지로 이동
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
        fastapi('post', '/generation', params,
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
        navigate(`/generate/${project_name}`, {state: { username: username, password: password, project_name: project_name }});
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
            <div class="video-container">
              <video autoPlay muted loop>
                <source src='/videos/loading.mp4' type='video/mp4'/>
              </video>
            </div>
            <h3>모델 학습중입니다! 조금만 기다려주세요</h3>
          </CardBody>
      </Card>
      <Footer />
    </div>
  );
};

export default Loading;
