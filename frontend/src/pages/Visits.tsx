import SideBarLayout from "@/layouts/SideBarLayout";

const Visits = () => {
  return (
    <SideBarLayout title="Visits" defaultOpen={false}>
      <div className="flex flex-col gap-4">
        <h1>Visits</h1>
      </div>
    </SideBarLayout>
  );
};

export default Visits;
