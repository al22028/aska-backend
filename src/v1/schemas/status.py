# Standard Library
from enum import Enum


class Status(Enum):
    """Status Enum"""

    pending = "PENDING"  # 待機状態
    preprocessing = "PREPROCESSING"  # 前処理中
    preprocessed = "PREPROCESSED"  # 前処理完了
    preprocessing_timedout = "PREPROCESSING_TIMEDOUT"  # 前処理タイムアウト
    preprocessing_failed = "PREPROCESSING_FAILED"  # 前処理失敗
    matching_calculation = "MATCHING_CALCULATION_IN_PROGRESS"  # マッチング計算中
    matching_calculation_timedout = "MATCHING_CALCULATION_TIMEDOUT"  # マッチング計算タイムアウト
    matching_calculation_failed = "MATCHING_CALCULATION_FAILED"  # マッチング計算失敗
    matching_calculation_success = "MATCHING_CALCULATION_SUCCESS"  # マッチング計算成功
    differential_calculation = "DIFFERENTIAL_CALCULATION_IN_PROGRESS"  # 差分計算中
    differential_calculation_timedout = "DIFFERENTIAL_CALCULATION_TIMEDOUT"  # 差分計算タイムアウト
    differential_calculation_no_differences_found = (
        "DIFFERENTIAL_CALCULATION_NO_DIFFERENCES_FOUND"  # 差分検出なし
    )
    differential_calculation_failed = "DIFFERENTIAL_CALCULATION_FAILED"  # 差分計算失敗
    differential_calculation_not_enough_matches = (
        "DIFFERENTIAL_CALCULATION_NOT_ENOUGH_MATCHES"  # マッチング数不足
    )
    completed = "COMPLETED"  # 正常終了
    failed = "FAILED"  # 異常終了
    canceled = "CANCELED"  # キャンセル
    retry = "RETRY"  # 再実行
