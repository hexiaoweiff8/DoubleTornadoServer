#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/21 14:52
#!@File     : .py

import handler
import packet_ids


REQUEST_HEANDLERS = {}

def init_request_handlers():
    global REQUEST_HANDLERS
    REQUEST_HANDLERS = {

        # ----------------用户-------------------
        packet_ids.db_msg_query_user:               handler.query_user,             # 查询用户
        packet_ids.db_msg_reg_user_by_wxinfo:       handler.reg_user_by_wxinfo,     # 注册微信用户
        packet_ids.db_msg_refresh_user_wxinfo:      handler.refresh_user_wxinfo,    # 刷新用户微信信息
        packet_ids.db_msg_query_follower:           handler.query_follower,         # 查询关注用户
        packet_ids.db_msg_query_be_follow:          handler.query_be_follow,        # 查询被关注用户
        packet_ids.db_msg_query_faber:              handler.query_faber,            # 查询我赞过用户
        packet_ids.db_msg_query_be_fab:             handler.query_be_fab,           # 查询赞过我的用户
        packet_ids.db_msg_recommend_user:           handler.recommend_user,         # 查询推荐用户
        # packet_ids.db_msg_recommend_and_normal_user: handler.recommend_and_normal_user, # 推荐用户与常规用户
        packet_ids.db_msg_set_user_info:            handler.set_user_info,          # 设置用户数据
        # ----------------内容-------------------
        packet_ids.db_msg_recommend_content:        handler.recomment_content,      # 获取推荐内容
        packet_ids.db_msg_query_content_with_name_tag: handler.query_content_with_name_tag,  # 名称模糊查询内容
        packet_ids.db_msg_query_content_with_tag_id_list: handler.query_content_with_tag_id_list,
        packet_ids.db_msg_new_content:              handler.new_content,            # 创建新内容
        # packet_ids.db_msg_recommend_and_normal_content: handler.recomment_and_normal_content,
        packet_ids.db_msg_update_content:           handler.update_content,         # 更新内容
        packet_ids.db_msg_del_content:              handler.del_content,            # 删除内容
        packet_ids.db_msg_query_content:            handler.query_content,
        packet_ids.db_msg_get_follow_content:       handler.get_follow_content,     # 获取关注内容列表
        packet_ids.db_msg_get_content_by_uid_list:  handler.query_content_by_list,  # list条件查询
        # ----------------分表-------------------
        packet_ids.db_msg_create_content_table:     handler.create_content_table,   # 创建内容表
        packet_ids.db_msg_create_message_table:     handler.create_message_table,   # 创建消息表
        packet_ids.db_msg_create_fab_table:         handler.create_fabulous_table,  # 创建赞表

        # ----------------消息-------------------
        packet_ids.db_msg_query_message:            handler.query_message,          # 查询消息
        packet_ids.db_msg_new_message:              handler.new_message,            # 添加消息
        packet_ids.db_msg_del_message:              handler.del_message,            # 删除消息
        packet_ids.db_msg_query_message_by_cid_list: handler.query_message_by_cid_list,  # 内容id列表查询消息
        packet_ids.db_msg_query_relpy_message:      handler.query_relpy_message,
        # ----------------关注-------------------
        packet_ids.db_msg_query_follow:             handler.query_follow,           # 查询关注
        packet_ids.db_msg_query_follow_by_id_list:  handler.query_follow_by_id_list, # id列表查询关注
        packet_ids.db_msg_new_follow:               handler.new_follow,             # 新关注
        packet_ids.db_msg_update_follow:            handler.update_follow,          # 修改关注
        packet_ids.db_msg_get_friend_list:          handler.get_friend_list,
        # packet_ids.db_msg_get_be_follow_and_be_fab: handler.get_be_follow_and_be_fab_user,
        packet_ids.db_msg_get_be_follow_and_be_fab_and_msg: handler.get_be_follow_and_be_fab_and_msg_user,
        # -----------------赞--------------------
        packet_ids.db_msg_query_fabulous:           handler.query_fabulous,         # 查询赞
        packet_ids.db_msg_new_fabulous:             handler.new_fabulous,           # 新赞
        packet_ids.db_msg_update_fabulous:          handler.update_fabulous,        # 修改赞
        packet_ids.db_msg_get_be_fab_info:          handler.get_be_fab_info,        # 获取赞过我的信息
        # -----------------Tag-------------------
        packet_ids.db_msg_query_tag_by_id_list_str: handler.query_tag_by_id_list,   # id列表查询tag
        packet_ids.db_msg_query_tag:                handler.query_tag,              # id查询tag

        # -----------------阿里OSS缓存-------------------
        packet_ids.db_msg_new_aliosscache:          handler.new_aliosscache,        # 添加缓存
        packet_ids.db_msg_del_aliosscache:          handler.del_aliosscache,        # 删除缓存
    }
