import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom';
import GrafanaValidation from './grafana.container';

describe('GrafanaValidation Component', () => {
    test('renders without crashing', () => {
        const { container } = render(<GrafanaValidation />);
        expect(container.firstChild).toBeInTheDocument();
    });
});