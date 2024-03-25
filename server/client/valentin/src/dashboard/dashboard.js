
import { ChakraProvider } from "@chakra-ui/react"
import { Box, Center } from '@chakra-ui/react'
import { Fade } from "react-awesome-reveal";

import Health from './compontents/health/health.base';
import Head from './compontents/head';
import GrafanaContainer from "./compontents/grafana/grafana.container.js";
import Grafana3Col from "./compontents/grafana/grafana.3col.js";
import Grafana2Col from "./compontents/grafana/grafana.2col.js"
import Logstream from "./compontents/logstream/logstream.js";

function Dashboard({ children }) {
  return <ChakraProvider>{children}
              <Center>  
                <Box m={5} width="100%" maxWidth={'1800px'}>
                  <Head></Head>    
                
                  <Fade>
                    <Health/>
                  </Fade>
                  
                  <Fade>
                    <Grafana3Col/>
                  </Fade>

                  <Fade>
                    <GrafanaContainer/>
                  </Fade>

                  <Fade>
                    <Grafana2Col/>
                  </Fade>

                  <Fade>
                    <Logstream/>
                  </Fade>
                </Box>
              </Center>
    </ChakraProvider>
}

export default Dashboard;
