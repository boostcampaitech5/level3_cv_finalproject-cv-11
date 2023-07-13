import React, { useState, useEffect } from "react";
import { Card, CardBody, Button } from "reactstrap";
import "./GenerateProject.css";
import Footer from "../../layouts/Footer";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";

const GenerateProject = () => {
  const [visible, setVisible] = useState(true);
  const [selectedImage, setSelectedImage] = useState([]);
  const [imageUrls, setImageUrls] = useState({});
  const navigate = useNavigate();
  const location = useLocation();

  const handleBackGenerateList = () => {
    navigate("/generate/projects"); // Generate list 조회 페이지로 이동
  };

  // Extracting username and project_name from location.state
  const { username, project_name: projectName } = location.state;

  useEffect(() => {
    fetchImageUrls();
  }, []);

  const fetchImageUrls = async () => {
    try {
      const response = await axios.get(`/generation/${projectName}`);
      const { complete, source, target, output } = response.data;
      setImageUrls({ complete, source, target, output });

      if (!complete) {
        navigate(`/generate/${projectName}/upload`);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const handleDownloadOutput = async () => {
    try {
      const response = await axios.get(imageUrls.output, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "output.jpeg");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div className="generate-project-container">
        <h1>AI Deepfake Detection</h1>
        <h2>프로젝트: {projectName}</h2>
        <div className="image-container">
          <div className="image-wrapper">
            <h3>Source Image</h3>
            {imageUrls.source && (
              <img src={imageUrls.source} alt="Source" className="image" />
            )}
          </div>
          <div className="image-wrapper">
            <h3>Target Image</h3>
            {imageUrls.target && (
              <img src={imageUrls.target} alt="Target" className="image" />
            )}
          </div>
          <div className="image-wrapper">
            <h3>Output Image</h3>
            {imageUrls.output && (
              <div>
                <img src={imageUrls.output} alt="Output" className="image" />
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
        <Button
          className="btns"
          color="secondary"
          size="lg"
          onClick={handleBackGenerateList}
        >
          이전으로
        </Button>
      </div>
      <Footer />
    </>
  );
};

export default GenerateProject;
