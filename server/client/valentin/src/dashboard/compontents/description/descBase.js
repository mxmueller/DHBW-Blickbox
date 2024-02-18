import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, Text, Code, SimpleGrid } from "@chakra-ui/react";
import { GoContainer } from "react-icons/go";
import { GoDatabase } from "react-icons/go";
import { SiGrafana } from "react-icons/si";
import { Fade } from "react-awesome-reveal";
import DescDetail from './descDetail';

const apis = [
    { 
        url: 'https://dhbwapi.maytastix.de/iot/api/pingBB', 
        header: 'Blickbox Hardware',
        success: 'Connected',
        error: 'Disconnected',
        delay: 100,
        duration: 300,
        interval: 60000, 
        icon: GoContainer
    },
    { 
        url: 'https://dhbwapi.maytastix.de/iot/api/pingDB', 
        header: 'Blickbox Datenbank',
        success: 'Connected',
        error: 'Disconnected',
        delay: 250,
        duration: 200,
        interval: 60000, 
        icon: GoDatabase
    },
    { 
        url: 'https://dhbwapi.maytastix.de/iot/api/pingGF', 
        header: 'Grafana',
        success: 'Connected',
        error: 'Disconnected',
        delay: 400,
        duration: 100,
        interval: 60000, 
        icon: SiGrafana
    },
];

function Desc() {
    const [loading, setLoading] = useState({});
    const [success, setSuccess] = useState({});
    const [error, setError] = useState({});

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
            <Box boxShadow='xl' bg='#EDF2F7' borderRadius={25} padding={4}>
                <SimpleGrid columns={[2, null, 4]} spacing={4}>
                    {apis.map(({ url, header, success: successText, error: errorText, delay, duration, icon, interval }) => (
                        <DescDetail
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
                <Text mt={5} fontSize='md'>Letzte Aktualisierung:
                    <Code ml={2} mr={2}>11.02.24 19:59:03</Code>
                </Text>
            </Box>
        </ChakraProvider>
    );
}

export default Desc;
