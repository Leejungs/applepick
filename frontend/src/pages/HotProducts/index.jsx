import React from 'react';
import { useInfiniteQuery, useQuery } from '@tanstack/react-query';
import * as Style from './styles';
import HotAPI from '../../api/hot';
import SearchAPI from '../../api/search';
import TopViews from '../../components/TopViews';
import useCatalog from '../../query/useCatalog';

const HOT_COUNT = 5;
const RECENT_PAGE_SIZE = 5;

function HotProducts() {
  const { categories } = useCatalog();

  const { data: hotProducts = {} } = useQuery({
    queryKey: ['hot', HOT_COUNT],
    queryFn: async () => (await HotAPI.getHotProducts(HOT_COUNT)).data,
  });

  const recent = useInfiniteQuery({
    queryKey: ['recent'],
    queryFn: async ({ pageParam }) =>
      (await SearchAPI.searchRecentQuery(pageParam)).data.result,
    initialPageParam: 0,
    getNextPageParam: (lastPage, pages) =>
      lastPage.length < RECENT_PAGE_SIZE ? undefined : pages.length,
  });

  // 상품 키 -> 카테고리 대표 이미지
  const categoryOf = key =>
    categories.find(c => c.products.some(p => p.key === key));

  const topViews = recent.data?.pages.flat() || [];

  return (
    <Style.Container>
      <Style.HotTitle>Hot Search</Style.HotTitle>
      <Style.HotSubText>
        해당 사이트에서 많이 검색된 제품들입니다.
      </Style.HotSubText>
      <Style.HotsWrapper>
        {Object.keys(hotProducts).length === 0 && (
          <Style.HotSubText>아직 검색 기록이 없습니다.</Style.HotSubText>
        )}
        {Object.keys(hotProducts).map((key, index) => {
          const category = categoryOf(key);
          const label = category?.products.find(p => p.key === key)?.label;
          return (
            <Style.HotWrapper key={key}>
              <Style.HotImg
                src={`/images/${category?.param || 'null_image'}.png`}
              />
              <Style.HotKeyword>
                {index + 1}. {label || key}
              </Style.HotKeyword>
            </Style.HotWrapper>
          );
        })}
      </Style.HotsWrapper>
      <Style.TopViewsWrapper>
        <Style.HotTitle>Top Views</Style.HotTitle>
        <Style.HotSubText>
          최근 7일 게시글 중, 조회수가 많은 매물입니다.
        </Style.HotSubText>
        <TopViews result={topViews} />
      </Style.TopViewsWrapper>
      {recent.hasNextPage && (
        <Style.MoreBtn
          onClick={() => recent.fetchNextPage()}
          disabled={recent.isFetchingNextPage}
        >
          더보기
        </Style.MoreBtn>
      )}
    </Style.Container>
  );
}

export default HotProducts;
