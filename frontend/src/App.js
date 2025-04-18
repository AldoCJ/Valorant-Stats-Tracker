import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './homepage'; // Ensure this matches the actual filename
import Stats from './stats'; // Ensure this matches the actual filename
import Events from './events'; // New component for Events
import Matches from './matches'; // New component for Matches
import Rankings from './rankings'; // New component for Rankings

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/stats" element={<Stats />} />
        <Route path="/events" element={<Events />} />
        <Route path="/matches" element={<Matches />} />
        <Route path="/rankings" element={<Rankings />} />
      </Routes>
    </Router>
  );
};

export default App;