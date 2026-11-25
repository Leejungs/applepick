import styled from 'styled-components';
import { NavLink } from 'react-router-dom';

export const Container = styled.div`
  animation: show 0.4s ease-out;
  @keyframes show {
    from {
      transform: translateY(12px);
      opacity: 0;
    }
    to {
      transform: none;
      opacity: 1;
    }
  }
`;

export const SectionTitle = styled.h2`
  margin: 3rem 0 0.25rem;
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.02em;

  & + p {
    margin: 0 0 1.25rem;
    color: var(--text-sub);
  }
`;

export const ListWrapper = styled.div`
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1rem;

  @media (max-width: 1000px) {
    grid-template-columns: repeat(3, 1fr);
  }
  @media (max-width: 520px) {
    grid-template-columns: repeat(2, 1fr);
  }
`;

export const ProductItem = styled(NavLink)`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6rem;
  padding: 1.25rem 0.75rem 1rem;
  border-radius: var(--radius);
  background: var(--surface);
  border: 2px solid transparent;
  box-shadow: var(--shadow);
  text-decoration: none;
  color: var(--text);
  font-size: 0.95rem;
  font-weight: 700;
  transition:
    transform 0.2s,
    box-shadow 0.2s,
    border-color 0.2s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }

  &.active {
    border-color: var(--primary);
    background: linear-gradient(180deg, #fff 0%, var(--primary-soft) 100%);
    color: var(--primary);
  }
`;

export const ProductImg = styled.img`
  width: 100%;
  max-width: 120px;
  height: 78px;
  object-fit: contain;
`;

export const ScrollToTop = styled.button`
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  z-index: 40;
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 1px solid var(--line);
  background: var(--surface);
  box-shadow: var(--shadow);
  cursor: pointer;
`;
