import {
  DialogRoot,
  DialogTrigger,
  DialogContent,
  DialogBody,
  DialogCloseTrigger, DialogHeader, DialogTitle
} from "../ui/dialog"
import { Button } from "../ui/button" // 使用你的 Button 封装
import type { ButtonProps } from "../ui/button"


interface CenterDialogProps {
  triggerText?: string
  titleText?: string
  contentText?: string
  triggerButtonProps?: ButtonProps
}

const CenterDialog = ({
                        triggerText = "点击按钮",
                        titleText = "敬请期待",
                        contentText = "此功能正在开发中，期待在之后的版本与您见面！",
                        triggerButtonProps,
                      }: CenterDialogProps) => {
  return (
      <DialogRoot placement="center" motionPreset="slide-in-bottom">
        <DialogTrigger asChild>
          <Button {...triggerButtonProps}>
            {triggerText}
          </Button>
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{ titleText }</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <p>{contentText}</p>
          </DialogBody>
          <DialogCloseTrigger />
        </DialogContent>
      </DialogRoot>
  )
}

export default CenterDialog
