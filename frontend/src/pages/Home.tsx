import { Flex, Text } from "@chakra-ui/react";

const Home = () => {
  return (
    <Flex
      flexDir={"column"}
      h={"full"}
      w={"full"}
      bg={"gray.100"}
      alignItems={"center"}
      justify={"center"}
    >
      <Text fontSize={"2xl"}>Home</Text>
    </Flex>
  );
};

export default Home;
