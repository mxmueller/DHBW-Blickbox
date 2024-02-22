
import {  Code, Tr, Td } from "@chakra-ui/react"

function LogstreamItem({ type, schema, message, date }) {
    
  return (

    <Tr>
        <Td>
            <Code colorScheme={schema}>{type}</Code>
        </Td>
        <Td>{message}</Td>
        <Td>{date}</Td>
    </Tr>
  )
}

export default LogstreamItem;
