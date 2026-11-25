import React from 'react';
import { useNavigate } from 'react-router-dom';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import SearchIcon from '@mui/icons-material/Search';
import * as Style from './styles';

function Introduction() {
  const navigate = useNavigate();
  return (
    <Style.BoxWrapper>
      <Style.TextWrapper>
        <span className="badge">✨ 중고 애플 통합 검색 · AI 거래 도우미</span>
        <Style.MainText>
          흩어진 중고 매물,
          <br />
          <em>한 번에 찾고 AI에게</em> 물어보세요
        </Style.MainText>
        <Style.SubText>
          여러 중고 마켓의 애플 매물을 모아 시세와 추이를 보여주고, AI
          어시스턴트가 좋은 거래인지 판단해 드려요.
        </Style.SubText>
        <div className="actions">
          <Style.CtaButton
            $primary
            onClick={() =>
              document
                .getElementById('categories')
                ?.scrollIntoView({ behavior: 'smooth' })
            }
          >
            <SearchIcon fontSize="small" /> 매물 검색하기
          </Style.CtaButton>
          <Style.CtaButton onClick={() => navigate('/assistant')}>
            <AutoAwesomeIcon fontSize="small" /> AI에게 물어보기
          </Style.CtaButton>
        </div>
      </Style.TextWrapper>
      <Style.SvgWrapper $w="380">
        <svg viewBox="0 0 420 420" xmlns="http://www.w3.org/2000/svg">
          <linearGradient id="linearColors" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#b8b3ff"></stop>
            <stop offset="50%" stopColor="#8e4ec6"></stop>
            <stop offset="100%" stopColor="#ff9e8f"></stop>
          </linearGradient>
          <circle
            r="190"
            cx="210"
            cy="210"
            strokeWidth="8"
            fill="rgba(255,255,255,0.04)"
            stroke="url(#linearColors)"
          ></circle>
          <image x="30" y="30" width="100" href="/images/introduceIphone.png" />
          <image
            x="250"
            y="300"
            width="150"
            href="/images/introduceMacbook.png"
          />
          <image x="250" y="0" width="175" href="/images/introduceWatch.png" />
        </svg>
      </Style.SvgWrapper>
    </Style.BoxWrapper>
  );
}

export default Introduction;
