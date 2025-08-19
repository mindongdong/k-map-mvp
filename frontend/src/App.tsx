// 메인 App 컴포넌트
//
// 이 파일에서 구현할 내용:
// 1. React Router 설정
// 2. 전체 레이아웃 구조
// 3. 라우트 정의 (홈, 데이터셋, 시각화, 관리자)
// 4. 공통 컴포넌트 배치 (Header, Footer)
//
// 예시 구조:
// import React from 'react';
// import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import './App.css';
//
// // 컴포넌트 임포트
// import Header from './components/Layout/Header';
// import Footer from './components/Layout/Footer';
// import HomePage from './pages/HomePage';
// import DatasetsPage from './pages/DatasetsPage';
// import DatasetDetailPage from './pages/DatasetDetailPage';
// import VisualizationPage from './pages/VisualizationPage';
// import AdminPage from './pages/AdminPage';
//
// function App() {
//   return (
//     <Router>
//       <div className="App">
//         <Header />
//         <main className="main-content">
//           <Routes>
//             <Route path="/" element={<HomePage />} />
//             <Route path="/datasets" element={<DatasetsPage />} />
//             <Route path="/datasets/:datasetId" element={<DatasetDetailPage />} />
//             <Route path="/visualizations" element={<VisualizationPage />} />
//             <Route path="/admin" element={<AdminPage />} />
//           </Routes>
//         </main>
//         <Footer />
//       </div>
//     </Router>
//   );
// }
//
// export default App;

// TODO: 위 구조를 참고하여 App 컴포넌트를 구현하세요