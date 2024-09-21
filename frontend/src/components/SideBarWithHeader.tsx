import {
  IconButton,
  Avatar,
  Box,
  CloseButton,
  Flex,
  HStack,
  VStack,
  Icon,
  useColorModeValue,
  Text,
  Drawer,
  DrawerContent,
  useDisclosure,
  BoxProps,
  FlexProps,
  Menu,
  MenuButton,
  MenuDivider,
  MenuItem,
  MenuList,
  Link as ChakraLink,
  useToast
} from "@chakra-ui/react";
import { FiHome, FiMenu, FiBell, FiChevronDown } from "react-icons/fi";
import { IconType } from "react-icons";
import { ReactNode } from "react";
import { Link as ReactRouterLink, useNavigate } from "react-router-dom";
import { authLogoutCreate } from "~/api/endpoints/auth/auth";
import { useUserStore } from "~/stores/UserStore";

interface LinkItemProps {
  name: string;
  icon: IconType;
  link: string;
}

interface NavItemProps extends FlexProps {
  icon: IconType;
  link: string;
  children: React.ReactNode;
}

interface MobileProps extends FlexProps {
  onOpen: () => void;
}

interface SidebarProps extends BoxProps {
  onClose: () => void;
}

const LinkItems: Array<LinkItemProps> = [
  { name: "Home", icon: FiHome, link: "/" }
];

const SidebarContent = ({ onClose, ...rest }: SidebarProps) => {
  return (
    <Box
      transition="3s ease"
      bg={useColorModeValue("white", "gray.900")}
      borderRight="1px"
      borderRightColor={useColorModeValue("gray.200", "gray.700")}
      w={{ base: "full", md: 60 }}
      pos="fixed"
      h="full"
      {...rest}
    >
      <Flex h="20" alignItems="center" mx="8" justifyContent="space-between">
        <ChakraLink
          href="/"
          fontSize={"2xl"}
          fontFamily="monospace"
          fontWeight="bold"
        >
          Logo
        </ChakraLink>
        <CloseButton display={{ base: "flex", md: "none" }} onClick={onClose} />
      </Flex>
      {LinkItems.map((link) => (
        <NavItem key={link.name} icon={link.icon} link={link.link}>
          {link.name}
        </NavItem>
      ))}
    </Box>
  );
};

const NavItem = ({ icon, children, link, ...rest }: NavItemProps) => {
  return (
    <ChakraLink
      as={ReactRouterLink}
      to={link}
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
          bg: "blue.200",
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
    </ChakraLink>
  );
};

const MobileNav = ({ onOpen, ...rest }: MobileProps) => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const toast = useToast();
  const navigate = useNavigate();
  const { user, clearUser } = useUserStore();

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

  /* --------------------------------- RENDER --------------------------------- */
  return (
    <Flex
      ml={{ base: 0, md: 60 }}
      px={{ base: 4, md: 4 }}
      height="14"
      alignItems="center"
      bg={useColorModeValue("white", "gray.900")}
      borderBottomWidth="1px"
      borderBottomColor={useColorModeValue("gray.200", "gray.700")}
      justifyContent={{ base: "space-between", md: "flex-end" }}
      {...rest}
    >
      <IconButton
        display={{ base: "flex", md: "none" }}
        onClick={onOpen}
        variant="outline"
        aria-label="open menu"
        icon={<FiMenu />}
      />

      <Text
        display={{ base: "flex", md: "none" }}
        fontSize="2xl"
        fontFamily="monospace"
        fontWeight="bold"
      >
        Logo
      </Text>

      <HStack spacing={{ base: "0", md: "6" }}>
        {/* Notifications */}
        <IconButton
          size="lg"
          variant="ghost"
          aria-label="open menu"
          icon={<FiBell />}
        />
        <Flex alignItems={"center"}>
          <Menu>
            <MenuButton
              py={2}
              transition="all 0.3s"
              _focus={{ boxShadow: "none" }}
            >
              <HStack>
                <Avatar
                  size={"sm"}
                  src={
                    "https://innostudio.de/fileuploader/images/default-avatar.png"
                  }
                />
                <VStack
                  display={{ base: "none", md: "flex" }}
                  alignItems="flex-start"
                  spacing="1px"
                  ml="2"
                >
                  <Text fontSize="sm">
                    {user?.first_name} {user?.last_name}
                  </Text>
                  {/* <Text fontSize="xs" color="gray.600">
                      Admin
                    </Text> */}
                </VStack>
                <Box display={{ base: "none", md: "flex" }}>
                  <FiChevronDown />
                </Box>
              </HStack>
            </MenuButton>
            <MenuList
              bg={useColorModeValue("white", "gray.900")}
              borderColor={useColorModeValue("gray.200", "gray.700")}
            >
              <ChakraLink as={ReactRouterLink} to="/profile">
                <MenuItem>Profile</MenuItem>
              </ChakraLink>
              <ChakraLink as={ReactRouterLink} to="/settings">
                <MenuItem>Settings</MenuItem>
              </ChakraLink>
              {/* <MenuItem>Billing </MenuItem> */}
              <MenuDivider />
              <MenuItem onClick={handleLogout}>Sign out</MenuItem>
            </MenuList>
          </Menu>
        </Flex>
      </HStack>
    </Flex>
  );
};

interface Props {
  children: ReactNode;
}

const SidebarWithHeader = ({ children }: Props) => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Box minH="100vh" bg={useColorModeValue("gray.50", "gray.900")}>
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
      <MobileNav onOpen={onOpen} />
      <Box ml={{ base: 0, md: 60 }} p="4">
        {children}
      </Box>
    </Box>
  );
};

export default SidebarWithHeader;
