import React, { useEffect, useState } from 'react';
import Navbar from './navbar'; // Import the Navbar component
import './styles.css';

const Stats = () => {
  const [stats, setStats] = useState([]); // Original dataset
  const [filteredStats, setFilteredStats] = useState([]); // Filtered dataset
  const [loading, setLoading] = useState(true);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [selectedTeam, setSelectedTeam] = useState('All');
  const [selectedRegion, setSelectedRegion] = useState('All'); // New state for region filter
  const [minRounds, setMinRounds] = useState(0); // New state for minimum rounds filter
  const [statRanges, setStatRanges] = useState({}); // Store dynamic min/max ranges for each stat

  // Function to calculate the color for a stat
  const getColorForStat = (value, min, max, inverse = false) => {
    if (value == null || min == null || max == null || min === max) {
      return { backgroundColor: 'rgb(255, 255, 255)', color: '#000' }; // Default to white background and black text
    }

    let percentage = (value - min) / (max - min);
    if (inverse) {
      percentage = 1 - percentage; // Invert the percentage for inverse logic
    }

    const clampedPercentage = Math.max(0, Math.min(1, percentage)); // Clamp percentage between 0 and 1

    // Define a lighter gradient color palette (light red -> light orange -> light yellow -> light green -> light blue -> light purple)
    const colors = [
      [255, 200, 200], // Light Red
      [255, 220, 180], // Light Orange
      [255, 255, 200], // Light Yellow
      [200, 255, 200], // Light Green
      [200, 220, 255], // Light Blue
      [220, 200, 255], // Light Purple
    ];

    const colorIndex = Math.floor(clampedPercentage * (colors.length - 1));
    const nextColorIndex = Math.min(colorIndex + 1, colors.length - 1);
    const colorStart = colors[colorIndex] || [255, 255, 255]; // Fallback to white
    const colorEnd = colors[nextColorIndex] || [255, 255, 255]; // Fallback to white
    const colorPercentage = (clampedPercentage * (colors.length - 1)) % 1;

    const red = Math.round(colorStart[0] + (colorEnd[0] - colorStart[0]) * colorPercentage);
    const green = Math.round(colorStart[1] + (colorEnd[1] - colorStart[1]) * colorPercentage);
    const blue = Math.round(colorStart[2] + (colorEnd[2] - colorStart[2]) * colorPercentage);

    // Always use black text for readability
    return { backgroundColor: `rgb(${red}, ${green}, ${blue})`, color: '#000' };
  };

  // Function to calculate min and max for each stat dynamically
  const calculateStatRanges = (data) => {
    const ranges = {};
    const statsToCalculate = [
      'rating',
      'acs',
      'kd_ratio',
      'kast',
      'adr',
      'kpr',
      'apr',
      'fkpr',
      'fdpr',
      'hs_percentage',
      'clutch_percentage',
    ];

    statsToCalculate.forEach((stat) => {
      const values = data.map((player) => parseFloat(player[stat])).filter((value) => !isNaN(value));
      ranges[stat] = {
        min: Math.min(...values),
        max: Math.max(...values),
      };
    });

    return ranges;
  };

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/stats');
        const data = await response.json();
        setStats(data); // Set the original dataset
        setFilteredStats(data); // Initialize the filtered dataset
        setStatRanges(calculateStatRanges(data)); // Dynamically calculate ranges
        setLoading(false);
      } catch (error) {
        console.error('Error fetching stats:', error);
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const sortData = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });

    // Always sort from the original filtered dataset
    const sortedStats = [...filteredStats].sort((a, b) => {
      const aValue = a[key] == null || a[key] === '' ? -Infinity : parseFloat(a[key]); // Handle null, undefined, or empty values
      const bValue = b[key] == null || b[key] === '' ? -Infinity : parseFloat(b[key]); // Handle null, undefined, or empty values

      if (aValue < bValue) {
        return direction === 'asc' ? -1 : 1;
      }
      if (aValue > bValue) {
        return direction === 'asc' ? 1 : -1;
      }
      return 0;
    });

    setFilteredStats(sortedStats); // Update the filtered dataset
  };

  const applyFilters = () => {
    const filtered = stats.filter(
      (player) =>
        (selectedTeam === 'All' || player.team === selectedTeam) &&
        (selectedRegion === 'All' || player.region === selectedRegion) &&
        player.rounds_played >= minRounds // Filter by minimum rounds
    );
    setFilteredStats(filtered); // Update the filtered dataset
  };

  useEffect(() => {
    applyFilters(); // Reapply filters whenever filters change
  }, [selectedTeam, selectedRegion, minRounds, stats]);

  // Dynamically calculate available regions and teams
  const availableRegions = [...new Set(stats.map((player) => player.region))].filter(Boolean).sort();
  const availableTeams = [...new Set(stats.map((player) => player.team))].filter(Boolean).sort();

  if (loading) {
    return <div className="loading">Loading stats...</div>;
  }

  return (
    <div className="stats-page">
      <Navbar /> {/* Add the Navbar at the top */}
      <h1 className="heading">Player Stats</h1>

      <div className="filter-container">
        <label htmlFor="team-filter">Filter by Team: </label>
        <select
          id="team-filter"
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
        >
          <option value="All">All</option>
          {availableTeams.map((team, index) => (
            <option key={index} value={team}>
              {team}
            </option>
          ))}
        </select>

        <label htmlFor="region-filter">Filter by Region: </label>
        <select
          id="region-filter"
          value={selectedRegion}
          onChange={(e) => setSelectedRegion(e.target.value)}
        >
          <option value="All">All</option>
          {availableRegions.map((region, index) => (
            <option key={index} value={region}>
              {region.toUpperCase()} {/* Convert region to uppercase */}
            </option>
          ))}
        </select>

        <label htmlFor="min-rounds-filter">Min Rounds: </label>
        <input
          id="min-rounds-filter"
          type="number"
          value={minRounds}
          onChange={(e) => setMinRounds(Number(e.target.value))}
          min="0"
          placeholder="Enter min rounds"
        />
      </div>

      <div className="stats-table-container">
        <table className="stats-table">
          <thead>
            <tr>
              <th onClick={() => sortData('name')}>Player</th>
              <th onClick={() => sortData('team')}>Team</th>
              <th onClick={() => sortData('rounds_played')}>Rounds Played</th>
              <th onClick={() => sortData('rating')}>Rating</th>
              <th onClick={() => sortData('acs')}>ACS</th>
              <th onClick={() => sortData('kd_ratio')}>K/D Ratio</th>
              <th onClick={() => sortData('kast')}>KAST</th>
              <th onClick={() => sortData('adr')}>ADR</th>
              <th onClick={() => sortData('kpr')}>KPR</th>
              <th onClick={() => sortData('apr')}>APR</th>
              <th onClick={() => sortData('fkpr')}>FKPR</th>
              <th onClick={() => sortData('fdpr')}>FDPR</th>
              <th onClick={() => sortData('hs_percentage')}>HS%</th>
              <th onClick={() => sortData('clutch_percentage')}>Clutch%</th>
              <th onClick={() => sortData('region')}>Region</th>
            </tr>
          </thead>
          <tbody>
            {filteredStats.length > 0 ? (
              filteredStats.map((player, index) => (
                <tr key={index}>
                  <td>{player.name}</td>
                  <td>{player.team}</td>
                  <td>{player.rounds_played}</td>
                  <td style={getColorForStat(player.rating, statRanges.rating?.min, statRanges.rating?.max)}>
                    {player.rating}
                  </td>
                  <td style={getColorForStat(player.acs, statRanges.acs?.min, statRanges.acs?.max)}>
                    {player.acs}
                  </td>
                  <td style={getColorForStat(player.kd_ratio, statRanges.kd_ratio?.min, statRanges.kd_ratio?.max)}>
                    {player.kd_ratio}
                  </td>
                  <td style={getColorForStat(parseFloat(player.kast), statRanges.kast?.min, statRanges.kast?.max)}>
                    {player.kast}
                  </td>
                  <td style={getColorForStat(player.adr, statRanges.adr?.min, statRanges.adr?.max)}>
                    {player.adr}
                  </td>
                  <td style={getColorForStat(player.kpr, statRanges.kpr?.min, statRanges.kpr?.max)}>
                    {player.kpr}
                  </td>
                  <td style={getColorForStat(player.apr, statRanges.apr?.min, statRanges.apr?.max)}>
                    {player.apr}
                  </td>
                  <td style={getColorForStat(player.fkpr, statRanges.fkpr?.min, statRanges.fkpr?.max)}>
                    {player.fkpr}
                  </td>
                  <td style={getColorForStat(player.fdpr, statRanges.fdpr?.min, statRanges.fdpr?.max, true)}>
                    {player.fdpr}
                  </td>
                  <td style={getColorForStat(parseFloat(player.hs_percentage), statRanges.hs_percentage?.min, statRanges.hs_percentage?.max)}>
                    {player.hs_percentage}
                  </td>
                  <td style={getColorForStat(parseFloat(player.clutch_percentage), statRanges.clutch_percentage?.min, statRanges.clutch_percentage?.max)}>
                    {player.clutch_percentage}
                  </td>
                  <td>{player.region?.toUpperCase()}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="15">No players found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Stats;