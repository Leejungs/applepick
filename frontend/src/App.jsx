import {
  BrowserRouter,
  Routes,
  Route,
  useLocation,
  useNavigate,
} from 'react-router-dom';
import styled from 'styled-components';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import './styles.css';
import Header from './components/Header';
import Introduction from './components/Introduction';
import Main from './pages/Main';
import ProductPriceChart from './pages/ProductPriceChart';
import HotProducts from './pages/HotProducts';
import Assistant from './pages/Assistant';

const Fab = styled.button`
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 60;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.9rem 1.2rem;
  border: 0;
  border-radius: 999px;
  background: var(--grad);
  color: #fff;
  font-weight: 700;
  font-size: 0.95rem;
  box-shadow: 0 10px 30px rgba(91, 91, 214, 0.45);
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-3px);
  }
`;

function Layout() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const isAssistant = pathname === '/assistant';

  return (
    <>
      <Header />
      {!isAssistant && <Introduction />}
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/assistant" element={<Assistant />} />
        <Route path="/pricechart" element={<ProductPriceChart />} />
        <Route path="/hotproducts" element={<HotProducts />} />
        <Route path="/:keyword" element={<Main />} />
      </Routes>
      {!isAssistant && (
        <Fab onClick={() => navigate('/assistant')}>
          <AutoAwesomeIcon fontSize="small" /> AI에게 물어보기
        </Fab>
      )}
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}

export default App;
