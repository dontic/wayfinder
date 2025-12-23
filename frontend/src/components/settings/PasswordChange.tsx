import { useState } from "react";
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
import { authPasswordChangeCreate } from "@/api/django/auth/auth";

/* ----------------------------------- Zod ---------------------------------- */
const PasswordChangeSchema = z.object({
  new_password1: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(128, "Password must be 128 characters or less"),
  new_password2: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(128, "Password must be 128 characters or less")
}).refine((data) => data.new_password1 === data.new_password2, {
  message: "Passwords do not match",
  path: ["new_password2"]
});

type PasswordChangeValues = z.infer<typeof PasswordChangeSchema>;

const PasswordChange = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<PasswordChangeValues>({
    resolver: zodResolver(PasswordChangeSchema),
    defaultValues: {
      new_password1: "",
      new_password2: ""
    }
  });

  const onSubmit = async (values: PasswordChangeValues) => {
    setIsSubmitting(true);
    try {
      await authPasswordChangeCreate({
        new_password1: values.new_password1,
        new_password2: values.new_password2
      });

      toast.success("Password changed successfully");
      
      // Reset the form after successful password change
      form.reset();
    } catch (error: any) {
      console.error("Failed to change password:", error);
      
      // Handle specific error messages from the API
      const errorMessage = error?.response?.data?.detail 
        || error?.response?.data?.new_password2?.[0]
        || "Failed to change password. Please try again.";
      
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="max-w-lg">
      <CardHeader>
        <CardTitle>Change Password</CardTitle>
        <CardDescription>Update your account password.</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="new_password1"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>New Password</FormLabel>
                  <FormControl>
                    <Input 
                      type="password" 
                      placeholder="Enter new password" 
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="new_password2"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirm New Password</FormLabel>
                  <FormControl>
                    <Input 
                      type="password" 
                      placeholder="Confirm new password" 
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
              Change Password
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export default PasswordChange;

