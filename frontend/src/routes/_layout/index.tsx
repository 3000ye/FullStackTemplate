import { Box, Container, Heading } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { Text } from "@chakra-ui/react"

import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const { user: currentUser } = useAuth()

  return (
    <>
      <Container maxW="1280px" mx="0" ml="0">
        <Box pt={12} m={4}>
          <Heading fontSize="4xl" truncate maxW="sm">
            Hi, {currentUser?.name}
          </Heading>
          <Text>Welcome back, nice to see you again, your role is {currentUser?.role}!</Text>
        </Box>
      </Container>
    </>
  )
}
