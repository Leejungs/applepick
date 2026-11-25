import styled from 'styled-components';

export const TopViewWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
`;

export const TopViewItem = styled.div`
  display: flex;
  gap: 1rem;
  padding: 0.9rem;
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
  cursor: pointer;
  transition:
    transform 0.2s,
    box-shadow 0.2s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }
`;

export const ProductImg = styled.img`
  width: 120px;
  height: 120px;
  flex-shrink: 0;
  object-fit: cover;
  border-radius: 12px;
  background: #eef0f5;
`;

export const TextWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  min-width: 0;
`;

export const TextTitle = styled.div`
  font-size: 1rem;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

export const TextPrice = styled.div`
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--primary);
`;

export const TextDateLocale = styled.div`
  font-size: 0.8rem;
  color: var(--text-faint);
`;

export const TextDesc = styled.div`
  font-size: 0.88rem;
  color: var(--text-sub);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;
