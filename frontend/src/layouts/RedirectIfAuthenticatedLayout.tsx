import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { authUserRetrieve } from "@/api/django/auth/auth";

interface Props {
  children: React.ReactNode;
}

const CenteredLayout = ({ children }: Props) => {
  /* ---------------------------------- HOOKS --------------------------------- */
  // Local useStates
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // Load the user data on mount
  useEffect(() => {
    const controller = new AbortController();

    const fetchUserData = async () => {
      setIsLoading(true);

      try {
        await authUserRetrieve({
          headers: {
            "Content-Type": "application/json"
          }
        });
        setIsLoading(false);

        console.debug("User logged in");

        // Redirect to the home page
        navigate("/");
      } catch {
        console.debug("User not logged in");
        setIsLoading(false);
      }
    };

    fetchUserData();

    return () => {
      // Cleanup
      controller.abort();
    };
  }, []);

  /* --------------------------------- RENDER --------------------------------- */
  if (isLoading) {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        Loading...
      </div>
    );
  }

  return <div className="h-screen w-full">{children}</div>;
};

export default CenteredLayout;
