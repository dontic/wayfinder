import SideBarLayout from "@/layouts/SideBarLayout";
import TripsFilterCard from "@/components/trips/TripsFilterCard";

const Trips = () => {
  const handleFilterSubmit = (startDateTime: string, endDateTime: string) => {
    console.log("Filter applied:", { startDateTime, endDateTime });
    // Add your filter logic here
  };

  return (
    <SideBarLayout title="Trips" defaultOpen={false}>
      <div className="flex flex-col gap-4">
        <h1>Trips</h1>
      </div>
      <TripsFilterCard onSubmit={handleFilterSubmit} />
    </SideBarLayout>
  );
};

export default Trips;
