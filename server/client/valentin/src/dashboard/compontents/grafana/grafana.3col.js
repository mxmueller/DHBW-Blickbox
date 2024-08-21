import { ChakraProvider, Text, Box, VStack, SimpleGrid } from "@chakra-ui/react"
import { useState, useEffect } from "react"
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts'

function GrafanaValidation({ children }) {
  const [isMockEnabled, setIsMockEnabled] = useState(false)
  const [dashboardUrls, setDashboardUrls] = useState([])

  useEffect(() => {
    setIsMockEnabled(process.env.REACT_APP_MOCK_GRAFANA === "true")

    const urls = [
      process.env.REACT_APP_GRAFANA_URL_3COL_1,
      process.env.REACT_APP_GRAFANA_URL_3COL_2,
      process.env.REACT_APP_GRAFANA_URL_3COL_3,
    ].map(url => url || "https://dhbwgrafana.maytastix.de/public-dashboards/placeholder")

    setDashboardUrls(urls)
  }, [])

  const MockComponent = ({ index }) => {
    const data = [
      { name: 'Gruppe A', value: 400 - index * 50 },
      { name: 'Gruppe B', value: 300 + index * 25 },
      { name: 'Gruppe C', value: 300 },
      { name: 'Gruppe D', value: 200 + index * 30 },
    ]
    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

    return (
        <VStack
            width="100%"
            height="600px"
            justifyContent="center"
            spacing={4}
        >
          <Text fontSize="xl" fontWeight="bold">
            Mock XS {index + 1}
          </Text>
          <Text fontSize="sm">URL: {dashboardUrls[index]}</Text>
          <Box width="100%" height="400px">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                    label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {data.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Box>
        </VStack>
    )
  }

  return (
      <ChakraProvider>
        {children}
        <Box boxShadow='xl' bg='blackAlpha.100' p={5} mt={10} borderRadius={25}>
          <SimpleGrid columns={{sm: 1, md: 1, lg: 3}} minChildWidth='250px' spacing={4}>
            {dashboardUrls.map((url, index) => (
                <Box key={index} bg='#f4f5f5' borderRadius={25} padding={2}>
                  {isMockEnabled ? (
                      <MockComponent index={index} />
                  ) : (
                      <iframe
                          src={url}
                          width="100%"
                          height="600"
                          title={`Grafana Dashboard ${index + 1}`}
                      />
                  )}
                </Box>
            ))}
          </SimpleGrid>
        </Box>
      </ChakraProvider>
  )
}

export default GrafanaValidation;