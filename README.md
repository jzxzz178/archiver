# Алгоритмы сжатия данных

Архиватор

## Реализованные алгоритмы

* BWT (Burrows-Wheeler Transform)
* MTF (Move-To-Front)
* ZLE (Zero Length Encoding)
* ARI (Arithmetic Coding)

## Использование

#### Сжатие файла:
```bash
python main.py compress input.txt compressed.arch
```
Сжать содержащийся в проекте текст:
```bash
python main.py compress '.\text_analyzer\Crime and Punishment by Fyodor Dostoyevsky 2.txt' compressed.json
```

#### Распаковка файла:
```bash
python main.py decompress compressed.json decompressed.txt
```

### Анализ энтропии и сжатия

Для анализа энтропии и эффективности сжатия текстовых файлов используйте скрипт `entropy_analyzer.py`:

```bash
python text_analyzer/entropy_analyzer.py
```

Скрипт выполнит:
1. Анализ энтропии текста для разных размеров блоков
2. Тестирование сжатия для каждого размера блока
3. Запишет результаты в файл `text_analyzer/analysis_results.txt`

Результаты включают:
- Среднюю энтропию для каждого размера блока
- Время сжатия
- Размер сжатого файла

## Тестирование

Запуск тестов:
```bash
python -m tests.tests_pipeline
```
