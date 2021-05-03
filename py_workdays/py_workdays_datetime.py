import datetime
from pytz import timezone

from .py_workdays_ver4 import option, check_workday_jp, get_near_workday_jp


def get_timezone_datetime_like(select_datetime, like_datetime):
    """
    指定したdatetimeのタイムゾーンを別のdatetimeのものに変換
    select_datetime: datetime.datetime
        タイムゾーンを変換したいdatetime
    like_datetime: datetime.datetime
        一致させたいタイムゾーンを持つdatetime
    """
    like_datetime_is_aware = like_datetime.tzinfo is not None
    if like_datetime_is_aware:
        like_timezone = timezone(str(like_datetime.tzinfo))
    
    select_datetime_is_aware = select_datetime.tzinfo is not None
    
    if not like_datetime_is_aware and not select_datetime_is_aware:# select_datetime, like_datetimeがどちらもnaiveな場合
        return select_datetime
    elif like_datetime_is_aware and not select_datetime_is_aware:# like_datetimeのみがawareな場合
        return like_timezone.localize(select_datetime)
    elif not like_datetime_is_aware and select_datetime_is_aware:# select_datetimeのみがawareな場合
        return select_datetime.replace(tzinfo=None)
    elif like_datetime_is_aware and select_datetime_is_aware:# select_datetime, like_datetimeがどちらもawareな場合
        if str(like_datetime.tzinfo) != str(select_datetime.tzinfo):
            return select_datetime.astimezone(like_timezone)
        else:
            return select_datetime


def check_workday_intraday_jp(select_datetime):
    """
    与えられたdatetime.datetimeが営業日・営業時間内であるかどうかを出力する
    select_datetime: datetime.datetime
        入力するdatetime
    """
    assert isinstance(select_datetime, datetime.datetime)

    select_date = select_datetime.date()
    # 休日であるかどうか
    is_holiday = (option.holidays_date_array==select_date).sum() > 0
    
    # 休日曜日であるかどうか
    is_holiday_weekday = select_date.weekday() in set(option.holiday_weekdays)
    
    # 営業時間であるかどうか
    select_time = select_datetime.time()
    is_intraday = any([one_borders[0] <= select_time and select_time < one_borders[1] for one_borders in option.intraday_borders])
    
    is_workday_intraday = not any([is_holiday, is_holiday_weekday, not is_intraday])
    return is_workday_intraday


def get_near_workday_intraday_jp(select_datetime, is_after=True):
    """
    引数のdatetime.datetimeが営業日・営業時間の場胃はそのまま，そうでない場合は最も近い境界を境界シンボルとともに返す．
    Paremeters
    ----------
    select_datetime: datetime.datetime
        指定する日時
    is_after: bool
        後ろを探索するかどうか
        
    Returns
    -------
    out_datetime: datetime.datetime
        営業日・営業時間（あるいはボーダー）の日時
    boder_symbol: str
        out_datetimeがボーダーなあるか・そうだとして開始か終了かを示す文字列
            "border_intra": 営業時間内
            "border_start": 営業時間の開始時刻
            "border_end": 営業時間の終了時刻
    """
    assert isinstance(select_datetime, datetime.datetime)
    select_date = select_datetime.date()
    
    if check_workday_jp(select_date):  # 営業日の場合
        if check_workday_intraday_jp(select_datetime):  # 営業時間・営業日の場合
            return select_datetime, "border_intra"
        else:
            select_time = select_datetime.time()
            border_starts = [one_borders[0] for one_borders in option.intraday_borders]
            border_ends = [one_borders[1] for one_borders in option.intraday_borders]
            
            if is_after:
                bigger_border_starts = [one_border for one_border in border_starts if one_border > select_time]
                if len(bigger_border_starts) > 0:
                    out_time = min(bigger_border_starts)
                    out_datetime = datetime.datetime(select_date.year,
                                                     select_date.month,
                                                     select_date.day,
                                                     out_time.hour,
                                                     out_time.minute,
                                                     out_time.second
                                                    )
                    out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
                    return out_datetime, "border_start"
                else:
                    out_date = get_near_workday_jp(select_date, is_after=True)
                    out_time = min(border_starts)
                    out_datetime = datetime.datetime(out_date.year,
                                                     out_date.month,
                                                     out_date.day,
                                                     out_time.hour,
                                                     out_time.minute,
                                                     out_time.second
                                                    )
                    out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
                    return out_datetime, "border_start"
            
            else:
                smaller_border_ends = [one_border for one_border in border_ends if one_border <= select_time]
                if len(smaller_border_ends) > 0:
                    out_time = max(smaller_border_ends)
                    out_datetime = datetime.datetime(select_date.year,
                                                     select_date.month,
                                                     select_date.day,
                                                     out_time.hour,
                                                     out_time.minute,
                                                     out_time.second
                                                    )
                    out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
                    return out_datetime, "border_end"
                else:
                    out_date = get_near_workday_jp(select_date, is_after=False)
                    out_time = max(border_ends)
                    out_datetime = datetime.datetime(out_date.year,
                                                     out_date.month,
                                                     out_date.day,
                                                     out_time.hour,
                                                     out_time.minute,
                                                     out_time.second
                                                    )
                    out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
                    return out_datetime, "border_end"
            
    else:  # 営業日でない場合
        if is_after:
            border_starts = [one_borders[0] for one_borders in option.intraday_borders]
            out_date = get_near_workday_jp(select_date, is_after=True)
            out_time = min(border_starts)
            out_datetime = datetime.datetime(out_date.year,
                                             out_date.month,
                                             out_date.day,
                                             out_time.hour,
                                             out_time.minute,
                                             out_time.second
                                            )
            out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
            return out_datetime, "border_start"
        else:
            border_ends = [one_borders[1] for one_borders in option.intraday_borders]
            out_date = get_near_workday_jp(select_date, is_after=False)
            out_time = max(border_ends)
            out_datetime = datetime.datetime(out_date.year,
                                             out_date.month,
                                             out_date.day,
                                             out_time.hour,
                                             out_time.minute,
                                             out_time.second
                                            )
            out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
            return out_datetime, "border_end"

if __name__ == "__main__":
    pass