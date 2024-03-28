
import { ChakraProvider, Text, Box, Image, Flex, SimpleGrid} from "@chakra-ui/react"

function GrafanaValidation({ children }) {
  return <ChakraProvider>{children} 
    <Box boxShadow='xl' bg='blackAlpha.100' p={5} mt={10} borderRadius={25}>
      
      
    <SimpleGrid columns={{sm: 1, md: 1, lg: 2}} minChildWidth='250px'  spacing={4}>
    
    <Box bg='#f4f5f5' borderRadius={25} padding={2}>
        <iframe src="https://dhbwgrafana.maytastix.de/public-dashboards/fc8daf716c5545abafe35e81ca78c8b0" width="100%" height="600"></iframe>
      </Box>

      <Box bg='#f4f5f5' borderRadius={25} padding={2}>
        <iframe src="https://dhbwgrafana.maytastix.de/public-dashboards/ac794c5a60b04f818cf6754246f32b0e" width="100%" height="600"></iframe>
      </Box>
    </SimpleGrid>
    </Box>

  </ChakraProvider>
}

export default GrafanaValidation;
