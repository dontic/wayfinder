import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ChakraProvider } from "@chakra-ui/react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
    errorElement: <NotFound />
  }
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ChakraProvider>
      <RouterProvider router={router} />
    </ChakraProvider>
  </StrictMode>
);
