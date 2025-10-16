import requests
from typing import Optional

custom_red = "#b30000"
custom_green = "#00b300"

color_dict = {
    "red": custom_red,
    "green": custom_green,
}


def post_text_msg(webhook, title: Optional[str], msg: str, to: Optional[dict[str, list[str]]] = None) -> None:
    if to is None:
        to = {}
    # mod by CF, replace '\n' with '\n\n' for better display on ios dingding app
    msg = msg.replace('\n', '\n\n')
    headers = { "Content-Type": "application/json" }
    at_users = [f"@{phone}" for phone in to.get("atMobiles", []) if phone]

    text = f"""{title}
{msg}
{" ".join(at_users)}
"""

    para = {
        "msgtype": "text",
        "text": {
            "content": text
        },
        "at": {
            "atMobiles": to.get("atMobiles", []) if to else [],
            "atUserIds": to.get("atUserIds", []) if to else [],
            "isAtAll": False
        }
    }
    requests.post(webhook, json=para, headers=headers)


def post_msg(webhook, title: Optional[str], msg: str, to: Optional[dict[str, list[str]]] = None, color = "green") -> None:
    if to is None:
        to = {}
    # mod by CF, replace '\n' with '\n\n' for better display on ios dingding app
    msg = msg.replace('\n', '\n\n')
    headers = { "Content-Type": "application/json" }
    at_users = [f"@{phone}" for phone in to.get("atMobiles", []) if phone]

    text = f"""## <font color={color_dict[color]}>{title}</font>
{msg}
"""

    if at_users:
        text += "\n\n" + " ".join(at_users)

    para = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        },
        "at": {
            "atMobiles": to.get("atMobiles", []) if to else [],
            "atUserIds": to.get("atUserIds", []) if to else [],
            "isAtAll": False
        }
    }
    requests.post(webhook, json=para, headers=headers)

def post_at_someone(webhook, to: Optional[dict[str, list[str]]] = None) -> None:
    if to is None:
        to = {}

    headers = { "Content-Type": "application/json" }
    at_users = [f"@{phone}" for phone in to.get("atMobiles", []) if phone]
    text = " ".join(at_users)

    para = {
        "msgtype": "text",
        "text": {
            "content": "福灵 robot: " + text
        },
        "at": {
            "atMobiles": to.get("atMobiles", []) if to else [],
            "atUserIds": to.get("atUserIds", []) if to else [],
            "isAtAll": False
        }
    }
    requests.post(webhook, json=para, headers=headers)
