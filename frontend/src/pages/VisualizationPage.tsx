// 시각화 페이지 컴포넌트
//
// 이 파일에서 구현할 내용:
// 1. 시각화 유형 선택 UI (UMAP, 히트맵, 박스플롯)
// 2. Plotly.js를 사용한 인터랙티브 차트 렌더링
// 3. 차트 전환 기능
// 4. 시각화별 설명 정보
// 5. 로딩 및 에러 상태 처리
//
// 필요한 라이브러리:
// - react-plotly.js: Plotly 차트 컴포넌트
// - plotly.js: 차트 라이브러리
//
// 필요한 Hook과 상태:
// - useState: activeChart, chartData, loading, error
// - useEffect: 차트 데이터 로딩
// - API 호출: visualizationService.getUmapVisualization() 등
//
// 예시 구조:
// import React, { useState, useEffect } from 'react';
// import Plot from 'react-plotly.js';
// import { visualizationService } from '../services/api';
// import './VisualizationPage.css';
//
// type ChartType = 'umap' | 'heatmap' | 'boxplot';
//
// const VisualizationPage: React.FC = () => {
//   const [activeChart, setActiveChart] = useState<ChartType>('umap');
//   const [chartData, setChartData] = useState<any>(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState<string | null>(null);
//
//   useEffect(() => {
//     loadVisualization(activeChart);
//   }, [activeChart]);
//
//   const loadVisualization = async (chartType: ChartType) => {
//     // API 호출 및 차트 데이터 로딩 로직
//   };
//
//   const chartOptions = [
//     { id: 'umap', label: 'UMAP Scatter Plot', description: '세포 타입별 분포 시각화' },
//     { id: 'heatmap', label: '계층적 클러스터링 히트맵', description: '유전자 발현량 패턴' },
//     { id: 'boxplot', label: '조직별 유전자 발현', description: '조직별 발현량 분포' },
//   ];
//
//   // 렌더링 로직 (차트 선택 UI, Plotly 차트, 정보 섹션)
// };

// TODO: 위 구조를 참고하여 VisualizationPage 컴포넌트를 구현하세요