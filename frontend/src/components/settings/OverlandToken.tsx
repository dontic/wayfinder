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
import { toast } from "sonner";
import { wayfinderTokenRetrieve } from "@/api/django/wayfinder/wayfinder";

const OverlandToken = () => {
  const [token, setToken] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);
  const [isRegenerating, setIsRegenerating] = useState(false);

  const fetchToken = async (recreate = false) => {
    try {
      if (recreate) {
        setIsRegenerating(true);
      } else {
        setIsLoading(true);
      }

      const response = await wayfinderTokenRetrieve({ recreate });
      
      if (response?.token) {
        setToken(response.token);
        if (recreate) {
          toast.success("Token regenerated successfully");
        }
      }
    } catch (error) {
      console.error("Failed to fetch token:", error);
      toast.error("Failed to load token. Please try again.");
    } finally {
      setIsLoading(false);
      setIsRegenerating(false);
    }
  };

  useEffect(() => {
    fetchToken();
  }, []);

  const handleCopyToken = async () => {
    try {
      await navigator.clipboard.writeText(token);
      toast.success("Token copied to clipboard");
    } catch (error) {
      console.error("Failed to copy token:", error);
      toast.error("Failed to copy token");
    }
  };

  const handleRegenerateToken = () => {
    fetchToken(true);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Overland Token</CardTitle>
        <CardDescription>
          Use this token to authenticate your Overland app for location tracking.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Input
            value={isLoading ? "Loading..." : token}
            readOnly
            className="font-mono text-sm"
            placeholder="Your token will appear here"
          />
        </div>
        
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={handleCopyToken}
            disabled={isLoading || !token}
            className="hover:cursor-pointer"
          >
            Copy Token
          </Button>
          <Button
            variant="default"
            onClick={handleRegenerateToken}
            loading={isRegenerating}
            disabled={isLoading}
            className="hover:cursor-pointer bg-orange-600 hover:bg-orange-700"
          >
            Regenerate Token
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default OverlandToken;

