import React, { useState, useEffect } from "react";
import {
  Card,
  CardBody,
  Button
} from "reactstrap";
import "./GenerateProject.css";
import Footer from "../../layouts/Footer";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from '../../lib/api';

const GenerateList = () => {
  const [projectCnt, setProjectCnt] = useState(0);
  const [projectList, setProjectList] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();
  const username = 'test';

  useEffect(() => {
    fetchProjectList(username);
  }, []);

  // 이전으로
  const handleBackGenerate = () => {
    // navigate("/generate", { state: { username: location.state } }); // generate 페이지로 이동
    navigate("/generate", { state: { username: username } }); // generate 페이지로 이동
  };

  // 조회된 프로젝트 리스트
  const fetchProjectList = (username) => {
    fastapi(
      "get",
      `/generate/${username}`,
      {},
      (response) => {
        const { project_len, project_list } = response;
        setProjectCnt(project_len);
        setProjectList(project_list);
      },
      (error) => {
        console.log(error);
      }
    );
  };

  const handleNavigateToProject = (projectName) => {
    navigate(`/generate/${projectName}`, { state: { username: username, project_name: projectName } });
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
            <h2>생성하기 프로젝트 리스트</h2>
            <p>프로젝트 {projectCnt} 개</p>
            <div className="generate-list">
              <div className="box">
                {projectList.map((projectName) => (
                  <p
                    key={projectName}
                    onClick={() => handleNavigateToProject(projectName)}
                    style={{ cursor: "pointer" }}
                  >
                    {projectName}
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