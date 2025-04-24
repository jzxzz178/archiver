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

Архиватор поддерживает два режима работы: сжатие и распаковка файлов.

#### Сжатие файла:
```bash
python main.py compress input.txt compressed.arch
```

#### Распаковка файла:
```bash
python main.py decompress compressed.arch output.txt
```

## Использование

### BWT
```python
from compressor import bwt_encode, bwt_decode

text = "banana"
encoded, index = bwt_encode(text)
decoded = bwt_decode(encoded, index)
```

### MTF
```python
from compressor import mtf_encode, mtf_decode
alphabet = list("abcde")
encoded = mtf_encode(text, alphabet)
decoded = mtf_decode(encoded, alphabet)
```

### Комбинированное использование
```python
bwt_text, idx = bwt_encode(text)
mtf_encoded = mtf_encode(bwt_text, alphabet)
```

## Тестирование

Запуск тестов:
```bash
python -m tests.tests_pipeline
```