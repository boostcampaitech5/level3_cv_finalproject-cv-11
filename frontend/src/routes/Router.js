import { lazy } from "react";
import { Navigate } from "react-router-dom";

/****Layouts*****/
const FullLayout = lazy(() => import("../layouts/FullLayout.js"));

/***** Pages ****/
const Starter = lazy(() => import("../views/Starter.js"));
const Login = lazy(() => import("../views/Login.js"));
const Register = lazy(() => import("../views/Register.js"));
const Badges = lazy(() => import("../views/ui/Badges"));
const About = lazy(() => import("../views/ui/Aboutus"));
const Cards = lazy(() => import("../views/ui/Cards"));
const Tables = lazy(() => import("../views/ui/Tables"));
const Forms = lazy(() => import("../views/ui/Forms"));
const Mypage = lazy(() => import("../views/ui/Mypage.js"));
const Survey = lazy(() => import("../views/ui/Survey.js"));

// main //
const Deepfake = lazy(() => import("../views/ui/Deepfake.js"));

// generation // 
const Generate = lazy(() => import("../views/ui/Generation/Generate.js"));
const GenerateStart = lazy(() => import("../views/ui/Generation/GenerateStart.js"));
const GenerateList = lazy(() => import("../views/ui/Generation/GenerateList.js"));
const GenerateProject = lazy(() => import("../views/ui/Generation/GenerateProject.js"));
const GenerateLoading = lazy(() => import("../views/ui/Generation/Loading.js"));

// detection // 
const Detect = lazy(() => import("../views/ui/Detection/Detect.js"));
const DetectStart = lazy(() => import("../views/ui/Detection/DetectStart.js"));
const DetectList = lazy(() => import("../views/ui/Detection/DetectList.js"));
const DetectProject = lazy(() => import("../views/ui/Detection/DetectProject.js"));
const DetectLoading = lazy(() => import("../views/ui/Detection/Loading.js"));


/*****Routes******/
const ThemeRoutes = [
  {
    path: "/",
    element: <FullLayout />,
    children: [
      { path: "/", element: <Navigate to="/starter" /> },
      { path: "/starter", exact: true, element: <Starter /> },
      { path: "/login", exact: true, element: <Login /> },
      { path: "/register", exact: true, element: <Register /> },
      { path: "/deepfake", exact: true, element: <Deepfake /> },
      { path: "/generate", exact: true, element: <Generate /> },
      { path: "/generate/start", exact: true, element: <GenerateStart /> },
      { path: "/generate/projects", exact: true, element: <GenerateList /> },
      { path: "/generate/:project", exact: true, element: <GenerateProject /> },
      { path: "/generate/loading", exact: true, element: <GenerateLoading /> },
      { path: "/detect", exact: true, element: <Detect /> },
      { path: "/detect/start", exact: true, element: <DetectStart /> },
      { path: "/detect/projects", exact: true, element: <DetectList /> },
      { path: "/detect/:project", exact: true, element: <DetectProject /> },
      { path: "/detect/loading", exact: true, element: <DetectLoading /> },
      { path: "/badges", exact: true, element: <Badges /> },
      { path: "/about", exact: true, element: <About /> },
      { path: "/cards", exact: true, element: <Cards /> },
      { path: "/table", exact: true, element: <Tables /> },
      { path: "/forms", exact: true, element: <Forms /> },
      { path: "/mypage", exact: true, element: <Mypage /> },
      { path: "/survey", exact: true, element: <Survey /> },
    ],
  },
];

export default ThemeRoutes;
