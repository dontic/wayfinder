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
export const LoginFormSchema = z.object({
  username: z.string().min(1, "Please enter a valid username."),
  password: z.string().min(1, "Please enter a password.")
});

export type LoginFormValues = z.infer<typeof LoginFormSchema>;

/* -------------------------------- Interface ------------------------------- */
interface Props {
  handleFormSubmit: (values: LoginFormValues) => void;
  isSubmitting: boolean;
}

const LoginForm = ({ handleFormSubmit, isSubmitting }: Props) => {
  /* ----------------------------- React hook form ---------------------------- */
  const {
    register,
    handleSubmit,
    formState: { errors, isValid }
  } = useForm<LoginFormValues>({
    resolver: zodResolver(LoginFormSchema)
  });

  /* --------------------------------- Render --------------------------------- */
  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <VStack spacing={4} w={"100%"}>
        <FormControl isInvalid={errors.username ? true : false}>
          <FormLabel htmlFor="username">Username</FormLabel>
          <Input id="username" {...register("username")} />
          <FormErrorMessage>
            {errors.username && errors.username.message}
          </FormErrorMessage>
        </FormControl>
        <FormControl isInvalid={errors.password ? true : false}>
          <FormLabel htmlFor="password">Password</FormLabel>
          <Input type="password" id="password" {...register("password")} />

          <FormErrorMessage>
            {errors.password && errors.password.message}
          </FormErrorMessage>
        </FormControl>

        <Button
          type="submit"
          colorScheme="blue"
          px={10}
          isLoading={isSubmitting}
          isDisabled={!isValid}
        >
          Login
        </Button>
      </VStack>
    </form>
  );
};

export default LoginForm;
