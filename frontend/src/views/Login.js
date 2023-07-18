import { Alert, Row, Col, Button } from "reactstrap";
import Footer from "../layouts/Footer";
import './Login.css'
import React, { useState, useMemo, useEffect} from 'react';
import { useNavigate } from "react-router-dom";
// import  axios from 'axios';
import fastapi from '../lib/api'
// import { access_token, user_name, is_login } from "../lib/store"

function Login() {
  const navigate = useNavigate();
  const [error, setError] = useState({ detail: [] });
  const [username, setInputId] = useState('')
  const [password, setInputPw] = useState('')
  const [isLogin, setIsLogin] = useState('');


  const handleLogin = (event) =>  {
    event.preventDefault()
        let url = "/login"
        let params = {
            username: username,
            password: password
        }
        fastapi('login', url, params, 
            (json) => {
                console.log(json['islogin']);
                setIsLogin(json['islogin']);
                if (json['islogin']===true){
                  navigate('/starter',{state: {username: username, password: password}});
                }
            },
            (json_error) => {
                setError(json_error);
            }
        );
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
                          value={username}
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
                        value={password}
                        autoComplete="new-password"
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
                  <form onSubmit={handleLogin}>
                    <Button className='btns' type='submit' color="primary" size="lg">
                        로그인
                    </Button>
                      {isLogin===false && (
                        <Alert color="danger">Login failed. Please try again.</Alert>
                      )}
                  </form>
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