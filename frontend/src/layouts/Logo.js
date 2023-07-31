import { Link } from "react-router-dom";
import aivengers from '../assets/images/logos/logo.JPG';

const Logo = () => {
  return (
    <Link to="/">
      <img src={aivengers} alt="Logo" width="180" height="50" />
    </Link>
  );
};

export default Logo;
