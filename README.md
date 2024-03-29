# HbookerAppNovelDownloader
## 使用前請仔細閱讀!!  
## 介紹  
* HbookerAppNovelDownloader  
* 基於https://github.com/hang333/HbookerAppNovelDownloader  
* 模仿 刺猬貓 / 歡樂書客 android app版內核的小說下載器  
* 此程序目的是:  
  為了預防書籍/章節哪天遭屏蔽或下架(特別是已購買的書籍/章節)，讓讀者有預先下載書籍到本地保存選擇。  
* 此程序不是"**破解**"看書，付費章節依然需要付費購買後才能獲取章節  
* 支持免費與已付費章節下載  
* 支持書籍內插圖下載  
* 支持書籍的章節更新/更新檢查  
* 若刪除Cache中的檔案，下次下載時缺失的部分會被重新下載  
* 支持導出文件格式：txt、epub，文件將會被下載至HBooker目錄下  
  
* 書籍/章節下架後然會無法下載  
* 不要大規模宣傳此程式，請低調個人使用。  
  ### 下載書籍僅個人閱讀，禁止分享上傳
## 免責聲明:  
* **使用此工具可能導致封號**  
* **請自行評估風險是否使用此程序**  
* **若發生封號等事件，後果自負，這裡不負責**  
* **用戶帳號與密碼會報保存在HbookerAppNovelDownloader - Config.json中，小心勿洩漏**  
* **若帳號密碼寫洩漏(請自行檢查代碼，自行評估)，後果自負，這裡不負責**  
* **使用此程式造成的任何意外接不負責**  
 
### 警告: 此版本的站存檔先前版本的暫存不相容，請移移除(備分舊版EPUB)後再執行下載
* 此此處站存主要是針對暫存`./Cache/OEBPS/Text/<Chapter_ID>.xhtml`的警告。
  其他暫存檔案**因該**沒有影響。
* 原因在於此版建立匯出書籍EPUB的過程有極大改動。
* 若未移除舊版的暫存直接執行，會導致章節順序混亂、目錄標題缺失卷名等問題，甚至出現崩潰。
* 若有保存現在已屏蔽章節想要加入，需要人工進行編輯，改成現在的檔名與格式後才能加入站存使用。

## 需求環境  
 * Python3  
 * requests  
 * pycryptodome或pycrypto  
## 使用法法  
- 類似控制台的操作  
* 內部指令說明 :  
  ```
  h | help						--- 顯示說明 (此訊息)  
  m | message						--- 切換提示訊息 (繁體/簡體)  
  q | quit						--- 退出腳本  
  i | import_token					--- 以匯入token方式登入帳號
  l | login <手機號/郵箱/用戶名> <密碼>			--- 登錄歡樂書客帳號 ！！！已失效！！！
  version							--- 從網路獲取現在版本號，詢問是否刷新版本號 (輸入完整單字)  
  	注:<用戶名>空格<密碼>，<用戶名>與<密碼>不能含有空格。  
  t | task						--- 執行每日簽到，領代幣 (啟動時自動執行，無異常不需再次執行)  
  s | shelf						--- 刷新並顯示當前書架列表 (啟動時會自動刷新1次)  
  s <書架編號> | shelf <書架編號>				--- 選擇與切換書架  
  b | book						--- 刷新並顯示當前書架的書籍列表  
  b <書籍編號/書籍ID> | book <書籍編號/書籍ID>		--- 選擇書籍  
  d | download						--- 下載當前書籍(book時選擇的書籍)  
  d <書籍編號/書籍ID> | download <書籍編號/書籍ID>		--- 下載指定ID書籍  
  ds <書架編號> | downloadshelf <書架編號>			--- 下載整個書架  
  u | update						--- 下載"list.txt"書單之中所列書籍  
  u <path.txt> | update <path.txt>			--- 下載指定書單中所列書籍  
  ```  

  注: 輸入指令開頭字母即可  
