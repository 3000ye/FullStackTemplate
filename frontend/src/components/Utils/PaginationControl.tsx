import { Flex } from "@chakra-ui/react"
import {
    PaginationItems,
    PaginationNextTrigger,
    PaginationPrevTrigger,
    PaginationRoot,
} from "../ui/pagination"

interface PaginationControlProps {
    count: number
    pageSize: number
    onPageChange: (page: number) => void
}

export function PaginationControl({ count, pageSize, onPageChange }: PaginationControlProps) {
    return (
        <Flex justifyContent="flex-end" mt={4}>
            <PaginationRoot count={count} pageSize={pageSize} onPageChange={({ page }) => onPageChange(page)}>
                <Flex>
                    <PaginationPrevTrigger />
                    <PaginationItems />
                    <PaginationNextTrigger />
                </Flex>
            </PaginationRoot>
        </Flex>
    )
}
