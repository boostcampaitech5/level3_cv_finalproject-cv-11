import React, { useState, useEffect } from "react";
import { Card, CardBody, Button } from "reactstrap";
import "./GenerateProject.css";
import Footer from "../../../layouts/Footer";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from '../../../lib/api';

const GenerateProject = () => {
  const [imageUrls, setImageUrls] = useState({});
  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state.username;
  const project_name = location.state.project_name;


  // 이전으로
  const handleBackGenerateList = () => {
    navigate(`/generate/projects`, { state: { username: username, project_name: project_name } });
  };
  const handleBackMain = () => {
    navigate(`/deepfake`, { state: { username: username, project_name: project_name } });
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
            navigate('/generate/loading');
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
            {imageUrls.source && (
              <img
                src={imageUrls.source}
                alt="Source"
                className="image"
                onClick={() => handleImageClick(imageUrls.source)}
              />
            )}
          </div>
          <div className="image-wrapper">
            <h3>Target Image</h3>
            {imageUrls.target && (
              <img
                src={imageUrls.target}
                alt="Target"
                className="image"
                onClick={() => handleImageClick(imageUrls.target)}
              />
            )}
          </div>
          <div className="image-wrapper">
            <h3>Output Image</h3>
            {imageUrls.output && (
              <div>
                <img
                  src={imageUrls.output}
                  alt="Output"
                  className="image"
                  onClick={() => handleImageClick(imageUrls.output)}
                />
                <Button
                  className="download-btn"
                  color="primary"
                  onClick={handleDownloadOutput}
                >
                  Download
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
};

export default GenerateProject;
