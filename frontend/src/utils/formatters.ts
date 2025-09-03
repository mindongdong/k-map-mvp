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
