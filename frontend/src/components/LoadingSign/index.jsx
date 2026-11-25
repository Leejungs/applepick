import React from 'react';
import BeatLoader from 'react-spinners/BeatLoader';
import { Container } from './styles';

const override = { display: 'block', margin: '0.5rem auto' };

const LoadingSign = ({ loading, color = '#5b5bd6', size = 20 }) => (
  <Container>
    <BeatLoader
      color={color}
      loading={loading}
      size={size}
      cssOverride={override}
    />
  </Container>
);

export default LoadingSign;
