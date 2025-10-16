import {Breadcrumb, Stack} from "@chakra-ui/react"


interface PageLinkProps {
  headText?: string
  headUrl?: string
  bodyText?: string
}

const PageLink = ({
                    headText = "Header",
                    headUrl = "",
                    bodyText = "Body",
                  }: PageLinkProps) => {
  return (
      <Stack mb={4}>
        <Breadcrumb.Root size={'md'}>
          <Breadcrumb.List>
            <Breadcrumb.Item>
              <Breadcrumb.Link href={headUrl}>{headText}</Breadcrumb.Link>
            </Breadcrumb.Item>
            <Breadcrumb.Separator/>
            <Breadcrumb.Item>
              <Breadcrumb.CurrentLink>{bodyText}</Breadcrumb.CurrentLink>
            </Breadcrumb.Item>
          </Breadcrumb.List>
        </Breadcrumb.Root>
      </Stack>
  )
}

export default PageLink
