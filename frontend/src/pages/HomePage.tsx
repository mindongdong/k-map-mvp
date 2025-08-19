import React from 'react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
  return (
    <div className="container">
      <h1>K-map</h1>
      <h2>한국인 인체 생물학 데이터 포털</h2>
      <p>
        복잡한 생물학 데이터에 대한 접근성을 높이고, 독자적인 한국인 인체 데이터를 제공하며, 
        최적화된 시각화 경험을 제공합니다.
      </p>
      <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
        <Link to="/datasets" className="btn">
          데이터셋 탐색
        </Link>
        <Link to="/visualization" className="btn btn-secondary">
          시각화 보기
        </Link>
      </div>
    </div>
  );
};

export default HomePage;