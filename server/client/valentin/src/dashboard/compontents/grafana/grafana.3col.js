
import { ChakraProvider, Text, Box, Image, Flex, SimpleGrid} from "@chakra-ui/react"

function GrafanaValidation({ children }) {
  return <ChakraProvider>{children} 
    <Box boxShadow='xl' bg='blackAlpha.100' p={5} mt={10} borderRadius={25}>
      
      
    <SimpleGrid columns={{sm: 1, md: 1, lg: 3}} minChildWidth='250px'  spacing={4}>
    
    <Box bg='#f4f5f5' borderRadius={25} padding={2}>
        <iframe src="https://dhbwgrafana.maytastix.de/public-dashboards/c25a27534ff54dceb7e0eba472cd2eca" width="100%" height="600"></iframe>
      </Box>

      <Box bg='#f4f5f5' borderRadius={25} padding={2}>
        <iframe src="https://dhbwgrafana.maytastix.de/public-dashboards/7477f40e1c6e41e3a81a176feb608949" width="100%" height="600"></iframe>
      </Box>

      <Box bg='#f4f5f5' borderRadius={25} padding={2}>
        <iframe src="https://dhbwgrafana.maytastix.de/public-dashboards/feec3948f2d14209b17c310b5d909d03" width="100%" height="600"></iframe>
      </Box>
    </SimpleGrid>
    </Box>

  </ChakraProvider>
}

export default GrafanaValidation;
