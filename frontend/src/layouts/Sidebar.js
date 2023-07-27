import { Button, Nav, NavItem } from "reactstrap";
import Logo from "./Logo";
import { Link, useLocation, useNavigate } from "react-router-dom";
import Login from "../views/Login";

const navigation = [
  {
    title: "Home",
    href: "/starter",
    icon: "bi bi-house",
  },
  {
    title: "이미지 생성/탐지하기",
    href: "/deepfake",
    icon: "bi bi-upc-scan",
  },
  // {
  //   title: "이미지 탐지하기",
  //   href: "/badges",
  //   icon: "bi bi-upc-scan",
  // },
  {
    title: "마이페이지",
    href: "/mypage",
    icon: "bi bi-link",
  },
  {
    title: "About Us",
    href: "/about",
    icon: "bi bi-hdd-stack",
  },

];

const Sidebar = () => {
  const showMobilemenu = () => {
    document.getElementById("sidebarArea").classList.toggle("showSidebar");
  };
  let location = useLocation();
  const login=location.state
  const navigate = useNavigate();
  const navigateToGenerate = () => {
    navigate("/deepfake", { state: login});
  };

  return (
    <div className="p-3">
      <div className="d-flex align-items-center">
        <Logo />
        <span className="ms-auto d-lg-none">
        <Button
          close
          size="sm"
          className="ms-auto d-lg-none"
          onClick={() => showMobilemenu()}
        ></Button>
        </span>
      </div>
      <div className="pt-4 mt-2">
        <Nav vertical className="sidebarNav">
          {navigation.map((navi, index) => (
            <NavItem key={index} className="sidenav-bg">
              {navi.title === "이미지 생성/탐지하기" ? (
                <button
                  className={
                    location.pathname === navi.href
                      ? "text-primary nav-link py-3"
                      : "nav-link text-secondary py-3"
                  }
                  onClick={navigateToGenerate}
                >
                  <i className={navi.icon}></i>
                  <span className="ms-3 d-inline-block">{navi.title}</span>
                </button>
              ) : (
              <Link
                to={navi.href}
                className={
                  location.pathname === navi.href
                    ? "text-primary nav-link py-3"
                    : "nav-link text-secondary py-3"
                }
              >
                <i className={navi.icon}></i>
                <span className="ms-3 d-inline-block">{navi.title}</span>
              </Link>
              )}
            </NavItem>
          ))}
        </Nav>
      </div>
    </div>
  );
};

export default Sidebar;
