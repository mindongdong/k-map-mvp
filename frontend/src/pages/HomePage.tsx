// 홈페이지 컴포넌트
//
// 이 파일에서 구현할 내용:
// 1. 메인 히어로 섹션
// 2. 프로젝트 소개 및 특징
// 3. 빠른 접근 링크 (데이터셋, 시각화, 관리자)
// 4. 반응형 레이아웃
//
// 예시 구조:
// import React from 'react';
// import { Link } from 'react-router-dom';
// import './HomePage.css';
//
// const HomePage: React.FC = () => {
//   return (
//     <div className="home-page">
//       <section className="hero">
//         <div className="hero-content">
//           <h1>K-map</h1>
//           <h2>한국인 인체 생물학 데이터 포털</h2>
//           <p>
//             복잡한 생물학 데이터에 대한 접근성을 높이고, 독자적인 한국인 인체 데이터를 제공하며, 
//             최적화된 시각화 경험을 제공합니다.
//           </p>
//           <div className="hero-buttons">
//             <Link to="/datasets" className="btn btn-primary">
//               데이터셋 탐색
//             </Link>
//             <Link to="/visualizations" className="btn btn-secondary">
//               시각화 보기
//             </Link>
//           </div>
//         </div>
//       </section>
//
//       <section className="features">
//         <div className="container">
//           <h2>주요 특징</h2>
//           <div className="features-grid">
//             <div className="feature-card">
//               <h3>🎯 직관적인 UI/UX</h3>
//               <p>연구자가 필요한 데이터를 복잡한 과정 없이 직관적으로 찾고 접근할 수 있습니다.</p>
//             </div>
//             
//             <div className="feature-card">
//               <h3>🇰🇷 독자적인 데이터셋</h3>
//               <p>다른 곳에서 얻기 힘든 한국인 인체 생물학 데이터를 중심으로 제공합니다.</p>
//             </div>
//             
//             <div className="feature-card">
//               <h3>⚡ 빠른 시각화</h3>
//               <p>데이터베이스 및 렌더링 최적화를 통해 대용량 데이터 시각화의 대기 시간을 최소화합니다.</p>
//             </div>
//           </div>
//         </div>
//       </section>
//
//       <section className="quick-access">
//         <div className="container">
//           <h2>빠른 접근</h2>
//           <div className="quick-access-grid">
//             <Link to="/datasets" className="quick-access-card">
//               <h3>📊 데이터셋</h3>
//               <p>다양한 생물학 데이터셋을 탐색하고 다운로드하세요.</p>
//             </Link>
//             
//             <Link to="/visualizations" className="quick-access-card">
//               <h3>📈 시각화</h3>
//               <p>UMAP, 히트맵 등 다양한 시각화를 통해 데이터를 분석하세요.</p>
//             </Link>
//             
//             <Link to="/admin" className="quick-access-card">
//               <h3>⚙️ 관리자</h3>
//               <p>데이터 업로드 및 관리 기능을 사용하세요.</p>
//             </Link>
//           </div>
//         </div>
//       </section>
//     </div>
//   );
// };
//
// export default HomePage;

// TODO: 위 구조를 참고하여 HomePage 컴포넌트를 구현하세요