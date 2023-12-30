// Desc: Protected layour, if the user is not logged in, redirect to login page

import { Outlet } from "react-router-dom";
import { Navigate } from "react-router-dom";
import useAuthStore from "../stores/authStore";
import { Box, Text } from "@chakra-ui/react";
import NavBar from "../components/NavBar";

const ProtectedLayout = () => {
  const basicUserInfo = useAuthStore((state) => state.basicUserInfo);
  const getUser = useAuthStore((state) => state.getUser);
  const status = useAuthStore((state) => state.getUserStatus);

  if (!basicUserInfo) {
    // Try to get the user from /auth/getuser/
    try {
      getUser();
    } catch (error) {
      console.log(error);
      return <Navigate replace to={"/login"} />;
    }
  }

  if (status === "loading") {
    return (
      <Box>
        <Text>Loading...</Text>
      </Box>
    );
  }

  return (
    <>
      <NavBar />
      <Outlet />
    </>
  );
};

export default ProtectedLayout;
