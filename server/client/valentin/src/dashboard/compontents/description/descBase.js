import React from 'react';
import { ChakraProvider, Box, Text, Code, SimpleGrid } from "@chakra-ui/react";
import { GoContainer } from "react-icons/go";
import { GoServer } from "react-icons/go";
import { Fade } from "react-awesome-reveal";
import { IoUnlink } from "react-icons/io5";
import { CgBlock } from "react-icons/cg";
import { FaDocker } from "react-icons/fa";
import DescDetail from './descDetail';
import DescSkeleton from './descSkeleton';

function Desc() {
    return (
        <ChakraProvider>
            <Box boxShadow='xl' bg='#EDF2F7' borderRadius={25} padding={4}>
                <SimpleGrid columns={[2, null, 3]} spacing={5}>
                    <DescDetail detailDelay={200} detailDuration={330} icon={GoContainer} text1="Blickbox Container" text2="Connected" isConnected />
                    <DescDetail detailDelay={200} detailDuration={330} icon={GoServer} text1="Data Server" text2="Disconnected" />
                    <DescDetail detailDelay={200} detailDuration={330} icon={FaDocker} text1="Auslastung Data Server" percentage="56%" />
                    <DescSkeleton skeletonDelay={200} skeletonDuration={125} />
                </SimpleGrid>

                <Text mt={5} fontSize='md'>Letzte Aktualisierung:
                    <Code ml={2} mr={2}>11.02.24 19:59:03</Code>
                </Text>
            </Box>
        </ChakraProvider>
    );
}

export default Desc;