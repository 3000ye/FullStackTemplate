import { createFileRoute } from '@tanstack/react-router';
import { Container } from '@chakra-ui/react';
import { Select } from "chakra-react-select";
import { useState } from "react";

const options = [
  { label: "苹果", value: "apple" },
  { label: "香蕉", value: "banana" },
  { label: "葡萄", value: "grape" },
  { label: "橘子", value: "orange" },
];

function TestCard() {
  const [selected, setSelected] = useState<any>(null);

  return (
      <Container maxW="1280px">
        <Select
            options={options}
            placeholder="请选择或输入..."
            isClearable
            isSearchable
            value={selected}
            onChange={(option) => {
              setSelected(option);
              console.log("选中内容:", option);
            }}
        />
      </Container>
  );
}

// 路由绑定
export const Route = createFileRoute('/_test/test_card')({
  component: TestCard,
});
export default TestCard;
