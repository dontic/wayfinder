// Chakra components
import {
  Box,
  Flex,
  Text,
  IconButton,
  Image,
  Stack,
  Collapse,
  Icon,
  Link,
  Popover,
  PopoverTrigger,
  PopoverContent,
  useColorModeValue,
  useDisclosure,
  Spacer
} from "@chakra-ui/react";

// Chakra Icons
import {
  HamburgerIcon,
  CloseIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  LockIcon
} from "@chakra-ui/icons";

// Router
import { Link as ReactLink } from "react-router-dom";

import LogoutLink from "./Logout";
import Trips from "../pages/Trips";
import Visits from "../pages/Visits";

// Define NavItem type
interface NavItem {
  label: string;
  subLabel?: string;
  children?: Array<NavItem>;
  href?: string;
  component?: JSX.Element;
}

const NAV_ITEMS: Array<NavItem> = [
  { label: "Trips", href: "/trips", component: <Trips /> },
  { label: "Visits", href: "/visits", component: <Visits /> }
];

const NavBar = () => {
  const { isOpen, onToggle } = useDisclosure();

  //   // Get the height of the NavBar
  //   const ref = useRef<HTMLDivElement>(null);
  //   useLayoutEffect(() => {
  //     if (ref.current != null) {
  //       let height = ref.current.offsetHeight; // Gets the height of the navbar
  //       let style = getComputedStyle(ref.current); // Gets the marging of the navbar
  //       let navBarHeight = height + parseInt(style.marginBottom); // Sums them both
  //       setNavBarHeight(navBarHeight); // Sets the nav bar height in the navbarheight context for the whole app
  //     }
  //   }, []);

  return (
    <Box pos="sticky" top={0} zIndex="sticky">
      <Flex
        bg={"transparent"}
        minH={"60px"}
        py={{ base: 2 }}
        px={{ base: 4 }}
        align={"center"}
      >
        <Flex flex={{ base: 1 }} justify={{ base: "center", md: "start" }}>
          <Link as={ReactLink} to={"/"}>
            <Image
              boxSize={"40px"}
              minW={"100px"}
              objectFit={"cover"}
              src="src/assets/full_logo_without_bg.svg"
              alt="Wayfinder Logo"
            />
          </Link>
          <Spacer />
          <Flex
            flex={{ base: 0, md: "auto" }}
            ml={{ base: -2 }}
            // Display this by default and hide from 'md' (medium devices) up
            display={{ base: "flex", md: "none" }}
          >
            <IconButton
              onClick={onToggle}
              icon={
                isOpen ? (
                  <CloseIcon w={3} h={3} />
                ) : (
                  <HamburgerIcon w={5} h={5} />
                )
              }
              variant={"ghost"}
              aria-label={"Toggle Navigation"}
            />
          </Flex>

          <Flex display={{ base: "none", md: "flex" }} mr={10}>
            <DesktopNav />
          </Flex>
        </Flex>
      </Flex>

      <Collapse in={isOpen} animateOpacity>
        <MobileNav />
      </Collapse>
    </Box>
  );
};

// Desktop NavBar
const DesktopNav = () => {
  /* -------------------------------------------------------------------------- */
  /*                                   RENDER                                   */
  /* -------------------------------------------------------------------------- */
  return (
    <Stack direction={"row"} spacing={4} align={"center"}>
      {NAV_ITEMS.map((navItem) => (
        // If the navItem has a restrict prop, check if the user has the permission to see it
        <Box key={navItem.label}>
          <Popover trigger={"hover"} placement={"bottom-start"}>
            <PopoverTrigger>
              <Link
                as={ReactLink}
                to={navItem.href}
                p={2}
                fontSize={"sm"}
                fontWeight={500}
                color={"black"}
                _hover={{
                  textDecoration: "none",
                  color: "#48a9ed"
                }}
              >
                {navItem.label}
              </Link>
            </PopoverTrigger>

            {navItem.children && (
              <PopoverContent
                border={0}
                boxShadow={"xl"}
                bg={"#116bac"}
                p={4}
                rounded={"xl"}
                minW={"sm"}
              >
                <Stack>
                  {navItem.children.map((child) => (
                    <DesktopSubNav key={child.label} {...child} />
                  ))}
                </Stack>
              </PopoverContent>
            )}
          </Popover>
        </Box>
      ))}
      <LogoutLink>
        <Link
          p={2}
          fontSize={"sm"}
          fontWeight={500}
          color={"black"}
          _hover={{
            textDecoration: "none",
            color: "red"
          }}
        >
          Logout <Icon as={LockIcon} />
        </Link>
      </LogoutLink>
    </Stack>
  );
};

// Desktop Sub Nav (Dropdowns)
const DesktopSubNav = ({ label, href, subLabel }: NavItem) => {
  return (
    <Link
      as={ReactLink}
      to={href}
      role={"group"}
      display={"block"}
      p={2}
      rounded={"md"}
      _hover={{ bg: "#3daeb2" }}
    >
      <Stack direction={"row"} align={"center"}>
        <Box>
          <Text
            transition={"all .3s ease"}
            _groupHover={{ color: "white" }}
            fontWeight={500}
          >
            {label}
          </Text>
          <Text fontSize={"sm"}>{subLabel}</Text>
        </Box>
        <Flex
          transition={"all .3s ease"}
          transform={"translateX(-10px)"}
          opacity={0}
          _groupHover={{ opacity: "100%", transform: "translateX(0)" }}
          justify={"flex-end"}
          align={"center"}
          flex={1}
        >
          <Icon color={"white"} w={5} h={5} as={ChevronRightIcon} />
        </Flex>
      </Stack>
    </Link>
  );
};

const MobileNav = () => {
  return (
    <Stack
      bg={useColorModeValue("white", "gray.800")}
      p={4}
      display={{ md: "none" }}
    >
      {NAV_ITEMS.map((navItem) => (
        <MobileNavItem key={navItem.label} {...navItem} />
      ))}
    </Stack>
  );
};

const MobileNavItem = ({ label, children, href }: NavItem) => {
  const { isOpen, onToggle } = useDisclosure();

  return (
    <Stack spacing={4} onClick={children && onToggle}>
      <Flex
        py={2}
        as={Link}
        href={href ?? "#"}
        justify={"space-between"}
        align={"center"}
        _hover={{
          textDecoration: "none"
        }}
      >
        <Text
          fontWeight={600}
          color={useColorModeValue("gray.600", "gray.200")}
        >
          {label}
        </Text>
        {children && (
          <Icon
            as={ChevronDownIcon}
            transition={"all .25s ease-in-out"}
            transform={isOpen ? "rotate(180deg)" : ""}
            w={6}
            h={6}
          />
        )}
      </Flex>

      <Collapse in={isOpen} animateOpacity style={{ marginTop: "0!important" }}>
        <Stack
          mt={2}
          pl={4}
          borderLeft={1}
          borderStyle={"solid"}
          borderColor={useColorModeValue("gray.200", "gray.700")}
          align={"start"}
        >
          {children &&
            children.map((child) => (
              <Link key={child.label} py={2} as={ReactLink} to={child.href}>
                {child.label}
              </Link>
            ))}
        </Stack>
      </Collapse>
    </Stack>
  );
};

export default NavBar;
