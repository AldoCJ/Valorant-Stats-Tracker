import React from 'react';
import { Link } from 'react-router-dom';
import './styles.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">
          <img src="vct_logo.png" alt="Home Logo" className="logo-image" />
        </Link>
      </div>
      <ul className="navbar-menu">
        <li>
          <Link to="/stats">Stats</Link>
        </li>
        <li>
          <Link to="/events">Events</Link>
        </li>
        <li>
          <Link to="/matches">Matches</Link>
        </li>
        <li>
          <Link to="/rankings">Rankings</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;