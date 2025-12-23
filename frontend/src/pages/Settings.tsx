import { useState, useEffect } from "react";
import SideBarLayout from "@/layouts/SideBarLayout";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
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
const UserProfileSchema = z.object({
  first_name: z.string().max(30, "First name must be 30 characters or less"),
  last_name: z.string().max(30, "Last name must be 30 characters or less")
});

type UserProfileValues = z.infer<typeof UserProfileSchema>;

const Settings = () => {
  const { user, setUser } = useUserStore();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<UserProfileValues>({
    resolver: zodResolver(UserProfileSchema),
    defaultValues: {
      first_name: "",
      last_name: ""
    }
  });

  // Update form when user data loads
  useEffect(() => {
    if (user) {
      form.reset({
        first_name: user.first_name ?? "",
        last_name: user.last_name ?? ""
      });
    }
  }, [user, form]);

  const onSubmit = async (values: UserProfileValues) => {
    setIsSubmitting(true);
    try {
      const updatedUser = await authUserPartialUpdate({
        first_name: values.first_name,
        last_name: values.last_name
      });

      // Update the user store with the new data
      setUser({
        ...user!,
        first_name: updatedUser.first_name,
        last_name: updatedUser.last_name
      });

      toast.success("Profile updated successfully");
    } catch (error) {
      console.error("Failed to update profile:", error);
      toast.error("Failed to update profile. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <SideBarLayout title="Settings">
      <div className="flex w-full justify-center overflow-y-auto">
        <div id="settings-container" className="flex flex-col gap-6 py-6">
          <Tabs defaultValue="user" className="w-full">
            <TabsList
              className={`grid w-full max-w-md ${
                user?.first_name !== "user" ? "grid-cols-2" : "grid-cols-1"
              }`}
            >
              <TabsTrigger value="user">User</TabsTrigger>
              {user?.first_name !== "user" && (
                <TabsTrigger value="team">Overland</TabsTrigger>
              )}
            </TabsList>
            <TabsContent value="user" className="mt-6 space-y-6">
              {/* Profile Information Card */}
              <Card className="max-w-lg">
                <CardHeader>
                  <CardTitle>Profile Information</CardTitle>
                  <CardDescription>
                    Update your personal information.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Form {...form}>
                    <form
                      onSubmit={form.handleSubmit(onSubmit)}
                      className="space-y-4"
                    >
                      <FormField
                        control={form.control}
                        name="first_name"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>First Name</FormLabel>
                            <FormControl>
                              <Input placeholder="John" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name="last_name"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Last Name</FormLabel>
                            <FormControl>
                              <Input placeholder="Doe" {...field} />
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
                        Save Changes
                      </Button>
                    </form>
                  </Form>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="team" className="mt-6"></TabsContent>
          </Tabs>
        </div>
      </div>
    </SideBarLayout>
  );
};

export default Settings;
