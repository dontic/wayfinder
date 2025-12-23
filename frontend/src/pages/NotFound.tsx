import { Button } from "@/components/ui/button";
import CenteredLayout from "@/layouts/CenteredLayout";
import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <CenteredLayout>
      <div className="flex flex-col items-center justify-center gap-4">
        <h1 className="text-2xl font-bold">404 - Page Not Found</h1>
        <p className="text-sm text-muted-foreground">
          The page you are looking for does not exist.
        </p>
        <Button asChild>
          <Link to="/">Go to home</Link>
        </Button>
      </div>
    </CenteredLayout>
  );
};

export default NotFound;
