# Yadro

## Как запустить:
   Создайте venv и установите требования
   
   В командной строке
   
   cd (путь к папки с проектом)
       
       Mac OS
          python3 -m venv env
          source env/bin/activate - for Unix or MacOS
          pip install -r requirements
  
        Windows
          py -m venv env
          .\env\Scripts\activate
          py -m pip install -r requirements.txt




## Получение отчетов: 
   Установка allure 
   
       Mac OS
          brew install allure

       Windows 
          scoop install allure


## Запуск программы:
   В командной строке 
         
          python csvreader.py --path csv\file.csv  



## Провести тест:
   В командной строке
   
          python -m pytest --alluredir=test_results_2/ tests/test_validate_csv.py 



## Сгенерировать отчет:
   В командной строке 
   
          allure serve test_results_2/
