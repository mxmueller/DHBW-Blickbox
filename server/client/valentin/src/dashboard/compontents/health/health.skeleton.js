import React from 'react';
import { Box, Circle, Flex, Icon, SimpleGrid, Text, HStack, SkeletonCircle, SkeletonText } from "@chakra-ui/react";
import { Fade } from "react-awesome-reveal";

function DescSkeleton({ skeletonDuration, skeletonDelay }) {
    return (
        <Fade direction="up" duration={skeletonDuration} delay={skeletonDelay}>
            <Box boxShadow='xl' borderRadius={25} bg='white' minHeight='80px' width='100%' padding={5} >
                <Flex>
                    <SkeletonCircle size='50px' bg='#e2001a' color='white' />
                    <SimpleGrid mt={2} ml={4} columns={1} spacing={0}>
                    <SkeletonText noOfLines={1} spacing='4' skeletonHeight='3' w={28}/>
                    <SkeletonText mt={1} noOfLines={1} spacing='4' skeletonHeight='3' w={20}/>
                    </SimpleGrid>
                </Flex>
            </Box>
        </Fade>
    );
}

export default DescSkeleton;