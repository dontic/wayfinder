import {
  Box,
  Button,
  HStack,
  Icon,
  Select,
  Text,
  VStack
} from "@chakra-ui/react";
import { DatePicker } from "../components/ChakraDatePicker";
import "react-datepicker/dist/react-datepicker.css";

import axios from "../api/axios";
import { useEffect, useState } from "react";

import { ChevronUpIcon, ChevronDownIcon } from "@chakra-ui/icons";

import Plotly from "react-plotly.js";
import createPlotlyComponent from "react-plotly.js/factory";
const Plot = createPlotlyComponent(Plotly);

const Visits = () => {
  const [isDateSelectVisible, setIsDateSelectVisible] =
    useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [dateRange, setDateRange] = useState<[Date | null, Date | null]>([
    null,
    null
  ]);
  const [startDate, endDate] = dateRange;
  const [data, setData] = useState<any>(null);
  const [layout, setLayout] = useState<any>(null);
  const [plotRevision, setPlotRevision] = useState<number>(0);
  const [selectedQuickDateRange, setSelectedQuickDateRange] =
    useState<string>("");

  const getVisitsPlot = async (start_date: string, end_date: string) => {
    setIsLoading(true);
    try {
      const response = await axios.get(
        `/wayfinder/visitsplot?start_date=${start_date}&end_date=${end_date}`
      );
      const resData = response.data;
      console.log(resData);

      if (!resData) {
        setData(null);
        setLayout(null);
        setIsLoading(false);
        return;
      }
      setData(resData.data);
      const newLayout = {
        ...resData.layout,
        datarevision: plotRevision + 1
      };
      setLayout(newLayout);
      console.log("New layout", newLayout);
      setPlotRevision(plotRevision + 1);

      setIsLoading(false);
      return data;
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

    setDateRange([new Date(start_date), new Date(end_date)]);
  };

  const onSubmit = () => {
    if (!startDate || !endDate) {
      return;
    }
    const start_date = startDate.toISOString();
    const end_date = endDate.toISOString();
    getVisitsPlot(start_date, end_date);
  };

  useEffect(() => {
    const start_date = new Date(
      new Date().setDate(new Date().getDate() - 7)
    ).toISOString();
    const end_date = new Date().toISOString();

    getVisitsPlot(start_date, end_date);
  }, []);

  return (
    <Box>
      <Box
        pos={"absolute"}
        top={0}
        left={0}
        h="100vh"
        w="100vw"
        justifyContent="center"
        alignItems="center"
      >
        <Plot
          data={data}
          layout={layout}
          config={{ responsive: true, displayModeBar: false }}
          style={{ width: "100%", height: "100%" }}
          revision={plotRevision}
        />
      </Box>
      <Box
        position="fixed"
        bottom="0"
        left="0"
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
              onChange={(update: [Date | null, Date | null]) => {
                setDateRange(update);
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
            <HStack>
              <Icon
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
              <Button
                colorScheme="blue"
                onClick={() => {
                  onSubmit();
                }}
                isLoading={isLoading}
              >
                Submit
              </Button>
            </HStack>
          </VStack>
        ) : (
          <Icon
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
