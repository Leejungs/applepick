import React from 'react';
import 'chart.js/auto';
import { Line } from 'react-chartjs-2';
import * as Style from './styles';

// result.weekly_price: [이번 주, 1주 전, 2주 전, 3주 전] (매물이 없는 주는 null)
function PriceChart({ result }) {
  const weekly = [...(result?.weekly_price || [])].reverse();
  const data = {
    labels: ['3주 전', '2주 전', '1주 전', '이번 주'],
    datasets: [
      {
        label: '평균 시세',
        data: weekly.map(v => (v === 'None' ? null : v)),
        borderColor: '#5b5bd6',
        backgroundColor: 'rgba(91, 91, 214, 0.12)',
        fill: true,
        pointRadius: 5,
        pointBackgroundColor: '#fff',
        borderWidth: 3,
        tension: 0.3,
        spanGaps: true,
      },
    ],
  };
  const options = {
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: ctx => `${Number(ctx.parsed.y).toLocaleString('ko-KR')}원`,
        },
      },
    },
    scales: {
      y: { ticks: { callback: v => `${Number(v).toLocaleString('ko-KR')}원` } },
    },
  };

  const empty =
    weekly.length > 0 && weekly.every(v => v == null || v === 'None');

  return (
    <Style.ChartWrapper>
      {empty ? (
        <p>최근 4주 동안 수집된 매물이 없습니다.</p>
      ) : (
        <Line data={data} options={options} />
      )}
    </Style.ChartWrapper>
  );
}

export default PriceChart;
