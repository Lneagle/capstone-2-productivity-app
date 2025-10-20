import { NavLink } from "react-router-dom";

function NavBar() {
  return (
    <nav className="navbar">
      <NavLink to="/">Dashboard</NavLink>
      <NavLink to="/timesheet">Timesheet</NavLink>
    </nav>
  );
}

export default NavBar;