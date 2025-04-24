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
# пример
python main.py compress '.\text_analyzer\Crime and Punishment by Fyodor Dostoyevsky 2.txt' output.json
```

#### Распаковка файла:
```bash
python main.py decompress compressed.arch output.txt
```


## Тестирование

Запуск тестов:
```bash
python -m tests.tests_pipeline
```