// 데이터 포맷팅 유틸리티 함수
//
// 이 파일에서 구현할 내용:
// 1. 날짜 포맷팅 함수
// 2. 파일 크기 포맷팅 함수
// 3. 숫자 포맷팅 함수
// 4. 상태 표시 함수
// 5. 문자열 유틸리티 함수
//
// 예시 구조:
// // 날짜 포맷팅
// export function formatDate(date: string | Date, locale: string = 'ko-KR'): string {
//   const dateObj = typeof date === 'string' ? new Date(date) : date;
//   return dateObj.toLocaleDateString(locale);
// }
//
// export function formatDateTime(date: string | Date, locale: string = 'ko-KR'): string {
//   const dateObj = typeof date === 'string' ? new Date(date) : date;
//   return dateObj.toLocaleString(locale);
// }
//
// // 파일 크기 포맷팅
// export function formatFileSize(bytes: number): string {
//   if (bytes === 0) return '0 Bytes';
//   
//   const k = 1024;
//   const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
//   const i = Math.floor(Math.log(bytes) / Math.log(k));
//   
//   return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
// }
//
// // 숫자 포맷팅
// export function formatNumber(num: number, locale: string = 'ko-KR'): string {
//   return num.toLocaleString(locale);
// }
//
// // 상태 한국어 변환
// export function formatStatus(status: string): string {
//   const statusMap: Record<string, string> = {
//     'active': '활성',
//     'inactive': '비활성',
//     'pending': '대기중',
//     'processing': '처리중',
//     'completed': '완료',
//     'failed': '실패'
//   };
//   
//   return statusMap[status] || status;
// }
//
// // 문자열 자르기
// export function truncateString(str: string, maxLength: number): string {
//   if (str.length <= maxLength) return str;
//   return str.substring(0, maxLength) + '...';
// }
//
// // 검색어 하이라이트
// export function highlightSearchTerm(text: string, searchTerm: string): string {
//   if (!searchTerm) return text;
//   
//   const regex = new RegExp(`(${searchTerm})`, 'gi');
//   return text.replace(regex, '<mark>$1</mark>');
// }

// TODO: 위 구조를 참고하여 포맷팅 유틸리티를 구현하세요