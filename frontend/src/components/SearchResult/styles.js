import styled from 'styled-components';

export const ResultWrapper = styled.div`
  margin-top: 1.25rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 1.25rem;
`;

export const ResultItem = styled.div`
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
  cursor: pointer;
  transition:
    transform 0.2s,
    box-shadow 0.2s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }
`;

export const ItemImg = styled.img`
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  background: #eef0f5;
`;

export const Title = styled.div`
  padding: 0.75rem 0.9rem 0;
  font-size: 0.92rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

export const Price = styled.div`
  padding: 0.3rem 0.9rem 0;
  font-size: 1.05rem;
  font-weight: 800;
`;

export const Date = styled.div`
  padding: 0.25rem 0.9rem 0.9rem;
  font-size: 0.78rem;
  color: var(--text-faint);
`;

export const Result = styled.li``;

export const Scroll = styled.div`
  scroll-margin-top: calc(var(--header-h) + 20px);
`;

export const Summary = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.25rem;

  .stat {
    flex: 1 1 200px;
    padding: 1rem 1.25rem;
    border-radius: var(--radius);
    background: var(--surface);
    box-shadow: var(--shadow);
  }
  .stat small {
    display: block;
    color: var(--text-sub);
    font-size: 0.82rem;
    margin-bottom: 0.25rem;
  }
  .stat strong {
    font-size: 1.35rem;
    font-weight: 800;
  }
  .stat.primary {
    background: var(--grad);
    color: #fff;
  }
  .stat.primary small {
    color: rgba(255, 255, 255, 0.8);
  }
`;

export const MarketTag = styled.span`
  align-self: flex-start;
  margin: 0.75rem 0.9rem 0;
  padding: 0.15rem 0.55rem;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 700;
  background: ${p => (p.$sample ? '#f1f2f6' : '#fff1ee')};
  color: ${p => (p.$sample ? 'var(--text-sub)' : 'var(--accent)')};
`;
