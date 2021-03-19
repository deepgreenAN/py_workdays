# 営業日・営業時間のデータを取得
## requirements
- jpholiday
- pytz
- pandas
- numpy

## 使い方

```python
import datetime
import pickle
```


```python
from py_workdays import get_workdays_jp, check_workday_jp, extract_workdays_jp, extract_workdays_intraday_jp, option
```

## 営業日を取得


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



## 既存のデータフレームから営業日・営業時間のものを取得 

デフォルトでは，東京証券取引所の営業日(土日・祝日，振替休日を除く)・営業時間(9時～11時30分，12時30分～15時)として利用できる．


```python
with open("aware_stock_df.pickle", "rb") as f:
    aware_stock_df = pickle.load(f)
    
aware_stock_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <th>2020-11-04 00:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-04 00:01:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-04 00:02:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-04 00:03:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-04 00:04:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2020-11-30 23:55:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 23:56:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 23:57:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 23:58:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 23:59:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>29520 rows × 5 columns</p>
</div>




```python
extracted_stock_df = extract_workdays_intraday_jp(aware_stock_df, return_as="df")
extracted_stock_df
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
      <th>2020-11-04 09:01:00+09:00</th>
      <td>2663.0</td>
      <td>2664.0</td>
      <td>2650.0</td>
      <td>2652.0</td>
      <td>17600.0</td>
    </tr>
    <tr>
      <th>2020-11-04 09:02:00+09:00</th>
      <td>2649.0</td>
      <td>2655.0</td>
      <td>2646.0</td>
      <td>2649.0</td>
      <td>19200.0</td>
    </tr>
    <tr>
      <th>2020-11-04 09:03:00+09:00</th>
      <td>2652.0</td>
      <td>2670.0</td>
      <td>2651.0</td>
      <td>2670.0</td>
      <td>31200.0</td>
    </tr>
    <tr>
      <th>2020-11-04 09:04:00+09:00</th>
      <td>2671.0</td>
      <td>2674.0</td>
      <td>2670.0</td>
      <td>2674.0</td>
      <td>12800.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2020-11-30 14:55:00+09:00</th>
      <td>2908.0</td>
      <td>2908.0</td>
      <td>2905.0</td>
      <td>2905.0</td>
      <td>26300.0</td>
    </tr>
    <tr>
      <th>2020-11-30 14:56:00+09:00</th>
      <td>2905.0</td>
      <td>2908.0</td>
      <td>2905.0</td>
      <td>2907.0</td>
      <td>21700.0</td>
    </tr>
    <tr>
      <th>2020-11-30 14:57:00+09:00</th>
      <td>2908.0</td>
      <td>2909.0</td>
      <td>2906.0</td>
      <td>2907.0</td>
      <td>27200.0</td>
    </tr>
    <tr>
      <th>2020-11-30 14:58:00+09:00</th>
      <td>2907.0</td>
      <td>2910.0</td>
      <td>2905.0</td>
      <td>2908.0</td>
      <td>42600.0</td>
    </tr>
    <tr>
      <th>2020-11-30 14:59:00+09:00</th>
      <td>2910.0</td>
      <td>2920.0</td>
      <td>2902.0</td>
      <td>2920.0</td>
      <td>146100.0</td>
    </tr>
  </tbody>
</table>
<p>5400 rows × 5 columns</p>
</div>



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

祝日・休日を取得する方法として，[jpholiday](https://pypi.org/project/jpholiday/)を利用するか("jpholiday")，特定のcsvファイルを利用するか("csv")選べる．csvは複数のパスを指定でき，
```
python scrape_and_make_source.py
```
で自動でスクレイピングできる．


```python
# default
print(option.backend)
print(option.csv_source_paths)
```

    csv
    [WindowsPath('E:/py_workdays/source/holiday_naikaku.csv')]
    

ここで，`csv_source_paths`のデフォルトは自動的にpyworkdaysのあるディレクトリのsourceディレクトリ内のholiday_naikaku.csv一つである．これは内部で`__file__`を参照しているためである．

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

下の例では代入しているが，リストの場合はappendでもよい．値の型を間違えると，関数の利用時にエラーが出る．optionの値を初期化したいときは`option.__init__()`を呼べばよい．


```python
option.intraday_borders = [[datetime.time(9, 0), datetime.time(13, 0)],]
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


