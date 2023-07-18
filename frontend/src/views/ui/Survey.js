import React, { useState, useEffect } from "react";
import { Row,Col,Card, CardBody, Button } from "reactstrap";
import { useNavigate, useLocation } from "react-router-dom";
import fastapi from '../../lib/api';
import Arrow from '../../assets/images/arrow.png'
import Footer from "../../layouts/Footer";

const Survey = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state.username;
  const project_name = location.state.project_name;
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleAgeChange = (event) => {
    setAge(event.target.value);
  };

  const handleGenderChange = (event) => {
    setGender(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // 폼 데이터 처리 로직 작성
    console.log('Name:', name);
    console.log('Age:', age);
    console.log('Gender:', gender);

    // 폼 제출 후 초기화
    setName('');
    setAge('');
    setGender('');
  };

  return (
    <>
    <div>
        <h1>설문조사</h1>
        <form onSubmit={handleSubmit}>
        <label>
            이름
            <input type="text" value={name} onChange={handleNameChange} />
        </label>
        <br />
        <label>
            나이:
            <input type="text" value={age} onChange={handleAgeChange} />
        </label>
        <br />
        <label>
            저희 서비스에 대한 만족도는 어느 정도 이신가요? (5점 만점):
            <select value={gender} onChange={handleGenderChange}>
            <option value="">선택하세요</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>

            </select>
        </label>
        <br />
        <button type="submit">제출</button>
        </form>
    </div>
    <Footer />
    </>
    );
};

export default Survey;