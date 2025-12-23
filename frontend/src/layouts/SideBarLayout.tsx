// UI stuff
import { AppSidebar } from "@/components/sidebar/app-sidebar";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger
} from "@/components/ui/sidebar";

const SideBarLayout = ({
  children,
  title,
  actions
}: {
  children: React.ReactNode;
  title: string;
  actions?: React.ReactNode;
}) => {
  return (
    <SidebarProvider id="mainbox">
      <AppSidebar />
      <SidebarInset>
        <div className="flex flex-col h-[100vh] overflow-hidden">
          <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
            <div className="flex items-center gap-2 px-4">
              <SidebarTrigger className="-ml-1" />
              <Separator
                orientation="vertical"
                className="mr-2 data-[orientation=vertical]:h-4"
              />
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold">{title}</h1>
              </div>
            </div>
            {actions ? (
              <div className="ml-auto flex items-center gap-2 px-4">
                {actions}
              </div>
            ) : null}
          </header>
          <div className="flex flex-1 min-h-0 overflow-hidden pt-0">
            {children}
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
};

export default SideBarLayout;
