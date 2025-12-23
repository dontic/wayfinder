import Logo from "@/assets/logo.svg?react";
import Icon from "@/assets/icon.svg?react";
import { useSidebar } from "@/components/ui/sidebar";

export function NavHeader() {
  const { state } = useSidebar();

  return (
    <div className="flex items-center justify-center py-2">
      {state === "collapsed" ? (
        <Icon className="h-[40px]" />
      ) : (
        <Logo className="h-[50px]" />
      )}
    </div>
  );
}
