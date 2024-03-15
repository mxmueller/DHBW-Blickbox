import {  Code, Tr, Td } from "@chakra-ui/react"
import Cookies from 'js-cookie';
import sendNotification from '../settings/settings.alerts.service.js';


function LogstreamItem({ type, code, message, date }) {

    console.log(code);

    if (code != null && code == 'red') {
        sendNotification('Blickbox: Error 🫤', message);
    }

  return (
    <Tr>
        <Td>
            <Code colorScheme={code}>{type}</Code>
        </Td>
        <Td>{message}</Td>
        <Td>{date}</Td>
    </Tr>
  )
}

export default LogstreamItem;
