import styled from 'styled-components';

export const BoxWrapper = styled.section`
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  margin-top: calc(var(--header-h) + 24px);
  padding: 3.5rem 3.5rem;
  border-radius: 28px;
  background:
    radial-gradient(
      circle at 85% 20%,
      rgba(142, 78, 198, 0.35),
      transparent 45%
    ),
    radial-gradient(
      circle at 10% 90%,
      rgba(255, 107, 91, 0.22),
      transparent 40%
    ),
    linear-gradient(135deg, #1b1d3a 0%, #2b2363 55%, #3b2a7a 100%);
  color: #fff;
  box-shadow: var(--shadow-lg);

  @media (max-width: 900px) {
    flex-direction: column;
    padding: 2.5rem 1.5rem;
    text-align: center;
  }
`;

export const TextWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 560px;
  z-index: 1;

  .badge {
    align-self: flex-start;
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-size: 0.82rem;
    font-weight: 600;
  }

  .actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 1.25rem;
    flex-wrap: wrap;
  }

  @media (max-width: 900px) {
    align-items: center;
    .badge {
      align-self: center;
    }
    .actions {
      justify-content: center;
    }
  }
`;

export const MainText = styled.h1`
  margin: 0.25rem 0;
  font-size: clamp(2.2rem, 5vw, 3.4rem);
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.03em;

  em {
    font-style: normal;
    background: linear-gradient(90deg, #b8b3ff, #ff9e8f);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }
`;

export const SubText = styled.p`
  margin: 0;
  font-size: 1.05rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.78);
`;

export const CtaButton = styled.button`
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.85rem 1.3rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: ${p => (p.$primary ? '#fff' : 'rgba(255,255,255,0.08)')};
  color: ${p => (p.$primary ? 'var(--primary)' : '#fff')};
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: transform 0.15s;

  &:hover {
    transform: translateY(-2px);
  }
`;

export const SvgWrapper = styled.div`
  width: ${props => props.$w}px;
  max-width: 100%;
  flex-shrink: 0;
  z-index: 1;

  svg {
    width: 100%;
    height: auto;
    filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.35));
  }
`;
