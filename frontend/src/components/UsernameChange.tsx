import { useToast } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { authUserRetrieve, authUserUpdate } from "~/api/endpoints/auth/auth";
import UsernameChangeForm, {
  UsernameChangeFormValues
} from "~/forms/UsernameChangeForm";

const UsernameChange = () => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const [isUsernameChangeSubmitting, setIsUsernameChangeSubmitting] =
    useState<boolean>(false);
  const toast = useToast();
  const [currentUsername, setCurrentUsername] = useState<string>("");

  // UseEffect to fetch the user data
  useEffect(() => {
    // Fetch the user data
    const fetchUserData = async () => {
      try {
        const userResponse = await authUserRetrieve();
        setCurrentUsername(userResponse.username);
      } catch (error) {
        console.error(error);
      }
    };

    fetchUserData();
  }, []);

  /* -------------------------------- FUNCTIONS ------------------------------- */
  const handleUsernameChange = async (formData: UsernameChangeFormValues) => {
    setIsUsernameChangeSubmitting(true);

    try {
      const usernameChangeResponse = await authUserUpdate({
        username: formData.newUsername
      });

      setCurrentUsername(usernameChangeResponse.username);

      toast({
        title: "Username changed successfully",
        description:
          'Your username has been updated to "' +
          usernameChangeResponse.username +
          '"',
        status: "success",
        duration: 5000,
        isClosable: true
      });
    } catch (error) {
      console.error(error);

      toast({
        title: "Username change failed",
        description: "Something went wrong",
        status: "error",
        duration: 5000,
        isClosable: true
      });
    }

    setIsUsernameChangeSubmitting(false);
  };

  /* --------------------------------- RENDER --------------------------------- */
  return (
    <UsernameChangeForm
      handleFormSubmit={handleUsernameChange}
      isSubmitting={isUsernameChangeSubmitting}
      currentUsername={currentUsername}
    />
  );
};

export default UsernameChange;