## 基本使用流程  
  * 首先執行  
    `py run.py`  
    確認仔細閱讀且同意README.md中之敘述事物，如果同意，輸入  
    `yes`  
     登入帳號，token 與 account 輸入
     `i`  
    進入匯入模式 提供2種匯入方式

    1 . 由xml檔案方式匯入 需從手機APP獲取 `/data/data/com.kuangxiangciweimao.novel/shared_prefs/com.kuangxiangciweimao.novel_preferences.xml`
    後放置於工作目錄後選擇第`1`選項
    獲取`com.kuangxiangciweimao.novel_preferences.xml`提供2方案
    
    對於root android 可嘗試
    ```
    adb shell
    su
    chmod 777 /data/data/com.kuangxiangciweimao.novel/shared_prefs/com.kuangxiangciweimao.novel_preferences.xml
    exit
    exit
    adb pull /data/data/com.kuangxiangciweimao.novel/shared_prefs/com.kuangxiangciweimao.novel_preferences.xml
    ```
    非root android 可嘗試
    ```
    備份data/data/com.kuangxiangciweimao.novel
    adb backup -f data -noapk com.kuangxiangciweimao.novel
    使用https://github.com/nelenkov/android-backup-extractor 將data轉成tar
    java -jar .\abe.jar unpack data data.tar
    再用7z或其他壓縮軟件解壓所
    "C:\Program Files\7-Zip\7z.exe" x .\data.tar
    後獲取檔案xml
    "apps\com.kuangxiangciweimao.novel\sp\com.kuangxiangciweimao.novel_preferences.xml"
    ```
    2 . 利用抓包軟體讀取payload中的`login_token`與 `account` 後手動輸入
    * login_token 為32位數16進位字串
    * account 類似`书客123456789`字串
    
  * 選擇書籍  
    * 方法1: 根據用戶架`選擇書架`  
      `shelf <書架編號>`  
      根據該`書架中書籍邊號`選擇書籍  
    `book <書架中書籍邊號>`  
    * 方法2: 根據`書籍ID` `選擇書籍`  
    `book <書籍ID>`  
      * <書籍ID> 可以從網站該書頁的書籍網址  
        範例網址: www.ciweimao.com/book/123456789  
        範例網址尾部的"`123456789`" (9位數字)為`<書籍ID>`  
      * 也可以在官方APP內書頁點選 "分享" -> "複製連結" 取得連結   
  * 書籍選擇後可開始下載書籍，輸入:  
`download`  
    * 指定編號 + 下載:  
    `download <書架中書籍編號>`  
    可跳過`book <書架中書籍邊號>`指令，但必須已選書架(法1)  
    *  指定書籍ID + 下載  
    `download <書籍ID>`  
      可以跳過`選擇書籍`步驟，直接進行下載，但須預先知道ID
     
## 其他功能  
  ### 下載整個書架 (若書架長，不建議使用)輸入  
