import React, { useEffect, useState } from 'react';
import { useInView } from 'react-intersection-observer';
import * as Style from './styles';
import LoadingSign from '../LoadingSign';
import SearchAPI from '../../api/search';
import SearchResult from '../SearchResult';
import useSearchQuery from '../../query/useSearchQuery';
import useCatalog from '../../query/useCatalog';

const PRICE_SAMPLE_SIZE = 100;

function ProductList({ keyword }) {
  const { categories } = useCatalog();
  const [price, setPrice] = useState(null);
  const [item, setItem] = useState('');

  const products =
    categories.find(category => category.param === keyword)?.products || [];

  // 카테고리가 바뀌면 선택 초기화
  useEffect(() => {
    setItem('');
    setPrice(null);
  }, [keyword]);

  const { data, isFetching, isError, fetchNextPage, hasNextPage } =
    useSearchQuery(item);

  const { ref, inView } = useInView({ threshold: 0.7 });

  // 화면 하단 observer 가 보이면 다음 페이지
  useEffect(() => {
    if (inView && hasNextPage && !isFetching) fetchNextPage();
  }, [inView, hasNextPage, isFetching, fetchNextPage]);

  const select = async key => {
    setItem(key);
    setPrice(null);
    const response = await SearchAPI.searchPriceQuery(key, PRICE_SAMPLE_SIZE);
    setPrice(response.data);
  };

  const isEmpty = data && data.pages.every(page => page.result.length === 0);

  return (
    <Style.Container>
      <Style.ItemWrapper>
        {products.map(product => (
          <Style.ItemBtn
            $isClicked={item === product.key}
            key={product.key}
            onClick={() => select(product.key)}
          >
            {product.label}
          </Style.ItemBtn>
        ))}
      </Style.ItemWrapper>

      {isError && <Style.Message>매물을 불러오지 못했습니다.</Style.Message>}
      {isEmpty && <Style.Message>아직 수집된 매물이 없습니다.</Style.Message>}
      {data && price && !isEmpty && (
        <SearchResult result={data} price={price} query={item} />
      )}
      <Style.Observer ref={ref}>
        <LoadingSign loading={!!item && isFetching} />
      </Style.Observer>
    </Style.Container>
  );
}

export default ProductList;
