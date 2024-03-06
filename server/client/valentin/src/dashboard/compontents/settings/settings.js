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

function Settings({ }) {
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
            onClick={onOpen}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            p={2} // Fügen Sie Padding hinzu, um den Klickbereich zu vergrößern
            borderRadius="50%" // Runden Sie die Ecken des Box-Elements ab, um ein kreisförmiges Icon zu erhalten
            cursor="pointer" // Ändern Sie den Mauszeiger, um anzuzeigen, dass das Element klickbar ist
            transition="background-color 0.3s" // Fügen Sie eine Übergangsanimation für die Hintergrundfarbe hinzu
            _hover={{ backgroundColor: "#f0f0f0" }} // Fügen Sie das Hover-Styling über die Chakra-UI Pseudo-Klasse hinzu
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
