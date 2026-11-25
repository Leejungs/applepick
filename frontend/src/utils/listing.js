// 매물(ES _source) 관련 공통 함수

const MARKET_IMAGE_DIR = { Daangn: 'daangn_image', Bunjang: 'bunjang_image' };

const CATEGORY_IMAGE = [
  ['맥북', 'macbook'],
  ['아이폰', 'iphone'],
  ['아이패드', 'ipad'],
  ['애플워치', 'applewatch'],
  ['에어팟', 'airpods'],
  ['맥', 'mac'],
];

// 매물 이미지 URL 목록. http 로 시작하면 원본 URL, 아니면 API 가 서빙하는 로컬 파일
export function getImages(source) {
  const pictures = source.pictures?.length
    ? source.pictures
    : source.images || [];
  return pictures.map(p =>
    p.startsWith('http')
      ? p
      : `/api/image/${MARKET_IMAGE_DIR[source.market] || ''}/${p}`,
  );
}

// 이미지가 없는 매물(샘플 등)은 카테고리 대표 이미지
export function getThumbnail(source) {
  const [first] = getImages(source);
  if (first) return first;
  const text = `${source.keyword || ''} ${source.title || ''}`;
  const match = CATEGORY_IMAGE.find(([word]) => text.includes(word));
  return match ? `/images/${match[1]}.png` : '/images/null_image.png';
}

export function getListingUrl(source) {
  if (source.url) return source.url;
  if (source.market === 'Daangn')
    return `https://www.daangn.com/articles/${source.pid}`;
  if (source.market === 'Bunjang')
    return `https://m.bunjang.co.kr/products/${source.pid}`;
  return null; // 샘플 데이터
}

export const MARKET_LABEL = {
  Bunjang: '번개장터',
  Daangn: '당근',
  Sample: '샘플 데이터',
};
