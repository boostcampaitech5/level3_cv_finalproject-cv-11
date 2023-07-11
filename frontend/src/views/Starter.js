import { Col, Row } from "reactstrap";
// import SalesChart from "../components/dashboard/SalesChart";
// import Feeds from "../components/dashboard/Feeds";
// import ProjectTables from "../components/dashboard/ProjectTable";
import React from "react";
import Footer from "../layouts/Footer";
import {
    Card,
    CardBody,
    Button
  } from "reactstrap";
import Video from '../assets/video/main.mp4'
import './Starter.css'
import Blog from "../components/dashboard/Blog";
import bg1 from "../assets/images/bg/bg1.jpg";
import bg2 from "../assets/images/bg/bg2.jpg";
import bg3 from "../assets/images/bg/bg3.jpg";
import bg4 from "../assets/images/bg/bg4.jpg";
import { useNavigate } from "react-router-dom";

const BlogData = [
  {
    image: bg1,
    title: "This is simple blog",
    subtitle: "2 comments, 1 Like",
    description:
      "This is a wider card with supporting text below as a natural lead-in to additional content.",
    btnbg: "primary",
  },
  {
    image: bg2,
    title: "Lets be simple blog",
    subtitle: "2 comments, 1 Like",
    description:
      "This is a wider card with supporting text below as a natural lead-in to additional content.",
    btnbg: "primary",
  },
  {
    image: bg3,
    title: "Don't Lamp blog",
    subtitle: "2 comments, 1 Like",
    description:
      "This is a wider card with supporting text below as a natural lead-in to additional content.",
    btnbg: "primary",
  },
  {
    image: bg4,
    title: "Simple is beautiful",
    subtitle: "2 comments, 1 Like",
    description:
      "This is a wider card with supporting text below as a natural lead-in to additional content.",
    btnbg: "primary",
  },
];

const Starter = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/generate"); // generate2 페이지로 이동
  };
  const handleAbout = () => {
    navigate("/buttons"); // generate2 페이지로 이동
  };
    return (
      <>
      <div className='hero-container'>
          <video autoPlay loop muted src={Video} type='video/mp4' />
          <h1>Deepfake Detection</h1>
          <p>Aivengers</p>
          <div className='hero-btns'>
          <Button className='btns'color="primary" size="lg" onClick={handleGetStarted}>
          Get Started!
          </Button>
          <Button className='btns'color="secondary"size="lg" onClick={handleAbout}>
          About Us
          </Button>
          </div>
      </div>
      <div className="cards">
      <h1>Our Services</h1>
      <Row>
      {BlogData.map((blg, index) => (
          <Col sm="6" lg="6" xl="3" key={index}>
          <Blog
              image={blg.image}
              title={blg.title}
              subtitle={blg.subtitle}
              text={blg.description}
              color={blg.btnbg}
          />
          </Col>
      ))}
      </Row>
      </div>
      <Footer/>
      </>
    );
};

export default Starter;
//   return (
//     <div>
//       {/***Top Cards***/}

//       {/***Sales & Feed***/}
//       <Row>
//         <Col sm="6" lg="6" xl="7" xxl="8">
//           <SalesChart />
//         </Col>
//         <Col sm="6" lg="6" xl="5" xxl="4">
//           <Feeds />
//         </Col>
//       </Row>
//       {/***Table ***/}
//       <Row>
//         <Col lg="12">
//           <ProjectTables />
//         </Col>
//       </Row>
//       {/***Blog Cards***/}
//       <Row>
//         {BlogData.map((blg, index) => (
//           <Col sm="6" lg="6" xl="3" key={index}>
//             <Blog
//               image={blg.image}
//               title={blg.title}
//               subtitle={blg.subtitle}
//               text={blg.description}
//               color={blg.btnbg}
//             />
//           </Col>
//         ))}
//       </Row>
//     </div>
//   );