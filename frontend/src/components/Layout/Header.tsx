import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="container">
        <Link to="/" className="logo">
          <h1>K-map</h1>
        </Link>
        <nav>
          <Link to="/datasets">Datasets</Link>
          <Link to="/visualization">Visualization</Link>
          <Link to="/admin">Admin</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;