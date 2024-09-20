import { Button, Flex, VStack, Text } from "@chakra-ui/react";
import { useState } from "react";
import { wayfinderTokenRetrieve } from "~/api/endpoints/wayfinder/wayfinder";

const OverlandToken = () => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [token, setToken] = useState<string>("");
  const [copyTokenButtonText, setCopyTokenButtonText] = useState("Copy Token");

  const getToken = async () => {
    setIsSubmitting(true);

    // Fetch the data
    try {
      const responseData = await wayfinderTokenRetrieve();
      setToken(responseData?.token ? responseData.token : "");
    } catch (error) {
      console.error(error);
    }

    setIsSubmitting(false);
  };

  const regenerateToken = async () => {
    setIsSubmitting(true);

    // Fetch the data
    try {
      const responseData = await wayfinderTokenRetrieve({ recreate: true });
      setToken(responseData?.token ? responseData.token : "");
    } catch (error) {
      console.error(error);
    }

    setIsSubmitting(false);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(token);
    setCopyTokenButtonText("Copied!");

    setTimeout(() => {
      setCopyTokenButtonText("Copy Token");
    }, 2000);
  };

  return (
    <VStack spacing={4} w={"100%"}>
      <Flex gap={4} w={"100%"} justifyContent={"center"}>
        <Button colorScheme="blue" isLoading={isSubmitting} onClick={getToken}>
          Get Token
        </Button>
        <Button
          colorScheme="orange"
          isLoading={isSubmitting}
          onClick={regenerateToken}
        >
          Regenerate Token
        </Button>
      </Flex>

      {/* Display the token if not an empty string */}
      {token && (
        <VStack w={"100%"} justifyContent={"center"}>
          <Text
            fontSize={"xl"}
            border={"1px"}
            borderColor={"gray.200"}
            p={4}
            rounded={"md"}
          >
            {token}
          </Text>
          <Button colorScheme="gray" size="sm" onClick={handleCopy}>
            {copyTokenButtonText}
          </Button>
        </VStack>
      )}
    </VStack>
  );
};

export default OverlandToken;
