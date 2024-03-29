import React, { useState, useEffect } from 'react';
import { ChakraProvider, Flex, Box, Text, HStack, Code, SimpleGrid, Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon } from "@chakra-ui/react";
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
        interval: 300000, // 5 Minuten
        icon: GoContainer
    },
    { 
        url: 'https://dhbwapi.maytastix.de/iot/api/pingDB', 
        header: 'Blickbox Datenbank',
        success: 'Connected',
        error: 'Disconnected',
        delay: 450,
        duration: 600,
        interval: 300000, // 5 Minuten
        icon: GoDatabase
    },
    { 
        url: 'https://dhbwapi.maytastix.de/iot/api/pingGF', 
        header: 'Grafana',
        success: 'Connected',
        error: 'Disconnected',
        delay: 500,
        duration: 700,
        interval: 300000, // 5 Minuten
        icon: SiGrafana
    },
];

function Desc() {
    const [loading, setLoading] = useState({});
    const [success, setSuccess] = useState({});
    const [error, setError] = useState({});
    const [lastUpdated, setLastUpdated] = useState(new Date());
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);
    const [lastOnline, setLastOnline] = useState(null); // Zustand für den letzten Online-Zeitstempel

    useEffect(() => {
        const currentDate = new Date();

        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, '0');
        const day = String(currentDate.getDate()).padStart(2, '0');

        const hours = String(currentDate.getHours()).padStart(2, '0');
        const minutes = String(currentDate.getMinutes()).padStart(2, '0');
        const seconds = String(currentDate.getSeconds()).padStart(2, '0');
        
        const formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

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

                Logstream.addItemToLogstream({ message: `Verbindungsaufbau: ` + apiUrl + '.', type: 'Client Verbindungsversuch', code: 'blackAlpha', date: formattedDateTime });

                if (response.status === 200) {
                    setSuccess(prevSuccess => ({
                        ...prevSuccess,
                        [apiUrl]: true
                    }));
                    setError(prevError => ({
                        ...prevError,
                        [apiUrl]: false
                    }));

                    Logstream.addItemToLogstream({ message: `Erfolgreiche Verbindung mit: ` + apiUrl, type: 'Server Erreichbar', code: 'green', date: formattedDateTime });

                    // Wenn die GET-Anfrage erfolgreich ist, setze den letzten Online-Zeitstempel
                    const data = await response.json();
                    if (data && data.last_online) {
                        setLastOnline(data.last_online);
                    }
                
                } else {
                    setError(prevError => ({
                        ...prevError,
                        [apiUrl]: true
                    }));
                    setSuccess(prevSuccess => ({
                        ...prevSuccess,
                        [apiUrl]: false
                    }));

                    Logstream.addItemToLogstream({ message: `Es konnte keine Verbindung mit ` + apiUrl + ' hergestellt werden.', type: 'Keine Verbindung zum Server', code: 'red', date: formattedDateTime });
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

                Logstream.addItemToLogstream({ message: apiUrl + ' ist nicht erreibar.', type: 'Client Verbindungsversuch Fehlgeschlagen', code: 'red', date: formattedDateTime });
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
                                    <Flex>
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
                                        {lastOnline && (
                                            <Text ml={5} mt={0} color='blackAlpha.600' fontSize='sm' mr={2} >Container zuletzt Online:<Code ml={2} colorScheme='blackAlpha'>{lastOnline}</Code></Text>
                                        )}
                                        </Flex>
                                    
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