`downloadshelf <書架編號>`  
    可用縮寫代替`ds <書架編號>`  
    若省略`<書架編號>`，則會下載當前書架  
  ### 下載書單  
  可以根據**書單**中所列出的書籍進行下載，預設書單 "list.txt"，輸入:  
  `update <書單位置>`  
    若省略`<書單位置>`則會下載預設`"list.txt"`中所列的書籍  
  * 書單語法 根據Regex :``^\s*([0-9]{9}).*$``進行辨認  
    * 規則概要 :  
      * 每行只能有1本書  
      * 書籍開頭只能是<空白>或<書籍ID_9位數>  
      * <書籍ID_9位數>後的會被忽略  
  *  若不符合規則 --> 會被忽略  
     * 可在刻意"**不符合規則**"書自前插入任意符號來停用該書下載，不必刪除該行  
     *  可自由添加"**不符合規則**"的文字來進行分類管理或註釋，增加閱讀辨識度  
  *  提供參考範例 "list.txt"  
  ### 自動簽到能(每日代幣)  
  登入後每當啟動時會行簽到嘗試，若已簽到則不會進行簽到  
  可手動執行，輸入:  
  `task` 或 `t`  
  ### 自動化  
  最初執行時可**添加參數**，執行完畢後自動退出，只能之行單相指令，參數與以上指令相同  
  * 例: 若要 下載特定書籍 :  
  `py run.py d <書籍ID>`  
  * 例: 若要 下載 / 更新 書單 :  
  `py run.py u <書單位置>`  
  * 例: 只簽到  
  `py run.py t`  
    * 注: 此方式執行的`簽到`成功後會立刻結束，不會獲取刷新書架。  
   * 若想要完全自動化，可使用Windows的工作排程器`task scheduler`或Unix的`cron job`等類似工具，設定`定時執行`執行。
  ###介面訊息繁/簡切換
  * 可以切換提示訊息繁體/簡體，  
    輸入`m`  
  * **僅介面提示訊息**，與匯出的書籍無關  
  ###可更黨檔案保存位置  
  * 可以編輯`HbookerAppNovelDownloader - Config.json`檔案中的以下的"`./XXX/`"來改變檔案保存位置
    * 書籍匯出位置: "output_dir": "`./Hbooker/`"  
    * 書籍備份匯出位置: "backup_dir": "`./Hbooker/`"  
    * 暫存檔案位置: "cache_dir": "`./Cache/`"  
  ### 可以選擇是否會在書籍匯出時生成備份  
  * 可以編輯`HbookerAppNovelDownloader - Config.json`檔案中的以下的 `"do_backup":` `true`  
    * 啟用`"do_backup":` `true`  
    * 停用`"do_backup":` `false`
  ###更新版本號功能
  * 可以透過網路獲取目前版本號  
    輸入`version`
    * 獲取候群問使否刷新版本號
      * 獲取輸入`yes`可確認，其他取消
      * (目前對於版本號的作用有待觀察)
    * 另外可手動改版本號  
      編輯`HbookerAppNovelDownloader - Config.json`中的`"current_app_version":` "`2.7.039`"  
      
## 與原版差異/改動
* \+ **簽到功能(領代幣)，(自動簽到)**。
* \+ **下載章節與獲取書籍目錄時使用多工，加快下載速度(取代原download)**，  
  預設平行下載上限為`32`，可在Config中更改。  
  注:根據觀察官方APP書籍下載速度，因該也是有進類似平行下載，因該不會封號。  
* \+ 登入失效會自動嘗試重新登入。  
* \+ **使用者帳號與密碼會以明文方式保存在Config中**，小心誤洩漏。  
* 改動config.json名稱與儲存位置至 ./HbookerAppNovelDownloader.json。  
* **更改書籍章節排序方式**，從依照index(因該是章節公開順序)，改成依照app中書籍目錄分眷章節排序。  
* \+ **增加命令行界面(command line interface)，方便自動化**。  
* \- 移除了下載單卷功能(認為此功能多餘)。  
* \- 指令介面中移除config相關指令。  
* \+ 在EPUB封面添加了書籍名稱、作者名、書籍簡介、更新時間。  
* \+ 將封面加入EPUB目錄。  
* \+ 取代原"update"更興功能，改成讀取使用者自建立的書單，進行書單下載。  
* \+ 增價下載帳號中整個書架功能。
* \- 不建立書籍.json。
* 更改提示文字。
* \+ 增加更多出錯重試與改變出錯處裡。
* \+ 遇到`未訂閱的付費章節`時，不會結束下載立刻匯出書籍，而會跳過該章，直到下載所有可被下載的`已付費`與`免費章節`後才匯出書籍。
* \+ 從章節目錄獲取章節資訊，得知那些章節已付費可被下載，以及那些章節被屏蔽無法下載，根據章節狀態執行下載，減少非必要的伺服器下載訪問。  
  因只會嘗試下載可下載的章節，沒有必定會失敗的下載嘗試，**理論上因該會減小封號機率**，較原版會嘗試訪下載問未購買章節與屏蔽章節，我認為算是可疑行為。  
  章節狀態分為(已下載\未下載)、(免費/已訂閱/未訂閱)、(屏蔽)，根據狀態判斷是否要嘗試下載章節。  
* \+ 改變"`章節已下載`"判定方式，現在根據暫存中使否存在該章節對應的檔案(`xxxx-yyyyyy-zzzzzzzzz.xhtm`)。  
  - 如要重新下載某書或某章節，刪除暫存內的該書或該章(建議刪除單章)，再次執行下載即可。  
