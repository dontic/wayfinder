import { Box, Center, Text, VStack } from "@chakra-ui/react";

const NotFound = () => {
  return (
    <Box h={"100vh"} w={"100%"} className="animated-gradient">
      <Center h={"100%"}>
        <VStack spacing={6}>
          <Text fontSize="6xl">404</Text>
          <Text fontSize="2xl">Page not found</Text>
        </VStack>
      </Center>
    </Box>
  );
};

export default NotFound;
