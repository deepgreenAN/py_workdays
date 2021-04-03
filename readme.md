# 営業日・営業時間のデータを取得・抽出
営業日のデータを取得，pandas.DataFrameから営業日・営業時間のデータを抽出できる．pandas・numpyを用いており[高速](https://github.com/deepgreenAN/py_workdays/wiki/%E9%80%9F%E5%BA%A6%E3%82%92%E8%A8%88%E6%B8%AC)．
## requirements
- jpholiday
- pytz
- pandas
- numpy
- requests
- [py_strict_list](https://github.com/deepgreenAN/py_strict_list)

## installation
クローンしたディレクトリ内で
```
pip install -r requirements.txt
```
(test)
```
python setup.py test
```
```
python setup.py install 
```
そのディレクトリでないどこか別のディレクトリに移動して
```
python
>>> import py_workdays
>>> py_workdays.initialize_source()
```
そして以下のような結果となればcsvが保存され，インストールは終了である．
```
>>> py_workdays.option.holidays_date_array[-5:]
array([datetime.date(2021, 8, 9), datetime.date(2021, 9, 20),
       datetime.date(2021, 9, 23), datetime.date(2021, 11, 3),
       datetime.date(2021, 11, 23)], dtype=object)
```
ここで注意しなければならないのは，`py_workdays.initialie_source`をクローンしたディレクトリで実行すると，クローンしたリポジトリ内にソースが作成されてしまうことである．
## 使い方

```python
import datetime
import pickle
```


```python
from py_workdays import get_workdays_jp, check_workday_jp, 
get_next_workday_jp, get_workdays_number_jp,extract_workdays_intraday_jp, option
```

## 指定期間の営業日を取得


```python
start_date = datetime.date(2020,11,1)
end_date = datetime.date(2021,1,1)

workdays = get_workdays_jp(start_date, end_date, return_as="date")
```


```python
workdays
```




    array([datetime.date(2020, 11, 2), datetime.date(2020, 11, 4),
           datetime.date(2020, 11, 5), datetime.date(2020, 11, 6),
           datetime.date(2020, 11, 9), datetime.date(2020, 11, 10),
           datetime.date(2020, 11, 11), datetime.date(2020, 11, 12),
           datetime.date(2020, 11, 13), datetime.date(2020, 11, 16),
           datetime.date(2020, 11, 17), datetime.date(2020, 11, 18),
           datetime.date(2020, 11, 19), datetime.date(2020, 11, 20),
           datetime.date(2020, 11, 24), datetime.date(2020, 11, 25),
           datetime.date(2020, 11, 26), datetime.date(2020, 11, 27),
           datetime.date(2020, 11, 30), datetime.date(2020, 12, 1),
           datetime.date(2020, 12, 2), datetime.date(2020, 12, 3),
           datetime.date(2020, 12, 4), datetime.date(2020, 12, 7),
           datetime.date(2020, 12, 8), datetime.date(2020, 12, 9),
           datetime.date(2020, 12, 10), datetime.date(2020, 12, 11),
           datetime.date(2020, 12, 14), datetime.date(2020, 12, 15),
           datetime.date(2020, 12, 16), datetime.date(2020, 12, 17),
           datetime.date(2020, 12, 18), datetime.date(2020, 12, 21),
           datetime.date(2020, 12, 22), datetime.date(2020, 12, 23),
           datetime.date(2020, 12, 24), datetime.date(2020, 12, 25),
           datetime.date(2020, 12, 28), datetime.date(2020, 12, 29),
           datetime.date(2020, 12, 30), datetime.date(2020, 12, 31)],
          dtype=object)



## 営業日かどうか判定 


```python
select_date = datetime.date(2020,1,1)

check_workday_jp(select_date)
```




    False



## 次の営業日を取得 


```python
select_datetime = datetime.date(2020,1,1)

next_workday = get_next_workday_jp(select_datetime, days=6, return_as="dt")
```


```python
next_workday
```




    Timestamp('2020-01-09 00:00:00')



## 指定する日数分の営業日を取得 


```python
start_date = datetime.date(2020,11,1)
days = 42

workdays = get_workdays_number_jp(start_date, days)
workdays
```




    array([datetime.date(2020, 11, 2), datetime.date(2020, 11, 4),
           datetime.date(2020, 11, 5), datetime.date(2020, 11, 6),
           datetime.date(2020, 11, 9), datetime.date(2020, 11, 10),
           datetime.date(2020, 11, 11), datetime.date(2020, 11, 12),
           datetime.date(2020, 11, 13), datetime.date(2020, 11, 16),
           datetime.date(2020, 11, 17), datetime.date(2020, 11, 18),
           datetime.date(2020, 11, 19), datetime.date(2020, 11, 20),
           datetime.date(2020, 11, 24), datetime.date(2020, 11, 25),
           datetime.date(2020, 11, 26), datetime.date(2020, 11, 27),
           datetime.date(2020, 11, 30), datetime.date(2020, 12, 1),
           datetime.date(2020, 12, 2), datetime.date(2020, 12, 3),
           datetime.date(2020, 12, 4), datetime.date(2020, 12, 7),
           datetime.date(2020, 12, 8), datetime.date(2020, 12, 9),
           datetime.date(2020, 12, 10), datetime.date(2020, 12, 11),
           datetime.date(2020, 12, 14), datetime.date(2020, 12, 15),
           datetime.date(2020, 12, 16), datetime.date(2020, 12, 17),
           datetime.date(2020, 12, 18), datetime.date(2020, 12, 21),
           datetime.date(2020, 12, 22), datetime.date(2020, 12, 23),
           datetime.date(2020, 12, 24), datetime.date(2020, 12, 25),
           datetime.date(2020, 12, 28), datetime.date(2020, 12, 29),
           datetime.date(2020, 12, 30), datetime.date(2020, 12, 31)],
          dtype=object)



## 既存のpandas.DataFrameから営業日・営業時間のものを取得 

もちろん，営業日のもののみ抽出・営業時間のもののみ抽出も可能である．

デフォルトでは，東京証券取引所の営業日(土日・祝日，振替休日を除く)・営業時間(9時～11時30分，12時30分～15時)として利用できる．


```python
with open("notebooks/aware_stock_df.pickle", "rb") as f:
    aware_stock_df = pickle.load(f)
    
aware_stock_df.at_time(datetime.time(9,0))
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Open_6502</th>
      <th>High_6502</th>
      <th>Low_6502</th>
      <th>Close_6502</th>
      <th>Volume_6502</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-11-04 09:00:00+09:00</th>
      <td>2669.0</td>
      <td>2670.0</td>
      <td>2658.0</td>
      <td>2664.0</td>
      <td>93000.0</td>
    </tr>
    <tr>
      <th>2020-11-05 09:00:00+09:00</th>
      <td>2631.0</td>
      <td>2641.0</td>
      <td>2630.0</td>
      <td>2639.0</td>
      <td>55000.0</td>
    </tr>
    <tr>
      <th>2020-11-06 09:00:00+09:00</th>
      <td>2615.0</td>
      <td>2644.0</td>
      <td>2609.0</td>
      <td>2617.0</td>
      <td>90700.0</td>
    </tr>
    <tr>
      <th>2020-11-07 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-08 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-09 09:00:00+09:00</th>
      <td>2711.0</td>
      <td>2719.0</td>
      <td>2707.0</td>
      <td>2710.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2020-11-10 09:00:00+09:00</th>
      <td>2780.0</td>
      <td>2782.0</td>
      <td>2770.0</td>
      <td>2777.0</td>
      <td>142700.0</td>
    </tr>
    <tr>
      <th>2020-11-11 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-12 09:00:00+09:00</th>
      <td>2788.0</td>
      <td>2800.0</td>
      <td>2781.0</td>
      <td>2789.0</td>
      <td>108400.0</td>
    </tr>
    <tr>
      <th>2020-11-13 09:00:00+09:00</th>
      <td>2750.0</td>
      <td>2754.0</td>
      <td>2741.0</td>
      <td>2750.0</td>
      <td>71500.0</td>
    </tr>
    <tr>
      <th>2020-11-14 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-15 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-16 09:00:00+09:00</th>
      <td>2714.0</td>
      <td>2716.0</td>
      <td>2705.0</td>
      <td>2710.0</td>
      <td>111000.0</td>
    </tr>
    <tr>
      <th>2020-11-17 09:00:00+09:00</th>
      <td>2748.0</td>
      <td>2748.0</td>
      <td>2729.0</td>
      <td>2734.0</td>
      <td>124400.0</td>
    </tr>
    <tr>
      <th>2020-11-18 09:00:00+09:00</th>
      <td>2819.0</td>
      <td>2823.0</td>
      <td>2814.0</td>
      <td>2820.0</td>
      <td>76000.0</td>
    </tr>
    <tr>
      <th>2020-11-19 09:00:00+09:00</th>
      <td>2858.0</td>
      <td>2867.0</td>
      <td>2858.0</td>
      <td>2860.0</td>
      <td>107000.0</td>
    </tr>
    <tr>
      <th>2020-11-20 09:00:00+09:00</th>
      <td>2875.0</td>
      <td>2887.0</td>
      <td>2873.0</td>
      <td>2884.0</td>
      <td>106000.0</td>
    </tr>
    <tr>
      <th>2020-11-21 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-22 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-23 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-24 09:00:00+09:00</th>
      <td>2957.0</td>
      <td>2967.0</td>
      <td>2952.0</td>
      <td>2966.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2020-11-25 09:00:00+09:00</th>
      <td>2927.0</td>
      <td>2934.0</td>
      <td>2926.0</td>
      <td>2933.0</td>
      <td>74000.0</td>
    </tr>
    <tr>
      <th>2020-11-26 09:00:00+09:00</th>
      <td>2822.0</td>
      <td>2831.0</td>
      <td>2818.0</td>
      <td>2824.0</td>
      <td>93500.0</td>
    </tr>
    <tr>
      <th>2020-11-27 09:00:00+09:00</th>
      <td>2809.0</td>
      <td>2828.0</td>
      <td>2809.0</td>
      <td>2822.0</td>
      <td>107600.0</td>
    </tr>
    <tr>
      <th>2020-11-28 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-29 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 09:00:00+09:00</th>
      <td>2940.0</td>
      <td>2954.0</td>
      <td>2936.0</td>
      <td>2940.0</td>
      <td>225300.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
extracted_stock_df = extract_workdays_intraday_jp(aware_stock_df, return_as="df")
extracted_stock_df.at_time(datetime.time(9,0))
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Open_6502</th>
      <th>High_6502</th>
      <th>Low_6502</th>
      <th>Close_6502</th>
      <th>Volume_6502</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-11-04 09:00:00+09:00</th>
      <td>2669.0</td>
      <td>2670.0</td>
      <td>2658.0</td>
      <td>2664.0</td>
      <td>93000.0</td>
    </tr>
    <tr>
      <th>2020-11-05 09:00:00+09:00</th>
      <td>2631.0</td>
      <td>2641.0</td>
      <td>2630.0</td>
      <td>2639.0</td>
      <td>55000.0</td>
    </tr>
    <tr>
      <th>2020-11-06 09:00:00+09:00</th>
      <td>2615.0</td>
      <td>2644.0</td>
      <td>2609.0</td>
      <td>2617.0</td>
      <td>90700.0</td>
    </tr>
    <tr>
      <th>2020-11-09 09:00:00+09:00</th>
      <td>2711.0</td>
      <td>2719.0</td>
      <td>2707.0</td>
      <td>2710.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2020-11-10 09:00:00+09:00</th>
      <td>2780.0</td>
      <td>2782.0</td>
      <td>2770.0</td>
      <td>2777.0</td>
      <td>142700.0</td>
    </tr>
    <tr>
      <th>2020-11-11 09:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-12 09:00:00+09:00</th>
      <td>2788.0</td>
      <td>2800.0</td>
      <td>2781.0</td>
      <td>2789.0</td>
      <td>108400.0</td>
    </tr>
    <tr>
      <th>2020-11-13 09:00:00+09:00</th>
      <td>2750.0</td>
      <td>2754.0</td>
      <td>2741.0</td>
      <td>2750.0</td>
      <td>71500.0</td>
    </tr>
    <tr>
      <th>2020-11-16 09:00:00+09:00</th>
      <td>2714.0</td>
      <td>2716.0</td>
      <td>2705.0</td>
      <td>2710.0</td>
      <td>111000.0</td>
    </tr>
    <tr>
      <th>2020-11-17 09:00:00+09:00</th>
      <td>2748.0</td>
      <td>2748.0</td>
      <td>2729.0</td>
      <td>2734.0</td>
      <td>124400.0</td>
    </tr>
    <tr>
      <th>2020-11-18 09:00:00+09:00</th>
      <td>2819.0</td>
      <td>2823.0</td>
      <td>2814.0</td>
      <td>2820.0</td>
      <td>76000.0</td>
    </tr>
    <tr>
      <th>2020-11-19 09:00:00+09:00</th>
      <td>2858.0</td>
      <td>2867.0</td>
      <td>2858.0</td>
      <td>2860.0</td>
      <td>107000.0</td>
    </tr>
    <tr>
      <th>2020-11-20 09:00:00+09:00</th>
      <td>2875.0</td>
      <td>2887.0</td>
      <td>2873.0</td>
      <td>2884.0</td>
      <td>106000.0</td>
    </tr>
    <tr>
      <th>2020-11-24 09:00:00+09:00</th>
      <td>2957.0</td>
      <td>2967.0</td>
      <td>2952.0</td>
      <td>2966.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2020-11-25 09:00:00+09:00</th>
      <td>2927.0</td>
      <td>2934.0</td>
      <td>2926.0</td>
      <td>2933.0</td>
      <td>74000.0</td>
    </tr>
    <tr>
      <th>2020-11-26 09:00:00+09:00</th>
      <td>2822.0</td>
      <td>2831.0</td>
      <td>2818.0</td>
      <td>2824.0</td>
      <td>93500.0</td>
    </tr>
    <tr>
      <th>2020-11-27 09:00:00+09:00</th>
      <td>2809.0</td>
      <td>2828.0</td>
      <td>2809.0</td>
      <td>2822.0</td>
      <td>107600.0</td>
    </tr>
    <tr>
      <th>2020-11-30 09:00:00+09:00</th>
      <td>2940.0</td>
      <td>2954.0</td>
      <td>2936.0</td>
      <td>2940.0</td>
      <td>225300.0</td>
    </tr>
  </tbody>
</table>
</div>



2020年11月11日はふつうに営業日だがこれはデータの方のミス

## Option 

### 祝日・休日の探索期間

祝日・休日はデフォルトでは現在年の5年前から利用できる．開始・終了年はオプションから変更できる


```python
# default
print(option.holiday_start_year)
print(option.holidays_date_array[:5])
print(option.holiday_end_year)
print(option.holidays_date_array[-5:])
```

    2016
    [datetime.date(2016, 1, 1) datetime.date(2016, 1, 11)
     datetime.date(2016, 2, 11) datetime.date(2016, 3, 20)
     datetime.date(2016, 3, 21)]
    2021
    [datetime.date(2021, 8, 9) datetime.date(2021, 9, 20)
     datetime.date(2021, 9, 23) datetime.date(2021, 11, 3)
     datetime.date(2021, 11, 23)]
    

### バックエンド

祝日・休日を取得する方法として，[jpholiday](https://pypi.org/project/jpholiday/)を利用するか("jpholiday")，特定のcsvファイルを利用するか("csv")選べる．csvは複数のパスを指定できる(追加方法は後述)．祝日のcsvファイルを新しくしたい場合は`py_restart.all_make_source()`を実行する．


```python
# default
print(option.backend)
print(option.csv_source_paths)
```

    csv
    [WindowsPath('E:/py_workdays/py_workdays/source/holiday_naikaku.csv')]
    

ここで，`csv_source_paths`のデフォルトは自動的にpyworkdaysのあるディレクトリのsourceディレクトリ内のholiday_naikaku.csv一つとなる．これは内部で`__file__`を参照しているためである．

### 休日曜日・営業時間 

休日とする曜日を整数で指定できる．デフォルトは土日(5,6)．営業時間は東京証券取引所のものであり，開始時間と終了時間のペアを複数指定できる．


```python
# default
print(option.holiday_weekdays)
print(option.intraday_borders)
```

    [5, 6]
    [[datetime.time(9, 0), datetime.time(11, 30)], [datetime.time(12, 30), datetime.time(15, 0)]]
    

### Optionの変更 

下の例では代入しているが，リストの場合はappendでもよい．値の型を間違えるとエラーが出る．optionの値を初期化したいときは`option.__init__()`を呼べばよい．


```python
option.intraday_borders = [[datetime.time(9, 0), datetime.time(13, 0)]]
```


```python
extracted_stock_df = extract_workdays_intraday_jp(aware_stock_df, return_as="df")
extracted_stock_df.at_time(datetime.time(12,0))
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Open_6502</th>
      <th>High_6502</th>
      <th>Low_6502</th>
      <th>Close_6502</th>
      <th>Volume_6502</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-11-04 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-05 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-06 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-09 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-10 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-11 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-12 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-13 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-16 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-17 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-18 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-19 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-20 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-24 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-25 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-26 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-27 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 12:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



csv_source_pathは追加するだけで取得できる休日の更新が行われるので，以下のようにすればよい

```python
from pathlib import Path
some_source_path = Path("some_source.csv")
option.csv_source_path.append(some_source_path)
```

some_source.csvは以下のような形式になっている必要がある

```
1955-01-01,元日
1955-01-15,成人の日
1955-03-21,春分の日
```
