# Алгоритмы сжатия данных

Проект по реализации различных алгоритмов сжатия данных и их комбинаций.

## Реализованные алгоритмы

### BWT (Burrows-Wheeler Transform)
- Преобразование Барроуза-Уилера
- Реализованы функции кодирования и декодирования
- Использует нулевой символ как терминатор

### MTF (Move-To-Front)
- Алгоритм перемещения в начало
- Работает с заданным алфавитом
- Часто используется в комбинации с BWT

## Структура проекта

```
.
├── compressor/
│   ├── __init__.py
│   ├── bwt.py
│   └── mtf.py
├── tests/
│   ├── __init__.py
│   ├── tests.py
│   └── tests_pipeline.py
└── text_analizer/
    └── analyze_charset.py
```

## Использование

### BWT
```python
from compressor import bwt_encode, bwt_decode

# Кодирование
text = "banana"
encoded, index = bwt_encode(text)

# Декодирование
decoded = bwt_decode(encoded, index)
```

### MTF
```python
from compressor import mtf_encode, mtf_decode

# Определение алфавита
alphabet = list("abcde")

# Кодирование
encoded = mtf_encode(text, alphabet)

# Декодирование
decoded = mtf_decode(encoded, alphabet)
```

### Комбинированное использование
```python
# BWT + MTF
bwt_text, idx = bwt_encode(text)
mtf_encoded = mtf_encode(bwt_text, alphabet)

# MTF + BWT
mtf_decoded = mtf_decode(mtf_encoded, alphabet)
recovered = bwt_decode(mtf_decoded, idx)
```

## Тестирование

Запуск тестов:
```bash
python -m tests.tests_pipeline
```

## Требования

- Python 3.6+
- Стандартная библиотека Python (без внешних зависимостей) 