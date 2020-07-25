# -*- coding: utf-8 -*-
"""
根据文件名发送该文件到微信群
"""
from lxml import etree
import os
import re

from PyWeChatSpy import WeChatSpy


chatroom_id_list = ['22071979677@chatroom', '5144330951@chatroom']

content_pattern = r'@计算机科学与技术—关茂柠'

contact_dict = {}

# 获取文件的名字
SAVED_FILES_DIR = r'D:\WeChat_Files_PDF'  # 合并后保存的路径
files = []
all_files_name = os.listdir(SAVED_FILES_DIR)  # 读取文件夹下的所有文件名
for file_name in all_files_name:
    if file_name.endswith('.pdf'):  # 判断是否为PDF文件名
        student_number = file_name.strip('.pdf')

        file = {
            'number': student_number,
            'file_name': file_name,
        }
        files.append(file)


def parser(data):
    if data["type"] == 1:
        # 登录信息
        print(data)
        # 查询联系人列表
        import time
        time.sleep(5)
        spy.query_contact_list()
    elif data["type"] == 203:
        # 微信登出
        print("微信退出登录")
    elif data["type"] == 5:
        # 消息
        for item in data["data"]:
            print(item)
            if item["msg_type"] == 37:
                # 好友请求消息
                obj = etree.XML(item["content"])
                encryptusername, ticket = obj.xpath("/msg/@encryptusername")[0], obj.xpath("/msg/@ticket")[0]
                # spy.accept_new_contact(encryptusername, ticket)
            elif item["wxid1"] == "filehelper":
                spy.uninject()

            # 微信群消息
            elif item.get('wxid2'):
                chatroom_id = item.get('wxid1')  # 群id
                member_id = item.get('wxid2')  # 群成员id
                if chatroom_id in chatroom_id_list:
                    content = item.get('content')
                    try:
                        result = re.search(content_pattern, content)
                        if result:
                            student_number = content.replace(content_pattern, '')
                            student_number = student_number.replace(r'\u2005', '')
                            student_number = student_number.strip()
                            file_exist_flag = 0
                            file_path = ''
                            for file_info in files:
                                if student_number == file_info.get('number'):
                                    file_path = os.path.join(SAVED_FILES_DIR, file_info.get('file_name'))
                                    file_exist_flag = 1
                                    break
                            if file_exist_flag == 1:
                                spy.send_file(chatroom_id, file_path)
                                # spy.send_text(chatroom_id, content='', at_wxid=member_id)
                            elif file_exist_flag == 0:
                                pass
                            # spy.send_text(chatroom_id, content='该学号不存在[旺柴]', at_wxid=member_id)
                    except:
                        print('非文本信息。')

    elif data["type"] == 2:
        # 联系人详情
        print(data)
    elif data["type"] == 3:
        # 联系人列表
        for contact in data["data"]:
            print(contact)
    elif data["type"] == 9527:
        spy.logger.warning(data)


if __name__ == '__main__':
    spy = WeChatSpy(parser=parser, key="18d421169d93611a5584affac335e690")
    spy.run()
