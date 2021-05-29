import datetime
import numpy as np
import pandas
from pytz import timezone

from .py_workdays_ver4 import option


def check_jst_datetimes_to_naive(*arg_datetimes):
    """
    ＊*今のところ，ローカルが東京でないnaiveなdatetimeはそのまま通してしまう
    引数のタイムゾーンが同じかどうかチェックし，存在するなら日本であるかチェック
    awareな場合は，naiveに変更
    """
    jst_timezone = timezone("Asia/Tokyo")
    tz_info_set = set([one_datetime.tzinfo for one_datetime in arg_datetimes])
    if len(tz_info_set) > 1:
        raise Exception("timezones are different")
        
    datetimes_tzinfo = list(tz_info_set)[0]
    
    if datetimes_tzinfo is not None:  # 長さが1のはず
        if timezone(str(datetimes_tzinfo)) != jst_timezone:
            raise Exception("timezones must be Asia/Tokyo")
        # naiveなdatetimeに変更
        arg_datetimes = [one_datetime.replace(tzinfo=None) for one_datetime in arg_datetimes]
    
    # 引数が一つであるかどうか
    if len(arg_datetimes) > 1:  # 引数が複数の場合
        return tuple(arg_datetimes)
    else:  # 引数が一つの場合
        return arg_datetimes[0]


def extract_workdays_index(dt_index, return_as="index"):
    """
    pd.DatetimeIndexから，営業日のデータのものを抽出
    dt_index: pd.DatetimeIndex
        入力するDatetimeIndex，すでにdatetimeでソートしていることが前提
    return_as: str
        出力データの形式
        - "index": 引数としたdfの対応するインデックスを返す
        - "bool": 引数としたdfに対応するboolインデックスを返す
    """
    # 返り値の形式の指定
    return_as_set = {"index", "bool"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))
        
    # すでにtimestampでソートさてている前提
    start_datetime = dt_index[0].to_pydatetime()
    end_datetime = dt_index[-1].to_pydatetime()
    
    start_datetime, end_datetime = check_jst_datetimes_to_naive(start_datetime, end_datetime)  # 二つのdatetimeのタイムゾーンをチェック・naiveに変更
    
    # 期間内のholidayを取得
    holidays_in_span_index = ((start_datetime-datetime.timedelta(days=1))<option.holidays_datetimeindex)&\
    (option.holidays_datetimeindex<=end_datetime)  # DatetimeIndexを使うことに注意, 当日を含めるため，startから1を引いている．
    holidays_in_span_datetimeindex = option.holidays_datetimeindex[holidays_in_span_index]  # pd.DatetimeIndexを使う
    
    # 休日に含まれないもの，さらに土日に含まれないもののboolインデックスを取得    
    holiday_bool_array = dt_index.tz_localize(None).floor("D").isin(holidays_in_span_datetimeindex)  # 休日
    
    dt_index_weekday = dt_index.weekday
    holiday_weekday_each_bool_arrays = [dt_index_weekday==weekday for weekday in option.holiday_weekdays]  # inを使うのを回避
    holiday_weekday_bool_array = np.logical_or.reduce(holiday_weekday_each_bool_arrays)  # 休日曜日
    
    workdays_bool_array = (~holiday_bool_array)&(~holiday_weekday_bool_array)  # 休日でなく休日曜日でない
    if return_as=="bool":  # boolで返す場合
        return workdays_bool_array
    
    elif return_as=="index":  # indexで返す場合
        workdays_df_indice = dt_index[workdays_bool_array]
        return workdays_df_indice


def extract_workdays(df, return_as="df"):
    """
    データフレームから，営業日のデータのものを抽出．出力データ形式をreturn_asで指定する．
    df: pd.DataFrame(インデックスとしてpd.DatetimeIndex)
        入力データ
    return_as: str
        出力データの形式
        - "df": 抽出した新しいpd.DataFrameを返す
        - "index": 引数としたdfの対応するインデックスを返す
        - "bool": 引数としたdfに対応するboolインデックスを返す
    """
    
    # 返り値の形式の指定
    return_as_set = {"df", "index", "bool"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))
    
    if return_as=="bool":
        workdays_bool_array = extract_workdays_index(df.index, return_as="bool")
        return workdays_bool_array
    elif return_as=="index":
        workdays_bool_array = extract_workdays_index(df.index, return_as="bool")
        workdays_df_indice = df.index[workdays_bool_array]
        return workdays_df_indice
    else:
        workdays_bool_array = extract_workdays_index(df.index, return_as="bool")
        out_df = df[workdays_bool_array].copy()
        return out_df


