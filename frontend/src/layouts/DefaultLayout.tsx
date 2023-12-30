// Desc: Default layout for the app, if the user is logged in, redirect to home page

import { Outlet } from "react-router-dom";
import { Navigate } from "react-router-dom";
import useAuthStore from "../stores/authStore";
import { Box } from "@chakra-ui/react";

const DefaultLayout = () => {
  const basicUserInfo = useAuthStore((state) => state.basicUserInfo);
  const status = useAuthStore((state) => state.getUserStatus);

  if (basicUserInfo) {
    return <Navigate replace to={"/"} />;
  }

  if (status === "loading") {
    return <Box>Loading...</Box>;
  }

  return (
    <>
      <Outlet />
    </>
  );
};

export default DefaultLayout;
