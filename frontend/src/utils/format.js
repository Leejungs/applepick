const pad = n => String(n).padStart(2, '0');

// unix timestamp(초) -> 'YYYY-MM-DD HH:mm:ss'
export function formatTimestamp(t) {
  const d = new Date(t * 1000);
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(
    d.getHours(),
  )}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

export const formatPrice = price =>
  `${Number(price).toLocaleString('ko-KR')}원`;
