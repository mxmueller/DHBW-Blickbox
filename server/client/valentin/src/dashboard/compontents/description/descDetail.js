import React from 'react';
import { Box, Circle, Flex, Icon, SimpleGrid, Text, HStack, SkeletonCircle, SkeletonText} from "@chakra-ui/react";
import { Fade } from "react-awesome-reveal";

function DescDetail({ loading, success, error, icon, successText, errorText, header, detailDelay, detailDuration}) {

    return (
        <Fade direction="up" duration={detailDuration} delay={detailDelay}>
            <Box boxShadow='xl' borderRadius={25} bg='white' minHeight='90px' width='100%' padding={5} >
                <Flex>
                    {loading ? (
                        <>
                            <SkeletonCircle size='50px' bg='#e2001a' color='white' />
                            <SimpleGrid mt={2} ml={4} columns={1} spacing={0}>
                                <SkeletonText noOfLines={1} spacing='4' skeletonHeight='3' w={28}/>
                                <SkeletonText mt={1} noOfLines={1} spacing='4' skeletonHeight='3' w={20}/>
                            </SimpleGrid>
                        </>
                    ) : (
                        <>
                        {success ? (
                            <>
                                <Flex>
                                 <Circle size='50px' bg='#e2001a' color='white'>
                                   <Icon boxSize={30} as={icon} />
                                </Circle>
                                    <SimpleGrid ml={4} columns={1} spacing={0}>
                                    <Text fontSize='m' color='blackAlpha.500'>{header}</Text>
                                        <HStack spacing='5px'>
                                            <Text fontSize='lg' as='b'>{successText}</Text>
                                        </HStack>
                                    </SimpleGrid>
                                </Flex>
                            </>
                        ) : error ? (
                            <>
                                <Flex>
                                 <Circle size='50px' bg='#e2001a' color='white'>
                                   <Icon boxSize={30} as={icon} />
                                </Circle>
                                    <SimpleGrid ml={4} columns={1} spacing={0}>
                                    <Text fontSize='m' color='blackAlpha.500'>{header}</Text>
                                        <HStack spacing='5px'>
                                            <Text fontSize='lg' as='b'>{errorText}</Text>
                                        </HStack>
                                    </SimpleGrid>
                                </Flex>
                            </>
                        ) : (
                            <>
                                missing setting
                            </>
                        )}
                        </>
                    )}
                </Flex>
            </Box>
        </Fade>
    );
}

export default DescDetail;