* \+ 改變"`已下載章節`"的存檔名稱為`xxxx`-`yyyyyy`-`zzzzzzzzz`.xhtml。  
  注:`xxxx`: 分卷號、`yyyyyy`: 分卷章節編號(順序)、`zzzzzzzzz`: 章節id  
  例:某書的`第2卷`-`第5章`會檔名會是`0002`-`000005`-123456789.xhtml
* 章節存檔內的`\<title>章節名\</title>`改成`\<title>捲名 : 章節名\</title>`對閱讀無引響
* \+ 匯出EPUB目錄中所列的`章節名`更改`捲名 : 章節名` 
* \+ 匯出EPUB與TXT的章節排方式根據"已下載章節"檔名排序
* 移動`template.epub`至主目錄下。  
* 不會自動解壓保存書籍EPUB至Cache暫存，若需要需手動執行。  
* \+ 書籍匯出時會進行備份，加上日期後綴，如有需要會再增加後編號綴數字(此功能意義不大)。  
* \+ 書籍下載時會顯示3組數字 : `<num_1>` / `<num_2>` / `<num_3>`  
  分別代表 : `該次執行實際下載章節數` / `目前已經處理章節數(進度)` / `該書總章節數`  
  * 當`<num_2>`等於`<num_3>`時，代表下載處完成，請等待書籍匯出。  
  * 若下載完成時`<num_1>`為`0`，則代表沒有下載任何章節。  
* 因習慣所以使用繁體中文顯示。  
  
## 其他事項  
  * 預設平行下載上限為`32`，可在Config中更改，編輯Config中`"max_concurrent_downloads": 32`的數字即可更改，下次啟動後生效。  
    **若值設過高，可能會提高封號風險。**  
  * 可在Config手動更改帳號密碼，編輯在Config中的  
    `user_account": "YOUR_ACCOUNT"`的`YOUR_ACCOUNT`以及  
    `"user_password": "YOUR_PASSWORD"`的`YOUR_PASSWORD`  
    下次啟動後生效，建議使用login指令比較實際  
  * 若某章節下載後有改動、修正等，"需要刷新"，需要手動進入該書籍暫存檔，找到該節對應檔案，進行刪除或改名，後再次執行下載以重新下載  
    * 進入`Cache\《該書籍名》\OEBPS\Text\`尋找到對應章節檔案進行`刪除`或`重新命名`  
      * 例: `0001-000002-123456789.xhtml`改名為`0001-000002-123456789-任意後綴.xhtml`  
    **重要: 重新命名時只能加上`後綴`，且必須用"`-`"號隔開，否則會導致錯誤。**  
  * 圖片可能會被刪除等原因無法下載，下載時會進行錯圖片下載錯誤提示，忽略即可。  
  * 有時會因為等待圖片重試下載，增價閜下時間，請耐心等待完成訊息。  
  * 若章節因屏蔽無法下載，會建立空檔案當作標記 (檔案大小為0)，該檔案匯出EPUB後會造成該章頁面無法顯示(當作標記)。  
    * 若個人有保存缺失的章節，可自行依照xhtml格式放入，取代空章節。  
      * 若發現某些章節被屏蔽，導致以後無法下載，建議保存該章節檔案(不要刪除)。  
  * 若未購買章節，則會進行告知，不會建立空檔檔案。  
  * 若下載中途出現問題，導致停止運行，請閱讀錯誤原因，大部分錯誤重新執行下載幾可排除。  
    注: 少數狀況下可能導致章節不全(機率極小)，需要手動刪除該章，重新下載。  
  * 若有需要EPUB黨可被解壓縮還原成暫存檔。
  * 在Windows上可建立捷徑，添加參數，點擊可執行特定功能。  
  * 可使用`pyinstaller`打包凍結封包程執行檔方便使用 :  
    `pyinstaller --noconfirm --onefile --console --add-data "template.epub;." "run.py" --name "HbookerAppNovelDownloader"`
