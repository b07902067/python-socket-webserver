# python_socket_webserver
###### `web server`

### 功能
- profile page
- 登入/登出
- 留言板

### 運行
- 本機測試 : 運行下列指令後，以瀏覽器搜尋 http://127.0.0.1:8000/
```cpp=
$ git clone ...
$ python phase2.py
```
- (我的)線上網站 : http://18.216.30.137:8000/


### 實作(待補)
使用 python 的 socket 套件，以 socket 將 html 及 css 等檔案傳輸給瀏覽器以建立網頁。
- 登入/登出
  - 使用 http header 中的 Set-Cookie 欄位，由 server 端將 client 的 username+password 製作成 Session ID，以 cookie 形式傳遞至 client 端。
  - 登入 : 將 client 的 Session ID 放在 http header 中，設定過期(Expired)的時間(Ex. 10日後)
  - 登出 : 同樣使用 set-cookie，但將過期日期設定在現在時刻以前，使 client 端的 cookie 過期，以達到登出目的。
- 留言板
  - 使用檔案儲存 client 的留言
  - 將 client 的留言儲存在一 dictionary 中，包括其用戶名稱(也有可能匿名)、留言時間、留言內容，並且以留言時間進行排序
  - 使用 pickle 將此 dictionary 存進檔案中，方便記錄以前的留言
  
### 範例(待補)

### 參考
- https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers (http header 的參考)
- https://medium.com/@trista_liu/2018年最好用的20個bootstrap網站模板-e99772f8ae38 （bootstrap profile 模板）
