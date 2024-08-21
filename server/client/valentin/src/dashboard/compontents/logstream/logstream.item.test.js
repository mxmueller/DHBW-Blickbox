import React from 'react';
import { render, screen } from '@testing-library/react';
import LogstreamItem from './logstream.item.js';
import { ChakraProvider, Table, Tbody, Tr, Td } from "@chakra-ui/react";

test('renders LogstreamItem with correct message and color', () => {
    const testMessage = {
        type: 'Websocket Error',
        code: 'red',
        message: 'Fehler beim Parsen der empfangenen Daten',
        date: '2023-08-19T12:34:56.789Z',
    };

    render(
        <ChakraProvider>
            <Table>
                <Tbody>
                    <LogstreamItem {...testMessage} />
                </Tbody>
            </Table>
        </ChakraProvider>
    );

    const typeElement = screen.getByText(/Websocket Error/i);
    const messageElement = screen.getByText(/Fehler beim Parsen der empfangenen Daten/i);
    const dateElement = screen.getByText(/2023-08-19T12:34:56.789Z/i);

    expect(typeElement).toBeInTheDocument();
    expect(messageElement).toBeInTheDocument();
    expect(dateElement).toBeInTheDocument();
    expect(typeElement).toHaveStyle('color: var(--chakra-colors-red)');
});
