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

// Form imports
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2Icon } from "lucide-react";

/* ----------------------------------- Zod ---------------------------------- */
export const SignUpFormSchema = z.object({
  first_name: z.string().min(1, "First name is required"),
  last_name: z.string().optional()
});

export type SignUpFormValues = z.infer<typeof SignUpFormSchema>;

/* -------------------------------- Interface ------------------------------- */
interface Props {
  onSubmit: (values: SignUpFormValues) => void;
  isSubmitting?: boolean;
}

export function SignUpForm({ onSubmit, isSubmitting }: Props) {
  /* ----------------------------- React hook form ---------------------------- */
  const form = useForm<z.infer<typeof SignUpFormSchema>>({
    resolver: zodResolver(SignUpFormSchema),
    defaultValues: {
      first_name: "",
      last_name: ""
    }
  });

  /* --------------------------------- Render --------------------------------- */
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          required
          control={form.control}
          name="first_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>First name</FormLabel>
              <FormControl>
                <Input required placeholder="John" {...field} />
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
              <FormLabel>Last name</FormLabel>
              <FormControl>
                <Input placeholder="Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? <Loader2Icon className="animate-spin" /> : null}
          Continue
        </Button>
      </form>
    </Form>
  );
}
