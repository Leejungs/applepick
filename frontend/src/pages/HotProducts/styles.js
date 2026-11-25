import styled from 'styled-components';

export const Container = styled.div`
  margin-top: 2.5rem;
`;

export const HotTitle = styled.h2`
  margin: 0;
  font-size: 1.4rem;
  font-weight: 800;
`;

export const HotSubText = styled.p`
  margin: 0.25rem 0 1.25rem;
  color: var(--text-sub);
`;

export const HotsWrapper = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 1rem;
`;

export const HotWrapper = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem 1rem 1.25rem;
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);

  &:first-child {
    background: var(--grad);
    color: #fff;
  }
`;

export const HotImg = styled.img`
  width: 110px;
  height: 80px;
  object-fit: contain;
`;

export const HotKeyword = styled.div`
  font-weight: 700;
  text-align: center;
`;

export const TopViewsWrapper = styled.div`
  margin-top: 3rem;
`;

export const MoreBtn = styled.button`
  display: block;
  margin: 1.5rem auto 0;
  padding: 0.8rem 2rem;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: var(--surface);
  font-weight: 700;
  cursor: pointer;
  box-shadow: var(--shadow);

  &:hover {
    color: var(--primary);
    border-color: var(--primary);
  }
`;
