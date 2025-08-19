// 공통 헤더 컴포넌트
//
// 이 파일에서 구현할 내용:
// 1. 상단 네비게이션 바
// 2. 로고 및 프로젝트명
// 3. 메뉴 링크 (데이터셋, 시각화, 관리자)
// 4. 현재 페이지 활성화 표시
// 5. 반응형 디자인
//
// 예시 구조:
// import React from 'react';
// import { Link, useLocation } from 'react-router-dom';
// import './Header.css';
//
// const Header: React.FC = () => {
//   const location = useLocation();
//
//   return (
//     <header className="header">
//       <div className="container">
//         <div className="header-content">
//           <Link to="/" className="logo">
//             <h1>K-map</h1>
//             <span>생물학 데이터 포털</span>
//           </Link>
//           
//           <nav className="nav">
//             <Link 
//               to="/datasets" 
//               className={`nav-link ${location.pathname.startsWith('/datasets') ? 'active' : ''}`}
//             >
//               데이터셋
//             </Link>
//             <Link 
//               to="/visualizations" 
//               className={`nav-link ${location.pathname === '/visualizations' ? 'active' : ''}`}
//             >
//               시각화
//             </Link>
//             <Link 
//               to="/admin" 
//               className={`nav-link ${location.pathname === '/admin' ? 'active' : ''}`}
//             >
//               관리자
//             </Link>
//           </nav>
//         </div>
//       </div>
//     </header>
//   );
// };
//
// export default Header;

// TODO: 위 구조를 참고하여 Header 컴포넌트를 구현하세요