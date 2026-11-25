import React, { useState } from 'react';
import * as Style from './styles';
import DetailModal from '../DetailModal';
import { formatPrice, formatTimestamp } from '../../utils/format';
import { getThumbnail } from '../../utils/listing';

function TopViews({ result }) {
  const [detail, setDetail] = useState(null);

  return (
    <Style.TopViewWrapper>
      {result.map(e => (
        <Style.TopViewItem key={e._id} onClick={() => setDetail(e._source)}>
          <Style.ProductImg
            src={getThumbnail(e._source)}
            alt={e._source.title}
            loading="lazy"
            referrerPolicy="no-referrer"
          />
          <Style.TextWrapper>
            <Style.TextTitle>{e._source.title}</Style.TextTitle>
            <Style.TextPrice>{formatPrice(e._source.price)}</Style.TextPrice>
            <Style.TextDateLocale>
              {[e._source.region, formatTimestamp(e._source.date)]
                .filter(Boolean)
                .join(', ')}{' '}
              · 조회 {e._source.views}
            </Style.TextDateLocale>
            <Style.TextDesc>{e._source.desc}</Style.TextDesc>
          </Style.TextWrapper>
        </Style.TopViewItem>
      ))}
      {detail && (
        <DetailModal detail={detail} onClose={() => setDetail(null)} />
      )}
    </Style.TopViewWrapper>
  );
}

export default TopViews;
