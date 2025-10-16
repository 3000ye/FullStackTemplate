import {
  Box,
  Container,
  Flex,
  Heading,
  Input,
  Text,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"

import {
  type ApiError,
  UsersService, UserUpdate,
} from "@/client"
import {Button} from "@/components/ui/button";
import useAuth from "@/hooks/useAuth"
import useCustomToast from "@/hooks/useCustomToast"
import { namePattern, handleError, passwordRules } from "@/utils"
import { PasswordInput } from "../ui/password-input"

const UserInformation = () => {
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const [editMode, setEditMode] = useState(false)
  const { user: currentUser } = useAuth()
  const {
    register,
    handleSubmit,
    reset,
    formState: { isSubmitting, isDirty, errors },
  } = useForm<UserUpdate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      id: currentUser?.id,
      name: currentUser?.name,
      role: currentUser?.role,
      status: currentUser?.status,
      supervisor_id: currentUser?.supervisor_id,
      password: "******"
    },
  })

  const toggleEditMode = () => {
    if (!editMode) {
      // 开启编辑模式时，清空 password
      reset({
        id: currentUser?.id,
        name: currentUser?.name,
        role: currentUser?.role,
        status: currentUser?.status,
        supervisor_id: currentUser?.supervisor_id,
        password: "", // 清空 password
      })
    }
    setEditMode(!editMode)
  }

  const mutation = useMutation({
    mutationFn: (data: UserUpdate) =>
      UsersService.updateUserSelf({ requestBody: data }),
    onSuccess: () => {
      showSuccessToast("User updated successfully.")
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries()
    },
  })

  const onSubmit: SubmitHandler<UserUpdate> = async (data) => {
    mutation.mutate(data)
  }

  const onCancel = () => {
    reset()
    toggleEditMode()
  }

  return (
    <>
      <Container maxW="full">
        <Heading size="sm" py={4}>
          User Information
        </Heading>
        <Box
          w={{ sm: "full", md: "sm" }}
          as="form"
          onSubmit={handleSubmit(onSubmit)}
        >
          <Flex direction="column" gap={4}>
            <Flex align="center">
              <Text w="150px" fontWeight="semibold">Id</Text>
              <Text fontSize="md" py={2} truncate maxW="sm">
                {currentUser?.id}
              </Text>
            </Flex>

            <Flex align="center">
              <Text w="150px" fontWeight="semibold">Name</Text>
              {editMode ? (
                  <Input
                      {...register("name", { maxLength: 30, pattern: namePattern })}
                      type="text"
                      size="md"
                      maxW="sm"
                  />
              ) : (
                  <Text
                      fontSize="md"
                      py={2}
                      color={!currentUser?.name ? "gray" : "inherit"}
                      truncate
                      maxW="sm"
                  >
                    {currentUser?.name || "N/A"}
                  </Text>
              )}
            </Flex>

            <Flex align="center">
              <Text w="150px" fontWeight="semibold">Role</Text>
              <Text fontSize="md" py={2} truncate maxW="sm">
                {currentUser?.role}
              </Text>
            </Flex>

            <Flex align="center">
              <Text w="150px" fontWeight="semibold">Status</Text>
              <Text fontSize="md" py={2} truncate maxW="sm">
                {currentUser?.status === 1 ? "Valid" : "InValid"}
              </Text>
            </Flex>

            {currentUser?.supervisor_id && (
                <Flex align="center">
                  <Text w="150px" fontWeight="semibold">Supervisor Id</Text>
                  <Text fontSize="md" py={2} truncate maxW="sm">
                    {currentUser.supervisor_id}
                  </Text>
                </Flex>
            )}

            <Flex align="center">
              <Text w="150px" fontWeight="semibold">Password</Text>
              {editMode ? (
                  <PasswordInput
                      type="password"
                      {...register("password", passwordRules() )}
                      size="md"
                      maxW="sm"
                      placeholder="Password"
                      errors={errors}
                  />
              ) : (
                  <Text
                      fontSize="md"
                      py={2}
                      color={"inherit"}
                      truncate
                      maxW="sm"
                  >
                    { "******" }
                  </Text>
              )}
            </Flex>
          </Flex>

          <Flex mt={4} gap={3}>
            <Button
              variant="solid"
              onClick={toggleEditMode}
              type={editMode ? "button" : "submit"}
              loading={editMode ? isSubmitting : false}
              disabled={editMode ? !isDirty : false}
            >
              {editMode ? "Save" : "Edit"}
            </Button>
            {editMode && (
              <Button
                variant="subtle"
                colorPalette="gray"
                onClick={onCancel}
                disabled={isSubmitting}
              >
                Cancel
              </Button>
            )}
          </Flex>
        </Box>
      </Container>
    </>
  )
}

export default UserInformation
