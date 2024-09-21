import { Box, Text, VStack } from "@chakra-ui/react";
import OverlandToken from "~/components/OverlandToken";
import PasswordChange from "~/components/PasswordChange";
import UsernameChange from "~/components/UsernameChange";

const Settings = () => {
  /* --------------------------------- RENDER --------------------------------- */
  return (
    <Box w="100%" h={"100vh"} overflowY={"scroll"}>
      <VStack spacing={10} py={{ base: 4, md: 10 }}>
        <Box bg={"white"} rounded={"md"} boxShadow={"md"} p={4}>
          <Text mb={3} fontSize="xl" fontWeight="bold" textAlign={"center"}>
            Overland Token
          </Text>
          <OverlandToken />
        </Box>

        <Box bg={"white"} rounded={"md"} boxShadow={"md"} p={4}>
          <Text mb={3} fontSize="xl" fontWeight="bold" textAlign={"center"}>
            Change Password
          </Text>
          <PasswordChange />
        </Box>

        <Box bg={"white"} rounded={"md"} boxShadow={"md"} p={4}>
          <Text mb={3} fontSize="xl" fontWeight="bold" textAlign={"center"}>
            Change Username
          </Text>
          <UsernameChange />
        </Box>
      </VStack>
    </Box>
  );
};

export default Settings;
