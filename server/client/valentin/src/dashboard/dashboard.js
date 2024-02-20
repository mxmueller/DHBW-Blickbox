
import { ChakraProvider } from "@chakra-ui/react"
import { Box, Center } from '@chakra-ui/react'
import { Fade } from "react-awesome-reveal";

import Health from './compontents/health/health.base';
import Head from './compontents/head';
// import GrafanaValidation from "./compontents/grafana/grafana.validation.js";
import Logstream from "./compontents/logstream/logstream.js";

function Dashboard({ children }) {
  return <ChakraProvider>{children}
              <Center>  
                <Box m={5} width="100%" maxWidth={'1400px'}>
                  <Head></Head>    
                
                  <Fade>
                    <Health/>
                  </Fade>

                  <Fade>
                    <Logstream/>
                  </Fade>

                  {/* <Fade>
                  <GrafanaValidation/>
                  </Fade> */}
                </Box>
              </Center>
    </ChakraProvider>
}

export default Dashboard;
