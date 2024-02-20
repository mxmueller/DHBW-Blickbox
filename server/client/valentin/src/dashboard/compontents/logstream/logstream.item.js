
import {  Code, Tr, Td } from "@chakra-ui/react"

function LogstreamItem({ type, schema, message }) {
    
  return (

    <Tr>
        <Td>
            <Code colorScheme={schema}>{type}</Code>
        </Td>
        <Td>{message}</Td>
    </Tr>
  )
}

export default LogstreamItem;
