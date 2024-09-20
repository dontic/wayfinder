import { Flex, Text } from "@chakra-ui/react";

const Trips = () => {
  return (
    <Flex
      flexDir={"column"}
      h={"full"}
      w={"full"}
      bg={"gray.100"}
      alignItems={"center"}
      justify={"center"}
    >
      <Text fontSize={"2xl"}>Trips</Text>
    </Flex>
  );
};

export default Trips;
