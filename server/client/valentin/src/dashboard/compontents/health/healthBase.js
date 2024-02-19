import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, Text, Button, HStack, Code, SimpleGrid,
    Accordion,
    AccordionItem,
    AccordionButton,
    AccordionPanel,
    AccordionIcon, } from "@chakra-ui/react";
import { GoContainer } from "react-icons/go";
import { GoDatabase } from "react-icons/go";
import { SiGrafana } from "react-icons/si";
import { Fade } from "react-awesome-reveal";
import HealthDetail from './healthDetail';

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

    useEffect(() => {
        const fetchData = async (apiUrl, interval) => {
            setLoading(prevState => ({
                ...prevState,
                [apiUrl]: true
            }));
            try {
                const response = await Promise.race([
                    fetch(apiUrl),
                    new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 4000))
                ]);
                if (response.status === 200) {
                    setSuccess(prevState => ({
                        ...prevState,
                        [apiUrl]: true
                    }));
                    setError(prevState => ({
                        ...prevState,
                        [apiUrl]: false
                    }));
                } else {
                    setError(prevState => ({
                        ...prevState,
                        [apiUrl]: true
                    }));
                    setSuccess(prevState => ({
                        ...prevState,
                        [apiUrl]: false
                    }));
                }
            } catch (error) {
                setError(prevState => ({
                    ...prevState,
                    [apiUrl]: true
                }));
                setSuccess(prevState => ({
                    ...prevState,
                    [apiUrl]: false
                }));
            } finally {
                setLoading(prevState => ({
                    ...prevState,
                    [apiUrl]: false
                }));
                setLastUpdated(new Date()); // Aktualisierung der letzten Aktualisierungszeit
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
    }, []);

    return (
        <ChakraProvider>

        <Box boxShadow='xl' bg='blackAlpha.100' borderRadius={25} padding={4}>
            <Accordion allowToggle defaultIndex={[0]}>
                <AccordionItem border='0px' >
                    <h2>
                    <AccordionButton>
                        <Box as="span" flex='1' textAlign='left'>
                        <Text fontSize='xl' color='blackAlpha.700' as='b'>Health monitoring</Text>
                        <HStack>
                        <Text mt={0} color='blackAlpha.600' fontSize='md'>Letzte Aktualisierung:</Text>
                            <Code colorScheme='blackAlpha'>{lastUpdated.toLocaleString()}</Code>
                        </HStack>
               
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
