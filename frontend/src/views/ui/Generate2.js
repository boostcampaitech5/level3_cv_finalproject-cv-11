import React, { useState } from "react";
import {
  Card,
  CardBody,
  Button
} from "reactstrap";
import './Generate.css'
import Footer from "../../layouts/Footer";
import Image from '../../assets/images/snow2.JPG'
import { useNavigate } from "react-router-dom";


const Generate2 = () => {
  // For Dismiss Button with Alert
  const [visible, setVisible] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);

  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/generate"); // generate2 페이지로 이동
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0]; // 업로드된 파일 가져오기
    setSelectedImage(URL.createObjectURL(file)); // 선택된 이미지 업데이트
    navigate('/loading');
  };

  const handleClickUploadButton = () => {
    const fileInput = document.getElementById('image-input');
    fileInput.click(); 
  };


  return (
    <div>
      <div className='generate-container'>
          <h1>AI Deepfake Detection</h1>
          <h2>생성하기</h2>
          <p>딥페이크를 통해서 타인과 '나'의 얼굴을 바꿔보세요</p>
          <div className='generate-btns'>
          <Button className='btns'color="secondary" size="lg" onClick={handleClick}>
          이전으로
          </Button>
          </div>
      </div>
        <Card>
        <CardBody className="">
          <div className="mt-3">
            <h3>생성하기</h3>
            <div className="box-container2">
              <div className="box2">
                <img src={Image} alt="이미지 유의사항"/>
                <Button className='btns2'color="primary"size="lg" onClick={handleClickUploadButton}>
                    사진 업로드
                </Button>
                <input
                    id='image-input'
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  style={{display:'none'}}
                />
              </div>          
            </div>
          </div>
        </CardBody>
        <Footer/>
      </Card>
    </div>
  );
};

export default Generate2;