def extract_intraday_index(dt_index, return_as="index"):
    """
    pd.DatetimeIndexから，日中のデータのものを抽出．出力データ形式をreturn_asで指定する．
    dt_index: pd.DatetimeIndex
        入力するDatetimeIndex
    return_as: str
        出力データの形式
        - "index": 引数としたdfの対応するインデックスを返す
        - "bool": 引数としたdfに対応するboolインデックスを返す
    """
    
    # 返り値の形式の指定
    return_as_set = {"index", "bool"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))    
  
    bool_array = np.full(len(dt_index), False)
    
    # ボーダー内のboolをTrueにする
    for borders in option.intraday_borders:
        start_time, end_time = borders[0], borders[1]  # 開始時刻と終了時刻
        in_border_indice = dt_index.indexer_between_time(start_time=start_time, end_time=end_time, include_end=False)
        bool_array[in_border_indice] = True
    
    if return_as=="bool":
        return bool_array

    elif return_as=="index":
        intraday_indice = dt_index[bool_array]
        return intraday_indice


def extract_intraday(df, return_as="df"):
    """
    データフレームから，日中のデータのものを抽出．出力データ形式をreturn_asで指定する．
    df: pd.DataFrame(インデックスとしてpd.DatetimeIndex)
        入力データ
    return_as: str
        出力データの形式
        - "df": 抽出した新しいpd.DataFrameを返す
        - "index": 引数としたdfの対応するインデックスを返す
        - "bool": 引数としたdfに対応するboolインデックスを返す
    """
    
    # 返り値の形式の指定
    return_as_set = {"df", "index", "bool"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))    

    if return_as=="bool":
        intraday_bool_array = extract_intraday_index(df.index, return_as="bool")
        return intraday_bool_array 
    elif return_as=="index":
        intraday_bool_array = extract_intraday_index(df.index, return_as="bool")
        intraday_indice = df.index[intraday_bool_array]
        return intraday_indice
    else:
        intraday_bool_array = extract_intraday_index(df.index, return_as="bool")
        out_df = df[intraday_bool_array].copy()
        return out_df


def extract_workdays_intraday_index(dt_index, return_as="index"):
    """
    pd.DatetimeIndexから，営業日+日中のデータのものを抽出．出力データ形式をreturn_asで指定する．
    dt_index: pd.DatetimeIndex
        入力するDatetimeIndex
    return_as: str
        出力データの形式
        - "index": 引数としたdfの対応するインデックスを返す
        - "bool": 引数としたdfに対応するboolインデックスを返す
    """

    # 返り値の形式の指定
    return_as_set = {"index", "bool"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))
        
    workday_bool_array = extract_workdays_index(dt_index, return_as="bool")
    intraday_bool_array = extract_intraday_index(dt_index, return_as="bool")
    
    workday_intraday_bool_array = workday_bool_array & intraday_bool_array
    if return_as=="bool":
        return workday_intraday_bool_array
    elif return_as=="index":
        workday_intraday_indice = dt_index[workday_intraday_bool_array]
        return workday_intraday_indice


def extract_workdays_intraday(df, return_as="df"):
    """
    データフレームから，営業日+日中のデータのものを抽出．出力データ形式をreturn_asで指定する．
    df: pd.DataFrame(インデックスとしてpd.DatetimeIndex)
        入力データ
    return_as: str
        出力データの形式
        - "df": 抽出した新しいpd.DataFrameを返す
        - "index": 引数としたdfの対応するインデックスを返す
        - "bool": 引数としたdfに対応するboolインデックスを返す
    """
    
    # 返り値の形式の指定
    return_as_set = {"df", "index", "bool"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))    
       
    if return_as=="bool":
        workday_intraday_bool_array = extract_workdays_intraday_index(df.index, return_as="bool")
        return workday_intraday_bool_array
    elif return_as=="index":
        workday_intraday_bool_array = extract_workdays_intraday_index(df.index, return_as="bool")
        workday_intraday_indice = df.index[workday_intraday_bool_array]
        return workday_intraday_indice
    else:
        workday_intraday_bool_array = extract_workdays_intraday_index(df.index, return_as="bool")
        out_df = df[workday_intraday_bool_array].copy()
        return out_df

if __name__ == "__main__":
  pass