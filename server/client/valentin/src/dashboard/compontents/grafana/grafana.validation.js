
import { ChakraProvider, Text, Box, Image, Flex } from "@chakra-ui/react"

function GrafanaValidation({ children }) {
  return <ChakraProvider>{children}
  
    <Box boxShadow='xl' bg='blackAlpha.100' borderRadius={25}  mt={10}> 
      <Box padding={15}>
        <iframe src="https://dhbwgrafana.maytastix.de/public-dashboards/557afbb6558043878ca3c6a223929e9d" width="100%" height="600"></iframe>
      </Box>
    </Box>
  </ChakraProvider>
}

export default GrafanaValidation;
