import React, { useState, useEffect, useRef } from 'react';
import * as Style from './styles';
import DetailModal from '../DetailModal';
import { formatPrice, formatTimestamp } from '../../utils/format';
import { getThumbnail, MARKET_LABEL } from '../../utils/listing';

// z-score 범위를 벗어난 가격(허위 매물, 부품 판매 등)은 숨긴다
const isReasonablePrice = (value, price) => {
  if (!price || !price.std) return true;
  const z = (value - price.avg_price) / price.std;
  return price.lower_threshold <= z && z <= price.upper_threshold;
};

function SearchResult({ result, price, query }) {
  const invisibleRef = useRef();
  const [detail, setDetail] = useState(null);

  useEffect(() => {
    invisibleRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [query]);

  const items = result.pages
    .flatMap(page => page.result)
    .filter(e => isReasonablePrice(e._source.price, price));

  return (
    <>
      <Style.Scroll ref={invisibleRef} />
      {price?.avg_price > 0 && (
        <Style.Summary>
          <div className="stat primary">
            <small>최근 7일 평균 시세</small>
            <strong>{formatPrice(price.avg_price)}</strong>
          </div>
          <div className="stat">
            <small>최근 7일 최저가</small>
            <strong>{formatPrice(price.min_price)}</strong>
          </div>
          <div className="stat">
            <small>표시 중인 매물</small>
            <strong>{items.length}개</strong>
          </div>
        </Style.Summary>
      )}
      <Style.ResultWrapper>
        {items.map(e => (
          <Style.ResultItem key={e._id} onClick={() => setDetail(e._source)}>
            <Style.ItemImg
              src={getThumbnail(e._source)}
              alt={e._source.title}
              loading="lazy"
              referrerPolicy="no-referrer"
            />
            <Style.MarketTag $sample={e._source.market === 'Sample'}>
              {MARKET_LABEL[e._source.market] || e._source.market}
            </Style.MarketTag>
            <Style.Title>{e._source.title}</Style.Title>
            <Style.Price>{formatPrice(e._source.price)}</Style.Price>
            <Style.Date>{formatTimestamp(e._source.date)}</Style.Date>
          </Style.ResultItem>
        ))}
      </Style.ResultWrapper>
      {detail && (
        <DetailModal detail={detail} onClose={() => setDetail(null)} />
      )}
    </>
  );
}

export default SearchResult;
