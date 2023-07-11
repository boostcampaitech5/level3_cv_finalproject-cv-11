import { Row, Col, Card, CardBody, CardTitle, Button } from "reactstrap";
import Footer from "../layouts/Footer";
import './Login.css'
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { func } from "prop-types";
import { useNavigate } from "react-router-dom";

function Login(props) {
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
    const userData = {
      username: inputId,
      password: inputPw,
    };
    fetch("http://115.85.182.51:30008/login", { //auth 주소에서 받을 예정
      method: "post", // method :통신방법
      headers: {      // headers: API 응답에 대한 정보를 담음
        "content-type": "application/json",
      },
      body: JSON.stringify(userData), //userData라는 객체를 보냄
    })
      .then((res) => res.json())
      .then((json) => {            
        if(json.isLogin==="True"){
          props.setMode("WELCOME");
        }
        else {
          alert(json.isLogin)
        }
      });
    }


  const handleRegisterClick = () => {
    navigate('/register');
  }

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
                  <form>
                  <input 
                      name='user-pw'
                      type='password'
                      autoComplete="new-password"
                      value={inputPw} 
                      onChange={handleInputPw}
                      required
                  ></input>
                  </form>
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