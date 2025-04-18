import React from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';

const Homepage = () => {
  const navigate = useNavigate();

  return (
    <div className="homepage">
      {/* Heading */}
      <h1 className="heading">Valorant Esports Tracker</h1>
      <h2 className="subheading">By Noah & Aldo</h2>

      {/* Central Image */}
      <div className="center-image">
        <img
          src="https://cdn.sanity.io/images/dsfx7636/news/01d2ec8c1f95390cdcc0c7785b82ca998316c782-1920x1080.jpg"
          alt="VCT Teams"
          className="vct-teams-image"
        />
      </div>

      {/* Buttons at the Bottom */}
      <div className="buttons-container">
        <button className="corner-button" onClick={() => navigate('/events')}>
          Events
        </button>
        <button className="corner-button" onClick={() => alert('Navigate to Matches')}>
          Matches
        </button>
        <button className="corner-button" onClick={() => navigate('/stats')}>
          Stats
        </button>
        <button className="corner-button" onClick={() => alert('Navigate to Rankings')}>
          Rankings
        </button>
      </div>
    </div>
  );
};

export default Homepage;