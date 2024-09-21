import {
  Box,
  BoxProps,
  SystemStyleObject,
  useBreakpointValue,
  useColorMode,
  ResponsiveValue,
  InputProps,
  Input,
  ColorMode
} from "@chakra-ui/react";
import React, {
  useEffect,
  useState,
  forwardRef,
  ForwardRefRenderFunction
} from "react";
import ReactDatePicker, { DatePickerProps } from "react-datepicker";

const datePickerThemes = {
  light: {
    gray100: "gray.100",
    gray200: "gray.200",
    gray300: "gray.300",
    gray400: "gray.400",
    gray500: "gray.500",
    color300: "blue.300",
    color500: "blue.500",
    color600: "blue.600",
    header: "white",
    text: "gray.800",
    negativeText: "whiteAlpha.900",
    monthBackground: "white",
    outsideDay: "#9f9696"
  },
  dark: {
    gray100: "gray.700",
    gray200: "gray.600",
    gray300: "gray.500",
    gray400: "gray.400",
    gray500: "gray.300",
    color300: "blue.200",
    color500: "blue.300",
    color600: "blue.500",
    header: "gray.700",
    text: "whiteAlpha.900",
    negativeText: "whiteAlpha.900",
    monthBackground: "gray.700",
    outsideDay: "#9f9696"
  }
};

type DatePickerTheme = typeof datePickerThemes.light;
type Size = "xs" | "sm" | "md" | "xl";

type OmittedInputProps = Omit<InputProps, "isDisabled" | "onChange">;
const ChakraInputWithRef: ForwardRefRenderFunction<
  HTMLInputElement,
  InputProps
> = (props, ref) => <Input {...props} ref={ref} />;
const CustomInput = forwardRef(ChakraInputWithRef);

type Props<
  CustomModifierNames extends string = never,
  WithRange extends boolean | undefined = undefined
> = Omit<
  // @ts-ignore
  DatePickerProps<CustomModifierNames, WithRange>,
  "todayButton"
> & {
  rootProps?: BoxProps;
  inputProps?: OmittedInputProps;
  datePickerSize?: ResponsiveValue<Size>;
  datePickerColorSchema?: InputProps["colorScheme"];
  extendDatePickerTheme?: (
    colorMode: ColorMode,
    provide: DatePickerTheme
  ) => DatePickerTheme;
};

const DatePicker = <
  CustomModifierNames extends string = never,
  WithRange extends boolean | undefined = undefined
