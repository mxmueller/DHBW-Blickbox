// logstream.js
import React, { useState, useEffect, useRef } from "react";
import LogstreamItem from "./logstream.item.js";
import { ChakraProvider, Box, Table, Tbody, AccordionPanel, TableContainer, Accordion, AccordionItem, AccordionButton, Text, AccordionIcon } from "@chakra-ui/react";

const Logstream = () => {
  const [logstreamItems, setLogstreamItems] = useState([]);

  Logstream.addItemToLogstream = (message) => {
    setLogstreamItems(prevItems => [message, ...prevItems]);
  };

  const [messages, setMessages] = useState([]);
  const [socket, setSocket] = useState(null);

  useEffect(() => {

    const ws = new WebSocket('wss://dhbwapi.maytastix.de/log-stream');

    ws.onopen = () => {
      console.log('WebSocket connection established.');
    };

    ws.onmessage = (event) => {
      try {

        let correctedJsonString = event.data.replace(/'/g, '"');


        console.log(correctedJsonString);
        let wsjson = JSON.parse(correctedJsonString);

        console.log(wsjson);

        let wsmessagestate = 'blackAlpha';
        if (wsjson.type == "info")
          wsmessagestate = "yellow"

        if (wsjson.type == "error")
          wsmessagestate = "red"

        if (wsjson.type == "success")
          wsmessagestate = "green"

        Logstream.addItemToLogstream({ message: wsjson.message, type: "Websocket " + wsjson.title, style: wsmessagestate, date: wsjson.timestamp });

      } catch (error) {
        const currentDate = new Date();
        Logstream.addItemToLogstream({ message: 'Fehler beim Parsen der empfangenen Daten:', error, type: "Websocket Error", style: "red", date: currentDate.toISOString()});
      }
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed.');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    setSocket(ws);

    return () => {
      if (ws) {
        ws.close();
      }
    };
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
                          schema={item.style}
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
