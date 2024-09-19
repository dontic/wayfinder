import { Box } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useLocation, Navigate, Outlet } from "react-router-dom";
import Sidebar from "~/components/Sidebar";

import { useUserStore } from "~/stores/UserStore";
import { authUserRetrieve } from "~/api/endpoints/auth/auth";

const ProtectedLayout = () => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const location = useLocation();
  const { setUser } = useUserStore();

  // Local useStates
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Load the user data on mount
  useEffect(() => {
    const controller = new AbortController();

    const fetchUserData = async () => {
      setIsLoading(true);

      try {
        const userDetails = await authUserRetrieve();
        setUser(userDetails);
        setIsAuthenticated(true);
        setIsLoading(false);
      } catch {
        setIsAuthenticated(false);
        setIsLoading(false);
      }
    };

    fetchUserData();

    return () => {
      // Cleanup
      controller.abort();
    };
  }, []);

  /* --------------------------------- RENDER --------------------------------- */
  if (isLoading) {
    return <Box>Loading...</Box>;
  }

  return isAuthenticated ? (
    <>
      {/* If a user is authenticated return an outlet, which are the nested routes */}
      <Box id="mainbox" as="main" w={"100%"} bg={"transparent"}>
        <Sidebar>
          <Outlet />
        </Sidebar>
      </Box>
    </>
  ) : (
    // If a user is not authenticated, navigate them to the login page
    // Provide the state prop to navigate the user to what they were doing
    <>
      {console.log("User is not authenticated, redirecting to login")}
      <Navigate to="/login" state={{ from: location }} replace />
    </>
  );
};

export default ProtectedLayout;
