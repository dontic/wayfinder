// Login Page
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import LoginForm, { LoginFormValues } from "~/forms/LoginForm";

import { Box, useToast, VStack } from "@chakra-ui/react";
import CenteredLayout from "~/layouts/CenteredLayout";

import {
  authLoginCreate,
  authUserRetrieve
} from "~/api/endpoints/auth/auth.ts";
import { AxiosError } from "axios";
import { WayfinderLogo } from "~/components/Icons";

const Login = () => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();

  // useEffect to check if user is already authenticated
  useEffect(() => {
    const controller = new AbortController();

    // Function to check if user is authenticated
    const checkAuth = async () => {
      setIsLoading(true);
      try {
        // Fetch user data
        await authUserRetrieve();

        // The user is already logged in, redirect to home page
        navigate("/");
      } catch (error) {
        // Don't do anything if the user is not authenticated
        // The user will see the login page
      }

      setIsLoading(false);
    };

    checkAuth();

    return () => {
      // Cleanup
      controller.abort();
    };
  }, []);

  /* -------------------------------- FUNCTIONS ------------------------------- */
  const handleLogin = async (data: LoginFormValues) => {
    setIsSubmitting(true);

    try {
      // Fetch the login endpoint
      await authLoginCreate(data);

      // If successful, redirect to home page
      navigate("/");
    } catch (error) {
      if (error instanceof AxiosError) {
        let errorDescription = error.response?.statusText;

        toast({
          title: "Login failed",
          description: errorDescription,
          status: "error",
          duration: 5000,
          isClosable: true
        });
      } else {
        console.log("Other Error");
      }
    }
    setIsSubmitting(false);
  };

  /* --------------------------------- RENDER --------------------------------- */
  if (isLoading) {
    return <Box>Loading...</Box>;
  }

  return (
    <CenteredLayout>
      <VStack spacing={6}>
        {/* <Image maxH={"50px"} src={logoUrl} alt="Logo" /> */}
        <WayfinderLogo h={"100px"} w={"300px"} />

        <Box
          minW={{ base: "", md: "sm" }}
          rounded={"lg"}
          boxShadow={"lg"}
          px={12}
          py={12}
          bg={"white"}
        >
          <LoginForm
            handleFormSubmit={handleLogin}
            isSubmitting={isSubmitting}
          />
        </Box>
      </VStack>
    </CenteredLayout>
  );
};

export default Login;
