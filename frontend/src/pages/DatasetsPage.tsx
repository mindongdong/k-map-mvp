// 데이터셋 목록 페이지 컴포넌트
//
// 이 파일에서 구현할 내용:
// 1. 데이터셋 목록 테이블 (Dataset ID, Group, Data Type, Organ, Status, Publication Date)
// 2. 필터링 기능 (그룹, 데이터 타입, 장기별)
// 3. 검색 기능
// 4. 페이징 처리
// 5. 상세보기 링크
// 6. 로딩 및 에러 상태 처리
//
// 필요한 Hook과 상태:
// - useState: datasets, loading, error, filters
// - useEffect: 데이터 로딩
// - API 호출: datasetService.getDatasets()
//
// 예시 구조:
// import React, { useState, useEffect } from 'react';
// import { Link } from 'react-router-dom';
// import { datasetService } from '../services/api';
// import { Dataset } from '../types/api';
// import './DatasetsPage.css';
//
// const DatasetsPage: React.FC = () => {
//   const [datasets, setDatasets] = useState<Dataset[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);
//   const [filters, setFilters] = useState({
//     group: '',
//     data_type: '',
//     organ: '',
//     search: ''
//   });
//
//   useEffect(() => {
//     fetchDatasets();
//   }, [filters]);
//
//   const fetchDatasets = async () => {
//     // API 호출 로직
//   };
//
//   const handleFilterChange = (key: string, value: string) => {
//     // 필터 변경 로직
//   };
//
//   // 렌더링 로직 (테이블, 필터 UI, 로딩/에러 상태)
// };

// TODO: 위 구조를 참고하여 DatasetsPage 컴포넌트를 구현하세요