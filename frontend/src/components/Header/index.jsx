import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import SearchIcon from '@mui/icons-material/Search';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import WhatshotIcon from '@mui/icons-material/Whatshot';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import * as Style from './styles';
import AlarmModal from '../AlarmModal';

const NAV = [
  { path: '/', label: '매물검색', icon: <SearchIcon /> },
  { path: '/pricechart', label: '가격추이', icon: <ShowChartIcon /> },
  { path: '/hotproducts', label: '인기매물', icon: <WhatshotIcon /> },
];

const Header = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const [modalOn, setModalOn] = useState(false);

  const isActive = path =>
    path === '/'
      ? !['/pricechart', '/hotproducts', '/assistant'].includes(pathname)
      : pathname === path;

  return (
    <Style.Container>
      <Style.HeaderWrapper>
        <Style.HeaderHome onClick={() => navigate('/')}>
          <span className="logo">🍎</span>
          ApplePick
          <span className="ko">애플픽</span>
        </Style.HeaderHome>
        <Style.HeaderContents>
          {NAV.map(item => (
            <Style.HeaderContent
              key={item.path}
              $active={isActive(item.path)}
              onClick={() => navigate(item.path)}
            >
              {item.icon}
              <span className="text">{item.label}</span>
            </Style.HeaderContent>
          ))}
          <Style.HeaderContent onClick={() => setModalOn(true)}>
            <NotificationsActiveIcon />
            <span className="text">알림등록</span>
          </Style.HeaderContent>
          <Style.HeaderContent
            className="ai"
            onClick={() => navigate('/assistant')}
          >
            <AutoAwesomeIcon />
            <span className="text">AI 어시스턴트</span>
          </Style.HeaderContent>
        </Style.HeaderContents>
      </Style.HeaderWrapper>
      {modalOn && <AlarmModal onClose={() => setModalOn(false)} />}
    </Style.Container>
  );
};

export default Header;
