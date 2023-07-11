import { Row, Col, Card, CardBody, CardTitle, Button } from "reactstrap";
import Footer from "../layouts/Footer";
import './Login.css'
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { func } from "prop-types";
import { useNavigate } from "react-router-dom";

function Login() {
  const [inputId, setInputId] = useState('')
  const [inputPw, setInputPw] = useState('')
  const handleInputId = (e) => {
    setInputId(e.target.value)
  }

  const navigate = useNavigate();

  const handleInputPw = (e) => {
      setInputPw(e.target.value)
  }

  // login 버튼 클릭 이벤트
  const onClickLogin = () => {
      console.log('click login')
  }
  const handleRegisterClick = () => {
    navigate('/register');
  }

  // 페이지 렌더링 후 가장 처음 호출되는 함수
  // useEffect(() => {
  //     axios.get('/user_inform/login')
  //     .then(res => console.log(res))
  //     .catch()
  // },
  // 페이지 호출 후 처음 한번만 호출될 수 있도록 [] 추가
  // [])
  
  return (
    <div>
      <Row>
        <Col xs="12" md="7">
            <div className="box-container">
              <div className="box">
                <h1>Welcome to Website!</h1>
              </div>
            </div>
        </Col>
        <Col xs="12" md="5">
          <div className="box-container2">
            <div className="box2">
              <h1>Sign In</h1>
                <div className="id">
                    <label htmlFor='user-id'>Email</label>
                    <br></br>
                    <input name='user-id'
                        type='text' 
                        value={inputId} 
                        onChange={handleInputId}
                        required
                    ></input>
                </div>
                <div className="pw">
                  <label htmlFor='user-pw' >Password</label>
                  <br></br>
                  <input 
                      name='user-pw'
                      type='password'
                      value={inputPw} 
                      onChange={handleInputPw}
                      required
                  ></input>
                </div>
                <div className='login-btns'>
                  <p>
                  아직 계정이 없으신가요?{' '}
                  <span onClick={handleRegisterClick} style={{ cursor: 'pointer', textDecoration: 'underline' }}>
                    회원가입
                  </span>
                  </p>
                <Button className='btns'color="primary" size="lg" onClick={onClickLogin}>
                    로그인
                </Button>
                </div>
            </div>
          </div>
        </Col>
        </Row>
      <Footer/>
      </div>
  );
};

export default Login;