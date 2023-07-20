import React, { useState, useEffect } from "react";
import { Card, CardBody, Button } from "reactstrap";
import "./DetectProject.css";
import Footer from "../../../layouts/Footer";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from '../../../lib/api';

const DetectProject = () => {
  const [imageUrls, setImageUrls] = useState({});
  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state.username;
  const project_name = location.state.project_name;
  const password=location.state.password
  const result = location.state.result; // fake, real


  // 이전으로
  const handleBackDetectList = () => {
    navigate(`/detect/projects`, { state: { username: username, password: password, project_name: project_name } });
  };
  const handleBackMain = () => {
    navigate(`/deepfake`, { state: { username: username, password: password, project_name: project_name } });
  };

  useEffect(() => {
    fetchImageUrls();
  }, []);

  const fetchImageUrls = async () => {
    try {
      fastapi(
        "get",
        `/detect/${username}/${project_name}`,
        {},
        (response) => {
          setImageUrls(response);
          if (!response.complete) {
            navigate('/generate/loading', {state: { username: username, password: password, project_name: project_name }});
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

        <div className="image-container">
          <h2>프로젝트: {project_name}</h2>
          <div className="image-wrapper">
            <h3>Source Image</h3>
            <p> {result} </p>

          </div>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default DetectProject;
