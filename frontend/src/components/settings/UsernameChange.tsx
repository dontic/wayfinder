import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { useUserStore } from "@/stores/UserStore";
import { authUserPartialUpdate } from "@/api/django/auth/auth";

/* ----------------------------------- Zod ---------------------------------- */
const UsernameChangeSchema = z.object({
  username: z
    .string()
    .min(1, "Username is required")
    .max(150, "Username must be 150 characters or less")
    .regex(
      /^[\w.@+-]+$/,
      "Username can only contain letters, numbers, and @/./+/-/_ characters"
    )
});

type UsernameChangeValues = z.infer<typeof UsernameChangeSchema>;

const UsernameChange = () => {
  const { user, setUser } = useUserStore();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<UsernameChangeValues>({
    resolver: zodResolver(UsernameChangeSchema),
    defaultValues: {
      username: ""
    }
  });

  // Update form when user data loads
  useEffect(() => {
    if (user) {
      form.reset({
        username: user.username ?? ""
      });
    }
  }, [user, form]);

  const onSubmit = async (values: UsernameChangeValues) => {
    setIsSubmitting(true);
    try {
      const updatedUser = await authUserPartialUpdate({
        username: values.username
      });

      // Update the user store with the new data
      setUser({
        ...user!,
        username: updatedUser.username
      });

      toast.success("Username updated successfully");
    } catch (error: any) {
      console.error("Failed to update username:", error);
      
      // Handle specific error messages from the API
      const errorMessage = error?.response?.data?.username?.[0]
        || error?.response?.data?.detail
        || "Failed to update username. Please try again.";
      
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="max-w-lg">
      <CardHeader>
        <CardTitle>Change Username</CardTitle>
        <CardDescription>Update your account username.</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Username</FormLabel>
                  <FormControl>
                    <Input 
                      placeholder="Enter your username" 
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              className="hover:cursor-pointer"
              loading={isSubmitting}
            >
              Update Username
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export default UsernameChange;

