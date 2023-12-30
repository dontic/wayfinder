import { Box, Text } from "@chakra-ui/react";
import useAuthStore from "../stores/authStore";

const Home = () => {
  const basicUserInfo = useAuthStore((state) => state.basicUserInfo);

  return (
    <Box>
      <Text>Hello {basicUserInfo?.username}</Text>
    </Box>
  );
};

export default Home;
