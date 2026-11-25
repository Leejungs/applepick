import Slider from 'react-slick';
import styled from 'styled-components';

export const Container = styled.div`
  width: 100%;
  background: #0f1020;
  border-radius: 24px 24px 0 0;
  overflow: hidden;
`;

export const StyledSlider = styled(Slider)`
  .slick-dots {
    bottom: 10px;
  }
  .slick-dots li button:before {
    color: #fff;
  }
  .slick-prev,
  .slick-next {
    z-index: 1;
  }
  .slick-prev {
    left: 12px;
  }
  .slick-next {
    right: 12px;
  }
`;

export const CardBox = styled.div``;

export const CardImg = styled.img`
  display: block;
  margin: auto;
  width: 100%;
  height: 420px;
  object-fit: contain;
`;
