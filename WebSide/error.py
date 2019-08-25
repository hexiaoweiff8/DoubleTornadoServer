#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/27 15:27
#!@File     : .py

ERR_NO_ERR                  = 0
ERR_INVALID_MSGID           = 1001      # 非法消息ID
ERR_CODE_EXCEPTION          = 1002      # 代码错误
ERR_DB_OPERATION_FAIL       = 1003      # 数据操作失败
ERR_NOT_IN_ALLOWED          = 1004      # 操作不被允许
ERR_PREAM_ERR               = 1005      # 参数错误
ERR_DOUBLE_REQUEST_ERR      = 1006      # 重复请求
ERR_NO_LOGIN                = 1007      # 未登录


ERR_USER_NOT_EXIST = 1                  # 用户不存在
ERR_USERNAME_OR_PWD_IS_EMPTY = 2        # 用户名或密码为空
ERR_OPENID_EXIST = 3                    # openId已注册
ERR_CONTENT_NOT_EXIST = 4               # 内容不存在
ERR_MSG_NOT_EXIST = 5                   # 消息不存在
ERR_FOLLOW_NOT_EXIST = 6                # 关注关系不存在
ERR_FAB_NOT_EXIST = 7                   # 赞不存在
ERR_TAG_NOT_EXIST = 8                   # 标签不存在
ERR_WX_ERROR = 9                        # 微信信息非法
ERR_FAB_EXIST = 10                      # 已经赞过
ERR_IS_SEALED = 11                      # 已被封号
ERR_COULD_FOLLOW_SELF = 12              # 不能关注自己
ERR_PUBLISH_SO_FAST = 13                # 发布过于频繁

