
import { ChakraProvider } from "@chakra-ui/react"
import { Button } from "@chakra-ui/react"
import { Container, Box, Center } from '@chakra-ui/react'

import Health from './compontents/health/healthBase';
import Head from './compontents/head';

function Dashboard({ children }) {
  return <ChakraProvider>{children}
        <Center>
        <Box m={5} width="100%" maxWidth={'1400px'}>
          <Head></Head>    
          <Health></Health>
        </Box>
        </Center>


    </ChakraProvider>
}

export default Dashboard;
