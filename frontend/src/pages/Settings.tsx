import SideBarLayout from "@/layouts/SideBarLayout";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useUserStore } from "@/stores/UserStore";
import ProfileInfo from "@/components/settings/ProfileInfo";

const Settings = () => {
  const { user } = useUserStore();

  return (
    <SideBarLayout title="Settings">
      <div className="flex w-full justify-center overflow-y-auto">
        <div id="settings-container" className="flex flex-col gap-6 py-6">
          <Tabs defaultValue="user" className="w-full">
            <TabsList
              className={`grid w-full max-w-md ${
                user?.first_name !== "user" ? "grid-cols-2" : "grid-cols-1"
              }`}
            >
              <TabsTrigger value="user">User</TabsTrigger>
              {user?.first_name !== "user" && (
                <TabsTrigger value="team">Overland</TabsTrigger>
              )}
            </TabsList>
            <TabsContent value="user" className="mt-6 space-y-6">
              <ProfileInfo />
            </TabsContent>
            <TabsContent value="team" className="mt-6"></TabsContent>
          </Tabs>
        </div>
      </div>
    </SideBarLayout>
  );
};

export default Settings;
