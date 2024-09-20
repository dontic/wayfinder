import { useToast } from "@chakra-ui/react";
import { useState } from "react";
import { authPasswordChangeCreate } from "~/api/endpoints/auth/auth";
import PasswordChangeForm, {
  PasswordChangeFormValues
} from "~/forms/PasswordChangeForm";

const PasswordChange = () => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const [isPasswordChangeSubmitting, setIsPasswordChangeSubmitting] =
    useState<boolean>(false);
  const toast = useToast();

  /* -------------------------------- FUNCTIONS ------------------------------- */
  const handlePasswordChange = async (formData: PasswordChangeFormValues) => {
    setIsPasswordChangeSubmitting(true);

    try {
      const passwordChangeResponse = await authPasswordChangeCreate({
        new_password1: formData.newPassword,
        new_password2: formData.confirmPassword
      });

      toast({
        title: passwordChangeResponse.detail,
        status: "success",
        duration: 5000,
        isClosable: true
      });
    } catch (error) {
      console.error(error);

      toast({
        title: "Password change failed",
        description: "Something went wrong",
        status: "error",
        duration: 5000,
        isClosable: true
      });
    }

    setIsPasswordChangeSubmitting(false);
  };

  /* --------------------------------- RENDER --------------------------------- */
  return (
    <PasswordChangeForm
      handleFormSubmit={handlePasswordChange}
      isSubmitting={isPasswordChangeSubmitting}
    />
  );
};

export default PasswordChange;
