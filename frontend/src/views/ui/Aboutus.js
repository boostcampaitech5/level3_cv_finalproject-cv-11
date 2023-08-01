import React, { useState } from "react";
import {
  Button,
  ButtonGroup,
  Card,
  CardBody,
  CardTitle,
  Row,
  Col,
} from "reactstrap";
import './Aboutus.css'
import Junha from '../../assets/images/junha.jpg'
import Yoonpyo from '../../assets/images/yoonpyo.jpg'
import Yonghee from '../../assets/images/yonghee.jpg'
import SH from '../../assets/images/seunghee.jpg'
import JY from '../../assets/images/jaeyoung.jpg'
import Footer from "../../layouts/Footer";
const Aboutus = () => {

  return (
    <>
    <div className='about-container'>
    <h1>Aivengers를 소개합니다!</h1>
  </div>
    <div>
      <Row>
        <Col xs="12" md="12">
          <Card>
            <CardTitle tag="h4" className="border-bottom p-3 mb-0">
              김용희
            </CardTitle>
            <CardBody className="d-flex flex-wrap">
              <div className="button-group">
                <img src={Yonghee} alt='yonghee' width='400' height='500'/>
              </div>
              <div className="button-group2">
                <h1>역할</h1>
                <h5>1. 선행 연구 검토</h5>
                <h5>2. FastAPI 기능 구현</h5>
                <h5>3. GCP 환경설정</h5>
                <h5>4. CS, CloudDB 연결</h5>
                <br></br>
                <h1>Github</h1>
                <h5>https://github.com/hykhhijk</h5>
                <br></br>
                <h1>Email</h1>
                <h5>hjhhijk@gmail.com</h5>
              </div>
            </CardBody>
          </Card>
        </Col>
        <Col xs="12" md="12">
          {/* --------------------------------------------------------------------------------*/}
          {/* Card-2*/}
          {/* --------------------------------------------------------------------------------*/}
          <Card>
            <CardTitle tag="h4" className="border-bottom p-3 mb-0">
              박승희
            </CardTitle>
            <CardBody className="d-flex flex-wrap">
              <div className="button-group">
                <img src={SH} alt='seunghee' width='400' height='500'/>
              </div>
              <div className="button-group2">
                <h1>역할</h1>
                <h5>1. 프로젝트 매니저</h5>
                <h5>2. FastAPI & DB 기능 구현</h5>
                <h5>3. React 기능 구현</h5>
                <h5>4. vertex.AI 모델 서빙 시도</h5>
                <br></br>
                <h1>Github</h1>
                <h5>https://github.com/HipJaengYiCat</h5>
                <br></br>
                <h1>Email</h1>
                <h5>shee6185@gmail.com</h5>
              </div>
            </CardBody>
          </Card>
        </Col>
        <Col xs="12" md="12">
          {/* --------------------------------------------------------------------------------*/}
          {/* Card-3*/}
          {/* --------------------------------------------------------------------------------*/}
          <Card>
            <CardTitle tag="h4" className="border-bottom p-3 mb-0">
              이윤표
            </CardTitle>
            <CardBody className="d-flex flex-wrap">
              <div className="button-group">
                <img src={Yoonpyo} alt='yoonpyo' width='400' height='500'/>
              </div>
              <div className="button-group2">
                <h1>역할</h1>
                <h5>1. 생성모델 환경 구축</h5>
                <h5>2. React 구현 및 api 연결</h5>
                <h5>3. GCP 환경설정</h5>
                <h5>4. Figma 목업디자인, 프로젝트 발표</h5>
                <br></br>
                <h1>Github</h1>
                <h5>https://github.com/imsmile2000</h5>
                <br></br>
                <h1>Email</h1>
                <h5>imsmile2000@naver.com</h5>
              </div>
            </CardBody>
          </Card>
        </Col>
        <Col xs="12" md="12">
          {/* --------------------------------------------------------------------------------*/}
          {/* Card-4*/}
          {/* --------------------------------------------------------------------------------*/}
          <Card>
            <CardTitle tag="h4" className="border-bottom p-3 mb-0">
              이준하
            </CardTitle>
            <CardBody className="d-flex flex-wrap">
              <div className="button-group">
                <img src={Junha} alt='yoonpyo' width='400' height='500'/>
              </div>
              <div className="button-group2">
                <h1>역할</h1>
                <h5>1. 선행 연구 검토</h5>
                <h5>2. 실험 설계 & 가설 검증</h5>
                <h5>3. 모델 파이프라인 구축</h5>
                <h5>4. 모델 후속 개발</h5>
                <br></br>
                <h1>Github</h1>
                <h5>https://github.com/junha-lee</h5>
                <br></br>
                <h1>Email</h1>
                <h5>junha4304@gmail.com</h5>
              </div>
            </CardBody>
          </Card>
        </Col>
        <Col xs="12" md="12">
          {/* --------------------------------------------------------------------------------*/}
          {/* Card-6*/}
          {/* --------------------------------------------------------------------------------*/}
          <Card>
            <CardTitle tag="h4" className="border-bottom p-3 mb-0">
              주재영
            </CardTitle>
            <CardBody className="d-flex flex-wrap">
              <div className="button-group">
                <img src={JY} alt='jaeyoung' width='400' height='500'/>
              </div>
              <div className="button-group2">
                <h1>역할</h1>
                <h5>1. SOTA 모델 실험</h5>
                <h5>2. Dataset preprocessing</h5>
                <h5>3. Docekr 환경 설정</h5>
                <h5>4. CS 연결</h5>
                <br></br>
                <h1>Github</h1>
                <h5>https://github.com/JaiyoungJoo</h5>
                <br></br>
                <h1>Email</h1>
                <h5>wodud3851@gmail.com</h5>
              </div>
            </CardBody>
          </Card>
        </Col>
      </Row>
      {/* --------------------------------------------------------------------------------*/}
      {/* Row*/}
      {/* --------------------------------------------------------------------------------*/}

      {/* --------------------------------------------------------------------------------*/}
      {/* End Inner Div*/}
      {/* --------------------------------------------------------------------------------*/}
    </div>
    <Footer/>
    </>
  );
};

export default Aboutus;
