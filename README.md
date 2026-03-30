裡面有兩個目錄，modules and singleRunTest.因為是AI產生的，modules太多使得AI混亂了，就改用singleRunTest避免太多又亂了。
```
python .\network_api_tester.py --help
usage: network_api_tester.py [-h] [--config CONFIG] [--modules MODULES [MODULES ...]] [--categories CATEGORIES [CATEGORIES ...]]
                             [--tests TESTS [TESTS ...]] [--output OUTPUT] [--list] [--list-modules] [--list-categories]

網路設備 REST API 統一測試框架

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        配置文件路徑
  --modules MODULES [MODULES ...], -m MODULES [MODULES ...]
                        指定要測試的模組
  --categories CATEGORIES [CATEGORIES ...], -cat CATEGORIES [CATEGORIES ...]
                        指定要測試的API類別
  --tests TESTS [TESTS ...], -t TESTS [TESTS ...]
                        指定要執行的測試案例
  --output OUTPUT, -o OUTPUT
                        測試報告輸出文件
  --list, -l            列出所有可用的測試案例
  --list-modules        列出所有可用的模組
  --list-categories     列出所有可用的類別
```

進入singleRunTest， 直接執行，每一個可能都不太一樣，他會直接告訴你缺甚麼 參數
