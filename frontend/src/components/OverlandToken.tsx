import { Button, VStack, Text, HStack } from "@chakra-ui/react";
import { useEffect, useState } from "react";
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

  useEffect(() => {
    const controller = new AbortController();

    getToken();

    return () => {
      controller.abort();
    };
  }, []);

  return (
    <VStack spacing={4} w={"100%"}>
      {/* Display the token if not an empty string */}
      {token && (
        <VStack w={"100%"} justifyContent={"center"}>
          <Text
            fontSize={{ base: "sm", md: "md" }}
            border={"1px"}
            borderColor={"gray.200"}
            p={4}
            rounded={"md"}
          >
            {token}
          </Text>
          <HStack>
            <Button colorScheme="gray" size="sm" onClick={handleCopy}>
              {copyTokenButtonText}
            </Button>
            <Button
              colorScheme="orange"
              size="sm"
              isLoading={isSubmitting}
              onClick={regenerateToken}
            >
              Regenerate Token
            </Button>
          </HStack>
        </VStack>
      )}
    </VStack>
  );
};

export default OverlandToken;
