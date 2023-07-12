import { Row, Col, Card, CardBody, CardTitle, Button } from "reactstrap";
import Footer from "../layouts/Footer";
import './Login.css'
import React, { useState, useEffect } from 'react';
import { func } from "prop-types";
import { useNavigate } from "react-router-dom";
import  Axios from 'axios';
import {Cookies} from 'react-cookie';
const cookies = new Cookies();

export const setCookie = (name: string, value: string, options?: any) => {
  return cookies.set(name, value, {...options}); 
}

function Login() {
  const [inputId, setInputId] = useState('')
  const [inputPw, setInputPw] = useState('')

  const navigate = useNavigate();

  // login 버튼 클릭 이벤트
  const onClickLogin = () => {
    Axios.post('http://115.85.182.51:30008/login', {
        username: inputId,
        password: inputPw,
      })
      .then(res => console.log(res.json)) 
      .catch()
      // .then((res) => res.json)
      // .then((json) => {            
      //   if(json.isLogin==="True"){
      //     props.setMode("WELCOME");
      //   }
      //   else {
      //     alert(json.isLogin)
      //   }
      // });
    }


  const handleRegisterClick = () => {
    // props.setMode("SIGNIN");
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
                        onChange={event => {setInputId(event.target.value);}}
                        required
                    ></input>
                </div>
                <div className="pw">
                  <label htmlFor='user-pw' >Password</label>
                  <br></br>
                  <input 
                      name='user-pw'
                      type='password'
                      autoComplete="new-password"
                      value={inputPw} 
                      onChange={event => {setInputPw(event.target.value);}}
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
                <Button className='btns' type='submit' color="primary" size="lg" onClick={onClickLogin}>
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