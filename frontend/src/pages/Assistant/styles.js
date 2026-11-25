import styled, { keyframes } from 'styled-components';

const pulse = keyframes`
  0%, 100% { opacity: .35 } 50% { opacity: 1 }
`;

export const Page = styled.div`
  margin-top: calc(var(--header-h) + 24px);
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.25rem;
  align-items: start;

  @media (max-width: 960px) {
    grid-template-columns: 1fr;
  }
`;

export const Side = styled.aside`
  position: sticky;
  top: calc(var(--header-h) + 24px);
  display: flex;
  flex-direction: column;
  gap: 1rem;

  @media (max-width: 960px) {
    position: static;
  }
`;

export const Card = styled.div`
  padding: 1.25rem;
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);

  h3 {
    margin: 0 0 0.75rem;
    font-size: 0.95rem;
    font-weight: 800;
  }
`;

export const HeroCard = styled(Card)`
  background: var(--grad);
  color: #fff;

  h2 {
    margin: 0.25rem 0 0.5rem;
    font-size: 1.3rem;
    font-weight: 800;
  }
  p {
    margin: 0;
    font-size: 0.88rem;
    line-height: 1.55;
    color: rgba(255, 255, 255, 0.85);
  }
  .model {
    display: inline-block;
    margin-top: 0.75rem;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.18);
    font-size: 0.75rem;
    font-weight: 600;
  }
`;

export const ToolList = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  li {
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
    font-size: 0.85rem;
    color: var(--text-sub);
  }
  li b {
    display: block;
    color: var(--text);
    font-size: 0.88rem;
  }
  .ico {
    font-size: 1.1rem;
    line-height: 1.3;
  }
`;

export const Chat = styled.section`
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - var(--header-h) - 60px);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
  overflow: hidden;
`;

export const Messages = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 1.5rem;
  overflow-y: auto;
  max-height: calc(100vh - var(--header-h) - 200px);
`;

export const Empty = styled.div`
  margin: auto;
  max-width: 560px;
  text-align: center;
  padding: 2rem 0;

  .big {
    font-size: 3rem;
  }
  h2 {
    margin: 0.5rem 0;
    font-size: 1.5rem;
    font-weight: 800;
  }
  p {
    color: var(--text-sub);
    margin: 0 0 1.5rem;
  }
`;

export const Examples = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  button {
    text-align: left;
    padding: 0.8rem 1rem;
    border-radius: 12px;
    border: 1px solid var(--line);
    background: #fafbfd;
    color: var(--text);
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.15s;
  }
  button:hover {
    border-color: var(--primary);
    background: var(--primary-soft);
    color: var(--primary);
  }
`;

export const Row = styled.div`
  display: flex;
  gap: 0.75rem;
  justify-content: ${p => (p.$user ? 'flex-end' : 'flex-start')};

  .avatar {
    flex-shrink: 0;
    display: grid;
    place-items: center;
    width: 36px;
    height: 36px;
    border-radius: 12px;
    background: var(--grad);
    color: #fff;
  }
`;

export const Bubble = styled.div`
  max-width: ${p => (p.$user ? '75%' : '100%')};
  min-width: 0;
  flex: ${p => (p.$user ? '0 1 auto' : '1')};
  padding: ${p => (p.$user ? '0.75rem 1rem' : '0')};
  border-radius: 18px 18px 4px 18px;
  background: ${p => (p.$user ? 'var(--grad)' : 'transparent')};
  color: ${p => (p.$user ? '#fff' : 'var(--text)')};
  line-height: 1.6;
  white-space: ${p => (p.$user ? 'pre-wrap' : 'normal')};
`;

export const Intent = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 0.6rem;

  span {
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary);
    font-size: 0.76rem;
    font-weight: 700;
  }
  span.sub {
    background: #f1f2f6;
    color: var(--text-sub);
    font-weight: 600;
  }
`;

export const Steps = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 0.75rem;
`;

export const Step = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.65rem;
  border-radius: 8px;
  border: 1px solid var(--line);
  background: ${p => (p.$error ? '#fff0f0' : '#fafbfd')};
  font-size: 0.8rem;
  color: var(--text-sub);

  b {
    color: var(--text);
  }
`;

export const Thinking = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-sub);
  font-size: 0.9rem;
  animation: ${pulse} 1.4s infinite;
