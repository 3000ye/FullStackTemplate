import {Box, Flex, Icon, Text} from "@chakra-ui/react"
import {useQueryClient} from "@tanstack/react-query"
import {Link as RouterLink} from "@tanstack/react-router"
import {FiHome, FiSettings} from "react-icons/fi"
import { GrTest } from "react-icons/gr";
import { MdOutlineNewReleases } from "react-icons/md";


import type {UserPublic} from "@/client"

const head_items = [
  {icon: FiHome, title: "Home", path: "/"},
]

const foot_items = [
  {icon: FiSettings, title: "User Setting", path: "/settings"},
  {icon: MdOutlineNewReleases, title: "Releases", path: "/release"},
]

interface SidebarItemsProps {
    onClose?: () => void
}

const SidebarItems = ({onClose}: SidebarItemsProps) => {
  const queryClient = useQueryClient()
  const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"])


  return (
      <>
          <Text fontSize="xs" px={4} py={2} fontWeight="bold">
              Menu
          </Text>
          <Box>
            {/* Home 和 Dashboard 页面，所有人可见 */}
            {head_items.map(({icon, title, path}) => (
                <RouterLink key={title} to={path} onClick={onClose}>
                  <Flex
                      gap={4}
                      px={4}
                      py={2}
                      _hover={{
                        background: "gray.subtle",
                      }}
                      alignItems="center"
                      fontSize="sm"
                  >
                    <Icon as={icon} alignSelf="center"/>
                    <Text ml={2}>{title}</Text>
                  </Flex>
                </RouterLink>
            ))}

            {/* UserSetting 和 Release 页面，所有人可见 */}
            {foot_items.map(({icon, title, path}) => (
                <RouterLink key={title} to={path} onClick={onClose}>
                  <Flex
                      gap={4}
                      px={4}
                      py={2}
                      _hover={{
                        background: "gray.subtle",
                      }}
                      alignItems="center"
                      fontSize="sm"
                  >
                    <Icon as={icon} alignSelf="center"/>
                    <Text ml={2}>{title}</Text>
                  </Flex>
                </RouterLink>
            ))}
          </Box>
      </>
  )
}

export default SidebarItems;
