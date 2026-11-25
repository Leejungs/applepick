import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import SearchAPI from '../../api/search';
import * as Style from './styles';
import PriceChart from '../../components/PriceChart';
import useCatalog from '../../query/useCatalog';

function ProductPriceChart() {
  const { products } = useCatalog();
  const [selected, setSelected] = useState('');
  const key = selected || products[0]?.key;

  const { data } = useQuery({
    queryKey: ['weekly', key],
    queryFn: async () => (await SearchAPI.searchWeeklyPriceQuery(key)).data,
    enabled: !!key,
  });

  return (
    <Style.Container>
      <Style.GuideText>
        상품을 선택하면, 해당 최근 한달의 가격 추이가 나타납니다.
      </Style.GuideText>
      <Style.SelectBox
        name="keyword"
        value={key || ''}
        onChange={e => setSelected(e.target.value)}
      >
        {products.map(item => (
          <option key={item.key} value={item.key}>
            {item.label}
          </option>
        ))}
      </Style.SelectBox>
      <PriceChart result={data} />
    </Style.Container>
  );
}

export default ProductPriceChart;
