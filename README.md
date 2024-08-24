# Система рекомендаций

Репозиторий: https://github.com/axinedy/mle-recsys-project-start

S3 bucket: s3-student-mle-20240325-3ac233b55a (https://storage.yandexcloud.net)

<br>

## Склонируйте репозиторий

Склонируйте репозиторий проекта:

```
git clone https://github.com/axinedy/mle-recsys-project-start
cd mle-recsys-project-start
```

## Активируйте виртуальное окружение

Создать новое виртуальное окружение можно командой:

```
python3 -m venv env_recsys_start
```

После его инициализации следующей командой

```
chmod +x ./env_recsys_start/bin/activate
./env_recsys_start/bin/activate
```

установите в него необходимые Python-пакеты следующей командой

```
pip install -r requirements.txt
```

### Скачайте файлы с данными

Для начала работы понадобится три файла с данными (из S3 bucket):
```
recommendations.parquet
similar.parquet
top_popular.parquet
```
 
Скачайте их в директорию локального репозитория. 
Для удобства вы можете примонтировать и скопировать следующей командой:

```
./load_data_from_s3.sh 
```
<!---
## Запустите Jupyter Lab

Запустите Jupyter Lab в командной строке

```
jupyter lab --ip=0.0.0.0 --no-browser
```

# Расчёт рекомендаций

Код для выполнения первой части проекта находится в файле `recommendations.ipynb`. Изначально, это шаблон. Используйте его для выполнения первой части проекта.
-->
# Сервис рекомендаций

Код сервиса рекомендаций находится в файле `recommendations_service.py`.

Запустить можно командой:
```
./rec_service.sh
```

# Инструкции для тестирования сервиса

Код для тестирования сервиса находится в файле `test_service.py`.

Запустить пачку тестов можно командой:

```
./batch_test_service.sh
```

Ознакомиться с опциями:
```
./test_service.py
```
