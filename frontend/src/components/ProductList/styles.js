import styled from 'styled-components';

export const Container = styled.div`
  width: 100%;
  margin-top: 2rem;
`;

export const ItemWrapper = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 1.25rem;
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
`;

export const ItemBtn = styled.button`
  padding: 0.6rem 1rem;
  border-radius: 999px;
  border: 1px solid ${p => (p.$isClicked ? 'transparent' : 'var(--line)')};
  background: ${p => (p.$isClicked ? 'var(--grad)' : 'var(--surface)')};
  color: ${p => (p.$isClicked ? '#fff' : 'var(--text)')};
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  box-shadow: ${p => (p.$isClicked ? '0 4px 12px rgba(91,91,214,.35)' : 'none')};

  &:hover {
    border-color: var(--primary);
    color: ${p => (p.$isClicked ? '#fff' : 'var(--primary)')};
  }
`;

export const Observer = styled.div`
  width: 100%;
  min-height: 10px;
`;

export const Message = styled.p`
  width: 100%;
  margin: 3rem 0;
  text-align: center;
  color: var(--text-sub);
`;
