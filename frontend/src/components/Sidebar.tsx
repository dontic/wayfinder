"use client";

import {
  IconButton,
  Box,
  CloseButton,
  Flex,
  Icon,
  useColorModeValue,
  Drawer,
  DrawerContent,
  useDisclosure,
  BoxProps,
  FlexProps,
  Image,
  Spacer,
  Button,
  useToast
} from "@chakra-ui/react";
import { FiHome, FiMenu } from "react-icons/fi";
import { BiTrip } from "react-icons/bi";
import { IoLocationOutline } from "react-icons/io5";

import { IconType } from "react-icons";
import { ReactNode, ReactText } from "react";
import { authLogoutCreate } from "~/api/endpoints/auth/auth";
import { useNavigate } from "react-router-dom";
import { useUserStore } from "~/stores/UserStore";

interface LinkItemProps {
  name: string;
  icon: IconType;
  href?: string;
}
const LinkItems: Array<LinkItemProps> = [
  { name: "Home", icon: FiHome, href: "/" },
  { name: "Trips", icon: BiTrip, href: "/trips" },
  { name: "Visits", icon: IoLocationOutline, href: "/visits" }
];

interface Props {
  children: ReactNode;
}

export default function SimpleSidebar({ children }: Props) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <Box minH="100vh" bg={useColorModeValue("gray.100", "gray.900")}>
      <SidebarContent
        onClose={() => onClose}
        display={{ base: "none", md: "block" }}
      />
      <Drawer
        isOpen={isOpen}
        placement="left"
        onClose={onClose}
        returnFocusOnClose={false}
        onOverlayClick={onClose}
        size="full"
      >
        <DrawerContent>
          <SidebarContent onClose={onClose} />
        </DrawerContent>
      </Drawer>
      {/* mobilenav */}
      <MobileNav display={{ base: "flex", md: "none" }} onOpen={onOpen} />
      <Box ml={{ base: 0, md: 60 }} p="4">
        {children}
      </Box>
    </Box>
  );
}

interface SidebarProps extends BoxProps {
  onClose: () => void;
}

const SidebarContent = ({ onClose, ...rest }: SidebarProps) => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const toast = useToast();
  const navigate = useNavigate();
  const { clearUser } = useUserStore();

  /* -------------------------------- FUNCTIONS ------------------------------- */
  const handleLogout = async () => {
    try {
      await authLogoutCreate();
      clearUser();
      navigate("/login");
    } catch (error) {
      toast({
        title: "Logout failed",
        description: "Something went wrong",
        status: "error",
        duration: 5000,
        isClosable: true
      });
    }
  };

  return (
    <Box
      bg={useColorModeValue("white", "gray.900")}
      borderRight="1px"
      borderRightColor={useColorModeValue("gray.200", "gray.700")}
      w={{ base: "full", md: 60 }}
      pos="fixed"
      h="full"
      {...rest}
    >
      <Flex flexDir={"column"} h={"100%"}>
        <Box>
          <Flex
            h="20"
            alignItems="center"
            mx="8"
            justifyContent="space-between"
          >
            <Image maxH={"50px"} src="src/assets/logo.svg" alt="Logo" />
            <CloseButton
              display={{ base: "flex", md: "none" }}
              onClick={onClose}
            />
          </Flex>
          {LinkItems.map((link) => (
            <NavItem
              key={link.name}
              icon={link.icon}
              onClick={() => {
                link.href && navigate(link.href);
              }}
            >
              {link.name}
            </NavItem>
          ))}
        </Box>

        <Spacer />
        <Box w="100%" textAlign="center" pb="4">
          <Button
            w="80%"
            colorScheme="gray"
            onClick={() => {
              handleLogout();
            }}
          >
            Logout
          </Button>
        </Box>
      </Flex>
    </Box>
  );
};

interface NavItemProps extends FlexProps {
  icon: IconType;
  children: ReactText;
}
const NavItem = ({ icon, children, ...rest }: NavItemProps) => {
  return (
    <Box
      as="a"
      href="#"
      style={{ textDecoration: "none" }}
      _focus={{ boxShadow: "none" }}
    >
      <Flex
        align="center"
        p="4"
        mx="4"
        borderRadius="lg"
        role="group"
        cursor="pointer"
        _hover={{
          bg: "cyan.400",
          color: "white"
        }}
        {...rest}
      >
        {icon && (
          <Icon
            mr="4"
            fontSize="16"
            _groupHover={{
              color: "white"
            }}
            as={icon}
          />
        )}
        {children}
      </Flex>
    </Box>
  );
};

interface MobileProps extends FlexProps {
  onOpen: () => void;
}
const MobileNav = ({ onOpen, ...rest }: MobileProps) => {
  return (
    <Flex
      ml={{ base: 0, md: 60 }}
      px={{ base: 4, md: 24 }}
      height="20"
      alignItems="center"
      bg={useColorModeValue("white", "gray.900")}
      borderBottomWidth="1px"
      borderBottomColor={useColorModeValue("gray.200", "gray.700")}
      justifyContent="flex-start"
      {...rest}
    >
      <IconButton
        variant="outline"
        onClick={onOpen}
        aria-label="open menu"
        icon={<FiMenu />}
      />

      <Spacer />

      <Image maxH={"50px"} src="src/assets/logo.svg" alt="Logo" />

      <Spacer />
    </Flex>
  );
};
