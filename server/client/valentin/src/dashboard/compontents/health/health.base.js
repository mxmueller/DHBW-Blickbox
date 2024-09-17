import React, { useState, useEffect } from "react";
import {
  ChakraProvider,
  Flex,
  Box,
  Text,
  HStack,
  Code,
  SimpleGrid,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from "@chakra-ui/react";
import { GoContainer, GoDatabase } from "react-icons/go";
import { SiGrafana } from "react-icons/si";
import HealthDetail from "./health.detail.js";
import { sendLogToBackendOnly } from "../logstream/logtobackend";

const API_URL = "https://blickbox.maytastix.de/api/iot/api/ping";

const apis = [
  {
    key: "Blickbox",
    header: "Blickbox Hardware",
    success: "Connected",
    error: "Disconnected",
    delay: 300,
    duration: 500,
    interval: 300000, // 5 minutes
    icon: GoContainer,
  },
  {
    key: "Database",
    header: "Blickbox Datenbank",
    success: "Connected",
    error: "Disconnected",
    delay: 450,
    duration: 600,
    interval: 300000, // 5 minutes
    icon: GoDatabase,
  },
  {
    key: "Grafana",
    header: "Grafana Dashboard",
    success: "Connected",
    error: "Disconnected",
    delay: 500,
    duration: 700,
    interval: 300000, // 5 minutes
    icon: SiGrafana,
  },
];

function Desc() {
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState({});
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [lastOnline, setLastOnline] = useState(null);

  const useHealthMocks = process.env.REACT_APP_USE_HEALTH_MOCKS === "true";

  useEffect(() => {
    const fetchData = async () => {
      const currentDate = new Date();
      const formattedDateTime = currentDate
        .toISOString()
        .replace("T", " ")
        .substr(0, 19);

      try {
        setLoading(true);

        let response;
        if (useHealthMocks) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          response = {
            status: 200,
            json: () =>
              Promise.resolve({
                "Blickbox-Last-Online": "2024-09-06 16:56:02",
                "Database-Online": true,
                "Grafana-Online": true,
              }),
          };
        } else {
          response = await Promise.race([
            fetch(API_URL),
            new Promise((_, reject) =>
              setTimeout(() => reject(new Error("Timeout")), 4000),
            ),
          ]);
        }

        sendLogToBackendOnly({
          message: `Verbindungsaufbau: ${API_URL}.`,
          type: "Client Verbindungsversuch",
          code: "blackAlpha",
          date: formattedDateTime,
        });

        if (response.status === 200) {
          const data = await response.json();
          setApiStatus({
            Blickbox: true,
            Database: data["Database-Online"],
            Grafana: data["Grafana-Online"],
          });
          setLastOnline(data["Blickbox-Last-Online"]);

          sendLogToBackendOnly({
            message: `Erfolgreiche Verbindung mit: ${API_URL}`,
            type: "Server Erreichbar",
            code: "green",
            date: formattedDateTime,
          });
        } else {
          setApiStatus({
            Blickbox: false,
            Database: false,
            Grafana: false,
          });
          sendLogToBackendOnly({
            message: `Es konnte keine Verbindung mit ${API_URL} hergestellt werden.`,
            type: "Keine Verbindung zum Server",
            code: "red",
            date: formattedDateTime,
          });
        }
      } catch (error) {
        setApiStatus({
          Blickbox: false,
          Database: false,
          Grafana: false,
        });
        sendLogToBackendOnly({
          message: `${API_URL} ist nicht erreichbar.`,
          type: "Client Verbindungsversuch Fehlgeschlagen",
          code: "red",
          date: formattedDateTime,
        });
      } finally {
        setLoading(false);
        setLastUpdated(new Date());
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 300000); // 5 minutes

    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      clearInterval(intervalId);
      window.removeEventListener("resize", handleResize);
    };
  }, [useHealthMocks]);

  return (
    <ChakraProvider>
      <Box boxShadow="xl" bg="blackAlpha.100" borderRadius={25} padding={3}>
        <Accordion allowToggle defaultIndex={[0]}>
          <AccordionItem border="0px">
            <h2>
              <AccordionButton>
                <Box as="span" flex="1" textAlign="left">
                  <Text fontSize="md" color="blackAlpha.700" as="b">
                    Health monitoring
                  </Text>
                  <Flex>
                    {windowWidth < 768 ? (
                      <Box>
                        <Text
                          mt={0}
                          color="blackAlpha.600"
                          fontSize="sm"
                          w={["100%"]}
                        >
                          Letzte Aktualisierung:
                        </Text>
                        <Code colorScheme="blackAlpha">
                          {lastUpdated.toLocaleString()}
                        </Code>
                      </Box>
                    ) : (
                      <HStack>
                        <Text mt={0} color="blackAlpha.600" fontSize="sm">
                          Letzte Aktualisierung:
                        </Text>
                        <Code colorScheme="blackAlpha">
                          {lastUpdated.toLocaleString()}
                        </Code>
                      </HStack>
                    )}
                    {lastOnline && (
                      <Text
                        ml={5}
                        mt={0}
                        color="blackAlpha.600"
                        fontSize="sm"
                        mr={2}
                      >
                        Container zuletzt Online:
                        <Code ml={2} colorScheme="blackAlpha">
                          {lastOnline}
                        </Code>
                      </Text>
                    )}
                  </Flex>
                </Box>
                <AccordionIcon />
              </AccordionButton>
            </h2>
            <AccordionPanel mb={0}>
              <SimpleGrid
                columns={{ sm: 1, md: 2, lg: 4 }}
                minChildWidth="250px"
                spacing={4}
              >
                {apis.map(
                  ({
                    key,
                    header,
                    success: successText,
                    error: errorText,
                    delay,
                    duration,
                    icon,
                    interval,
                  }) => (
                    <HealthDetail
                      key={key}
                      loading={loading}
                      success={apiStatus[key]}
                      error={!apiStatus[key]}
                      header={header}
                      successText={successText}
                      errorText={errorText}
                      delay={delay}
                      duration={duration}
                      icon={icon}
                      interval={interval}
                    />
                  ),
                )}
              </SimpleGrid>
            </AccordionPanel>
          </AccordionItem>
        </Accordion>
      </Box>
    </ChakraProvider>
  );
}

export default Desc;
