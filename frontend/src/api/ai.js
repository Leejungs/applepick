import axiosInstance from '../utils/axiosInstance';

export const getAiStatus = () => axiosInstance.get('/api/ai/status');

// 서버가 보내는 SSE(text/event-stream) 이벤트를 하나씩 onEvent 로 전달
export async function chatStream({ message, history, onEvent, signal }) {
  const res = await fetch('/api/ai/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history }),
    signal,
  });

  if (!res.ok) {
    let detail = `요청 실패 (${res.status})`;
    try {
      detail = (await res.json()).message || detail;
    } catch {
      /* 본문 없음 */
    }
    throw new Error(detail);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const chunks = buffer.split('\n\n');
    buffer = chunks.pop();
    for (const chunk of chunks) {
      const line = chunk.trim();
      if (line.startsWith('data:')) onEvent(JSON.parse(line.slice(5)));
    }
  }
}
