import {
  Box,
  Button,
  Flex,
  Icon,
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

import { wayfinderVisitsPlotRetrieve } from "~/api/endpoints/wayfinder/wayfinder";
import {
  VisitPlotlyData,
  VisitPlotlyLayout
} from "~/api/endpoints/api.schemas";

const Visits = () => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // State to manage the visibility of the date select
  const [isDateSelectVisible, setIsDateSelectVisible] = useState<boolean>(true);
  const [selectedQuickDateRange, setSelectedQuickDateRange] =
    useState<string>("");

  // Set initial date range to last week
  const [startDate, setStartDate] = useState<Date>(
    new Date(new Date().setDate(new Date().getDate() - 7))
  );
  const [endDate, setEndDate] = useState<Date>(new Date());

  // Plot states
  const [plotData, setPlotData] = useState<VisitPlotlyData[]>([]);
  const [plotLayout, setPlotLayout] = useState<VisitPlotlyLayout | {}>({});

  // Plot revision state to force plotly to update
  const [plotRevision, setPlotRevision] = useState<number>(0);

  const getVisitsPlot = async (start_date: string, end_date: string) => {
    setIsLoading(true);

    // Fetch the data
    try {
      // Fetch the visits plot endpoint
      let newVisitPlotlyData = await wayfinderVisitsPlotRetrieve({
        start_datetime: start_date,
        end_datetime: end_date
      });

      // If no visits, set data to null
      if (!newVisitPlotlyData) {
        setPlotData([]);
        setPlotLayout({});
        setIsLoading(false);
        return;
      }

      const newLayout = {
        ...newVisitPlotlyData.layout,
        datarevision: plotRevision + 1
      };

      setPlotData(newVisitPlotlyData.data);
      setPlotLayout(newLayout);
      setPlotRevision(plotRevision + 1);
      setIsLoading(false);
      return newVisitPlotlyData;
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
    const start_date = startDate.toISOString();
    const end_date = endDate.toISOString();
    getVisitsPlot(start_date, end_date);
  };

  // Create a use effect to set the default date range
  useEffect(() => {
    getVisitsPlot(startDate.toISOString(), endDate.toISOString());
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
            <Text>Select Date Range</Text>
            <DatePicker
              selectsRange={true}
              startDate={startDate}
              endDate={endDate}
              onChange={(update: Date[]) => {
                // Update the date range
                const [newStartDate, newEndDate] = update;
                setStartDate(newStartDate);
                setEndDate(newEndDate);

                // Reset the quick date range
                setSelectedQuickDateRange("");
              }}
              withPortal
            />
            <Text>OR</Text>
            <Select
              placeholder="Quick Date Range"
              onChange={(e) => {
                onQuickDateRangeChange(e);
              }}
              value={selectedQuickDateRange}
            >
              <option value="last_week">Last Week</option>
              <option value="last_month">Last Month</option>
              <option value="last_year">Last Year</option>
              <option value="ytd">YTD</option>
            </Select>
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

export default Visits;
