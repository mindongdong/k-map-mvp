// 관리자 페이지 컴포넌트
//
// 이 파일에서 구현할 내용:
// 1. 관리자 로그인 폼
// 2. 데이터셋 업로드 폼 (Dataset ID, Group, Data Type, Organ, etc.)
// 3. 파일 업로드 처리 (.csv, .json, .h5ad)
// 4. 상세 기술 메타데이터 동적 입력 필드
// 5. 데이터셋 관리 기능 (생성, 수정, 삭제)
// 6. 인증 상태 관리
//
// 필요한 Hook과 상태:
// - useState: isLoggedIn, loginForm, formData, uploadFiles
// - 폼 상태 관리 및 검증
// - API 호출: adminService.login(), adminService.createDataset() 등
//
// 예시 구조:
// import React, { useState } from 'react';
// import { adminService } from '../services/api';
// import './AdminPage.css';
//
// const AdminPage: React.FC = () => {
//   const [isLoggedIn, setIsLoggedIn] = useState(false);
//   const [loginForm, setLoginForm] = useState({ username: '', password: '' });
//   const [loginError, setLoginError] = useState('');
//
//   const handleLogin = async (e: React.FormEvent) => {
//     // 로그인 처리 로직
//   };
//
//   const handleLogout = () => {
//     // 로그아웃 처리 로직
//   };
//
//   // 로그인하지 않은 경우 로그인 폼 표시
//   if (!isLoggedIn) {
//     return (
//       // 로그인 폼 UI
//     );
//   }
//
//   // 로그인한 경우 관리자 기능 표시
//   return (
//     // 관리자 페이지 UI (데이터 업로드 폼, 관리 기능)
//   );
// };

// TODO: 위 구조를 참고하여 AdminPage 컴포넌트를 구현하세요