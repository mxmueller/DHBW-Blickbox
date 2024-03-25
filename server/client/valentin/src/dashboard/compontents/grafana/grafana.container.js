
import { ChakraProvider, Text, Box, Image, Flex } from "@chakra-ui/react"

function GrafanaValidation({ children }) {
  return <ChakraProvider>{children} 
    <Box boxShadow='xl' bg='blackAlpha.100' p={5} mt={10} borderRadius={25}>
    <Box bg='#f4f5f5' borderRadius={25}> 
      <Box padding={15}>
        <iframe src="https://dhbwgrafana.maytastix.de/public-dashboards/d0688f51a9534c4bbfedec86c8b175cb" width="100%" height="800"></iframe>
      </Box>
    </Box>
    </Box>
  </ChakraProvider>
}

export default GrafanaValidation;
