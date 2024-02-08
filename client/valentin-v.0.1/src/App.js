import logo from './logo.svg';
import './App.css';
import { ChakraProvider } from "@chakra-ui/react"
import { Button } from "@chakra-ui/react"
function App({ children }) {
  return <ChakraProvider>{children}
  <Button>I just consumed some ⚡️Chakra!</Button>
  
  </ChakraProvider>
}

export default App;
