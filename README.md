# Yadro


## Получение отчетов: 
   Установка allure 
   
   В командной строке
   
       Mac OS
          brew install allure

       Windows 
          scoop install allure


## Как запустить:
   Создайте venv и установите требования
   
   cd (путь к папки с проектом)
       
       Mac OS
          python3 -m venv env
          source env/bin/activate - for Unix or MacOS
          pip install -r requirements
  
        Windows
          py -m venv env
          .\env\Scripts\activate
          py -m pip install -r requirements.txt


## Запуск программы:
   В командной строке 
         
          python csvreader.py --path csv\file.csv  



## Провести тест:
   В командной строке
   
          python -m pytest --alluredir=test_results_2/ tests/test_validate_csv.py 



## Сгенерировать отчет:
   В командной строке 
   
          allure serve test_results_2/


## Краткое описание отчета:
| Название | Файлы | Описание |
|:----|:----:|:----------|
| Недопустимые значения | test_broken.csv, test_broken_headers.csv, test_invalid_character.csv | Была получена правильная ошибка с недопустимыми значениями в csv  |
| Корректные значения 	| file.csv, test_nested.csv |	Получены результаты проверки корректных файлов |
| Деление на 0	| test_zero.csv	| Была получена правильная ошибка при проверки деления на ноль и пустой ячейкой |
| Пустой файл | test_empty.csv  |	Была получена правильная ошибка с пустым csv-файлом |
