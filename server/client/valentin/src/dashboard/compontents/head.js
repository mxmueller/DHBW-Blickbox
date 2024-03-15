
import {ChakraProvider, Text, Box, Image, Flex, HStack, Spacer} from "@chakra-ui/react"
import Settings from './settings/settings.js';

function Head({ children }) {
return <ChakraProvider>{children}
  

    <Box mb={2} > 
        <Flex>

            {/* <Image height='100px' float='left' src={dhbw} alt='Logo Dhbw'></Image> */}
            <Box>
            <Text color='blackAlpha.400' fontSize='ml'>Duale Hochschule Baden-Württemberg (DHBW) Heidenheim  /  Fakultät Informatik</Text>
            <Text as='b' color='blackAlpha.700' fontSize='4xl'>Blickbox Sensometrie Dashboard</Text>
            </Box>
            <Spacer />
            <HStack>
                <Settings right={0} float='right'/>
            </HStack>
        </Flex>
    </Box>

  </ChakraProvider>
}

export default Head;
