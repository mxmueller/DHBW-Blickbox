// Mock IntersectionObserver
class IntersectionObserver {
    constructor() {}
    observe() {}
    unobserve() {}
    disconnect() {}
}
  
global.IntersectionObserver = IntersectionObserver;
  
import React from 'react';
import { render } from '@testing-library/react';
import DescDetail from './healthDetail';

// Eine einfache Komponente, die das Test-Icon rendert
const TestIconComponent = () => {
    return <img src={TestIcon} alt="Test Icon" />;
};

test('DescDetail renders fallback state correctly', () => {
    const { getByText } = render(<DescDetail icon={<TestIconComponent />} />);
    const fallbackText = getByText(/missing setting/i);
    expect(fallbackText).toBeInTheDocument();
});

test('DescDetail renders success state correctly', () => {
    const { getByText } = render(<DescDetail success={true} successText={"success!"} />);
    const fallbackText = getByText(/success!/i);
    expect(fallbackText).toBeInTheDocument();
});

test('DescDetail renders error state correctly', () => {
    const { getByText } = render(<DescDetail error={true} errorText={"error!"} />);
    const fallbackText = getByText(/error!/i);
    expect(fallbackText).toBeInTheDocument();
});
