import {
  Box,
  Button,
  Divider,
  Flex,
  Icon,
  Input,
  Select,
  Spacer,
  Text,
  VStack
} from "@chakra-ui/react";
import { DatePicker } from "~/components/ChakraDatePicker";
import "react-datepicker/dist/react-datepicker.css";

import { useEffect, useState } from "react";

import { ChevronUpIcon, ChevronDownIcon } from "@chakra-ui/icons";

import Plot from "react-plotly.js";

import { wayfinderTripsPlotRetrieve } from "~/api/endpoints/wayfinder/wayfinder";
import {
  VisitPlotlyData,
  VisitPlotlyLayout
} from "~/api/endpoints/api.schemas";

const Trips = () => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // State to manage the visibility of the date select
  const [isDateSelectVisible, setIsDateSelectVisible] = useState<boolean>(true);
  const [selectedQuickDateRange, setSelectedQuickDateRange] =
    useState<string>("");

  // Set initial date range to last 24h
  const [startDate, setStartDate] = useState<Date>(
    new Date(new Date().setDate(new Date().getDate() - 1))
  );
  const [endDate, setEndDate] = useState<Date>(new Date());

  // Set other parameters
  const [showVisits, setShowVisits] = useState<boolean>(false);
  const [showStationary, setShowStationary] = useState<boolean>(false);
  const [colorTrips, setColorTrips] = useState<boolean>(false);
  const [locationsDuringVisits, setLocationsDuringVisits] =
    useState<boolean>(false);
  const [desiredAccuracy, setDesiredAccuracy] = useState<number>(0);

  // Plot states
  const [plotData, setPlotData] = useState<VisitPlotlyData[]>([]);
  const [plotLayout, setPlotLayout] = useState<VisitPlotlyLayout | {}>({});

  // Plot revision state to force plotly to update
  const [plotRevision, setPlotRevision] = useState<number>(0);

  const getTripsPlot = async () => {
    setIsLoading(true);

    // Fetch the data
    try {
      // Fetch the trips plot endpoint
      let newTripPlotlyData = await wayfinderTripsPlotRetrieve({
        start_datetime: startDate.toISOString(),
        end_datetime: endDate.toISOString(),
        show_visits: showVisits,
        show_stationary: showStationary,
        color_trips: colorTrips,
        locations_during_visits: locationsDuringVisits,
        desired_accuracy: desiredAccuracy
      });

      // If no trips, set data to null
      if (!newTripPlotlyData) {
        setPlotData([]);
        setPlotLayout({});
        setIsLoading(false);
        return;
      }

      const newLayout = {
        ...newTripPlotlyData.layout,
        datarevision: plotRevision + 1
      };

      setPlotData(newTripPlotlyData.data);
      setPlotLayout(newLayout);
      setPlotRevision(plotRevision + 1);
      setIsLoading(false);
      return newTripPlotlyData;
    } catch (err) {
      setIsLoading(false);
      console.log(err);
    }
  };

  const onQuickDateRangeChange = (e: any) => {
    const value = e.target.value;

    setSelectedQuickDateRange(value);

    if (!value) {
      return;
    }

    let start_date = "";
    let end_date = "";

    switch (value) {
      case "last_24h":
        start_date = new Date(
          new Date().setDate(new Date().getDate() - 1)
        ).toISOString();
        end_date = new Date().toISOString();
        break;
      case "last_week":
        start_date = new Date(
          new Date().setDate(new Date().getDate() - 7)
        ).toISOString();
        end_date = new Date().toISOString();
        break;
      case "last_month":
        start_date = new Date(
          new Date().setDate(new Date().getDate() - 30)
        ).toISOString();
        end_date = new Date().toISOString();
        break;
      case "last_year":
        start_date = new Date(
          new Date().setDate(new Date().getDate() - 365)
        ).toISOString();
        end_date = new Date().toISOString();
        break;
      case "ytd":
        start_date = new Date(new Date().getFullYear(), 0, 1).toISOString();
        end_date = new Date().toISOString();
        break;
    }

    // Set date states
    setStartDate(new Date(start_date));
    setEndDate(new Date(end_date));
  };

  // On submit, fetch the data
  const onSubmit = () => {
    if (!startDate || !endDate) {
      return;
    }
    getTripsPlot();
  };

  // Create a use effect to set the default date range
  useEffect(() => {
    getTripsPlot();
  }, []);

  return (
    <Box w={"100%"} h={"100vh"} justifyContent="center" alignItems="center">
      {/* Plot */}

      <Plot
        // @ts-ignore
        data={plotData}
        layout={plotLayout}
        config={{ responsive: true, displayModeBar: false, scrollZoom: true }}
        style={{ width: "100%", height: "100%" }}
        revision={plotRevision}
      />

      {/* Date selector */}
      <Box
        position="fixed"
        bottom="0"
        left={{ md: "60", base: "0" }}
        padding="4"
        rounded={"md"}
        boxShadow={"lg"}
        bg="white"
      >
        {isDateSelectVisible ? (
          <VStack>
            <Text>Select Datetime Range</Text>
            {/* Start datetime */}

            <DatePicker
              selected={startDate}
              onChange={(date: Date) => setStartDate(date)}
              timeInputLabel="Time:"
              dateFormat="MM/dd/yyyy h:mm aa"
              showTimeInput
            />
            <Text>to</Text>
            <DatePicker
              selected={endDate}
              onChange={(date: Date) => setEndDate(date)}
              timeInputLabel="Time:"
              dateFormat="MM/dd/yyyy h:mm aa"
              showTimeInput
            />
            <Divider />
            <Text>OR</Text>
            <Select
              placeholder="Quick Date Range"
              onChange={(e) => {
                onQuickDateRangeChange(e);
              }}
              value={selectedQuickDateRange}
            >
              <option value="last_24h">Last 24h</option>
              <option value="last_week">Last Week</option>
              <option value="last_month">Last Month</option>
              <option value="last_year">Last Year</option>
              <option value="ytd">YTD</option>
            </Select>
            <Divider />
            <Flex w={"100%"} alignItems={"center"}>
              <Text>Show Visits</Text>
              <Spacer />
              <input
                type="checkbox"
                checked={showVisits}
                onChange={(e) => {
                  setShowVisits(e.target.checked);
                }}
              />
            </Flex>
            <Flex w={"100%"} alignItems={"center"}>
              <Text>Show Stationary</Text>
              <Spacer />
              <input
                type="checkbox"
                checked={showStationary}
                onChange={(e) => {
                  setShowStationary(e.target.checked);
                }}
              />
            </Flex>
            <Flex w={"100%"} alignItems={"center"}>
              <Text>Color Trips</Text>
              <Spacer />
              <input
                type="checkbox"
                checked={colorTrips}
                onChange={(e) => {
                  setColorTrips(e.target.checked);
                }}
              />
            </Flex>
            <Flex w={"100%"} alignItems={"center"}>
              <Text>Locations during visits</Text>
              <Spacer />
              <input
                type="checkbox"
                checked={locationsDuringVisits}
                onChange={(e) => {
                  setLocationsDuringVisits(e.target.checked);
                }}
              />
            </Flex>
            <Flex w={"100%"} alignItems={"center"}>
              <Text>Desired accuracy</Text>
              <Spacer />
              <Input
                maxW={"75px"}
                type="number"
                value={desiredAccuracy}
                onChange={(e) => {
                  setDesiredAccuracy(parseInt(e.target.value));
                }}
              />
            </Flex>
            <Flex w={"100%"} alignItems={"center"}>
              <Icon
                border={"1px"}
                borderColor={"gray.300"}
                rounded={"md"}
                boxSize={6}
                as={ChevronUpIcon}
                _hover={{
                  cursor: "pointer",
                  color: "blue",
                  transform: "rotate(180deg)"
                }}
                onClick={() => {
                  setIsDateSelectVisible(false);
                }}
              />

              <Spacer />

              <Button
                colorScheme="blue"
                onClick={() => {
                  onSubmit();
                }}
                isLoading={isLoading}
              >
                Submit
              </Button>

              <Spacer />
            </Flex>
          </VStack>
        ) : (
          <Icon
            rounded={"md"}
            boxSize={6}
            as={ChevronDownIcon}
            _hover={{
              cursor: "pointer",
              color: "blue",
              transform: "rotate(180deg)"
            }}
            onClick={() => {
              setIsDateSelectVisible(true);
            }}
          />
        )}
      </Box>
    </Box>
  );
};

export default Trips;
