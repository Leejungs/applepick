import styled from 'styled-components';

export const Container = styled.header`
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  z-index: 50;
  height: var(--header-h);
  display: flex;
  justify-content: center;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: saturate(180%) blur(16px);
  border-bottom: 1px solid var(--line);
`;

export const HeaderWrapper = styled.div`
  width: 100%;
  max-width: 1200px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
`;

export const HeaderHome = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  cursor: pointer;
  white-space: nowrap;

  span.logo {
    display: grid;
    place-items: center;
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: var(--grad);
    color: #fff;
    font-size: 1.1rem;
  }

  span.ko {
    padding: 0.15rem 0.45rem;
    border-radius: 6px;
    background: var(--primary-soft);
    color: var(--primary);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0;
  }
`;

export const HeaderContents = styled.nav`
  display: flex;
  align-items: center;
  gap: 0.25rem;
  overflow-x: auto;
`;

export const HeaderContent = styled.button`
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.55rem 0.85rem;
  border: 0;
  border-radius: 999px;
  background: ${p => (p.$active ? 'var(--primary-soft)' : 'transparent')};
  color: ${p => (p.$active ? 'var(--primary)' : 'var(--text-sub)')};
  font-size: 0.92rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition:
    background 0.2s,
    color 0.2s;

  svg {
    font-size: 1.15rem;
  }

  &:hover {
    background: var(--primary-soft);
    color: var(--primary);
  }

  &.ai {
    background: var(--grad);
    color: #fff;
    box-shadow: 0 4px 14px rgba(91, 91, 214, 0.35);
  }
  &.ai:hover {
    filter: brightness(1.08);
  }

  @media (max-width: 720px) {
    span.text {
      display: none;
    }
  }
`;
