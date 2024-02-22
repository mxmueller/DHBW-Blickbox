import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, Text, HStack, Code, SimpleGrid, Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon } from "@chakra-ui/react";
import { GoContainer } from "react-icons/go";
import { GoDatabase } from "react-icons/go";
import { SiGrafana } from "react-icons/si";
import HealthDetail from './health.detail.js';
import Logstream from '../logstream/logstream.js';

const apis = [
    { 
        url: 'https://dhbwapi.maytastix.de/iot/api/pingBB', 
        header: 'Blickbox Hardware',
        success: 'Connected',
        error: 'Disconnected',
        delay: 300,
        duration: 500,
        interval: 60000, 
        icon: GoContainer
    },
    { 
        url: 'https://dhbwapi.maytastix.de/iot/api/pingDB', 
        header: 'Blickbox Datenbank',
        success: 'Connected',
        error: 'Disconnected',
        delay: 450,
        duration: 600,
        interval: 60000, 
        icon: GoDatabase
    },
    { 
        url: 'https://dhbwapi.maytastix.de/iot/api/pingGF', 
        header: 'Grafana',
        success: 'Connected',
        error: 'Disconnected',
        delay: 500,
        duration: 700,
        interval: 60000, 
        icon: SiGrafana
    },
];

function Desc() {
    const [loading, setLoading] = useState({});
    const [success, setSuccess] = useState({});
    const [error, setError] = useState({});
    const [lastUpdated, setLastUpdated] = useState(new Date());
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);

    useEffect(() => {
        const fetchData = async (apiUrl, interval) => {
            try {
                setLoading(prevLoading => ({
                    ...prevLoading,
                    [apiUrl]: true
                }));

                const response = await Promise.race([
                    fetch(apiUrl),
                    new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 4000))
                ]);

                Logstream.addItemToLogstream({ message: `Verbindungsaufbau: ` + apiUrl + '.', type: 'Versuch', style: 'blackAlpha', date: Date.now() });

                if (response.status === 200) {
                    setSuccess(prevSuccess => ({
                        ...prevSuccess,
                        [apiUrl]: true
                    }));
                    setError(prevError => ({
                        ...prevError,
                        [apiUrl]: false
                    }));

                    Logstream.addItemToLogstream({ message: `Erfolgreiche Verbindung mit: ` + apiUrl, type: 'Erreichbar', style: 'green', date: Date.now() });
                
                } else {
                    setError(prevError => ({
                        ...prevError,
                        [apiUrl]: true
                    }));
                    setSuccess(prevSuccess => ({
                        ...prevSuccess,
                        [apiUrl]: false
                    }));

                    Logstream.addItemToLogstream({ message: `Es konnte keine Verbindung mit ` + apiUrl + ' hergestellt werden.', type: 'Keine Verbindung', style: 'red', date: Date.now() });
                }
            } catch (error) {
                setError(prevError => ({
                    ...prevError,
                    [apiUrl]: true
                }));
                setSuccess(prevSuccess => ({
                    ...prevSuccess,
                    [apiUrl]: false
                }));

                Logstream.addItemToLogstream({ message: apiUrl + ' ist nicht erreibar.', type: 'Fehlgeschlagen', style: 'red', date: Date.now() });
            } finally {
                setLoading(prevLoading => ({
                    ...prevLoading,
                    [apiUrl]: false
                }));
                setLastUpdated(new Date());
            }
        };

        const fetchDataWithInterval = ({ url, interval }) => {
            fetchData(url);
            const intervalId = setInterval(() => {
                fetchData(url);
            }, interval);
            return () => clearInterval(intervalId);
        };

        apis.forEach(api => {
            fetchDataWithInterval(api);
        });

       

          const handleResize = () => {
            setWindowWidth(window.innerWidth);
          };
      
          window.addEventListener('resize', handleResize);
      
          return () => {
            window.removeEventListener('resize', handleResize);
          };
    }, []);

    return (
        <ChakraProvider>
            <Box boxShadow='xl' bg='blackAlpha.100' borderRadius={25} padding={3}>
                <Accordion allowToggle defaultIndex={[0]}>
                    <AccordionItem border='0px'>
                        <h2>
                            <AccordionButton>
                                <Box as="span" flex='1' textAlign='left'>
                                    <Text fontSize='md' color='blackAlpha.700' as='b'>Health monitoring</Text>
                                    {windowWidth < 768 ? 
                                        <Box>
                                            <Text mt={0} color='blackAlpha.600' fontSize='sm' w={["100%"]}>Letzte Aktualisierung:</Text>
                                            <Code colorScheme='blackAlpha'>{lastUpdated.toLocaleString()}</Code>
                                        </Box>
                                    : 
                                        <HStack>
                                            <Text mt={0} color='blackAlpha.600' fontSize='sm'>Letzte Aktualisierung:</Text>
                                            <Code colorScheme='blackAlpha'>{lastUpdated.toLocaleString()}</Code>
                                        </HStack>
                                    }
                                    
                                </Box>
                                <AccordionIcon />
                            </AccordionButton>
                        </h2>
                        <AccordionPanel mb={0}>
                            <SimpleGrid columns={{sm: 1, md: 2, lg: 4}} minChildWidth='250px'  spacing={4}>
                                {apis.map(({ url, header, success: successText, error: errorText, delay, duration, icon, interval }) => (
                                    <HealthDetail
                                        key={url}
                                        loading={loading[url]}
                                        success={success[url]}
                                        error={error[url]}
                                        header={header}
                                        successText={successText}
                                        errorText={errorText}
                                        delay={delay}
                                        duration={duration}
                                        icon={icon}
                                        interval={interval}
                                    />
                                ))}
                            </SimpleGrid>
                        </AccordionPanel>
                    </AccordionItem>
                </Accordion>
            </Box>
        </ChakraProvider>
    );
}


export default Desc;
