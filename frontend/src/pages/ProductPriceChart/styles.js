import styled from 'styled-components';

export const Container = styled.div`
  margin-top: 2.5rem;
  padding: 1.75rem;
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
`;

export const GuideText = styled.p`
  margin: 0 0 1rem;
  font-size: 1.05rem;
  font-weight: 700;

  &::before {
    content: '📈 ';
  }
`;

export const SelectBox = styled.select`
  min-width: 260px;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--line);
  background: #fafbfd;
  font-size: 0.95rem;
  font-weight: 600;
`;