`;

export const Answer = styled.div`
  font-size: 0.97rem;

  h1,
  h2,
  h3 {
    font-size: 1.05rem;
    margin: 1rem 0 0.4rem;
  }
  p {
    margin: 0.4rem 0;
  }
  ul,
  ol {
    margin: 0.3rem 0;
    padding-left: 1.3rem;
  }
  li {
    margin: 0.15rem 0;
  }
  a {
    color: var(--primary);
  }
  table {
    border-collapse: collapse;
    margin: 0.5rem 0;
    font-size: 0.9rem;
  }
  th,
  td {
    border: 1px solid var(--line);
    padding: 0.35rem 0.6rem;
  }
  code {
    background: #f1f2f6;
    padding: 0.1rem 0.3rem;
    border-radius: 4px;
  }
`;

export const Error = styled.div`
  padding: 0.75rem 1rem;
  border-radius: 12px;
  background: #fff0f0;
  color: var(--warn);
  font-size: 0.9rem;
`;

export const Artifacts = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.9rem;
`;

export const ListingGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 0.6rem;
`;

export const ListingCard = styled.a`
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  border: 1px solid var(--line);
  overflow: hidden;
  text-decoration: none;
  color: var(--text);
  background: #fff;
  transition:
    box-shadow 0.15s,
    transform 0.15s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow);
  }
  img {
    width: 100%;
    aspect-ratio: 4 / 3;
    object-fit: cover;
    background: #eef0f5;
  }
  .t {
    padding: 0.5rem 0.6rem 0;
    font-size: 0.82rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .p {
    padding: 0.15rem 0.6rem 0.55rem;
    font-weight: 800;
  }
  .m {
    padding: 0 0.6rem 0.55rem;
    font-size: 0.72rem;
    color: var(--text-faint);
  }
`;

export const InfoCard = styled.div`
  padding: 1rem 1.1rem;
  border-radius: 14px;
  border: 1px solid var(--line);
  background: #fafbfd;

  .head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
    font-weight: 800;
    font-size: 0.92rem;
  }
  .nums {
    display: flex;
    flex-wrap: wrap;
    gap: 1.25rem;
    font-size: 0.85rem;
    color: var(--text-sub);
  }
  .nums b {
    display: block;
    color: var(--text);
    font-size: 1.1rem;
  }
  .chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 0.6rem;
  }
  .chip {
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 700;
  }
  .chip.bad {
    background: #ffe9e9;
    color: var(--warn);
  }
  .chip.good {
    background: #e5f6ee;
    color: var(--good);
  }
  .chip.src {
    background: #f1f2f6;
    color: var(--text-sub);
    text-decoration: none;
  }
`;

export const Verdict = styled.span`
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  color: #fff;
  background: ${p => p.$color};
`;

export const Composer = styled.form`
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid var(--line);
  background: #fcfcfe;

  textarea {
    flex: 1;
    min-height: 48px;
    max-height: 160px;
    resize: none;
    padding: 0.8rem 1rem;
    border-radius: 14px;
    border: 1px solid var(--line);
    background: #fff;
    font-size: 0.95rem;
    line-height: 1.5;
    outline: none;
  }
  textarea:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px var(--primary-soft);
  }
`;

export const IconBtn = styled.button`
  flex-shrink: 0;
  display: grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: 14px;
  border: 1px solid ${p => (p.$primary ? 'transparent' : 'var(--line)')};
  background: ${p =>
    p.$primary ? 'var(--grad)' : p.$active ? 'var(--accent)' : '#fff'};
  color: ${p => (p.$primary || p.$active ? '#fff' : 'var(--text-sub)')};
  cursor: pointer;
  transition: filter 0.15s;

  &:hover {
    filter: brightness(1.06);
  }
  &:disabled {
    opacity: 0.45;
    cursor: default;
  }
`;

export const Banner = styled.div`
  margin: 1rem 1.5rem 0;
  padding: 0.9rem 1rem;
  border-radius: 12px;
  background: #fff8e6;
  color: #8a5a00;
  font-size: 0.88rem;
  line-height: 1.5;

  code {
    background: #fff;
    padding: 0.1rem 0.35rem;
    border-radius: 4px;
  }
`;