>({
  rootProps,
  inputProps,
  datePickerSize: datePickerSizeProps = "md",
  datePickerColorSchema,
  extendDatePickerTheme,
  ...datePickerProps
}: React.PropsWithChildren<Props<CustomModifierNames, WithRange>>) => {
  const colorMode = useColorMode().colorMode;
  const isLight = colorMode === "light";

  const datepickerSize = useDetermineSize(datePickerSizeProps);
  if (!datepickerSize) {
    return null;
  }

  const datePickerTheme = customizeDatePickerTheme(
    datePickerThemes[isLight ? "light" : "dark"],
    datePickerColorSchema,
    extendDatePickerTheme
      ? (theme: DatePickerTheme) => extendDatePickerTheme(colorMode, theme)
      : undefined
  );

  const normalizedInputProps = {
    ...inputProps,
    isDisabled: datePickerProps.disabled
  };

  const timeWidth = getTimeWidth(datepickerSize);
  const container = {
    borderColor: datePickerTheme.gray200
  };
  const dayContainer = {
    padding: 1.5,
    bg: datePickerTheme.monthBackground,
    margin: 0
  };
  const day = {
    ...getDayCellSize(datepickerSize),
    color: datePickerTheme.text,
    hoverBg: datePickerTheme.gray200,
    selecting: {
      bg: datePickerTheme.color300
    },
    selected: {
      bg: datePickerTheme.color500,
      fontWeight: "normal",
      color: datePickerTheme.negativeText,
      hover: {
        bg: datePickerTheme.color600
      }
    },
    disabled: {
      bg: "unset",
      opacity: 0.2,
      cursor: "not-allowed"
    }
  };
  const header = {
    topSpace: 3,
    borderColor: datePickerTheme.gray300,
    fontWeight: 600,
    fontSize: "1rem",
    color: datePickerTheme.text,
    bg: datePickerTheme.header
  };
  const navigationButton = {
    size: datepickerSize === "xs" ? 5 : 7,
    leftRightSpace: "0.8rem",
    color: datePickerTheme.gray400,
    hover: {
      color: datePickerTheme.gray500
    }
  };

  const sx: SystemStyleObject = {
    ".react-datepicker": {
      minWidth: "max-content",
      fontFamily: "unset",
      fontSize: datepickerSize === "xs" ? "xs" : "md",
      borderColor: container.borderColor,
      boxShadow: "sm",
      bg: dayContainer.bg,
      margin: dayContainer.margin,
      color: datePickerTheme.text
    },
    ".react-datepicker__input-container": {
      display: "block",
      ".react-datepicker__close-icon": {
        // clear button
        "&::after": {
          backgroundColor: "unset",
          borderRadius: "unset",
          fontSize:
            inputProps?.size === "lg"
              ? "2xl"
              : inputProps?.size === "xs"
                ? "md"
                : "xl",
          color: datePickerTheme.gray300,
          h: "20px",
          w: "20px"
        },
        "&:hover::after": {
          color: datePickerTheme.gray400
        }
      }
    },
    ".react-datepicker__header": {
      paddingBlockStart: header.topSpace,
      borderColor: header.borderColor,
      bg: header.bg,
      ".react-datepicker__header__dropdown": {
        // year/month picker
        marginBlockStart: 2,
        display: "flex",
        justifyContent: "center",
        _empty: {
          display: "none"
        },
        [multipleSelector(
          ".react-datepicker__month-dropdown-container",
          ".react-datepicker__year-dropdown-container"
        )]: {
          cursor: "pointer",
          borderRadius: "md",
          paddingInlineStart: 1,
          paddingInlineEnd: 1
        },
        [multipleSelector(
          ".react-datepicker__month-read-view",
          ".react-datepicker__year-read-view"
        )]: {
          display: "flex",
          flexDirection: "row-reverse",
          paddingInlineEnd: 4,
          paddingInlineStart: 1,
          _hover: {
            bg: datePickerTheme.gray200,
            [multipleSelector(
              ".react-datepicker__month-read-view--down-arrow",
              ".react-datepicker__year-read-view--down-arrow"
            )]: {
              borderColor: navigationButton.hover.color
            }
          }
        },
        [multipleSelector(
          ".react-datepicker__month-read-view--down-arrow",
          ".react-datepicker__year-read-view--down-arrow"
        )]: {
          position: "relative",
          top: 2,
          right: "-0.5rem",
          borderColor: navigationButton.color,
          borderWidth: "2px 2px 0 0",
          h: "7px",
          w: "7px"
        },
        [multipleSelector(
          ".react-datepicker__month-dropdown",
          ".react-datepicker__year-dropdown"
        )]: {
          bg: datePickerTheme.monthBackground,
          borderColor: datePickerTheme.gray200,
          boxShadow: "md",
          "& > div": {
            paddingBlockStart: 1,
            paddingBlockEnd: 1,
            color: datePickerTheme.text,
            "&:hover": {
              bg: datePickerTheme.gray200
            }
          }
        }
      },
      [multipleSelector(
        ".react-datepicker__current-month",
        ".react-datepicker-time__header",
        ".react-datepicker-year-header"
      )]: {
        fontWeight: header.fontWeight,
        color: header.color,
        fontSize: header.fontSize
      },
      ".react-datepicker__day-names": {
        padding: dayContainer.padding,
        paddingBlockEnd: 0,
        ".react-datepicker__day-name": {
          w: day.width,
          lineHeight: day.lineHeight,
          color: day.color
        }
      }
    },
    /* / .react-datepicker__header */
    ".react-datepicker__navigation": {
      w: navigationButton.size,
      h: navigationButton.size,
      top: header.topSpace,
      marginTop: datepickerSize !== "xs" ? -1 : undefined,
      color: "transparent",
      _hover: {
        ".react-datepicker__navigation-icon::before": {
          borderColor: navigationButton.hover.color
        }
      },
      ".react-datepicker__navigation-icon": {
        fontSize: "unset",
        w: "100%",
        h: "100%",
        top: "unset",
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        _before: {
          left: "unset",
          top: "unset",
          right: "unset",
          bottom: "unset",
          borderColor: navigationButton.color
        }
      },
      "&.react-datepicker__navigation--previous": {
        left: navigationButton.leftRightSpace
      },
      "&.react-datepicker__navigation--next": {
        right: navigationButton.leftRightSpace
      },
      "&.react-datepicker__navigation--next--with-time:not(.react-datepicker__navigation--next--with-today-button)":
        {
          right: `calc(${timeWidth}px - -0.8rem)`
        }
    },
    /* / .react-datepicker__navigation' */
    [multipleSelector(
      ".react-datepicker__month-read-view--selected-month",
      ".react-datepicker__year-read-view--selected-year"
    )]: {
      fontWeight: header.fontWeight,
      color: header.color
    },
    ".react-datepicker__month": {
      ...dayContainer,
      borderBottomRightRadius: "md",
      borderBottomLeftRadius: "md",
      ".react-datepicker__day": {
        w: day.width,
        lineHeight: day.lineHeight,
        color: day.color,
        _hover: {
          bg: day.hoverBg
        },
        "&.react-datepicker__day--disabled": {
          ...day.disabled,
          _hover: {
            ...day.disabled
          }
        },
        [multipleSelector(
          "&.react-datepicker__day--in-selecting-range",
          "&.react-datepicker__month-text--in-selecting-range",
          "&.react-datepicker__day--keyboard-selected",
          "&.react-datepicker__month-text--keyboard-selected",
          "&.react-datepicker__quarter-text--keyboard-selected",
          "&.react-datepicker__year-text--keyboard-selected"
        )]: {
          bg: day.selecting.bg
        },
        [multipleSelector(
          "&.react-datepicker__day--selected:not(.react-datepicker__day--disabled)",
          "&.react-datepicker__day--in-range:not(.react-datepicker__day--disabled)",
          "&.react-datepicker__month-text--selected:not(.react-datepicker__day--disabled)",
          "&.react-datepicker__month-text--in-range:not(.react-datepicker__day--disabled)"
        )]: {
          bg: day.selected.bg,
          fontWeight: day.selected.fontWeight,
          color: day.selected.color,
          _hover: {
            bg: day.selected.hover.bg
          }
        }
      },
      ".react-datepicker__day--outside-month": {
        // outside month day
        color: datePickerTheme.outsideDay
      }
    },
    /* / .react-datepicker__month */
    ".react-datepicker__time-container": {
      borderColor: header.borderColor,
      w: timeWidth,
      ".react-datepicker__time": {
        bg: dayContainer.bg,
        margin: dayContainer.margin,
        ".react-datepicker__time-box ": {
          w: "100%",
          "ul.react-datepicker__time-list": {
            "li.react-datepicker__time-list-item": {
              h: "auto",
              padding: 2,
              color: day.color,
              _hover: {
                bg: day.hoverBg
              }
            },
            "li.react-datepicker__time-list-item--selected:not(.react-datepicker__day--disabled)":
              {
                bg: day.selected.bg,
                fontWeight: day.selected.fontWeight,
                color: day.selected.color,
                _hover: {
                  bg: day.selected.hover.bg
                }
              }
          }
        }
      }
    },
    /* / .react-datepicker__time-container */
    ".react-datepicker__triangle": {
      // https://github.com/Hacker0x01/react-datepicker/issues/3176
      "@media screen and (min-width:420px)": {
        left: `${
          ["top-end", "bottom-end"].includes(
            datePickerProps.popperPlacement || ""
          )
            ? "3rem"
            : "-3rem"
        } !important`
      }
    },
    ".react-datepicker-popper[data-placement^=bottom]": {
      ".react-datepicker__triangle": {
        "&::before": {
          // top triangle (border)
          borderBottomColor: container.borderColor
        },
        "&::after": {
          // top triangle (fill color)
          borderBottomColor: header.bg,
          top: "1px"
        }
      }
    },
    ".react-datepicker-popper[data-placement^=top]": {
      ".react-datepicker__triangle": {
        "&::before": {
          // bottom triangle (border)
          borderTopColor: container.borderColor
        },
        "&::after": {
          // bottom triangle (fill color)
          borderTopColor: dayContainer.bg
        }
      }
    },
    ".react-datepicker__input-time-container": {
      m: 0,
      p: 3,
      ".react-datepicker-time__caption": {
        color: datePickerTheme.text
      }
    },
    ".react-datepicker__portal": {
      bg: "blackAlpha.600"
    }
  };

  return (
    <Box sx={sx} w={"100%"} lineHeight={"normal"} {...rootProps}>
      <ReactDatePicker
        {...datePickerProps}
        customInput={
          datePickerProps.customInput || (
            <CustomInput {...normalizedInputProps} />
          )
        }
      />
    </Box>
  );
};

