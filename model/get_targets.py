import numpy as np
import pandas as pd
from enum import IntEnum

class DirectionThresholdTarget(IntEnum):
    NEUTRAL = 0
    UP = 1
    DOWN = 2

class BuyThresholdTarget(IntEnum):
    NEUTRAL = 0
    UP = 1

class AbnormalTarget(IntEnum):
    NORMAL = 0
    ABNORMAL = 1

def get_direction_with_threshold_target(dataset: pd.DataFrame, time_lag: int, threshold: float) -> pd.Series:
    diffs = dataset["close"].diff(time_lag).shift(-time_lag)
    target = np.zeros(dataset.shape[0], dtype=np.float32)
    target[diffs - threshold > 0] = DirectionThresholdTarget.UP.value
    target[diffs + threshold < 0] = DirectionThresholdTarget.DOWN.value
    target[np.abs(diffs) < threshold] = DirectionThresholdTarget.NEUTRAL.value
    target[diffs.isna()] = np.nan
    return pd.Series(target, name="target")

def get_direction_with_fractional_threshold_target(dataset: pd.DataFrame, time_lag: int, fraction: float) -> pd.Series:
    diffs = dataset["close"].diff(time_lag).shift(-time_lag)
    thresholds = dataset["close"] * fraction
    target = np.zeros(dataset.shape[0], dtype=np.float32)
    target[diffs - thresholds > 0] = DirectionThresholdTarget.UP.value
    target[diffs + thresholds < 0] = DirectionThresholdTarget.DOWN.value
    target[np.abs(diffs) < thresholds] = DirectionThresholdTarget.NEUTRAL.value
    target[diffs.isna()] = np.nan
    return pd.Series(target, name="target")

def get_direction_with_std_threshold_target(dataset: pd.DataFrame, time_lag: int, window: int, factor: float) -> pd.Series:
    diffs = dataset["close"].diff(time_lag).shift(-time_lag)
    thresholds = dataset["close"].rolling(window).std() * factor
    target = np.zeros(dataset.shape[0], dtype=np.float32)
    target[diffs - thresholds > 0] = DirectionThresholdTarget.UP.value
    target[diffs + thresholds < 0] = DirectionThresholdTarget.DOWN.value
    target[np.abs(diffs) < thresholds] = DirectionThresholdTarget.NEUTRAL.value
    target[diffs.isna()] = np.nan
    return pd.Series(target, name="target")

def get_buy_signal_with_std_threshold_target(dataset: pd.DataFrame, time_lag: int, window: int, factor: float) -> pd.Series:
    diffs = dataset["close"].diff(time_lag).shift(-time_lag)
    thresholds = dataset["close"].rolling(window).std() * factor
    target = np.zeros(dataset.shape[0], dtype=np.float32)
    target[diffs - thresholds > 0] = BuyThresholdTarget.UP.value
    target[diffs - thresholds <= 0] = BuyThresholdTarget.NEUTRAL.value
    target[diffs.isna()] = np.nan
    return pd.Series(target, name="target")

def get_abnormal_returns_target(dataset: pd.DataFrame, time_lag: int, threshold: float) -> pd.Series:
    diffs = dataset["close"].diff(time_lag).shift(-time_lag)
    target = np.zeros(dataset.shape[0], dtype=np.float32)
    target[np.abs(diffs) > threshold] = AbnormalTarget.ABNORMAL.value
    target[np.abs(diffs) <= threshold] = AbnormalTarget.NORMAL.value
    target[diffs.isna()] = np.nan
    return pd.Series(target, name="target")

def get_abnormal_returns_with_std_target(dataset: pd.DataFrame, time_lag: int, window: int, factor: float) -> pd.Series:
    diffs = dataset["close"].diff(time_lag).shift(-time_lag)
    thresholds = dataset["close"].rolling(window).std() * factor
    target = np.zeros(dataset.shape[0], dtype=np.float32)
    target[np.abs(diffs) > thresholds] = AbnormalTarget.ABNORMAL.value
    target[np.abs(diffs) <= thresholds] = AbnormalTarget.NORMAL.value
    target[diffs.isna()] = np.nan
    return pd.Series(target, name="target")