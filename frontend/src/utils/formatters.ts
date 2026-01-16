export function formatDate(
  date: string | Date,
  locale: string = "ko-KR",
): string {
  const dateObj = typeof date === "string" ? new Date(date) : date;
  return dateObj.toLocaleDateString(locale);
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

export function formatStatus(status: string): string {
  const statusMap: Record<string, string> = {
    Published: "출판됨",
    "In Review": "검토중",
    Draft: "초안",
  };

  return statusMap[status] || status;
}

/**
 * 숫자를 천 단위 구분자와 함께 포맷팅
 */
export function formatNumber(num: number): string {
  return num.toLocaleString("ko-KR");
}

/**
 * 데이터셋 ID를 표시용 포맷으로 변환
 * 예: "dataset_001" -> "DS-001"
 */
export function formatDatasetId(id: string): string {
  const match = id.match(/(\d+)/);
  if (match) {
    const num = match[1].padStart(3, "0");
    return `DS-${num}`;
  }
  return id;
}

/**
 * 상대 시간 포맷팅 (예: "3일 전", "방금 전")
 */
export function formatRelativeTime(date: string | Date): string {
  const dateObj = typeof date === "string" ? new Date(date) : date;
  const now = new Date();
  const diff = now.getTime() - dateObj.getTime();

  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) return `${days}일 전`;
  if (hours > 0) return `${hours}시간 전`;
  if (minutes > 0) return `${minutes}분 전`;
  return "방금 전";
}
