import { useQuery } from '@tanstack/react-query';
import SearchAPI from '../api/search';

// 상품 카탈로그 (백엔드 backend/catalog.py 가 단일 소스)
const useCatalog = () => {
  const query = useQuery({
    queryKey: ['catalog'],
    queryFn: async () => (await SearchAPI.getProducts()).data.categories,
    staleTime: Infinity,
  });
  const categories = query.data || [];
  const products = categories.flatMap(c => c.products);
  return { ...query, categories, products };
};

export default useCatalog;
