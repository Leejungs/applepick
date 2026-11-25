import React, { useEffect, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import 'chart.js/auto';
import { Line } from 'react-chartjs-2';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import SendRoundedIcon from '@mui/icons-material/SendRounded';
import MicRoundedIcon from '@mui/icons-material/MicRounded';
import VolumeUpRoundedIcon from '@mui/icons-material/VolumeUpRounded';
import VolumeOffRoundedIcon from '@mui/icons-material/VolumeOffRounded';
import RestartAltRoundedIcon from '@mui/icons-material/RestartAltRounded';
import * as S from './styles';
import { chatStream, getAiStatus } from '../../api/ai';
import { formatPrice } from '../../utils/format';
import { getThumbnail, MARKET_LABEL } from '../../utils/listing';

const TOOL_ICONS = {
  find_product: '🔎',
  search_listings: '🛒',
  get_market_price: '📊',
  evaluate_deal: '⚖️',
  search_buying_guide: '📚',
  register_price_alert: '🔔',
  web_search: '🌐',
};

const TOOL_GUIDE = [
  ['🧭', '의도 분류', '질문을 분석해 어떤 도움이 필요한지 파악'],
  ['🛒', '매물 검색', '예산·정렬 조건으로 수집된 매물 검색'],
  ['📊', '시세 분석', '7일 평균가·최저가와 4주 추이'],
  ['⚖️', '거래 평가', '가격 수준 분류 + 사기 위험 신호 탐지'],
  ['📚', '가이드 검색 (RAG)', '체크리스트·사기 예방 문서 검색'],
  ['🌐', '웹 검색', '출시 가격·뉴스 등 최신 정보'],
  ['🔔', '알림 등록', '원하는 가격 이하 매물 이메일 알림'],
  ['🎙️', '음성 입력/읽기', '말로 묻고, 답변을 소리로 듣기'],
];

const verdictColor = verdict => {
  if (!verdict) return '#9aa0ad';
  if (verdict.includes('의심')) return '#e5484d';
  if (verdict.includes('저렴')) return '#1f9d6b';
  if (verdict.includes('적정')) return '#5b5bd6';
  if (verdict.includes('비')) return '#f76b15';
  return '#9aa0ad';
};

const stripMarkdown = text =>
  text
    .replace(/[#*_`>|-]/g, ' ')
    .replace(/\[(.*?)\]\(.*?\)/g, '$1')
    .replace(/\s+/g, ' ');

const SpeechRecognition =
  typeof window !== 'undefined' &&
  (window.SpeechRecognition || window.webkitSpeechRecognition);

function Artifact({ event }) {
  const a = event.artifact;
  if (event.type === 'web_results') {
    return (
      <S.InfoCard>
        <div className="head">🌐 웹 검색 출처</div>
        <div className="chips">
          {event.sources.map(s => (
            <a
              key={s.url}
              className="chip src"
              href={s.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              {s.title || s.url}
            </a>
          ))}
        </div>
      </S.InfoCard>
    );
  }
  if (!a) return null;

  switch (event.name) {
    case 'search_listings':
      if (!a.listings?.length) return null;
      return (
        <S.ListingGrid>
          {a.listings.map(l => (
            <S.ListingCard
              key={l.id}
              href={l.url || undefined}
              target="_blank"
              rel="noopener noreferrer"
              as={l.url ? 'a' : 'div'}
            >
              <img
                src={getThumbnail({
                  pictures: l.thumbnail ? [l.thumbnail] : [],
                  keyword: l.keyword,
                  title: l.title,
                  market: l.market,
                })}
                alt={l.title}
                loading="lazy"
                referrerPolicy="no-referrer"
              />
              <div className="t">{l.title}</div>
              <div className="p">{formatPrice(l.price)}</div>
              <div className="m">
                {MARKET_LABEL[l.market] || l.market} · {l.date.slice(5)} · 조회{' '}
                {l.views}
              </div>
            </S.ListingCard>
          ))}
        </S.ListingGrid>
      );
    case 'get_market_price': {
      const weekly = [...(a.weekly_avg_recent_first || [])].reverse();
      return (
        <S.InfoCard>
          <div className="head">
            <span>📊 {a.product} 시세</span>
            <span>{a.trend}</span>
          </div>
          <div className="nums">
            <span>
              7일 평균
              <b>{a.avg_price_7d ? formatPrice(a.avg_price_7d) : '-'}</b>
            </span>
            <span>
              7일 최저
              <b>{a.min_price_7d ? formatPrice(a.min_price_7d) : '-'}</b>
            </span>
            <span>
              분석 매물
              <b>{a.sample_count_7d}개</b>
            </span>
          </div>
          <div style={{ height: 140, marginTop: 10 }}>
            <Line
              data={{
                labels: ['3주 전', '2주 전', '1주 전', '이번 주'],
                datasets: [
                  {
                    data: weekly,
                    borderColor: '#5b5bd6',
                    backgroundColor: 'rgba(91,91,214,.12)',
                    fill: true,
                    tension: 0.3,
                    spanGaps: true,
                  },
                ],
              }}
              options={{
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                  y: {
                    ticks: {
                      callback: v => `${Math.round(v / 10000)}만`,
                    },
                  },
                },
              }}
            />
          </div>
        </S.InfoCard>
      );
    }
    case 'evaluate_deal':
      return (
        <S.InfoCard>
          <div className="head">
            <span>
              ⚖️ {a.product} {formatPrice(a.price)} 평가
            </span>
            <S.Verdict $color={verdictColor(a.verdict)}>{a.verdict}</S.Verdict>
          </div>
          <div className="nums">
            <span>
              시세 대비<b>{a.price_vs_avg || '-'}</b>
            </span>
            <span>
              7일 평균
              <b>{a.market_avg_7d ? formatPrice(a.market_avg_7d) : '-'}</b>
            </span>
          </div>
          {(a.risk_signals?.length > 0 || a.positive_signals?.length > 0) && (
            <div className="chips">
              {a.risk_signals.map(r => (
                <span key={r} className="chip bad">
                  ⚠ {r}
                </span>
              ))}
              {a.positive_signals.map(r => (
                <span key={r} className="chip good">
                  ✓ {r}
                </span>
              ))}
            </div>
          )}
        </S.InfoCard>
      );
    case 'search_buying_guide':
      return (
        <S.InfoCard>
          <div className="head">📚 참고한 가이드 문서 (RAG)</div>
          <div className="chips">
            {a.map(s => (
              <span key={s.title + s.section} className="chip src">
                {s.title} · {s.section}
              </span>
            ))}
          </div>
        </S.InfoCard>
      );
    case 'register_price_alert':
      return (
        <S.InfoCard>
          <div className="head">🔔 알림 등록 완료</div>
          <div className="nums">
            <span>
              상품<b>{a.product}</b>
            </span>
            <span>
              지정가<b>{formatPrice(a.target_price)}</b>
            </span>
            <span>
              이메일<b>{a.email}</b>
            </span>
          </div>
        </S.InfoCard>
      );
    default:
      return null;
  }
}

function AssistantMessage({ msg }) {
  const visibleSteps = msg.events.filter(e => e.type === 'tool');
  const artifacts = msg.events.filter(
    e => (e.type === 'tool' && e.artifact) || e.type === 'web_results',
  );
  return (
    <S.Row>
      <div className="avatar">
        <AutoAwesomeIcon fontSize="small" />
      </div>
      <S.Bubble>
        {msg.intent && (
          <S.Intent>
            <span>🧭 {msg.intent.intent_label}</span>
            {msg.intent.products?.map(p => (
              <span key={p} className="sub">
                {p}
              </span>
            ))}
            {msg.intent.budget ? (
              <span className="sub">예산 {formatPrice(msg.intent.budget)}</span>
            ) : null}
          </S.Intent>
        )}
        {visibleSteps.length > 0 && (
          <S.Steps>
            {visibleSteps.map((s, i) => (
              <S.Step key={i} $error={s.error}>
                {TOOL_ICONS[s.name] || '🛠'} <b>{s.label}</b>
                {s.input?.query && ` "${s.input.query}"`}
                {s.input?.product_key && ` ${s.input.product_key}`}
                {s.input?.text && ` "${s.input.text}"`}
              </S.Step>
            ))}
          </S.Steps>
        )}
        {msg.pending && !msg.answer && (
          <S.Thinking>
            <AutoAwesomeIcon fontSize="small" />
            {msg.status || '생각하는 중...'}
          </S.Thinking>
        )}
        {msg.error && <S.Error>⚠ {msg.error}</S.Error>}
        {msg.answer && (
          <S.Answer>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {msg.answer}
            </ReactMarkdown>
          </S.Answer>
        )}
        {artifacts.length > 0 && (
          <S.Artifacts>
            {artifacts.map((e, i) => (
              <Artifact key={i} event={e} />
            ))}
          </S.Artifacts>
        )}
      </S.Bubble>
    </S.Row>
  );
}

const NODE_STATUS = {
  analyze: '질문을 이해했어요. 필요한 도구를 고르는 중...',
  agent: '도구 결과를 바탕으로 정리하는 중...',
  tools: '도구를 실행했어요. 결과를 확인하는 중...',
};

function Assistant() {
  const { data: status } = useQuery({
    queryKey: ['ai-status'],
    queryFn: async () => (await getAiStatus()).data,
  });
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [listening, setListening] = useState(false);
  const [speak, setSpeak] = useState(false);
  const bottomRef = useRef();
  const recogRef = useRef();
  const abortRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [messages]);

  useEffect(() => () => abortRef.current?.abort(), []);

  const updateLast = fn =>
    setMessages(prev => [...prev.slice(0, -1), fn(prev[prev.length - 1])]);

  const send = async text => {
    const question = (text ?? input).trim();
    if (!question || busy) return;
    setInput('');
    setBusy(true);

    const history = messages
      .filter(m => (m.role === 'user' ? m.text : m.answer))
      .map(m => ({
        role: m.role,
        content: m.role === 'user' ? m.text : m.answer,
      }));
    setMessages(prev => [
      ...prev,
      { role: 'user', text: question },
      { role: 'assistant', events: [], pending: true },
    ]);

    abortRef.current = new AbortController();
    try {
      await chatStream({
        message: question,
        history,
        signal: abortRef.current.signal,
        onEvent: e => {
          if (e.type === 'node') {
            updateLast(m => ({ ...m, status: NODE_STATUS[e.node] }));
          } else if (e.type === 'intent') {
            updateLast(m => ({ ...m, intent: e }));
          } else if (e.type === 'answer') {
            updateLast(m => ({ ...m, answer: e.text }));
            if (speak && window.speechSynthesis) {
              const u = new SpeechSynthesisUtterance(stripMarkdown(e.text));
              u.lang = 'ko-KR';
              window.speechSynthesis.cancel();
              window.speechSynthesis.speak(u);
            }
          } else if (e.type === 'error') {
            updateLast(m => ({ ...m, error: e.message }));
          } else if (e.type === 'tool' || e.type === 'web_results') {
            updateLast(m => ({ ...m, events: [...m.events, e] }));
          }
        },
      });
    } catch (err) {
      if (err.name !== 'AbortError')
        updateLast(m => ({ ...m, error: err.message }));
    } finally {
      updateLast(m => ({ ...m, pending: false }));
      setBusy(false);
    }
  };

  const toggleMic = () => {
    if (!SpeechRecognition) {
      alert(
        '이 브라우저는 음성 입력을 지원하지 않아요. Chrome 을 사용해 주세요.',
      );
      return;
    }
    if (listening) {
      recogRef.current?.stop();
      return;
    }
    const recog = new SpeechRecognition();
    recog.lang = 'ko-KR';
    recog.interimResults = true;
    recog.onresult = e => {
      const text = Array.from(e.results)
        .map(r => r[0].transcript)
        .join('');
      setInput(text);
      if (e.results[e.results.length - 1].isFinal) send(text);
    };
    recog.onend = () => setListening(false);
    recog.onerror = () => setListening(false);
    recogRef.current = recog;
    setListening(true);
    recog.start();
  };

  const reset = () => {
    abortRef.current?.abort();
    window.speechSynthesis?.cancel();
    setMessages([]);
    setBusy(false);
  };

  const enabled = status?.enabled;

  return (
    <S.Page>
      <S.Side>
        <S.HeroCard>
          <AutoAwesomeIcon />
          <h2>AI 중고거래 어시스턴트</h2>
          <p>
            매물 검색, 시세 분석, 거래 평가, 구매 가이드, 최신 정보 검색까지
            대화 한 번으로 처리해요.
          </p>
          {status?.model && <span className="model">{status.model}</span>}
        </S.HeroCard>
        <S.Card>
          <h3>AI가 쓰는 도구</h3>
          <S.ToolList>
            {TOOL_GUIDE.map(([ico, name, desc]) => (
              <li key={name}>
                <span className="ico">{ico}</span>
                <span>
                  <b>{name}</b>
                  {desc}
                </span>
              </li>
            ))}
          </S.ToolList>
        </S.Card>
      </S.Side>

      <S.Chat>
        {status && !enabled && (
          <S.Banner>
            🔑 AI 기능을 쓰려면 프로젝트 폴더의 <code>.env</code> 파일에{' '}
            <code>OPENAI_API_KEY=sk-...</code> 를 넣고 백엔드를 다시
            실행하세요.
          </S.Banner>
        )}
        <S.Messages>
          {messages.length === 0 ? (
            <S.Empty>
              <div className="big">🍎</div>
              <h2>무엇을 도와드릴까요?</h2>
              <p>원하는 제품, 예산, 궁금한 점을 자유롭게 말씀해 주세요.</p>
              <S.Examples>
                {(status?.examples || []).map(ex => (
                  <button key={ex} onClick={() => send(ex)} disabled={!enabled}>
                    {ex}
                  </button>
                ))}
              </S.Examples>
            </S.Empty>
          ) : (
            messages.map((m, i) =>
              m.role === 'user' ? (
                <S.Row key={i} $user>
                  <S.Bubble $user>{m.text}</S.Bubble>
                </S.Row>
              ) : (
                <AssistantMessage key={i} msg={m} />
              ),
            )
          )}
          <div ref={bottomRef} />
        </S.Messages>

        <S.Composer
          onSubmit={e => {
            e.preventDefault();
            send();
          }}
        >
          <S.IconBtn
            type="button"
            title="새 대화"
            onClick={reset}
            disabled={messages.length === 0}
          >
            <RestartAltRoundedIcon />
          </S.IconBtn>
          <textarea
            value={input}
            placeholder={
              enabled
                ? '예) 아이폰 15 프로 90만원 이하로 괜찮은 매물 있어?'
                : 'API 키를 설정하면 대화할 수 있어요'
            }
            disabled={!enabled}
            rows={1}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => {
              if (
                e.key === 'Enter' &&
                !e.shiftKey &&
                !e.nativeEvent.isComposing
              ) {
                e.preventDefault();
                send();
              }
            }}
          />
          <S.IconBtn
            type="button"
            title="음성으로 질문"
            $active={listening}
            onClick={toggleMic}
            disabled={!enabled || busy}
          >
            <MicRoundedIcon />
          </S.IconBtn>
          <S.IconBtn
            type="button"
            title={speak ? '답변 읽기 끄기' : '답변 소리로 읽기'}
            $active={speak}
            onClick={() => {
              window.speechSynthesis?.cancel();
              setSpeak(!speak);
            }}
          >
            {speak ? <VolumeUpRoundedIcon /> : <VolumeOffRoundedIcon />}
          </S.IconBtn>
          <S.IconBtn
            type="submit"
            $primary
            disabled={!enabled || busy || !input.trim()}
          >
            <SendRoundedIcon />
          </S.IconBtn>
        </S.Composer>
      </S.Chat>
    </S.Page>
  );
}

export default Assistant;
