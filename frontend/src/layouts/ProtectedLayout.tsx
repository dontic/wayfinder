/* 
This layout is used to protect routes that require authentication.
It checks if the user is authenticated and then renders the children components.
If the user is not authenticated, it redirects them to the login page.
*/

// React
import { useEffect, useState } from "react";
import { useLocation, Navigate, Outlet } from "react-router-dom";

// Zustand
import { useUserStore } from "@/stores/UserStore";

// API
import { authUserRetrieve } from "@/api/django/auth/auth";

const ProtectedLayout = () => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const location = useLocation();
  const { setUser, user } = useUserStore();

  // Local useStates
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Load user and tenant data together
  useEffect(() => {
    const controller = new AbortController();

    const fetchData = async () => {
      // Skip if data is already loaded in the store
      if (user) {
        setIsAuthenticated(true);
        setIsLoading(false);
        return;
      }

      setIsLoading(true);

      try {
        // Fetch both in parallel
        const [userDetails] = await Promise.all([
          user
            ? Promise.resolve(user)
            : authUserRetrieve({
                headers: { "Content-Type": "application/json" },
                signal: controller.signal
              })
        ]);

        console.debug("User logged in:", userDetails);

        // Update stores only if data was fetched
        if (!user) {
          setUser(userDetails);
        }

        setIsAuthenticated(true);
      } catch (error: any) {
        // Only handle errors that aren't from abort
        if (error.name !== "AbortError" && error.name !== "CanceledError") {
          console.debug("User not logged in or error fetching data:", error);
          setIsAuthenticated(false);
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      // Cleanup
      controller.abort();
    };
  }, [user, setUser]);

  /* --------------------------------- RENDER --------------------------------- */
  if (isLoading) {
    return (
      <div className="flex h-full w-full items-center justify-center">
        Loading...
      </div>
    );
  }

  return isAuthenticated ? (
    <Outlet />
  ) : (
    // If a user is not authenticated, navigate them to the login page
    // Provide the state prop to navigate the user to what they were doing
    <Navigate to="/login" state={{ from: location }} replace />
  );
};

export default ProtectedLayout;
