import { Table } from "@chakra-ui/react"

interface SortableTableHeaderProps {
    label: string
    field?: string
    currentSortField?: string
    currentSortOrder?: "asc" | "desc"
    onSort?: (field: string) => void
}

export function SortableTableHeader({
                                        label,
                                        field,
                                        currentSortField,
                                        currentSortOrder,
                                        onSort,
                                    }: SortableTableHeaderProps) {
    const isActive = currentSortField === field

    const renderSortIcon = () => {
        if (!isActive) return ""
        return currentSortOrder === "asc" ? "↑" : "↓"
    }

    return (
        <Table.ColumnHeader
            onClick={field && onSort ? () => onSort(field) : undefined}
            className={field ? "cursor-pointer" : ""}
            _hover={field ? { bg: "gray.100" } : undefined}
            transition="background-color 0.2s ease"
        >
            {label} {field ? renderSortIcon() : ""}
        </Table.ColumnHeader>
    )
}
