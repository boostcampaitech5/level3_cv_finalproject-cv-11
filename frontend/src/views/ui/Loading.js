import React from "react";
import {
  Card,
  CardBody,
  Button
} from "reactstrap";
import './Generate.css'
import Footer from "../../layouts/Footer";
import { useNavigate } from "react-router-dom";
import Video from '../../assets/video/loading.mp4'

const Loading = () => {
  // For Dismiss Button with Alert
  const navigate = useNavigate();

  const handleClickGenerate = () => {
    navigate("/generate"); // generate 페이지로 이동
  };

  const handleClickGenerateList = () => {
    navigate("/generate/projects"); // generate 페이지로 이동
  };


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
          <div className="box-container3">
            <div className="box3">
              <video autoPlay loop muted src={Video} type='video/mp4' />
              <h3>모델 학습중입니다! 조금만 기다려주세요</h3>
            </div>
          </div>
        </CardBody>
        <Footer />
      </Card>
    </div>
  );
};

export default Loading;
