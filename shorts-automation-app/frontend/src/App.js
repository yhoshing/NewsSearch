import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

import Dashboard from './pages/Dashboard';
import Channels from './pages/Channels';
import ChannelDetail from './pages/ChannelDetail';
import Ideas from './pages/Ideas';
import Videos from './pages/Videos';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-logo">
              🎬 Shorts Automation
            </Link>
            <ul className="nav-menu">
              <li className="nav-item">
                <Link to="/" className="nav-link">대시보드</Link>
              </li>
              <li className="nav-item">
                <Link to="/channels" className="nav-link">채널 관리</Link>
              </li>
              <li className="nav-item">
                <Link to="/ideas" className="nav-link">아이디어</Link>
              </li>
              <li className="nav-item">
                <Link to="/videos" className="nav-link">비디오</Link>
              </li>
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/channels" element={<Channels />} />
            <Route path="/channels/:id" element={<ChannelDetail />} />
            <Route path="/ideas" element={<Ideas />} />
            <Route path="/videos" element={<Videos />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
