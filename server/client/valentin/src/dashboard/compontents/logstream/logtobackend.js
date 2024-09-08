const sendLogToBackend = async (logData) => {
    try {
      const response = await fetch('https://blickbox.maytastix.de/api/iot/api/valentin-log/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(logData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      console.log('Log sent to backend successfully');
    } catch (error) {
      console.error('Error sending log to backend:', error);
    }
  };

  export const sendLogToBackendOnly = (message) => {
    const logData = {
      title: message.type,
      message: message.message,
      type: message.code === 'red' ? 'error' : message.code === 'yellow' ? 'info' : message.code === 'green' ? 'success' : 'log',
      timestamp: message.date,
    };

    sendLogToBackend(logData);
  };