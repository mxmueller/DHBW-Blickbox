import { ChakraProvider, Box } from '@chakra-ui/react';
import { IoIosSettings } from "react-icons/io";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Button,
  useDisclosure
} from '@chakra-ui/react';

import AlertSettings from './settings.alerts.js';

function Settings() {
  const { isOpen, onOpen, onClose } = useDisclosure();

  const handleMouseEnter = (event) => {
    event.currentTarget.style.backgroundColor = "#f0f0f0"; // Ändern Sie die Hintergrundfarbe beim Mouseover
  };

  const handleMouseLeave = (event) => {
    event.currentTarget.style.backgroundColor = "transparent"; // Setzen Sie die Hintergrundfarbe zurück, wenn die Maus das Icon verlässt
  };

  return (
      <ChakraProvider>
        <Box
            data-testid="settings-icon"
            onClick={onOpen}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            p={2}
            borderRadius="50%"
            cursor="pointer"
            transition="background-color 0.3s"
            _hover={{ backgroundColor: "#f0f0f0" }}
        >
          <IoIosSettings size={24} color='#00000033'/>
        </Box>

        <Modal isOpen={isOpen} onClose={onClose}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Dashboard Einstellungen</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <AlertSettings />
            </ModalBody>
            <ModalFooter>
              <Button colorScheme='gray' mr={3} onClick={onClose}>
                Schließen
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>

      </ChakraProvider>
  );
}

export default Settings;
