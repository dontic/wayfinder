import { Box, Text, VStack } from "@chakra-ui/react";
import OverlandToken from "~/components/OverlandToken";
import PasswordChange from "~/components/PasswordChange";
import UsernameChange from "~/components/UsernameChange";

const Settings = () => {
  /* --------------------------------- RENDER --------------------------------- */
  return (
    <Box w="100%" h={"100vh"} overflowY={"scroll"}>
      <VStack spacing={10} py={{ base: 20, md: 10 }}>
        {/* Overland Token */}
        <Box bg={"white"} rounded={"md"} boxShadow={"md"} p={4}>
          <Text mb={3} fontSize="xl" fontWeight="bold" textAlign={"center"}>
            Overland Token
          </Text>
          <OverlandToken />
        </Box>

        {/* Change Password */}
        <Box bg={"white"} rounded={"md"} boxShadow={"md"} p={4}>
          <Text mb={3} fontSize="xl" fontWeight="bold" textAlign={"center"}>
            Change Password
          </Text>
          <PasswordChange />
        </Box>

        {/* Change Username */}
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
