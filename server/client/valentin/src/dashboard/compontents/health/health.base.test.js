import React from 'react';
import { render, act, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';

jest.mock('@chakra-ui/react', () => ({
    ChakraProvider: ({ children }) => <div data-testid="chakra-provider">{children}</div>,
    Flex: ({ children }) => <div data-testid="flex">{children}</div>,
    Box: ({ children, as }) => as === 'span' ? <span data-testid="box">{children}</span> : <div data-testid="box">{children}</div>,
    Text: ({ children }) => <span data-testid="text">{children}</span>,
    HStack: ({ children }) => <div data-testid="hstack">{children}</div>,
    Code: ({ children }) => <code data-testid="code">{children}</code>,
    SimpleGrid: ({ children }) => <div data-testid="simple-grid">{children}</div>,
    Accordion: ({ children }) => <div data-testid="accordion">{children}</div>,
    AccordionItem: ({ children }) => <div data-testid="accordion-item">{children}</div>,
    AccordionButton: ({ children }) => <button data-testid="accordion-button">{children}</button>,
    AccordionPanel: ({ children }) => <div data-testid="accordion-panel">{children}</div>,
    AccordionIcon: () => <span data-testid="accordion-icon">Icon</span>,
}));

jest.mock('react-icons/go', () => ({
    GoContainer: () => <span data-testid="go-container">GoContainer</span>,
    GoDatabase: () => <span data-testid="go-database">GoDatabase</span>,
}));

jest.mock('react-icons/si', () => ({
    SiGrafana: () => <span data-testid="si-grafana">SiGrafana</span>,
}));

jest.mock('./health.detail.js', () => ({ header }) => <div data-testid="health-detail">{header}</div>);

import Desc from './health.base';

jest.useFakeTimers();

describe('Desc Component', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        jest.setSystemTime(new Date('2024-08-20T10:00:00Z'));
    });

    test('renders without crashing', () => {
        render(<Desc />);
        expect(screen.getByTestId('chakra-provider')).toBeInTheDocument();
    });

    test('renders health monitoring title', () => {
        render(<Desc />);
        expect(screen.getByText('Health monitoring')).toBeInTheDocument();
    });

    test('renders HealthDetail components', () => {
        render(<Desc />);
        expect(screen.getByText('Blickbox Hardware')).toBeInTheDocument();
        expect(screen.getByText('Blickbox Datenbank')).toBeInTheDocument();
        expect(screen.getByText('Grafana')).toBeInTheDocument();
    });

    test('handles window resize', async () => {
        global.innerWidth = 1024;
        render(<Desc />);

        expect(screen.getByTestId('hstack')).toBeInTheDocument();

        await act(async () => {
            global.innerWidth = 500;
            global.dispatchEvent(new Event('resize'));
        });

        await waitFor(() => {
            expect(screen.queryByTestId('hstack')).not.toBeInTheDocument();
        });
    });
});