import { Button, useToast } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import useAuthStore from "../stores/authStore";

const LogoutButton = () => {
  const toast = useToast();
  const navigate = useNavigate();
  const logout = useAuthStore((state) => state.logout);
  const status = useAuthStore((state) => state.logoutStatus);

  const handleLogout = async () => {
    console.log("Logging out...");
    try {
      await logout();
      navigate("/login");
      console.log("Logged out!");
    } catch (e) {
      console.log("Error logging out!");
      toast({
        title: "Logout failed",
        description: "Something went wrong",
        status: "error",
        duration: 5000,
        isClosable: true
      });
    }
  };

  return (
    <Button onClick={handleLogout} isLoading={status === "loading"}>
      Logout
    </Button>
  );
};

export default LogoutButton;
