import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  VStack,
  Text
} from "@chakra-ui/react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

/* ----------------------------------- Zod ---------------------------------- */
export const UsernameChangeFormSchema = z.object({
  newUsername: z
    .string()
    .min(3, "Username must be at least 3 characters long.")
    .max(20, "Username must not exceed 20 characters.")
    .regex(
      /^[a-zA-Z0-9_]+$/,
      "Username can only contain letters, numbers, and underscores."
    )
});

export type UsernameChangeFormValues = z.infer<typeof UsernameChangeFormSchema>;

/* -------------------------------- Interface ------------------------------- */
interface Props {
  currentUsername?: string;
  handleFormSubmit: (values: UsernameChangeFormValues) => void;
  isSubmitting: boolean;
}

const UsernameChangeForm = ({
  currentUsername,
  handleFormSubmit,
  isSubmitting
}: Props) => {
  /* ----------------------------- React hook form ---------------------------- */
  const {
    register,
    handleSubmit,
    formState: { errors, isValid }
  } = useForm<UsernameChangeFormValues>({
    resolver: zodResolver(UsernameChangeFormSchema)
  });

  /* --------------------------------- Render --------------------------------- */
  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <VStack spacing={4} w={"100%"} align="stretch">
        {currentUsername && (
          <FormControl>
            <FormLabel htmlFor="currentUsername">Current Username:</FormLabel>
            <Text fontWeight="bold" fontSize="lg" mb={2}>
              {currentUsername ? currentUsername : ""}
            </Text>
          </FormControl>
        )}

        <FormControl isInvalid={errors.newUsername ? true : false}>
          <FormLabel htmlFor="newUsername">New Username</FormLabel>
          <Input id="newUsername" {...register("newUsername")} />
          <FormErrorMessage>
            {errors.newUsername && errors.newUsername.message}
          </FormErrorMessage>
        </FormControl>

        <Button
          type="submit"
          colorScheme="blue"
          px={10}
          mt={4}
          isLoading={isSubmitting}
          isDisabled={!isValid}
        >
          Change Username
        </Button>
      </VStack>
    </form>
  );
};

export default UsernameChangeForm;
