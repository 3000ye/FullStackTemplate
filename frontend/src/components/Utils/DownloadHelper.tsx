import {toPng} from "html-to-image";
import jsPDF from "jspdf";
import {RefObject} from "react";

export const handleDownload = (reportRef: RefObject<HTMLDivElement|null>, filename: string|null) => {
  // 使用 ref 来获取元素，而不是 document.getElementById
  const reportElement = reportRef.current;
  if (!reportElement) {
    console.log("报告元素未找到。请确保 ReportDisplay 组件已正确渲染。");
    // 可以添加一个用户可见的提示，例如 Chakra Toast
    return;
  }

  // 使用 html-to-image 的 toPng 函数
  toPng(reportElement, {
    cacheBust: true, // 避免缓存问题
    quality: 1, // 图片质量 (0-1)
    pixelRatio: 10, // 提高分辨率，相当于 html2canvas 的 scale
    backgroundColor: '#FAFAFA' // 如果你想为生成的图片设置一个背景色
  }).then((dataUrl) => {
    const link = document.createElement('a');
    link.download = `report-${filename}.png`; // 设置下载的文件名
    link.href = dataUrl;
    document.body.appendChild(link); // 临时将链接添加到 DOM
    link.click(); // 触发点击下载
    document.body.removeChild(link); // 移除临时链接
  }).catch((err) => {
    console.error("下载失败:", err);
    // 可以添加一个用户可见的错误提示
  });
};

export const handleDownloadPdf = async (reportRef: RefObject<HTMLDivElement|null>, filename: string|null) => {
  const reportElement = reportRef.current;
  if (!reportElement) {
    console.log("报告元素未找到。请确保 ReportDisplay 组件已正确渲染。");
    return;
  }

  try {
    const dataUrl = await toPng(reportElement, {
      cacheBust: true,
      quality: 1,
      pixelRatio: 10,
      backgroundColor: '#FFFFFF'
    });

    const img = new Image();
    img.src = dataUrl;

    img.onload = () => {
      const imgWidthPx = img.width;
      const imgHeightPx = img.height;

      // 转换像素为 mm，假设 96 dpi
      const pxToMm = (px: number) => (px * 25.4) / 96;
      const pdfWidthMm = pxToMm(imgWidthPx);
      const pdfHeightMm = pxToMm(imgHeightPx);

      // 创建自定义尺寸的 PDF（和图片一样大）
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: [pdfWidthMm, pdfHeightMm],
      });

      // 直接放入图片，不缩放、不分页
      pdf.addImage(dataUrl, 'PNG', 0, 0, pdfWidthMm, pdfHeightMm);
      pdf.save(`report-${filename}.pdf`);
    };
  } catch (err) {
    console.error("下载 PDF 失败:", err);
    // 可以添加 Chakra Toast 错误提示
  }
};
