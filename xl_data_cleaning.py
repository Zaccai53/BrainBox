import json
import re
import csv


def clean_content(content):
    # 清洗拍一拍消息
    if "tickled" in content:
        return None
    # 清洗表情包消息
    if "<emoji" in content:
        return None
    # 清洗撤回消息
    if "撤回了一条消息" in content:
        return None
    # 清洗其他非文本内容
    content = re.sub(r"<.*?>", "", content)  # 移除HTML标签
    content = re.sub(r"\[.*?\]", "", content)  # 移除表情符号
    return content.strip()


def parse_invite_message(content, nick_name, str_time):
    # 提取邀请消息中的邀请者和被邀请者
    match = re.search(r"(.*) invited (.*) to the group chat", content)
    if match:
        inviter = match.group(1).strip()
        invitee = match.group(2).strip()
        return {
            "Type": "Invite",
            "Inviter": inviter,
            "Invitee": invitee,
            "Date": str_time
        }
    return None


def parse_image_message(content, nick_name, str_time):
    # 提取图片链接
    match = re.search(r'cdnthumburl="(.*?)"', content)
    if match:
        image_url = match.group(1)
        return {
            "Type": "Image",
            "NickName": nick_name,
            "Date": str_time,
            "ImageUrl": image_url
        }
    return None


def process_wechat_records(file_path):
    all_messages = []  # 用于存储所有消息（包括普通消息、邀请消息和图片消息）

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            # 解析每一行数据
            local_id, talker_id, msg_type, sub_type, is_sender, create_time, status, str_content, str_time, remark, nick_name, sender = row

            # 检测是否为邀请消息
            if "invited" in str_content:
                invite_message = parse_invite_message(str_content, nick_name, str_time)
                if invite_message:
                    all_messages.append(invite_message)
            # 检测是否为图片消息
            elif "<img" in str_content:
                image_message = parse_image_message(str_content, nick_name, str_time)
                if image_message:
                    all_messages.append(image_message)
            else:
                # 清洗普通消息内容
                cleaned_content = clean_content(str_content)
                if cleaned_content:
                    # 构造普通消息的JSON格式
                    entry = {
                        "Type": "Normal",
                        "NickName": nick_name,
                        "Date": str_time,
                        "Content": cleaned_content
                    }
                    all_messages.append(entry)

    return all_messages


def save_to_json(data, output_file):
    with open(output_file, mode="w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# 主程序
if __name__ == "__main__":
    input_file = r" "  # 输入文件路径
    output_file = r" "  # 输出文件路径

    # 处理微信记录
    all_messages = process_wechat_records(input_file)

    # 保存为JSON文件
    save_to_json(all_messages, output_file)

    print(f"处理完成，结果已保存到 {output_file}")