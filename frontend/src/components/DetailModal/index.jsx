import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import CloseIcon from '@mui/icons-material/Close';
import * as Style from './styles';
import Carousel from '../Carousel';
import { formatPrice, formatTimestamp } from '../../utils/format';
import { getImages, getListingUrl, MARKET_LABEL } from '../../utils/listing';

function DetailModal({ detail, onClose }) {
  // detail = {market, pid, url, title, desc, price, date, pictures, region, views, keyword}
  const outModal = useRef();
  const images = getImages(detail);
  const url = getListingUrl(detail);

  useEffect(() => {
    document.body.style.overflow = 'hidden';
    const onKey = e => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = 'visible';
      window.removeEventListener('keydown', onKey);
    };
  }, [onClose]);

  return createPortal(
    <Style.Background
      ref={outModal}
      onClick={e => outModal.current === e.target && onClose()}
    >
      <Style.Content>
        {images.length > 0 && <Carousel title={detail.title} images={images} />}
        <Style.Main>
          <Style.TitleLinkWrapper>
            <Style.Title>{detail.title}</Style.Title>
            {url ? (
              <Style.HyperLink
                href={url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {MARKET_LABEL[detail.market] || detail.market}에서 보기
              </Style.HyperLink>
            ) : (
              <span>{MARKET_LABEL[detail.market] || detail.market}</span>
            )}
          </Style.TitleLinkWrapper>
          <Style.InfoWrapper>
            <Style.Price>{formatPrice(detail.price)}</Style.Price>
            <Style.UploadDate>{formatTimestamp(detail.date)}</Style.UploadDate>
            <Style.Region>{detail.region}</Style.Region>
          </Style.InfoWrapper>
          <Style.Desc>{detail.desc}</Style.Desc>
        </Style.Main>
        <Style.CloseBtn aria-label="닫기">
          <CloseIcon
            fontSize="large"
            sx={{ color: 'white' }}
            onClick={onClose}
          />
        </Style.CloseBtn>
      </Style.Content>
    </Style.Background>,
    document.getElementById('modal'),
  );
}

export default DetailModal;
