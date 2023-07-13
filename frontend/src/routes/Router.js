import { lazy } from "react";
import { Navigate } from "react-router-dom";

/****Layouts*****/
const FullLayout = lazy(() => import("../layouts/FullLayout.js"));

/***** Pages ****/
const Starter = lazy(() => import("../views/Starter.js"));
const Login = lazy(() => import("../views/Login.js"));
const Register = lazy(() => import("../views/Register.js"));
const Deepfake = lazy(() => import("../views/ui/Deepfake.js"));
const Generate = lazy(() => import("../views/ui/Generate.js"));
const GenerateStart = lazy(() => import("../views/ui/GenerateStart.js"));
const GenerateList = lazy(() => import("../views/ui/GenerateList.js"));
const GenerateProject = lazy(() => import("../views/ui/GenerateProject.js"));
const Detect = lazy(() => import("../views/ui/Detect.js"));
const Loading = lazy(() => import("../views/ui/Loading.js"));
const Badges = lazy(() => import("../views/ui/Badges"));
const Buttons = lazy(() => import("../views/ui/Buttons"));
const Cards = lazy(() => import("../views/ui/Cards"));
const Grid = lazy(() => import("../views/ui/Grid"));
const Tables = lazy(() => import("../views/ui/Tables"));
const Forms = lazy(() => import("../views/ui/Forms"));
const Breadcrumbs = lazy(() => import("../views/ui/Breadcrumbs"));

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
      { path: "/generate/:project/loading", exact: true, element: <Loading /> },
      { path: "/detect", exact: true, element: <Detect /> },
      { path: "/loading", exact: true, element: <Loading /> },
      { path: "/badges", exact: true, element: <Badges /> },
      { path: "/buttons", exact: true, element: <Buttons /> },
      { path: "/cards", exact: true, element: <Cards /> },
      { path: "/grid", exact: true, element: <Grid /> },
      { path: "/table", exact: true, element: <Tables /> },
      { path: "/forms", exact: true, element: <Forms /> },
      { path: "/breadcrumbs", exact: true, element: <Breadcrumbs /> },
    ],
  },
];

export default ThemeRoutes;
