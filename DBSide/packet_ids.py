#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/27 11:58
#!@File     : .py


# ---------------------用户---------------------
db_msg_query_user =                 "QueryUser"
db_msg_reg_user_by_wxinfo =         "RegByWxInfo"
db_msg_refresh_user_wxinfo =        "RefreshWxInfo"
db_msg_recommend_user =             "RecommendUser"
# db_msg_recommend_and_normal_user =  "RecommendUserAndNormal"
db_msg_query_follower =             "QueryFollower"
db_msg_query_be_follow =            "QueryBeFollow"
db_msg_query_faber =                "QueryFaber"
db_msg_query_be_fab =               "QueryBeFab"
db_msg_set_user_info =              "SetUserInfo"

# ---------------------内容---------------------
db_msg_recommend_content =          "RecommendContent"
db_msg_query_content =              "QueryContent"
db_msg_query_content_with_name_tag ="QueryContentWithName"
db_msg_query_content_with_tag_id_list = "QueryContentWithTagIdList"
db_msg_new_content =                "NewContent"
db_msg_update_content =             "UpdateContent"
db_msg_del_content =                "DelContent"
db_msg_get_follow_content =         "GetFollowContent"
db_msg_get_content_by_uid_list =    "GetContentByUidList"



# ---------------------分表---------------------
db_msg_create_content_table =       "CreateContTbl"
db_msg_create_message_table =       "CreateMsgTbl"
db_msg_create_imgurl_table =        "CreateImgUrlTbl"
db_msg_create_fab_table =           "CreateFabTbl"

# ---------------------消息---------------------
db_msg_query_message =              "QueryMessage"
db_msg_new_message =                "NewMessage"
db_msg_del_message =                "UpdateMessage"
db_msg_query_message_by_cid_list =  "QueryMessageByCidList"
db_msg_query_relpy_message =        "QueryRelpyMsgByCid"

# ----------------------赞----------------------
db_msg_query_fabulous =             "QueryFabulous"
db_msg_new_fabulous =               "NewFabulous"
db_msg_update_fabulous =            "UpdateFabulous"
db_msg_get_be_fab_info =               "GetFabInfo"

# ---------------------关注---------------------
db_msg_query_follow =               "QueryFollow"
db_msg_query_follow_by_id_list =    "QueryFollowByIdList"
db_msg_new_follow =                 "NewFollow"
db_msg_update_follow =              "UpdateFollow"

db_msg_get_friend_list =            "GetFriendList"
# db_msg_get_be_follow_and_be_fab =   "GetBeFolAndBeFab"
db_msg_get_be_follow_and_be_fab_and_msg =   "GetBeFolAndBeFabAndMsg"

# ---------------------Tag----------------------
db_msg_query_tag_by_id_list_str =   "QueryTagByIdList"
db_msg_query_tag =                  "QueryTag"


# ---------------------AliossCache----------------------
db_msg_del_aliosscache =   "DelAliossCache"
db_msg_new_aliosscache =   "NewAliossCache"
