import React, { useState, use } from "react";
import {
  Card,
  CardBody,
  Button
} from "reactstrap";
import './Generate.css'
import Footer from "../../../layouts/Footer";
import Image from '../../../assets/images/snow.JPG'
import { useNavigate, useLocation } from "react-router-dom";


const Generate = () => {
  // For Dismiss Button with Alert
  const [visible, setVisible] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();
  const login = location.state
  console.log(login)

  const handleGenerateStart = () => {
    if (!login) {
      alert("로그인이 필요합니다");
      return;
    }
    else {
      navigate("/generate/start", { state: login }); // 생성 시작 페이지 이동
    }
  };

  const handleGenerateList = () => {
    if (!login) {
      alert("로그인이 필요합니다");
      return;
    }
    else {
      navigate("/generate/projects", { state: login }); // 결과 확인 페이지 이동
    }
  };

  const handleBackDeepfake = () => {
    navigate("/deepfake", { state: login }); // deepfake 페이지로 이동
  };

  const onDismiss = () => {
    setVisible(false);
  };

  return (
    <>
      <div className='generate-container'>
        <h1>AI Deepfake Detection</h1>
        <p>1. 딥페이크를 통해서 타인과 '나'의 얼굴을 바꿔보세요</p>
        <div className='generate-btns'>
          <Button className='btns' color="secondary" size="lg" onClick={handleGenerateStart}>
            생성하기
          </Button>
          <Button className='btns' color="secondary" size="lg" onClick={handleGenerateList}>
            결과보기
          </Button>
          <Button className='btns' color="secondary" size="lg" onClick={handleBackDeepfake}>
            이전으로
          </Button>
        </div>
      </div>
      <Card>
        <CardBody className="">
          <div className="mt-3">
            <h3>💡 시작하기 전 유의사항</h3>
            <div className="box-container">
              <div className="box">
                <p>1. 한 사람의 얼굴만 넣어야 해요.</p>
                <p>2. 사진의 포즈는 다양할수록 좋아요.</p>
                <p>3. 배경이 복잡하거나 얼굴이 작으면 인식이 어려워요.</p>
                <p>4. 탐지 결과를 받는 데 시간이 소요될 수 있어요.</p>
                <p>5. 동일한 사진으로만 제출하면 학습이 어려워요.</p>
                <img src={Image} alt="snow 이미지" />
              </div>
            </div>
          </div>
        </CardBody>
        <Footer />
      </Card>
    </>
  );
};

export default Generate;
