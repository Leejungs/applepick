import styled from 'styled-components';

export const Background = styled.div`
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(14, 15, 28, 0.6);
  backdrop-filter: blur(4px);
  animation: modal-bg-show 0.2s;
  @keyframes modal-bg-show {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
`;

export const Content = styled.div`
  position: relative;
  width: 100%;
  max-width: 680px;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 24px;
  background: var(--surface);
  box-shadow: var(--shadow-lg);
  animation: modal-show 0.25s ease-out;
  @keyframes modal-show {
    from {
      opacity: 0;
      transform: translateY(20px) scale(0.98);
    }
    to {
      opacity: 1;
      transform: none;
    }
  }
`;

export const Main = styled.div`
  padding: 1.5rem 1.75rem 1.75rem;
`;

export const TitleLinkWrapper = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;

  > span {
    flex-shrink: 0;
    padding: 0.4rem 0.8rem;
    border-radius: 999px;
    background: #f1f2f6;
    color: var(--text-sub);
    font-size: 0.8rem;
    font-weight: 600;
  }
`;

export const Title = styled.div`
  font-size: 1.3rem;
  font-weight: 800;
  line-height: 1.35;
`;

export const HyperLink = styled.a`
  flex-shrink: 0;
  padding: 0.55rem 1rem;
  border-radius: 999px;
  background: var(--grad);
  color: #fff;
  font-size: 0.85rem;
  font-weight: 700;
  text-decoration: none;
`;

export const InfoWrapper = styled.div`
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.75rem;
  margin: 0.75rem 0 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--line);
  color: var(--text-sub);
  font-size: 0.85rem;
`;

export const Price = styled.div`
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text);
`;

export const Region = styled.div``;

export const UploadDate = styled.div``;

export const Desc = styled.div`
  white-space: pre-wrap;
  line-height: 1.7;
  font-size: 0.95rem;
`;

export const CloseBtn = styled.button`
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 2;
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 0;
  background: rgba(0, 0, 0, 0.45);
  cursor: pointer;

  svg {
    font-size: 1.5rem !important;
  }
`;

export const ImgBox = styled.div``;
