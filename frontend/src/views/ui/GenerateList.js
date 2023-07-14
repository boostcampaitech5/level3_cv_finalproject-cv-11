import React, { useState, useEffect } from "react";
import {
  Card,
  CardBody,
  Button
} from "reactstrap";
import "./GenerateList.css";
import Footer from "../../layouts/Footer";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from '../../lib/api';

const GenerateList = () => {
  const [projectList, setProjectList] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    fetchProjectList();
  }, []);

  // 이전으로
  const handleBackGenerate = () => {
    navigate("/generate", { state: { username: location.state } }); // deepfake 페이지로 이동
  };

  // 조회된 프로젝트 리스트
  const fetchProjectList = () => {
    fastapi(
      "get",
      "/generate/projects",
      {},
      (response) => {
        const { username, project_list } = response;
        setProjectList(project_list);
      },
      (error) => {
        console.log(error);
      }
    );
  };

  // const handleNavigateToProject = (projectName) => {
  //   let project = projectList.find(
  //     (p) => p.project_name === projectName
  //   );
  //   if (project) {
  //     let username = location.state.username;
  //     navigate(`/generate/${projectName}`, { state: { username, project_name: projectName } });
  //   }
  // };


  const handleNavigateToProject = (projectName) => {
    navigate(`/generate/${projectName}`, { state: { username: location.state, project_name: projectName } });
  };

  return (
    <>
      <div className="generate-container">
        <h1>AI Deepfake Detection</h1>
        <p>1. 딥페이크를 통해서 타인과 '나'의 얼굴을 바꿔보세요</p>
        <div className='generate-btns'>
          <Button className='btns' color="secondary" size="lg" onClick={handleBackGenerate}>
            이전으로
          </Button>
        </div>
      </div>
      <Card>
        <CardBody>
          <div className="mt-3">
            <h3>생성하기 프로젝트 리스트</h3>
            <div className="generate-list">
              <div className="box">
                {projectList.map((project) => (
                  <p
                    key={project}
                    onClick={() => handleNavigateToProject(project)}
                    style={{ cursor: "pointer" }}
                  >
                    {project}
                  </p>
                ))}
              </div>
            </div>
          </div>
        </CardBody>
      </Card>
      <Footer />
    </>
  );
};

export default GenerateList;