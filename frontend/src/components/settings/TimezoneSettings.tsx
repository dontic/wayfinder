import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from "@/components/ui/form";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList
} from "@/components/ui/command";
import { ChevronsUpDown, Check } from "lucide-react";
import { cn } from "@/lib/utils";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import {
  wayfinderSettingsRetrieve,
  wayfinderSettingsPartialUpdate
} from "@/api/django/wayfinder/wayfinder";

const TIMEZONES = Intl.supportedValuesOf("timeZone");

const TimezoneSchema = z.object({
  home_timezone: z.string().min(1, "Please select a timezone")
});

type TimezoneValues = z.infer<typeof TimezoneSchema>;

const TimezoneSettings = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [open, setOpen] = useState(false);

  const form = useForm<TimezoneValues>({
    resolver: zodResolver(TimezoneSchema),
    defaultValues: {
      home_timezone: ""
    }
  });

  useEffect(() => {
    wayfinderSettingsRetrieve()
      .then((settings) => {
        form.reset({
          home_timezone: settings.home_timezone ?? ""
        });
      })
      .catch(() => {
        // If no settings yet, leave the form empty
      });
  }, [form]);

  const onSubmit = async (values: TimezoneValues) => {
    setIsSubmitting(true);
    try {
      await wayfinderSettingsPartialUpdate({ home_timezone: values.home_timezone });
      toast.success("Timezone updated successfully");
    } catch {
      toast.error("Failed to update timezone. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Timezone</CardTitle>
        <CardDescription>
          Set your home timezone for activity history grouping.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="home_timezone"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Home Timezone</FormLabel>
                  <Popover open={open} onOpenChange={setOpen}>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant="outline"
                          role="combobox"
                          className="w-full justify-between font-normal"
                        >
                          {field.value || "Select a timezone"}
                          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                        </Button>
                      </FormControl>
                    </PopoverTrigger>
                    <PopoverContent className="w-[--radix-popover-trigger-width] p-0">
                      <Command>
                        <CommandInput placeholder="Search timezone..." />
                        <CommandList>
                          <CommandEmpty>No timezone found.</CommandEmpty>
                          <CommandGroup>
                            {TIMEZONES.map((tz) => (
                              <CommandItem
                                key={tz}
                                value={tz}
                                onSelect={(val) => {
                                  field.onChange(val);
                                  setOpen(false);
                                }}
                              >
                                <Check
                                  className={cn(
                                    "mr-2 h-4 w-4",
                                    field.value === tz ? "opacity-100" : "opacity-0"
                                  )}
                                />
                                {tz}
                              </CommandItem>
                            ))}
                          </CommandGroup>
                        </CommandList>
                      </Command>
                    </PopoverContent>
                  </Popover>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              className="hover:cursor-pointer"
              loading={isSubmitting}
            >
              Save Timezone
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export default TimezoneSettings;
