import React, { useState, useEffect } from "react";
import { Card, CardBody, Button, Table } from "reactstrap";
import "./GenerateList.css";
import Footer from "../../../layouts/Footer";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from "../../../lib/api";

const GenerateList = () => {
  const [projectCnt, setProjectCnt] = useState(0);
  const [projectList, setProjectList] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state.username;

  useEffect(() => {
    fetchProjectList(username);
  }, []);

  // 이전으로
  const handleBackGenerate = () => {
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
    navigate(`/generate/${projectName}`, {
      state: { username: username, project_name: projectName },
    });
  };

  const renderProjectStateCircle = (state) => {
    let color = "circle-red"; // 기본값으로 빨간색 설정 - error를 포함하거나 값이 없을 경우

    if (state === "created") {
      color = "circle-gray";
    } else if (state === "running") {
      color = "circle-yellow";
    } else if (state === "finished") {
      color = "circle-green";
    }

    return (
      <div className="state-container">
        {state} <div className={`circle ${color}`}></div>
      </div>
    );
  };

  return (
    <>
      <div className="generate-container">
        <h1>AI Deepfake Detection</h1>
        <p>1. 딥페이크를 통해서 타인과 '나'의 얼굴을 바꿔보세요</p>
        <div className="generate-btns">
          <Button
            className="btns"
            color="secondary"
            size="lg"
            onClick={handleBackGenerate}
          >
            이전으로
          </Button>
        </div>
      </div>
      <Card>
        <CardBody>
          <div className="mt-3">
            <h2>생성하기 프로젝트 리스트</h2>
            <p>프로젝트 {projectCnt} 개</p>
            <Table className="text-center">
              <thead>
                <tr>
                  <th>프로젝트명</th>
                  <th>시작 시간</th>
                  <th>종료 시간</th>
                  <th>상태</th>
                </tr>
              </thead>
              <tbody>
                {projectList.map((project) => (
                  <tr
                    key={project.project_id}
                    onClick={() => handleNavigateToProject(project.project_name)}
                    style={{ cursor: "pointer" }}
                  >
                    <td>{project.project_name}</td>
                    <td>{project.start_time}</td>
                    <td>{project.end_time}</td>
                    <td>{renderProjectStateCircle(project.state)}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        </CardBody>
      </Card>
      <Footer />
    </>
  );
};

export default GenerateList;
