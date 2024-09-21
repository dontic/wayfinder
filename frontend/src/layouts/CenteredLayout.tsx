import { Box, Center, HStack, Image } from "@chakra-ui/react";

interface Props {
  children: React.ReactNode;
  splitImage?: string;
}

const CenteredLayout = ({ children, splitImage }: Props) => {
  return (
    <>
      <HStack spacing={0} h={"100vh"} w={"100%"}>
        <Box h={"full"} w={splitImage ? { base: "100%", md: "50%" } : "100%"}>
          <Center h={"100%"}>{children}</Center>
        </Box>
        <Box h={"100%"} w={splitImage ? { base: "0", md: "50%" } : "0"}>
          <Image
            h={"100%"}
            src={splitImage}
            alt="Calendar"
            objectFit={"cover"}
          />
        </Box>
      </HStack>
    </>
  );
};

export default CenteredLayout;
