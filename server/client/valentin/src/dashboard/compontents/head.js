
import { ChakraProvider, Text, Box, Image, Flex } from "@chakra-ui/react"
import dhbw from "../icons/dhbw.png"

function Head({ children }) {
  return <ChakraProvider>{children}
  
    <Box mb={2} > 
        <Flex>
            {/* <Image height='100px' float='left' src={dhbw} alt='Logo Dhbw'></Image> */}
            <Box>
            <Text color='blackAlpha.400' fontSize='ml'>Duale Hochschule Baden-Württemberg (DHBW) Heidenheim  /  Fakultät Informatik</Text>
            <Text as='b' color='blackAlpha.700' fontSize='4xl'>Blickbox Sensometrie Dashboard</Text>
            </Box>
        </Flex>
    </Box>

  </ChakraProvider>
}

export default Head;
