import { createFileRoute } from '@tanstack/react-router'
import {Blockquote, Container, Heading, List, Stack, Text} from "@chakra-ui/react";
import {LuCircleCheck, LuCircleDashed} from "react-icons/lu";

export const Route = createFileRoute('/_layout/release')({
  component: RouteComponent,
})

function Version_0_0_1() {
  return (
      <>
        <Stack gap="5" align="flex-start">
          <Stack align="center" direction="row" gap="8" px="4" width="full">
            <Text color="#5C6FB2" fontSize="2xl" fontWeight="bold" w="40">Version 0.0.1</Text>
            <Blockquote.Root variant="subtle" colorPalette="purple">
              <Blockquote.Content cite="Castor">
                <List.Root gap="2" variant="plain" align="center">
                  <List.Item>
                    <List.Indicator asChild color="#5C6FB2">
                      <LuCircleCheck />
                    </List.Indicator>
                    前端框架主体搭建，登录校验
                  </List.Item>
                  <List.Item>
                    <List.Indicator asChild color="#5C6FB2">
                      <LuCircleCheck />
                    </List.Indicator>
                    产品列表与产品主页面
                  </List.Item>
                  <List.Item>
                    <List.Indicator asChild color="#5C6FB2">
                      <LuCircleCheck />
                    </List.Indicator>
                    产品信息更新与月度报告生成，并支持导出为 PNG 与 PDF
                  </List.Item>
                  <List.Item>
                    <List.Indicator asChild color="#5C6FB2">
                      <LuCircleDashed />
                    </List.Indicator>
                    用户权限系统与操作行为记录
                  </List.Item>
                </List.Root>
              </Blockquote.Content>
              <Blockquote.Caption>
                —— <cite>Castor 2025-06-17</cite>
              </Blockquote.Caption>
            </Blockquote.Root>
          </Stack>
        </Stack>
      </>
  )
}

function Version_0_0_2() {
  return (
      <>
        <Stack gap="5" align="flex-start" mb={4}>
          <Stack align="center" direction="row" gap="8" px="4" width="full">
            <Text color="#5C6FB2" fontSize="2xl" fontWeight="bold" w="40">Version 0.0.2</Text>
            <Blockquote.Root variant="subtle" colorPalette="purple">
              <Blockquote.Content cite="Castor">
                <List.Root gap="2" variant="plain" align="center">
                  <List.Item>
                    <List.Indicator asChild color="#5C6FB2">
                      <LuCircleCheck />
                    </List.Indicator>
                    周度报告与季度报告生成，并支持导出为 PNG 与 PDF
                  </List.Item>
                  <List.Item>
                    <List.Indicator asChild color="#5C6FB2">
                      <LuCircleCheck />
                    </List.Indicator>
                    多产品报告 DEMO 实现，后端开发完成
                  </List.Item>
                  <List.Item>
                    <List.Indicator asChild color="#5C6FB2">
                      <LuCircleDashed />
                    </List.Indicator>
                    多产品报告生成，支持时间维度的选择，导出为 PNG 与 PDF
                  </List.Item>
                  <List.Item>
                    <List.Indicator asChild color="#5C6FB2">
                      <LuCircleDashed />
                    </List.Indicator>
                    用户权限系统与操作行为记录
                  </List.Item>
                </List.Root>
              </Blockquote.Content>
              <Blockquote.Caption>
                —— <cite>Castor 2025-07-14</cite>
              </Blockquote.Caption>
            </Blockquote.Root>
          </Stack>
        </Stack>
      </>
  )
}


function RouteComponent() {
  return (
      <>
        <Container maxW="full">
          <Heading px="4" mt="20" mb="4" size="4xl" color="#5C6FB2">Data Vista Releases</Heading>
          <Version_0_0_2 />
          <Version_0_0_1 />
        </Container>
      </>
  )
}
