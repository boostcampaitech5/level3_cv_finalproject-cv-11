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
const Aboutus = () => {

  return (
    <>
    <div className='about-container'>
    <h1>Aivengers를 소개합니다!</h1>
  </div>
    <div>
      {/* --------------------------------------------------------------------------------*/}
      {/* Start Inner Div*/}
      {/* --------------------------------------------------------------------------------*/}
      {/* --------------------------------------------------------------------------------*/}
      {/* Row*/}
      {/* --------------------------------------------------------------------------------*/}
      <Row>
        <Col xs="12" md="12">
          {/* --------------------------------------------------------------------------------*/}
          {/* Card-1*/}
          {/* --------------------------------------------------------------------------------*/}
          <Card>
            <CardTitle tag="h4" className="border-bottom p-3 mb-0">
              김용희
            </CardTitle>
            <CardBody className="">
              <div className="button-group">
                <img src={Yonghee} alt='yonghee' width='400' height='500'/>
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
            <CardBody className="">
              <div className="button-group">
                <img src={SH} alt='seunghee' width='400' height='500'/>
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
            <CardBody className="">
              <div className="button-group">
                <img src={Yoonpyo} alt='yoonpyo' width='400' height='500'/>
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
            <CardBody className="">
              <div className="button-group">
                <img src={Junha} alt='yoonpyo' width='400' height='500'/>
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
            <CardBody className="">
              <div className="button-group">
                <img src={JY} alt='jaeyoung' width='400' height='500'/>
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
    </>
  );
};

export default Aboutus;
