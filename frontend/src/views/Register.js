import { Alert, Row, Col, Button } from "reactstrap";
import Footer from "../layouts/Footer";
import './Login.css'
import React, { useState} from 'react';
import { useNavigate } from "react-router-dom";
import fastapi from '../lib/api'

function Register(props) {
  const [error, setError] = useState({ detail: [] });
  const [signin_name,setInputName]=useState('')
  const [username, setInputId] = useState('')
  const [password, setInputPw] = useState('')
  const [isvalid, setIsValid] = useState('')

  const navigate = useNavigate();

  const handleLogin = (event) =>  {
    event.preventDefault()
        let url = "/signin"
        let params = {
            signin_name: signin_name,
            username: username,
            password: password
        }
        fastapi('signin', url, params, 
            (json) => {
                console.log(json['isvalid']);
                setIsValid(json['isvalid']);
                if (json['isvalid']===true){
                   navigate("/login");
                }
            },
            (json_error) => {
                setError(json_error);
            }
        );
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
          <div className="box-container3">
            <div className="box3">
              <h1>Sign Up</h1>
              <div className="name">
                    <label htmlFor='user-name'>이름</label>
                    <br></br>
                    <input name='user-name'
                        type='text' 
                        value={signin_name} 
                        onChange={event => {setInputName(event.target.value);}}
                        required
                    ></input>
                </div>
                <div className="id">
                    <label htmlFor='user-id'>ID</label>
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
                      onChange={event => {setInputPw(event.target.value);}}
                      required
                  ></input>
                </div>
                <div className='login-btns'>
                  <form onSubmit={handleLogin}>
                  {isvalid===false && (
                        <Alert color="danger">이미 가입된 이메일이 있습니다. 다시 시도해주세요</Alert>
                      )}
                  <Button className='btns' type='submit' color="primary" size="lg">
                      회원가입
                  </Button>
                  </form>
                {/* <Button className='btns' color="primary" size="lg" onClick={()=>navigate('/login')}>
                    이전으로
                </Button> */}
                </div>
            </div>
          </div>
        </Col>
        </Row>
      <Footer/>
      </div>
  );
};

export default Register;