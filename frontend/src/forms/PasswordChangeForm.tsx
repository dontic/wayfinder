import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  VStack
} from "@chakra-ui/react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

/* ----------------------------------- Zod ---------------------------------- */
export const PasswordChangeFormSchema = z
  .object({
    newPassword: z
      .string()
      .min(8, "New password must be at least 8 characters long."),
    confirmPassword: z.string().min(1, "Please confirm your new password.")
  })
  .refine((data) => data.newPassword === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"]
  });

export type PasswordChangeFormValues = z.infer<typeof PasswordChangeFormSchema>;

/* -------------------------------- Interface ------------------------------- */
interface Props {
  handleFormSubmit: (values: PasswordChangeFormValues) => void;
  isSubmitting: boolean;
}

const PasswordChangeForm = ({ handleFormSubmit, isSubmitting }: Props) => {
  /* ----------------------------- React hook form ---------------------------- */
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    reset
  } = useForm<PasswordChangeFormValues>({
    resolver: zodResolver(PasswordChangeFormSchema)
  });

  const onSubmit = (values: PasswordChangeFormValues) => {
    handleFormSubmit(values);

    // Reset the form on submit
    reset();
  };

  /* --------------------------------- Render --------------------------------- */
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <VStack spacing={4} w={"100%"}>
        <FormControl isInvalid={errors.newPassword ? true : false}>
          <FormLabel htmlFor="newPassword">New Password</FormLabel>
          <Input
            type="password"
            id="newPassword"
            {...register("newPassword")}
          />
          <FormErrorMessage>
            {errors.newPassword && errors.newPassword.message}
          </FormErrorMessage>
        </FormControl>
        <FormControl isInvalid={errors.confirmPassword ? true : false}>
          <FormLabel htmlFor="confirmPassword">Confirm New Password</FormLabel>
          <Input
            type="password"
            id="confirmPassword"
            {...register("confirmPassword")}
          />
          <FormErrorMessage>
            {errors.confirmPassword && errors.confirmPassword.message}
          </FormErrorMessage>
        </FormControl>

        <Button
          type="submit"
          colorScheme="blue"
          px={10}
          isLoading={isSubmitting}
          isDisabled={!isValid}
        >
          Change Password
        </Button>
      </VStack>
    </form>
  );
};

export default PasswordChangeForm;
