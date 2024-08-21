import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import GrafanaValidation from './grafana.3col';

describe('GrafanaValidation Component', () => {
    test('renders without crashing and displays correct number of dashboards', () => {
        render(<GrafanaValidation />);
        const dashboards = screen.getAllByTitle(/Grafana Dashboard \d/);
        expect(dashboards).toHaveLength(3);
    });
});