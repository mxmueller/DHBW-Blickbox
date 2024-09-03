import React, { useState, useEffect } from 'react';
import { ChakraProvider, Flex, Box, Text, HStack, Code, SimpleGrid, Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon } from "@chakra-ui/react";
import { GoContainer, GoDatabase } from "react-icons/go";
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
        interval: 300000, // 5 minutes
        icon: GoContainer
    },
    {
        url: 'https://dhbwapi.maytastix.de/iot/api/pingDB',
        header: 'Blickbox Datenbank',
        success: 'Connected',
        error: 'Disconnected',
        delay: 450,
        duration: 600,
        interval: 300000, // 5 minutes
        icon: GoDatabase
    },
    {
        url: 'https://dhbwapi.maytastix.de/iot/api/pingGF',
        header: 'Grafana',
        success: 'Connected',
        error: 'Disconnected',
        delay: 500,
        duration: 700,
        interval: 300000, // 5 minutes
        icon: SiGrafana
    },
];

// Mock data
const mockData = {
    'https://dhbwapi.maytastix.de/iot/api/pingBB': { status: 200, last_online: '2024-08-20 10:00:00' },
    'https://dhbwapi.maytastix.de/iot/api/pingDB': { status: 500, last_online: null },
    'https://dhbwapi.maytastix.de/iot/api/pingGF': { status: 200, last_online: '2024-08-20 09:55:00' },
};

function Desc() {
    const [loading, setLoading] = useState({});
    const [success, setSuccess] = useState({});
    const [error, setError] = useState({});
    const [lastUpdated, setLastUpdated] = useState(new Date());
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);
    const [lastOnline, setLastOnline] = useState(null);

    // Check if mocks should be used for health monitoring
    const useHealthMocks = process.env.REACT_APP_USE_HEALTH_MOCKS === 'true';

    useEffect(() => {
        const currentDate = new Date();
        const formattedDateTime = currentDate.toISOString().replace('T', ' ').substr(0, 19);

        const fetchData = async (apiUrl, interval) => {
            try {
                setLoading(prevLoading => ({
                    ...prevLoading,
                    [apiUrl]: true
                }));

                let response;
                if (useHealthMocks) {
                    // Use mock data
                    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network delay
                    response = {
                        status: mockData[apiUrl].status,
                        json: () => Promise.resolve(mockData[apiUrl])
                    };
                } else {
                    // Real API call
                    response = await Promise.race([
                        fetch(apiUrl),
                        new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 4000))
                    ]);
                }

                Logstream.addItemToLogstream({ message: `Verbindungsaufbau: ${apiUrl}.`, type: 'Client Verbindungsversuch', code: 'blackAlpha', date: formattedDateTime });

                if (response.status === 200) {
                    setSuccess(prevSuccess => ({
                        ...prevSuccess,
                        [apiUrl]: true
                    }));
                    setError(prevError => ({
                        ...prevError,
                        [apiUrl]: false
                    }));

                    Logstream.addItemToLogstream({ message: `Erfolgreiche Verbindung mit: ${apiUrl}`, type: 'Server Erreichbar', code: 'green', date: formattedDateTime });

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

                    Logstream.addItemToLogstream({ message: `Es konnte keine Verbindung mit ${apiUrl} hergestellt werden.`, type: 'Keine Verbindung zum Server', code: 'red', date: formattedDateTime });
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

                Logstream.addItemToLogstream({ message: `${apiUrl} ist nicht erreichbar.`, type: 'Client Verbindungsversuch Fehlgeschlagen', code: 'red', date: formattedDateTime });
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
    }, [useHealthMocks]);

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