const getTimeWidth = (size?: Size) => {
  if (size === "xl") {
    return 120;
  }

  if (size === "sm" || size === "xs") {
    return 75;
  }

  return 105;
};

const getDayCellSize = (size: Size) => {
  const baseSize = getBaseSize(size);
  if (size === "xl") {
    return { width: baseSize, lineHeight: "3rem" };
  }

  return { width: baseSize, lineHeight: baseSize };
};

const getBaseSize = (size: Size) => {
  if (size === "xl") {
    return 12;
  }

  if (size === "sm") {
    return 8;
  }

  if (size === "xs") {
    return 6;
  }

  return 10;
};

const useDetermineSize = (size?: ResponsiveValue<Size>) => {
  const [tick, setTick] = useState(0);
  const breakPoints =
    size == null || typeof size === "string" ? [size || "md"] : size;
  const result = useBreakpointValue(breakPoints) ?? undefined;

  useEffect(() => {
    setTick((v) => v + 1);
  }, []);

  if (tick === 0) {
    // for SSR
    return undefined;
  }
  return result;
};

const multipleSelector = (...selectors: string[]) => selectors.join(",");

const customizeDatePickerTheme = (
  theme: DatePickerTheme,
  colorScheme: Props["datePickerColorSchema"],
  extendDatePickerTheme?: (provide: DatePickerTheme) => DatePickerTheme
) => {
  let customizedTheme = theme;
  if (colorScheme) {
    customizedTheme = {
      ...customizedTheme,
      color300: `${colorScheme}.300`,
      color500: `${colorScheme}.500`,
      color600: `${colorScheme}.600`
    };
  }

  if (extendDatePickerTheme) {
    customizedTheme = extendDatePickerTheme(customizedTheme);
  }

  return customizedTheme;
};

export { DatePicker };
export type { Props };
