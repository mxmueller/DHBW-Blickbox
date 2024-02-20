// logstream.js
import React, { useState } from "react";
import LogstreamItem from "./logstream.item.js";
import { ChakraProvider, Box, Table, Tbody, AccordionPanel, TableContainer, Accordion, AccordionItem, AccordionButton, Text, AccordionIcon} from "@chakra-ui/react";

const Logstream = () => {
  const [logstreamItems, setLogstreamItems] = useState([]);

  Logstream.addItemToLogstream = (message) => {
    setLogstreamItems(prevItems => [message, ...prevItems]); 
  };

  return (
    <ChakraProvider>
      <Box mt={10} boxShadow='xl' bg='blackAlpha.100' borderRadius={25} pt={4} pl={4} pr={4} pb={4}>
          <Accordion allowToggle defaultIndex={[0]}>
            <AccordionItem border='0px'>
              <h2>
                <AccordionButton>
                    <Box as="span" flex='1' textAlign='left'>
                        <Text fontSize='md' color='blackAlpha.700' as='b'>Loggin</Text>
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
                      '::-webkit-scrollbar':{
                            display:'none'
                        }
                      }
                    }
                    display='block' 
                    overflowY='scroll' 
                    boxShadow='lg' 
                    borderRadius={25} 
                    bg='white' 
                    minHeight='90px' 
                    width='100%'
                    padding={5} mb={4} >
                  <Table variant="simple" size="sm">
                    <Tbody>
                      {logstreamItems.map((item, index) => (
                        <LogstreamItem
                          key={index}
                          message={item.message}
                          type={item.type}
                          schema={item.style}
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
