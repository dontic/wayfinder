import { Box, Text } from "@chakra-ui/react";
import LogoutButton from "../components/LogoutButton";
import useAuthStore from "../stores/authStore";

const Home = () => {
  const basicUserInfo = useAuthStore((state) => state.basicUserInfo);

  return (
    <Box>
      <Text>Home</Text>
      <Text>Hello {basicUserInfo?.username}</Text>
      <LogoutButton />
    </Box>
  );
};

export default Home;
