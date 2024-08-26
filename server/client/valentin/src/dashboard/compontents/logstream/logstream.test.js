import React from 'react';
import { render, screen } from '@testing-library/react';
import Logstream from './logstream.js';

test('renders Logstream component', () => {
    render(<Logstream />);
    const panelElement = screen.getByText(/Logging Panel/i);
    expect(panelElement).toBeInTheDocument();
});
