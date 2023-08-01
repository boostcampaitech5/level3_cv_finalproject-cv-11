import {
  Row,
  Col,
  Card,
  CardBody,
  Button
} from "reactstrap";
import Footer from "../../layouts/Footer";
import './Aboutus.css'
import { useNavigate, useLocation } from "react-router-dom";

const Mypage = () => {

  const navigate = useNavigate();
  const location = useLocation();
  const login = location.state
  console.log(login)

  const handleGenerate = () => {
    if (!login) {
      alert("로그인이 필요합니다");
      return;
    }
    else {
      navigate("/generate/projects", { state: login }); // generate 페이지로 이동
    };
  };

  const handleDetect = () => {
    if (!login) {
      alert("로그인이 필요합니다");
      return;
    }
    else {
      navigate("/detect/projects", { state: login }); // generate 페이지로 이동
    };
  };
  return (
    <>
    <div className='about-container'>
    <h1>프로젝트 목록 확인</h1>
  </div>
    <div>
      <Row>
        <Col xs="12" md="12">
          <Card>
            <CardBody className="d-flex flex-wrap">
              <Button className='btns' color="secondary" size="lg" onClick={handleGenerate}>
              생성하기 프로젝트
            </Button>
            <Button className='btns' color="secondary" size="lg" onClick={handleDetect}>
              탐지하기 프로젝트
            </Button>
            </CardBody>
          </Card>
        </Col>
      </Row>
    </div>
    <Footer/>
    </>
  );
};

export default Mypage;
