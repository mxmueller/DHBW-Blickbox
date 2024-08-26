import React, { useState, useEffect } from "react";
import LogstreamItem from "./logstream.item.js";
import { ChakraProvider, Box, Table, Tbody, AccordionPanel, TableContainer, Accordion, AccordionItem, AccordionButton, Text, AccordionIcon } from "@chakra-ui/react";

// Mock-Daten-Generator importieren
const generateMockLogstreamItem = () => {
  const types = ['Mock Success', 'Mock Info', 'Mock Error'];
  const codes = ['green', 'yellow', 'red'];
  const messages = [
    'Mock log message 1',
    'Mock log message 2',
    'Mock log message 3',
    'Mock log message 4',
    'Mock log message 5'
  ];

  const randomIndex = Math.floor(Math.random() * 3);

  return {
    message: messages[Math.floor(Math.random() * messages.length)],
    code: codes[randomIndex],
    type: types[randomIndex],
    date: new Date().toISOString()
  };
};

const Logstream = () => {
  const [logstreamItems, setLogstreamItems] = useState([]);

  Logstream.addItemToLogstream = (message) => {
    setLogstreamItems(prevItems => [message, ...prevItems]);
  };

  useEffect(() => {
    if (process.env.REACT_APP_USE_LOGSTREAM_MOCKS === 'true') {
      // Mock-Daten in einem Intervall hinzufügen
      const intervalId = setInterval(() => {
        const mockItem = generateMockLogstreamItem();
        Logstream.addItemToLogstream(mockItem);
      }, 2000); // Neue Mock-Nachricht alle 2 Sekunden

      // Intervall bei Komponentendeaktivierung stoppen
      return () => clearInterval(intervalId);
    } else {
      // WebSocket-Verbindung herstellen
      const ws = new WebSocket('wss://dhbwapi.maytastix.de/log-stream');

      ws.onopen = () => {
        console.log('WebSocket connection established.');
      };

      ws.onmessage = (event) => {
        try {
          let correctedJsonString = event.data.replace(/'/g, '"');
          let wsjson = JSON.parse(correctedJsonString);

          console.log(wsjson);

          let wsmessagestate = 'blackAlpha';

          if (wsjson.type === "info") wsmessagestate = "yellow";
          if (wsjson.type === "error") wsmessagestate = "red";
          if (wsjson.type === "success") wsmessagestate = "green";

          Logstream.addItemToLogstream({ message: wsjson.message, code: wsmessagestate, type: "Websocket " + wsjson.title, date: wsjson.timestamp });

        } catch (error) {
          const currentDate = new Date();
          Logstream.addItemToLogstream({ message: 'Fehler beim Parsen der empfangenen Daten:', error, type: "Websocket Error", code: "red", date: currentDate.toISOString() });
        }
      };

      ws.onclose = () => {
        console.log('WebSocket connection closed.');
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      return () => {
        if (ws) {
          ws.close();
        }
      };
    }
  }, []);

  return (
      <ChakraProvider>
        <Box mt={10} boxShadow='xl' bg='blackAlpha.100' borderRadius={25} pt={3} pl={3} pr={3} pb={3}>
          <Accordion allowToggle defaultIndex={[0]}>
            <AccordionItem border='0px'>
              <h2>
                <AccordionButton>
                  <Box as="span" flex='1' textAlign='left'>
                    <Text fontSize='md' color='blackAlpha.700' as='b'>Logging Panel</Text>
                  </Box>
                  <AccordionIcon />
                </AccordionButton>
              </h2>
              <AccordionPanel mb={0}>
                <TableContainer>
                  <Box
                      maxHeight={'700px'}
                      sx={
                        {
                          '::-webkit-scrollbar': {
                            display: 'none'
                          }
                        }
                      }
                      display='block'
                      overflowY='scroll'
                      overflowX='scroll'
                      borderRadius={25}
                      bg='white'
                      minHeight='90px'
                      width='100%'
                      padding={5} >
                    <Table variant="simple" size="sm">
                      <Tbody>
                        {logstreamItems.map((item, index) => (
                            <LogstreamItem
                                key={index}
                                message={item.message}
                                type={item.type}
                                code={item.code}
                                date={item.date}
                            />
                        ))}
                      </Tbody>
                    </Table>
                  </Box>
                </TableContainer>
              </AccordionPanel>
            </AccordionItem>
          </Accordion>
        </Box>
      </ChakraProvider>
  );
};

export default Logstream;
