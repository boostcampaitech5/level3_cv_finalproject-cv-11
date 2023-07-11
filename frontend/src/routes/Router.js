import { lazy } from "react";
import { Navigate } from "react-router-dom";

/****Layouts*****/
const FullLayout = lazy(() => import("../layouts/FullLayout.js"));

/***** Pages ****/
const Starter = lazy(() => import("../views/Starter.js"));
const Login = lazy(() => import("../views/Login.js"));
const Register = lazy(() => import("../views/Register.js"));
const Generate = lazy(() => import("../views/ui/Generate.js"));
const Generate2 = lazy(() => import("../views/ui/Generate2.js"));
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
      { path: "/generate", exact: true, element: <Generate /> },
      { path: "/generate2", exact: true, element: <Generate2 /> },
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
