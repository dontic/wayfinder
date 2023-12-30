import { Box, Center, Image, useToast, VStack } from "@chakra-ui/react";
import "./styles.css";

import LoginForm, { LoginFormValues } from "../forms/LoginForm";
import useAuthStore from "../stores/authStore";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const login = useAuthStore((state) => state.login);
  const status = useAuthStore((state) => state.loginStatus);

  const handleLogin = async (values: LoginFormValues) => {
    const { username, password } = values;

    if (username && password) {
      try {
        console.log("Logging in...");
        await login(username, password);

        // Navigate to the home page.
        navigate("/");
        console.log("Logged in!");
      } catch (e: any) {
        console.log("Error logging in!");

        const statusCode = e.response?.status;

        if (statusCode === 400) {
          toast({
            title: "Login failed",
            description: "Invalid username or password",
            status: "error",
            duration: 5000,
            isClosable: true
          });
        } else {
          toast({
            title: "Login failed",
            description: "Something went wrong",
            status: "error",
            duration: 5000,
            isClosable: true
          });
        }
      }
    } else {
      // Show an error message.
    }
  };
  return (
    <Box h={"100vh"} w={"100%"} className="animated-gradient">
      <Center h={"100%"}>
        <VStack spacing={6}>
          <Image
            src="src/assets/full_logo_without_bg.svg"
            alt="Wayfinder Logo"
          />
          <Box
            minW={{ base: "", md: "sm" }}
            rounded={"lg"}
            boxShadow={"lg"}
            px={8}
            py={12}
            bg={"white"}
          >
            <VStack spacing={4}>
              <LoginForm
                handleFormSubmit={handleLogin}
                isSubmitting={status === "loading"}
              />
            </VStack>
          </Box>
        </VStack>
      </Center>
    </Box>
  );
};

export default Login;
