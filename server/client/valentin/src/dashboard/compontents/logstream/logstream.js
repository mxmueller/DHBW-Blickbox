import React, { useState, useEffect } from "react";
import LogstreamItem from "./logstream.item.js";
import { ChakraProvider, Box, Table, Tbody, AccordionPanel, TableContainer, Accordion, AccordionItem, AccordionButton, Text, AccordionIcon } from "@chakra-ui/react";

const Logstream = () => {
  const [logstreamItems, setLogstreamItems] = useState([]);
  const [, setConnectionStatus] = useState('Disconnected');

  useEffect(() => {
    if (process.env.REACT_APP_USE_LOGSTREAM_MOCKS !== 'true') {
      const ws = new WebSocket('wss://blickbox.maytastix.de/logs/');

      ws.onopen = () => {
        console.log('WebSocket connection established.');
        setConnectionStatus('Connected');
      };

      ws.onmessage = (event) => {
        try {
          let correctedJsonString = event.data.replace(/'/g, '"');
          let wsjson = JSON.parse(correctedJsonString);

          console.log('Received message:', wsjson);

          let wsmessagestate = 'blackAlpha';

          if (wsjson.type === "info") wsmessagestate = "yellow";
          if (wsjson.type === "error") wsmessagestate = "red";
          if (wsjson.type === "success") wsmessagestate = "green";

          setLogstreamItems(prevItems => [{
            message: wsjson.message,
            code: wsmessagestate,
            type: "Websocket " + wsjson.title,
            date: wsjson.timestamp
          }, ...prevItems]);

        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
          const currentDate = new Date();
          setLogstreamItems(prevItems => [{
            message: 'Fehler beim Parsen der empfangenen Daten:',
            error,
            type: "Websocket Error",
            code: "red",
            date: currentDate.toISOString()
          }, ...prevItems]);
        }
      };

      ws.onclose = () => {
        console.log('WebSocket connection closed.');
        setConnectionStatus('Disconnected');
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('Error');
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
                  sx={{
                    '::-webkit-scrollbar': {
                      display: 'none'
                    }
                  }}
                  display='block'
                  overflowY='scroll'
                  overflowX='scroll'
                  borderRadius={25}
                  bg='white'
                  minHeight='90px'
                  width='100%'
                  padding={5}
                >
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