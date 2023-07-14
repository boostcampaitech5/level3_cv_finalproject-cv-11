import React, { useState, useEffect } from "react";
import { Card, CardBody, Button } from "reactstrap";
import "./GenerateList.css";
import Footer from "../../layouts/Footer";
import { useNavigate } from "react-router-dom";
import fastapi from '../lib/api'

const GenerateList = () => {
  const [visible, setVisible] = useState(true);
  const [projectList, setProjectList] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProjectList();
  }, []);

  // Fetch project list using fastapi
  const fetchProjectList = () => {
    fastapi(
      "post",
      "/generate/projects",
      {},
      (response) => {
        const { username, project_list } = response.data;
        setProjectList(project_list);
      },
      (error) => {
        console.log(error);
      }
    );
  };

  const handleNavigateToProject = (projectName) => {
    const { username } = projectList.find(
      (project) => project.project_name === projectName
    );
    navigate(`/generate/${projectName}`, {
      state: { username, project_name: projectName },
    });
  };

  const onDismiss = () => {
    setVisible(false);
  };

  return (
    <>
      <div className="generate-container">
        <h1>AI Deepfake Detection</h1>
        <p>1. 딥페이크를 통해서 타인과 '나'의 얼굴을 바꿔보세요</p>
      </div>
      <Card>
        <CardBody className="">
          <div className="mt-3">
            <h3>생성하기 프로젝트 리스트</h3>
            <div className="generate-list">
              <div className="box">
                {projectList.map((project) => (
                  <p
                    key={project.project_name}
                    onClick={() =>
                      handleNavigateToProject(project.project_name)
                    }
                  >
                    {project.project_name}
                  </p>
                ))}
              </div>
            </div>
          </div>
        </CardBody>
        <Footer />
      </Card>
    </>
  );
};

export default GenerateList;