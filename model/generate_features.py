import pandas as pd
import numpy as np
from stockstats import StockDataFrame

def indicators_with_rowwise_ewm(dataset: pd.DataFrame, ewm_alpha: float = 0.3, ewm_period: int = 10) -> pd.DataFrame:
    INDICATORS = [
        "volume_26_ema", "volume_42_ema", "volume_86_ema", "volume_174_ema", "volume_363_ema", 
        "volume_42_smma",
        "volume_14_mstd", "volume_26_mstd", "volume_42_mstd", "volume_86_mstd", "volume_174_mstd", 
        "high_42_mstd", "high_86_mstd", "high_174_mstd", 
        "low_42_mstd", "low_86_mstd", "low_174_mstd", 
        "close_42_mstd", "close_86_mstd", "close_174_mstd", "close_363_mstd",
        "vr_26", "vr_86", "vr_174", "vr_363",
        "atr_6", "atr_14",
        "cr", "cr-ma1", "cr-ma2", "cr-ma3",
        "chop_14", "chop_42", "chop_174", "chop_363",
        "mfi_42", "mfi_174", 
        'rsi_42', 'rsi_86', 'rsi_174', 
        'wt2', 
        'close_12_trix', 'close_174_trix', 'close_363_trix',  
        'volume_12_trix', 'volume_174_trix', 'volume_363_trix', 
        'close_12_tema', 'close_174_tema', 'close_363_tema',  
        'volume_12_tema', 'volume_174_tema', 'volume_363_tema',  
        'boll', 'boll_ub', 'boll_lb', 'macdh', 'ppo',
        'vwma', 'vwma_174', 'vwma_363',
        'close_10_kama', 'close_174_kama',
        'supertrend', 'supertrend_ub', 'supertrend_lb'
    ]
    # DROP_COLUMNS = ["t", "n", "vw"]
    RENAME_COLUMNS = {"Close": "close", "High": "high", "Low": "low", "Open": "open", "Volume": "volume"}

    result_dataset = dataset.copy()
    
    # result_dataset.drop(DROP_COLUMNS, axis=1, inplace=True)
    result_dataset.reset_index(drop=True, inplace=True)
    result_dataset.rename(RENAME_COLUMNS, axis=1, inplace=True)

    result_dataset = StockDataFrame(result_dataset)
    
    result_dataset['boll_dif'] = result_dataset['boll_ub'] - result_dataset['boll_lb']
    # result_dataset['pdi_mdi'] = result_dataset['pdi'] - result_dataset['mdi']
    result_dataset['boll_ub_close'] = result_dataset['boll_ub'] - result_dataset['close']
    result_dataset['boll_lb_close'] = result_dataset['close'] - result_dataset['boll_lb']

    # result_dataset = result_dataset.join(result_dataset.ewm(alpha=ewm_alpha, min_periods=ewm_period).mean(), rsuffix="_ewm")
    INDICATORS.extend(['close', 'high', 'low', 'open', 'volume', 'boll_dif', 'boll_ub_close', 'boll_lb_close'])
    result_dataset = result_dataset[INDICATORS]

    return result_dataset

def lstm_indicators(dataset: pd.DataFrame) -> pd.DataFrame:
    INDICATORS = [
        "volume_6_ema", "volume_14_ema", "volume_26_ema", "volume_42_ema", 
        "volume_6_smma", "volume_14_smma", "volume_26_smma", "volume_42_smma",
        "volume_6_mstd", "volume_14_mstd", "volume_26_mstd", "volume_42_mstd",
        "high_6_mstd", "high_14_mstd", "high_26_mstd", "high_42_mstd",
        "low_6_mstd", "low_14_mstd", "low_26_mstd", "low_42_mstd",
        "wt1", "wt2",
        # "vr_6",
        "atr_6",
        "adxr",
        "kdjk_6",
        "cr", "cr-ma1", "cr-ma2", "cr-ma3",
        "macd", "boll",
        "chop_14", "chop_26", "chop_42",
        "mfi_6", "mfi_14", "mfi_26", "mfi_42",
    ]

    DROP_COLUMNS = ["t", "n", "vw"]
    RENAME_COLUMNS = {"c": "close", "h": "high", "l": "low", "o": "open", "v": "volume"}

    result_dataset = dataset.copy()
    
    result_dataset.drop(DROP_COLUMNS, axis=1, inplace=True)
    result_dataset.reset_index(drop=True, inplace=True)
    result_dataset.rename(RENAME_COLUMNS, axis=1, inplace=True)

    stock_df = StockDataFrame(result_dataset)
    stock_df[INDICATORS]

    return stock_df
