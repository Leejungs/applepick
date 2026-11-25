import { useInfiniteQuery } from '@tanstack/react-query';
import SearchAPI from '../api/search';

const PAGE_SIZE = 20;

const useSearchQuery = item =>
  useInfiniteQuery({
    queryKey: ['search', item],
    queryFn: async ({ pageParam }) => {
      const { data } = await SearchAPI.searchPageQuery(item, pageParam);
      return { result: data.result || [], page: pageParam };
    },
    initialPageParam: 0,
    getNextPageParam: lastPage =>
      lastPage.result.length < PAGE_SIZE ? undefined : lastPage.page + 1,
    enabled: !!item,
    gcTime: 60 * 1000,
  });

export default useSearchQuery;
