import React from 'react';
import { Box, Circle, Flex, Icon, SimpleGrid, Text, HStack } from "@chakra-ui/react";
import { Fade } from "react-awesome-reveal";

function DescDetail({ icon, text1, text2, isConnected, percentage, detailDelay, detailDuration}) {
    return (
        <Fade direction="up" duration={detailDuration} delay={detailDelay}>
            <Box boxShadow='xl' borderRadius={25} bg='white' minHeight='80px' width='100%' padding={5} >
                <Flex>
                    <Circle size='50px' bg='#e2001a' color='white'>
                        <Icon boxSize={30} as={icon} />
                    </Circle>
                    <SimpleGrid ml={4} columns={1} spacing={0}>
                        <Text fontSize='m' color='blackAlpha.500'>{text1}</Text>
                        <HStack spacing='5px'>
                            <Text fontSize='lg' as='b'>{text2}</Text>
                        </HStack>
                        {percentage && <Text fontSize='lg' as='b'>{percentage}</Text>}
                    </SimpleGrid>
                </Flex>
            </Box>
        </Fade>
    );
}

export default DescDetail;