import styled from 'styled-components';
export { Background, CloseBtn } from '../DetailModal/styles';

export const Content = styled.div`
  position: relative;
  width: 100%;
  max-width: 440px;
  border-radius: 24px;
  background: var(--surface);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
`;

export const AlarmWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 2rem 1.75rem 1.75rem;
`;

export const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.35rem;
  font-weight: 800;

  &::before {
    content: '🔔';
  }
`;

export const GuideText = styled.p`
  margin: 0 0 0.5rem;
  color: var(--text-sub);
  font-size: 0.92rem;
`;

export const InputWrapper = styled.div``;

export const InputItem = styled.input`
  width: 100%;
  padding: 0.85rem 1rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--line);
  background: #fafbfd;
  font-size: 0.95rem;
  outline: none;

  &:focus {
    border-color: var(--primary);
    background: #fff;
    box-shadow: 0 0 0 3px var(--primary-soft);
  }
`;

export const SelectBox = styled.select`
  width: 100%;
  padding: 0.85rem 1rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--line);
  background: #fafbfd;
  font-size: 0.95rem;
`;

export const SubmitBtn = styled.button`
  margin-top: 0.5rem;
  padding: 0.9rem;
  border: 0;
  border-radius: var(--radius-sm);
  background: var(--grad);
  color: #fff;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;

  &:disabled {
    opacity: 0.6;
  }
`;
