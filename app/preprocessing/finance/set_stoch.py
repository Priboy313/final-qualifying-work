
import pandas as pd

if __name__ == "__main__":
    from cls_over import cls_over

if __name__ != "__main__":
    from finance.cls_over import cls_over

# Функция для проверки наличия необходимых колонок в DataFrame
def validate_dataframe(df: pd.DataFrame, required_columns: list) -> None:
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Input DataFrame must contain the '{col}' column.")

# Функция для расчёта скользящего максимума
def calculate_rolling_max(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=1).max()

# Функция для расчёта скользящего минимума
def calculate_rolling_min(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=1).min()

# Функция для расчёта стохастического осциллятора %K
def calculate_stochastic_k(close: pd.Series, low: pd.Series, high: pd.Series) -> pd.Series:
    result = (close - low) / (high - low)
    return result * 100

# Функция для сдвига значений серии на заданное количество периодов
def shift_series(series: pd.Series, periods: int) -> pd.Series:
    return series.shift(periods=periods)

# Функция для применения классификации к значениям серии
def apply_classification(series: pd.Series, func) -> pd.Series:
    return series.apply(func)

# Функция для добавления сдвинутых колонок в DataFrame
def add_shifted_columns(df: pd.DataFrame, base_column: str, segments: int, abs_seg: bool, clas: bool, cls_func) -> None:
    for i in range(segments):
        shift_ = i + 1
        shifted_column_name = f"{base_column}_{shift_}"
        df[shifted_column_name] = shift_series(df[base_column], periods=shift_)
        if clas:
            classified_column_name = f"{base_column}_cls_{shift_}"
            df[classified_column_name] = shift_series(df[f"{base_column}_cls"], periods=shift_)

# Основная функция для расчёта стохастического осциллятора
def set_stoch(df: pd.DataFrame, 
              segments: int = 0, 
              abs_seg:  bool = True, 
              clas:     bool = True,
              k_period: int = 14,
              d_period: int = 3) -> pd.DataFrame:

    validate_dataframe(df, ['high', 'low', 'close'])  
    n_high = calculate_rolling_max(df['high'], k_period)
    n_low = calculate_rolling_min(df['low'], k_period)
    stoch_k = calculate_stochastic_k(df['close'], n_low, n_high)
    df['stoch'] = stoch_k

    if clas:
        df['stoch_cls'] = apply_classification(stoch_k, cls_over)

    if segments > 0:
        add_shifted_columns(df, 'stoch', segments, abs_seg, clas, cls_over)

    return df

# Дополнительная функция для логирования DataFrame
def log_dataframe(df: pd.DataFrame, message: str = "") -> None:
    print(message)
    print(df.head())

# Функция для тестирования
def main():
    sample_data = {
        'high': [10, 12, 15, 14, 16, 18, 20, 22],
        'low': [5, 6, 7, 8, 9, 10, 11, 12],
        'close': [7, 9, 11, 13, 15, 17, 19, 21]
    }
    df = pd.DataFrame(sample_data)
    segments    = 3     # Количество сегментов для сдвига
    abs_seg     = True  # Флаг абсолютного сдвига
    clas        = True  # Флаг использования классификации
    k_period    = 5     # Период для расчёта стохастического осциллятора
    d_period    = 3     # Период для сглаживания (если требуется)

    result_df = set_stoch(df, segments=segments, abs_seg=abs_seg, clas=clas, k_period=k_period, d_period=d_period)
    log_dataframe(result_df, "Final DataFrame:")

if __name__ == "__main__":
    main()
