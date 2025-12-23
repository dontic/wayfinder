import Logo from "@/assets/logo.svg?react";
import Icon from "@/assets/icon.svg?react";
import { useSidebar } from "@/components/ui/sidebar";

export function NavHeader() {
  const { state } = useSidebar();

  return (
    <div className="flex items-center justify-center h-[40px] py-2">
      {state === "collapsed" ? (
        <Icon className="h-full" />
      ) : (
        <Logo className="h-full" />
      )}
    </div>
  );
}
