import { ChakraProvider, Text, Box, VStack } from "@chakra-ui/react"
import { useState, useEffect } from "react"
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts'

function GrafanaValidation({ children }) {
  const [isMockEnabled, setIsMockEnabled] = useState(false)
  const [dashboardUrl, setDashboardUrl] = useState("")

  useEffect(() => {
    setIsMockEnabled(process.env.REACT_APP_MOCK_GRAFANA === "true")

    if (process.env.REACT_APP_GRAFANA_DEV_URL) {
      setDashboardUrl(process.env.REACT_APP_GRAFANA_DEV_URL)
    } else if (process.env.REACT_APP_GRAFANA_URL) {
      setDashboardUrl(process.env.REACT_APP_GRAFANA_URL)
    } else {
      setDashboardUrl("https://dhbwgrafana.maytastix.de/public-dashboards/d0688f51a9534c4bbfedec86c8b175cb")
    }
  }, [])

  const MockComponent = () => {
    const data = [
      { name: 'Gruppe A', value: 400 },
      { name: 'Gruppe B', value: 300 },
      { name: 'Gruppe C', value: 300 },
      { name: 'Gruppe D', value: 200 },
    ]
    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

    return (
        <VStack
            width="100%"
            height="800px"
            justifyContent="center"
            spacing={4}
        >
          <Text fontSize="2xl" fontWeight="bold">
              Dashboard Mock - Full Width
          </Text>
          <Box width="100%" height="400px">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={150}
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
          <Box bg='#f4f5f5' borderRadius={25}>
            <Box padding={15}>
              {isMockEnabled ? (
                  <MockComponent />
              ) : (
                  <iframe
                      src={dashboardUrl}
                      width="100%"
                      height="800"
                      title="Grafana Dashboard"
                  ></iframe>
              )}
            </Box>
          </Box>
        </Box>
      </ChakraProvider>
  )
}

export default GrafanaValidation;