# Kobo 99 特價書日曆爬蟲
- 日曆公開網址: https://calendar.google.com/calendar/embed?src=rcmvnfej75s7c9sjdbic1f55v8%40group.calendar.google.com&ctz=Asia%2FTaipei
- iCal: https://calendar.google.com/calendar/ical/rcmvnfej75s7c9sjdbic1f55v8%40group.calendar.google.com/public/basic.ics

## 如何新增日曆
- 開啟 [Google 日曆](https://calendar.google.com/)
- 點選右上角 齒輪 > 設定
- 左側 一般 > 新增日曆 > 加入日曆網址
- 輸入 https://calendar.google.com/calendar/ical/rcmvnfej75s7c9sjdbic1f55v8%40group.calendar.google.com/public/basic.ics
- 點選 新增日曆

## 爬蟲動作
- 於 [Kobo Blog 好讀書單](https://tw.news.kobo.com/%E5%B0%88%E9%A1%8C%E4%BC%81%E5%8A%83/%E5%A5%BD%E8%AE%80%E6%9B%B8%E5%96%AE) 中尋找最新的一週99書單文章
- 尋找 "mm/dd 週x選書" 文字，爬取 書本連結 與 書名
- 根據書本連結尋找對應的 .book-block 內的書本資訊
- 新增至 Google Calendar

## pipenv pack packages to zip (aws lambda)
```shell
mkdir output
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t output
```
[source](https://github.com/pypa/pipenv/issues/2705#issuecomment-410949164)

```shell
cp credentials.json output
cp *.py output
cd output
zip -r ../output.zip .
```