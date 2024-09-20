import { Box, Divider, Text, VStack } from "@chakra-ui/react";
import OverlandToken from "~/components/OverlandToken";
import PasswordChange from "~/components/PasswordChange";
import UsernameChange from "~/components/UsernameChange";

import CenteredLayout from "~/layouts/CenteredLayout";

const Settings = () => {
  /* --------------------------------- RENDER --------------------------------- */
  return (
    <CenteredLayout>
      <Box
        w={{ base: "100%", md: "50%" }}
        bg={"white"}
        rounded={"lg"}
        boxShadow={"lg"}
        p={10}
      >
        <VStack spacing={4} w={"100%"}>
          <Box>
            <Text mb={3} fontSize="xl" fontWeight="bold" textAlign={"center"}>
              Overland Token
            </Text>
            <OverlandToken />
          </Box>

          <Divider />
          <Box>
            <Text mb={3} fontSize="xl" fontWeight="bold" textAlign={"center"}>
              Change Password
            </Text>
            <PasswordChange />
          </Box>

          <Divider />

          <Box>
            <Text mb={3} fontSize="xl" fontWeight="bold" textAlign={"center"}>
              Change Username
            </Text>
            <UsernameChange />
          </Box>
        </VStack>
      </Box>
    </CenteredLayout>
  );
};

export default Settings;
