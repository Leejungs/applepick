import React, { useEffect, useState, useRef } from 'react';
import { createPortal } from 'react-dom';
import * as Style from './styles';
import CloseIcon from '@mui/icons-material/Close';
import NotificationAPI from '../../api/notification';
import useCatalog from '../../query/useCatalog';

function AlarmModal({ onClose }) {
  const outModal = useRef();

  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'visible';
    };
  }, []);

  const [alarmInfo, setAlarmInfo] = useState({
    email: '',
    price: '',
  });

  const { products } = useCatalog();
  const [product, setProduct] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const selected = product || products[0]?.key || '';

  const handleKeywordChange = e => {
    const { name, value } = e.target;
    setAlarmInfo({ ...alarmInfo, [name]: value });
  };

  const submit = async () => {
    const price = Number(alarmInfo.price.replace(/[^0-9]/g, ''));
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(alarmInfo.email)) {
      alert('이메일 형식을 확인해 주세요.');
      return;
    }
    if (!price) {
      alert('가격을 숫자로 입력해 주세요.');
      return;
    }
    setSubmitting(true);
    try {
      await NotificationAPI.notificationSubmit(
        alarmInfo.email,
        price,
        selected,
      );
      alert(
        `${selected} ${price.toLocaleString('ko-KR')}원 이하 알림 등록 완료`,
      );
      onClose();
    } catch {
      alert('등록 중 오류가 발생했습니다.');
    } finally {
      setSubmitting(false);
    }
  };

  return createPortal(
    <Style.Background
      ref={outModal}
      onClick={e => {
        if (outModal.current === e.target) {
          onClose();
        }
      }}
    >
      <Style.Content>
        <Style.AlarmWrapper>
          <Style.Header>알림등록</Style.Header>
          <Style.GuideText>
            이메일과 가격을 입력하고, 키워드를 선택하세요.
          </Style.GuideText>
          <Style.InputWrapper>
            <Style.InputItem
              maxLength="100"
              type="text"
              value={alarmInfo.email}
              name="email"
              onChange={handleKeywordChange}
              placeholder="이메일"
            />
          </Style.InputWrapper>
          <Style.InputWrapper>
            <Style.InputItem
              maxLength="100"
              type="text"
              value={alarmInfo.price}
              name="price"
              onChange={handleKeywordChange}
              placeholder="가격 (이 금액 이하 매물이 올라오면 알림)"
              inputMode="numeric"
            />
          </Style.InputWrapper>
          <Style.SelectBox
            name="keyword"
            value={selected}
            onChange={e => setProduct(e.target.value)}
          >
            {products.map(item => (
              <option key={item.key} value={item.key}>
                {item.label}
              </option>
            ))}
          </Style.SelectBox>
          <Style.SubmitBtn onClick={submit} disabled={submitting}>
            등록
          </Style.SubmitBtn>
        </Style.AlarmWrapper>
        <Style.CloseBtn>
          <CloseIcon
            fontSize="large"
            sx={{ color: 'white' }}
            onClick={onClose}
          />
        </Style.CloseBtn>
      </Style.Content>
    </Style.Background>,
    document.getElementById('modal'),
  );
}

export default AlarmModal;
