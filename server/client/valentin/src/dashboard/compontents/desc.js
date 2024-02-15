import {
    ChakraProvider,
    Button,
    Container,
    SimpleGrid,
    Box,
    Center,
    Square,
    Circle,
    Stat,
    StatLabel,
    StatNumber,
    StatHelpText,
    StatArrow,
    Kbd,
    Text,
    Code,
    Image,
    Flex,
    Icon,
    HStack
  } from "@chakra-ui/react";

import { GoContainer } from "react-icons/go";
import { GoServer } from "react-icons/go";
import { Fade } from "react-awesome-reveal";
import { IoUnlink } from "react-icons/io5";
import { CgBlock } from "react-icons/cg";
import { FaDocker } from "react-icons/fa";
import { FaRegChartBar } from "react-icons/fa";

import container from '../icons/container.png';
import server from '../icons/server.png'

function Desc({ children }) {
  return <ChakraProvider>{children}
    
    <Box boxShadow='xl' bg='#EDF2F7' borderRadius={25} padding={4} > 
        <SimpleGrid columns={[2, null, 3]} spacing={5}>
            <Box>
                <SimpleGrid columns={1} spacingY={2} >       
                    <Fade direction="up" duration={300} delay={100}>
                        <Box boxShadow='xl' borderRadius={25} bg='white' minHeight='80px' width='100%' padding={5}>
                            <Flex>
                                <Circle size='50px' bg='#e2001a' color='white'>
                                    <Icon boxSize={30} as={GoContainer} />
                                </Circle>
                                <SimpleGrid ml={4} columns={1} spacing={0}>
                                    <Box><Text fontSize='m' color='blackAlpha.500' float='left'>Blickbox Container</Text></Box>
                                    <Box> <HStack spacing='5px' ><Icon boxSize={6} as={IoUnlink} />  <Text fontSize='lg' as='b'>Connected</Text></HStack>
                                   </Box>
                                </SimpleGrid>   
                            </Flex>
                        </Box>
                    </Fade>                
                    <Fade direction="up"  duration={400} delay={200}>
                        <Box boxShadow='xl' borderRadius={25} mt={2} bg='white' minHeight='80px' width='100%' padding={5}>
                            <Flex>
                                <Circle size='50px' bg='#e2001a' color='white'>
                                    <Icon boxSize={27} as={GoServer} />
                                </Circle>
                                <SimpleGrid ml={4} columns={1} spacing={0}>
                                    <Box><Text fontSize='m' color='blackAlpha.500' float='left'>Data Server</Text></Box>
                                    <Box> <HStack spacing='2px' ><Icon boxSize={6} as={CgBlock} />  <Text fontSize='lg' as='b'>Disconnected</Text></HStack>
                                   </Box>
                                </SimpleGrid>   
                            </Flex>                           
                        </Box>
                    </Fade>
                </SimpleGrid>
            </Box>
            
            <Box>
                <SimpleGrid columns={1} spacingY={2} >       
                    <Fade direction="up" duration={500} delay={250}>
                        <Box boxShadow='xl' borderRadius={25} bg='white' minHeight='80px' width='100%' padding={5}>
                            <Flex>
                                <Circle size='50px' bg='#e2001a' color='white'>
                                    <Icon boxSize={30} as={FaDocker} />
                                </Circle>
                                <SimpleGrid ml={4} columns={1} spacing={0}>
                                    <Box><Text fontSize='m' color='blackAlpha.500' float='left'>Auslastung Data Server</Text></Box>
                                    <Box> <HStack>  <Text fontSize='lg' as='b'>56%</Text></HStack>
                                   </Box>
                                </SimpleGrid>   
                            </Flex>
                        </Box>
                    </Fade>                
                    <Fade direction="up"  duration={500} delay={340}>
                        <Box boxShadow='xl' borderRadius={25} mt={2} bg='white' minHeight='80px' width='100%' padding={5}>
                            <Flex>
                                <Circle size='50px' bg='#e2001a' color='white'>
                                    <Icon boxSize={27} as={FaRegChartBar} />
                                </Circle>
                                <SimpleGrid ml={4} columns={1} spacing={0}>
                                    <Box><Text fontSize='m' color='blackAlpha.500' float='left'>Data #X</Text></Box>
                                    <Box> <HStack spacing='2px'><Text fontSize='lg' as='b'>87493</Text></HStack>
                                   </Box>
                                </SimpleGrid>   
                            </Flex>                           
                        </Box>
                    </Fade>
                </SimpleGrid>
            </Box>

            <Box>
                <SimpleGrid columns={1} spacingY={2} >       
                    <Fade direction="up" duration={500} delay={430}>
                        <Box boxShadow='xl' borderRadius={25} bg='white' minHeight='80px' width='100%' padding={5}>
                        <Flex>
                                <Circle size='50px' bg='#e2001a' color='white'>
                                    <Icon boxSize={27} as={FaRegChartBar} />
                                </Circle>
                                <SimpleGrid ml={4} columns={1} spacing={0}>
                                    <Box><Text fontSize='m' color='blackAlpha.500' float='left'>Data #X</Text></Box>
                                    <Box> <HStack spacing='2px'><Text fontSize='lg' as='b'>87493</Text></HStack>
                                   </Box>
                                </SimpleGrid>   
                            </Flex>  
                        </Box>
                    </Fade>                
                    <Fade direction="up"  duration={500} delay={500}>
                        <Box boxShadow='xl' borderRadius={25} mt={2} bg='white' minHeight='80px' width='100%' padding={5}>
                            <Flex>
                                <Circle size='50px' bg='#e2001a' color='white'>
                                    <Icon boxSize={27} as={FaRegChartBar} />
                                </Circle>
                                <SimpleGrid ml={4} columns={1} spacing={0}>
                                    <Box><Text fontSize='m' color='blackAlpha.500' float='left'>Data #X</Text></Box>
                                    <Box> <HStack spacing='2px'><Text fontSize='lg' as='b'>87493</Text></HStack>
                                   </Box>
                                </SimpleGrid>   
                            </Flex>                            
                        </Box>
                    </Fade>
                </SimpleGrid>
            </Box>
            

        </SimpleGrid>
    
        <Text mt={5} fontSize='md'>Letzte Aktualisierung:
        <Code ml={2} mr={2}>11.02.24 19:59:03</Code>
        </Text>

    </Box>



    </ChakraProvider>
}


export default Desc;
