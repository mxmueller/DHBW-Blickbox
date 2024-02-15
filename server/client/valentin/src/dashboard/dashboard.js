import '../App.css';
import { ChakraProvider } from "@chakra-ui/react"
import { Button } from "@chakra-ui/react"
import { Container, Box } from '@chakra-ui/react'

import Desc from './compontents/desc';
import Head from './compontents/head';

function Dashboard({ children }) {
  return <ChakraProvider>{children}
        
        <Box m={5}>
          <Head></Head>    
          <Desc></Desc>
        </Box>


    </ChakraProvider>
}

export default Dashboard;
