# RunPod Dev Notes

## Что делает сервис

Этот сервис переводит текст в речь.

- Маршрут: `POST /tts/synthesize/`
- Проверка здоровья: `GET /ping`
- Порт по умолчанию: `8000`

Backend можно оставить как есть: после деплоя нужно будет только заменить старый Pod URL на новый Serverless endpoint URL.

## Почему сервис подходит под RunPod Serverless

Этот репозиторий уже поднимает обычный FastAPI HTTP-сервис.
Поэтому для него подходит именно `Serverless Load Balancing`, а не queue-based Serverless.

Почему:

- RunPod Load Balancing поддерживает кастомные HTTP endpoints
- он умеет работать с любым HTTP framework
- `/ping` используется для проверки готовности
- у сервиса уже есть свои обычные HTTP маршруты

Документация:

- [RunPod Load Balancing Overview](https://docs.runpod.io/serverless/load-balancing/overview)
- [RunPod Endpoints Overview](https://docs.runpod.io/serverless/endpoints/overview)

## Как правильно деплоить

Рекомендуемый порядок такой:

1. Собрать Docker image локально на своем компьютере.
2. Запушить image в container registry.
3. В RunPod Serverless создать новый endpoint через `Import from Docker Registry`.
4. Выбрать тип `Load Balancing`.
5. Подставить новый endpoint URL в backend.

Важно:

- RunPod не видит твой локальный Docker image напрямую.
- Локальная сборка не тратит деньги RunPod.
- Деньги RunPod начнут тратиться, когда будет создан endpoint и пойдут запросы.

Документация:

- [RunPod Quickstart](https://docs.runpod.io/serverless/quickstart)
- [RunPod Workers Overview](https://docs.runpod.io/serverless/workers/overview)

## Что уже готово в этом репозитории

- реализован `GET /ping`
- реализован `POST /tts/synthesize/`
- запуск идет через `PORT` и env переменные
- в рантайме больше нет `pip install`, `git pull`, `git lfs pull` и загрузки моделей
- есть `Dockerfile` для деплоя
- локальный `MeloTTS` ставится во время `docker build`
- локальные `melo_models` и `piper_models` копируются внутрь image

Это значит, что image должен приезжать в RunPod уже подготовленным, а не скачивать зависимости на каждом старте.

## Оценка готовности

Текущий статус: `подходит для деплоя, но более хрупкий, чем STT`

Почему этот сервис сложнее:

- он сочетает `MeloTTS` и `Piper`
- у `MeloTTS` менее стандартная установка
- для `MeloTTS` нужен `python -m unidic download`
- цепочка зависимостей здесь больше, чем у STT
- сам image, скорее всего, получится тяжелее

Что еще не подтверждено на практике:

- первая реальная сборка `docker build`
- первый реальный запуск в RunPod
- точная совместимость зависимостей при сборке image

То есть код уже подходит как база для деплоя, но именно TTS с большей вероятностью потребует еще одну небольшую доработку во время первой сборки.

## Примечание по Melo

`MeloTTS` здесь используется не как обычный pip-пакет из PyPI.
Он ожидается как папка с репозиторием и ставится во время сборки image.

Что важно:

- в репозитории есть локальная папка `MeloTTS`
- в `.gitmodules` стоит форк `Elixir-team/MeloTTS`
- Docker image ставит `./MeloTTS`
- `python -m unidic download` выполняется во время `docker build`

Ссылки:

- [Local Melo install doc](/C:/Users/lenovo/Desktop/tts_server/MeloTTS/docs/install.md)
- [Local Melo setup.py](/C:/Users/lenovo/Desktop/tts_server/MeloTTS/setup.py)
- [Official Melo install doc](https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md)

## Примечание по формату ответа

Сервис понимает и полные MIME types, например `audio/mpeg`, и короткие алиасы, например `mp3`.
Это сделано для того, чтобы минимально трогать backend, если он уже отправляет `mp3` в `mediaType`.

Формат ответа по умолчанию:

- `audio/mpeg`

## Рекомендуемые настройки RunPod для dev

- Тип endpoint: `Load Balancing`
- Тип worker: `CPU`
- Active workers: `0`
- Min workers: `0`
- Max workers: `1`
- Idle timeout: `5s`

Это самый дешевый режим для dev: worker поднимается только когда приходит запрос.

Документация:

- [RunPod Endpoint Settings](https://docs.runpod.io/serverless/endpoints/endpoint-configurations)

## Переменные окружения

- `PORT=8000`
- `DEFAULT_MEDIA_TYPE=audio/mpeg`
- `SLOW_REQUEST_SECONDS=1.0`
- `MELO_DEVICE=auto`
- `PIPER_USE_CUDA=false`

## Сборка image

```bash
docker build --platform linux/amd64 -t YOUR_REGISTRY/tts-serverless:dev .
docker push YOUR_REGISTRY/tts-serverless:dev
```

## Главный практический вывод

Этот код можно использовать как основу для деплоя.
Правильный рабочий путь такой:

- собрать image локально
- запушить его в registry
- создать RunPod endpoint из этого image

Главный оставшийся риск здесь не в API и не в маршрутах.
Главный оставшийся риск — первая сборка image для `MeloTTS` и `Piper`.
