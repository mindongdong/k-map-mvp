// 데이터셋 상세 페이지 컴포넌트
//
// 이 파일에서 구현할 내용:
// 1. 데이터셋 상세 정보 표시 (요약, 설명, 메타데이터)
// 2. 파일 목록 및 다운로드 기능
// 3. 인용 정보 표시
// 4. 상세 기술 메타데이터 테이블
// 5. 브레드크럼 네비게이션
// 6. 로딩 및 에러 상태 처리
//
// URL 파라미터: /datasets/:datasetId
//
// 필요한 Hook과 상태:
// - useParams: datasetId 추출
// - useState: dataset, loading, error
// - useEffect: 데이터 로딩
// - API 호출: datasetService.getDataset(), datasetService.downloadFile()
//
// 예시 구조:
// import React, { useState, useEffect } from 'react';
// import { useParams, Link } from 'react-router-dom';
// import { datasetService } from '../services/api';
// import { Dataset } from '../types/api';
//
// const DatasetDetailPage: React.FC = () => {
//   const { datasetId } = useParams<{ datasetId: string }>();
//   const [dataset, setDataset] = useState<Dataset | null>(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);
//
//   useEffect(() => {
//     if (datasetId) {
//       fetchDataset(datasetId);
//     }
//   }, [datasetId]);
//
//   const fetchDataset = async (id: string) => {
//     // API 호출 로직
//   };
//
//   const handleDownload = async (fileName: string) => {
//     // 파일 다운로드 로직
//   };
//
//   // 렌더링 로직 (상세 정보, 파일 테이블, 메타데이터)
// };

// TODO: 위 구조를 참고하여 DatasetDetailPage 컴포넌트를 구현하세요