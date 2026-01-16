import { useState, useEffect, useCallback } from "react";

export function useApi<T>(apiCall: () => Promise<T>, dependencies: any[] = []) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiCall();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "오류가 발생했습니다");
    } finally {
      setLoading(false);
    }
  }, [apiCall]);

  useEffect(() => {
    fetchData();
  }, dependencies);

  const refetch = useCallback(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch };
}

export function useMutation<T, P>(
  mutationFn: (params: P) => Promise<T>
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = useCallback(
    async (params: P) => {
      try {
        setLoading(true);
        setError(null);
        const result = await mutationFn(params);
        setData(result);
        return result;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "오류가 발생했습니다";
        setError(errorMessage);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [mutationFn]
  );

  const reset = useCallback(() => {
    setData(null);
    setError(null);
  }, []);

  return { mutate, data, loading, error, reset };
}

export function usePagination<T>(
  fetchFn: (page: number, pageSize: number) => Promise<{ data: T[]; total: number }>,
  initialPageSize: number = 20
) {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(initialPageSize);
  const [data, setData] = useState<T[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const result = await fetchFn(page, pageSize);
      setData(result.data);
      setTotal(result.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "오류가 발생했습니다");
    } finally {
      setLoading(false);
    }
  }, [fetchFn, page, pageSize]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const totalPages = Math.ceil(total / pageSize);
  const hasNextPage = page < totalPages;
  const hasPrevPage = page > 1;

  return {
    data,
    loading,
    error,
    page,
    pageSize,
    total,
    totalPages,
    hasNextPage,
    hasPrevPage,
    setPage,
    setPageSize,
    refetch: fetchData,
  };
}
