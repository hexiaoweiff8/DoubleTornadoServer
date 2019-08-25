#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/27 11:04
#!@File     : .py



"""
redis中玩家信息前缀
"""
rkeyPrefix = 'role#'



'''
分页每页内容数量
'''
PageCount = 13

'''
推荐用户缓存时间单位秒
'''
RecommendUserTime = 60

'''
推荐内容缓存时间单位秒
'''
RecommendContentTime = 60
'''
消息缓存时间
'''
MessageTime = 60

'''
发布时间间隔
'''
PublishContentTimeGap = 60

'''
推荐内容redis key
'''
RecommendContentRedisKey = 'recommendContent'

'''
内容缓存redis key
'''
ContentCacheRedisKey = 'contentCache'

'''
推荐内容缓存时间redis key
'''
RecommendContentTimeRedisKey = 'recommendContentTime'

'''
内容缓存时间redis key
'''
ContentCacheTimeRedisKey = 'ContentTime'

'''
推荐用户redis key
'''
RecommendUserRedisKey = 'recommendUser'

'''
推荐用户缓存时间redis key
'''
RecommendUserTimeRedisKey = 'recommendUserTime'

'''
用户redis key
'''
UserRedisKey = 'recommendUser'

'''
用户缓存时间redis key
'''
UserTimeRedisKey = 'recommendUserTime'

'''
openId影射UserId
'''
OpenIdMappingUserIdKey = 'openIdMappingUserId'

'''
tag缓存key
'''
TagRedisKey = 'tagRedisKey'

'''
tag缓存时间key
'''
TagTimeRedisKey = 'tagTimeRedisKey'


'''
kol缓存key
'''
KolUserRedisKey = 'kolUserRedisKey'

'''
kol缓存时间
'''
KolUserTimeRedisKey = 'kolUserTimeRedisKey'


'''
消息缓存key
'''
MessageCacheRedisKey = 'messageCacheRedisKey'

'''
消息时间缓存key
'''
MessageCacheTimeRedisKey = 'messageCacheTimeRedisKey'


'''
查看次数缓存key
'''
ViewCountRedisKey = 'viewCountRedisKey'

'''
点赞次数缓存key
'''
FabCountRedisKey = 'fabCountRedisKey'





'''
微信获取openId地址
'''
WXCodeToOpenId = 'https://api.weixin.qq.com/sns/jscode2session?grant_type=authorization_code&'

'''
微信获取Token地址
'''
WXAccessToken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&'

'''
缓存Token的key
'''
CacheWXAccessTokenKey = 'cacheToken'

'''
缓存时间key
'''
CacheWXAccessTokenTime = 'cacheTime'

'''
微信小程序appId
'''
WXAppId = 'wxdd05a9733d0677b3'

'''
微信小程序密钥
'''
WXAppSecret = '7ec7eaa629e639fadb4c520098e73817'

'''
防刷排除列表1
'''
PoofExpectList = ['/getOSSToken/', '/auth/loginWithWX/', '/ali-oss-back/', '/ali-oss-back','api_action']



############################################## API 相关 ##################################

'''
API 请求Token
'''
APIToken = 'qcSfl8y5dMId3xPJW_BTqouB_cBxBQck'

'''
API 信任IP
'''
APITrustIPList = ['::1','127.0.0.1','localhost']

'''
API 请求过期时间
'''
APIExpire = 30 
