lang = {}
TC = {
    # msg
    'lang': "切換為繁體中文",
    # run
    'read_readme': "!!使用前請仔細閱讀README.md!!  !!使用前請仔細閱讀README.md!!\n\n!!使用前請仔細閱讀README.md!!  "
                   "!使用前請仔細閱讀README.md!!\n\n!!使用前請仔細閱讀README.md!!  !!使用前請仔細閱讀README.md!!\n\n",
    'agree_terms': "是否以仔細閱讀且同意README.md中敘述事物\n如果兩者回答皆為\"是\"，請輸入英文 \"yes\" 後按Enter建，如果不同意請關閉此程式\n",
    'not_login_pl_login': "未登入，請先登入",
    'input_correct_var': "請輸入正確的參數",
    'login_success_user': "登錄成功, 用戶暱稱為: ",
    'error_response': "Error: ",
    'picked_shelf_s': "選擇書架: \"",
    'picked_shelf_e': "\"",
    'not_picked_shelf': "未選擇書架",
    'check_in_success_got': "簽到成功, 獲得: ",
    'check_in_xp': " 經驗, ",
    'check_in_token': " 代幣, ",
    'check_in_recommend': " 推薦票\n",
    'check_in_no_redo': "任務已完成，請勿重複簽到\n",
    'check_in_failed': "簽到失敗:\n",
    'check_in_already': "已簽到\n",
    'check_in_token_failed': "登入過期或失效，自動嘗試重新登入",
    'check_in_re_login_retry_check_in': "成功重新登入，再次執行簽到",
    'check_in_error_1': "簽到失敗，特殊原因，請手動處理:\n",
    'check_in_re_login_failed': "重新登入失敗，請手動處理\n",
    'check_in_error_2': "簽到失敗，特殊原因，請手動處理:\n",
    'check_in_error_day_not_found': "日期異常，未找本日對應簽到記錄，不進行簽到嘗試，可能是因為裝置時間不準確\n",
    'failed_get_book_info_index': "獲取書籍信息失敗, shelf_index:",
    'failed_get_book_info_id': "獲取書籍信息失敗, book_id:",
    'not_picked_book': "未選擇書籍",
    'start_book_dl': "開始下載書籍...\n",
    # shelf
    'shelf_index': "書架编號:",
    'shelf_name': ", 書架名:",
    'show_list_author': "》作者:",
    'show_list_book_index': "\n書籍编號:",
    'show_list_book_id': ", 書籍ID:",
    'show_list_uptime': "更新時間:",
    'show_list_last_chap': "\n最新章節:",
    # book
    'show_div_index': "分卷編號:",
    'show_div_total': " 共:",
    'show_div_name': " 章 分卷名: ",
    'failed_get_chap': "章節獲取失敗: ",
    'get_div': "正在獲取書籍分卷...",
    'failed_get_div': "分捲獲取失敗: ",
    'show_last_chap_s_index': "  最新章節, 編號: ",
    'show_last_chap_uptime': ", 更新時間:",
    'show_last_chap_name': "\n  章節:",
    'show_chap_list_index': "分卷:",
    'dl_chap_block_e': ".xhtml，章節屏蔽無法下載，以空檔案標記。\n",
    'dl_chap_block_c': ".xhtml，章節屏蔽無法下載，使用本地檔案。\n",
    'dl_chap_not_paid': "，該章節未訂閱無法下載。\n",
    'dl_fin': "\n\n下載完畢",
    'expo_s': "匯出書籍...",
    'expo_e': "匯出完成...\n\n",
    'expo_no': "書籍無更新...\n\n",
    'dl_0_chap_re_dl': ".xhtml，發現缺失章節(空檔案)，重新下載。\n",
    'dl_error_paid_stat_conflict': "，錯誤，該章節訂授權態異常無法下載，請再次嘗試下載。!!!!!\n",
    'dl_error_chap_get_failed_1': ".xhtml，錯誤，章節下載異常，請重新嘗試下載，章節缺失以空檔案標記!!!!!\n",
    'dl_error_chap_get_failed_2': ".xhtml，錯誤，章節下載異常，請重新嘗試下載!!!!!\n",
    # epub
    'cover_dl_rt': "下載封面圖片失敗，重試: ",
    'cover_dl_f': "下載封面圖片失敗，放棄: ",
    'image_dl_rt': "下載圖片失敗，重試: ",
    'image_dl_f': "下載圖片失敗，放棄: ",
    # help
    'help_msg': """HbookerAppNovelDownloader 刺蝟貓 / 歡樂書客 小說下載器
請閱讀README.md
指令(指令輸入字首即可):
h | help\t\t\t\t\t\t--- 顯示說明 (此訊息)
m | message\t\t\t\t\t\t--- 切換提示訊息 (繁體/簡體)
q | quit\t\t\t\t\t\t--- 退出腳本
l | login <手機號/郵箱/用戶名> <密碼>\t\t\t--- 登錄歡樂書客帳號
t | task\t\t\t\t\t\t--- 執行每日簽到，領代幣 (啟動時自動執行，無異常不需再次執行)
s | shelf\t\t\t\t\t\t--- 刷新並顯示當前書架列表 (啟動時會自動刷新1次)
s <書架編號> | shelf <書架編號>\t\t\t\t--- 選擇與切換書架
b | book\t\t\t\t\t\t--- 刷新並顯示當前書架的書籍列表
b <書籍編號/書籍ID> | book <書籍編號/書籍ID>\t\t--- 選擇書籍
d | download\t\t\t\t\t\t--- 下載當前書籍(book時選擇的書籍)
d <書籍編號/書籍ID> | download <書籍編號/書籍ID>\t--- 下載指定ID書籍
ds <書架編號> | downloadshelf <書架編號> \t\t--- 下載整個書架
u | update\t\t\t\t\t\t--- 下載"list.txt"書單之中所列書籍
u <path.txt> | update <path.txt>\t\t\t--- 下載指定書單中所列書籍
"""
}
# 下載指定檔案"list_path.txt"中的所有書籍
SC = {
    # msg
    'lang': "切换为简体中文",
    # run
    'read_readme': "!!使用前请仔细阅读README.md!!  !!使用前请仔细阅读README.md!!\n\n!!使用前请仔细阅读README.md!!  "
                   "!使用前请仔细阅读README.md!!\n\n!!使用前请仔细阅读README.md!!  !!使用前请仔细阅读README.md!!\n\n",
    'agree_terms': "是否以仔细阅读且同意README.md中叙述事物\n如果两者回答皆为\"是\"，请输入英文 \"yes\" 后按Enter建，如果不同意请关闭此程式\n",
    'not_login_pl_login': "未登入，请先登入",
    'input_correct_var': "请输入正确的参数",
    'login_success_user': "登录成功, 用户暱称为: ",
    'error_response': "Error: ",
    'picked_shelf_s': "选择书架: \"",
    'picked_shelf_e': "\"",
    'not_picked_shelf': "未选择书架",
    'check_in_success_got': "签到成功, 获得: ",
    'check_in_xp': " 经验, ",
    'check_in_token': " 代币, ",
    'check_in_recommend': " 推荐票\n",
    'check_in_no_redo': "任务已完成，请勿重複签到\n",
    'check_in_failed': "签到失败:\n",
    'check_in_already': "已签到\n",
    'check_in_token_failed': "登入过期或失效，自动尝试重新登入",
    'check_in_re_login_retry_check_in': "成功重新登入，再次执行签到",
    'check_in_error_1': "签到失败，特殊原因，请手动处理:\n",
    'check_in_re_login_failed': "重新登入失败，请手动处理\n",
    'check_in_error_2': "签到失败，特殊原因，请手动处理:\n",
    'check_in_error_day_not_found': "日期异常，未找本日对应签到记录，不进行签到尝试，可能是因为装置时间不准确\n",
    'failed_get_book_info_index': "获取书籍信息失败, shelf_index:",
    'failed_get_book_info_id': "获取书籍信息失败, book_id:",
    'not_picked_book': "未选择书籍",
    'start_book_dl': "开始下载书籍...\n",
    # shelf
    'shelf_index': "书架编号:",
    'shelf_name': ", 书架名:",
    'show_list_author': "》作者:",
    'show_list_book_index': "\n书籍编号:",
    'show_list_book_id': ", 书籍ID:",
    'show_list_uptime': "更新时间:",
    'show_list_last_chap': "\n最新章节:",
    # book
    'show_div_index': "分卷编号:",
    'show_div_total': " 共:",
    'show_div_name': " 章 分卷名: ",
    'failed_get_chap': "章节获取失败: ",
    'get_div': "正在获取书籍分卷...",
    'failed_get_div': "分捲获取失败: ",
    'show_last_chap_s_index': "  最新章节, 编号: ",
    'show_last_chap_uptime': ", 更新时间:",
    'show_last_chap_name': "\n  章节:",
    'show_chap_list_index': "分卷:",
    'dl_chap_block_e': ".xhtml，章节屏蔽无法下载，以空档案标记。\n",
    'dl_chap_block_c': ".xhtml，章节屏蔽无法下载，使用本地档案。\n",
    'dl_chap_not_paid': "，该章节未订阅无法下载。\n",
    'dl_fin': "\n\n下载完毕",
    'expo_s': "汇出书籍...",
    'expo_e': "汇出完成...\n\n",
    'expo_no': "书籍无更新...\n\n",
    'dl_0_chap_re_dl': ".xhtml，發现缺失章节(空档案)，重新下载。\n",
    'dl_error_paid_stat_conflict': "，错误，该章节订授权态异常无法下载，请再次尝试下载。!!!!!\n",
    'dl_error_chap_get_failed_1': ".xhtml，错误，章节下载异常，请重新尝试下载，章节缺失以空档案标记!!!!!\n",
    'dl_error_chap_get_failed_2': ".xhtml，错误，章节下载异常，请重新尝试下载!!!!!\n",
    # epub
    'cover_dl_rt': "下载封面图片失败，重试: ",
    'cover_dl_f': "下载封面图片失败，放弃: ",
    'image_dl_rt': "下载图片失败，重试: ",
    'image_dl_f': "下载图片失败，放弃: ",
    # help
    'help_msg': """HbookerAppNovelDownloader 刺蝟猫 / 欢乐书客 小说下载器
请阅读README.md
指令(指令输入字首即可):
h | help\t\t\t\t\t\t--- 显示说明 (显示此讯息)
m | message\t\t\t\t\t\t--- 切换提示讯息 (繁体/简体)
q | quit\t\t\t\t\t\t--- 退出脚本
l | login <手机号/邮箱/用户名> <密码>\t\t\t--- 登录欢乐书客帐号
t | task\t\t\t\t\t\t--- 执行每日签到，领代币 (启动时自动执行，无异常不需再次执行)
s | shelf\t\t\t\t\t\t--- 刷新并显示当前书架列表 (启动时会自动刷新1次)
s <书架编号> | shelf <书架编号>\t\t\t\t--- 选择与切换书架
b | book\t\t\t\t\t\t--- 刷新并显示当前书架的书籍列表
b <书籍编号/书籍ID> | book <书籍编号/书籍ID>\t\t--- 选择书籍
d | download\t\t\t\t\t\t--- 下载当前书籍(book时选择的书籍)
d <书籍编号/书籍ID> | download <书籍编号/书籍ID>\t--- 下载指定ID书籍
ds <书架编号> | downloadshelf <书架编号> \t\t--- 下载整个书架
u | update\t\t\t\t\t\t--- 下载"list.txt"书单之中所列书籍
u <path.txt> | update <path.txt>\t\t\t--- 下载指定书单中所列书籍
"""
}


def set_message_lang(tc: bool = False):
    global lang
    if tc:
        lang = TC
    else:
        lang = SC


def m(key: str = ''):
    message = lang.get(key)
    if message is not None:
        return str(message)
    else:
        return ''
