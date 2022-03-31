class GeneticAlgorithm:
    def __init__(self):
        ...

    def mutation(self):
        ...

    def crossingover(self):
        ...

'''
Необходимый уровень мониторинга сервиса
RAM, HDD, CPU; Prometheus + Grafana, ELK = elasticsearch + logstash + kibana, logstash собирает логи, elastic search движок поиска


Достаточный уровень мониторинга сервиса
sentry, startupProbe, healthcheck
Используйте readiness probes, чтобы определить, когда pod готов принимать трафик.
Используйте liveness probes только тогда, когда они действительно необходимы.
Неверное использование readiness/liveness probes может привести к снижению доступности и каскадным сбоям.
Например, 10 подов зависят от одной БД, а одна зависла, все 10 бодов перезапустятся


Паттерны проектирования (применяя в разработке)
понять чужой код гораздо быстрее, время, которое тратится на обсуждение и принятие решения, одинаковое понимание дизайна, понимание работы сторонних инструментов и библиотек
Антипаттерны: копипаст, спагетти код, золотой класс, магические числа, хардкодинг, софткодинг (куча параметризации), старый неиспользуемый код, изобретение велосипедов, комментирование ради комментирования
SOLID - single responsibility, open–closed, Liskov substitution, interface segregation и dependency inversion


Микросервисная архитектура
 - 12 факторов:
Одна кодовая база, отслеживаемая в системе контроля версий, – множество развёртываний
Явно объявляйте и изолируйте зависимости - requirements.txt
Сохраняйте конфигурацию в среде выполнения - переменные окружения
Считайте сторонние службы (backing services) подключаемыми ресурсами - как отдельные сервисы при развертывании
Строго разделяйте стадии сборки и выполнения - build, Quality, (deploy)
Запускайте приложение как один или несколько процессов не сохраняющих внутреннее состояние (stateless)
Экспортируйте сервисы через привязку портов - экспорт портов, чтобы было понятно на какие порты запросы слать
Масштабируйте приложение с помощью процессов - горизонтальное масштабирование
Максимизируйте надёжность с помощью быстрого запуска и корректного завершения работы - graceful stop, SIGTERM
Держите окружения разработки, промежуточного развёртывания (staging) и рабочего развёртывания (production) максимально похожими
Рассматривайте журнал как поток событий - не пишем в файлы, пишем в stderr и stdout
Выполняйте задачи администрирования/управления с помощью разовых процессов - manage.py migrate

Скрытые расходы при распиливании монолита:
Изменение подхода к работе с мастер-данными
Невозможность переиспользования исходного кода монолита
Проектирование системы заново
Создание нового подхода к управлению инфраструктурой
Измерение и проверка SLA каждого микросервиса
Микросервисы добавят на порядок больше точек отказа
Реорганизация команд
Обратная совместимость с монолитом
Интеграция и обучение служб поддержки
Догоняющий поток фич от бизнеса


Обоснование выбора архитектурного решения


Асинхронное взаимодействие через очереди - RabbitMQ, Kafka
RabbitMQ:
RabbitMQ дает гарантии «одноразовой доставки» и «хотя бы одной доставки», но не «ровно одной доставки».
Exchange - маршрутизатор, fanout, direct, topic
* Паблишеры (publishers) отправляют сообщения на exchange’и
* Exchange’и отправляют сообщения в очереди и в другие exchange’и
* RabbitMQ отправляет подтверждения паблишерам при получении сообщения
* Получатели (consumers) поддерживают постоянные TCP-соединения с RabbitMQ и объявляют, какую очередь(-и) они получают
* RabbitMQ проталкивает (push) сообщения получателям
* Получатели отправляют подтверждения успеха/ошибки
* После успешного получения, сообщения удаляются из очередей
Kafka  - партиции, группы консьюмеров, публишер - подписчик, сдвиг в очереди


Масштабирование и отказоустойчивость сервиса
Оси-модель: 4 и 7 уровень, 4 - транспортный уровень TCP или UDP, 7 - уровень протокола HTTP
Липкие сессии, 4-балансеры открывают новые соединения к новому бэкенду, 7-балансеры балансируют пакеты
Шардирование - по строкам или столбцам


Организация процессов взаимодействия на межкомандном уровне
Эффективное взаимодействие - как минимум экономнее
Почему люди чего-то не делают:
1 Нечеткая цель (понял по-своему)
2 Не умеет (сюда же отнесем: не знает)
3 Не может - нет времени к примеру
4 Не хочет - не понимает зачем это нужно
Приемы эффективности
1 Четкое распределение ролей
2 Создание словаря терминов
3 Назначение ответственного исполнителя
4 Ведение записей
5 Подтверждающие фразы - итог
6 Правила использования каналов связи


Обучение и развитие команды
Три типа обучения:
поверхностное обучение (surface learning) 
глубокое обучение (deep learning) 
перенос навыков (transfer).


Постановка задач
Постановка задач по smart - цель конкретна, измерима, достижима, актуальна, ограничена сроком


Декомпозиция бизнес-фичи на атомарные задачи для разработки. Оценка сроков реализации фичи


Базы данных (c точки зрения разработчика)
NoSQL - нереляционная, нет четко заданной структуры
Ключ-значение - Redis, распределенные - Cassandra, документи-ориентированные - MongoDB, на основе графов
Отличия noSQL - скорость, безсхемная разработка, автоматизированная репликация/масштабирование, большой выбор
Postgres - индекс ускоряет доступ к данным, но вставка удаление обновление будут медленнее, можно делать индексы по выражениям, по нескольким колонкам. Если данных мало то индексы не нужны. Также индексы занимают место на диске.
Нормальные формы - 1-ая: атомарность, 2-ая: отсутствие зависимости неключевых полей от части составного ключа, 3-я: исключает зависимость неключевых полей от других неключевых полей
Денормализация - поместить избыточные данные туда, где они смогут принести максимальную пользу, типы: Сохранение исторических данных, Повышение производительности запросов, Ускорение создания отчетов, Предварительные вычисления часто запрашиваемых значений
Минусы денормализации: место на диске, аномалии в данных, документация, замедление других операций, больше кода
pg_stat_kcache - статистика по вызовам, какие запросы жрут больше процессорного времени, потом по самому жирному делаем explain analyze; perf - на что тратится процессор; gdb - отладчик, бэктрейс
Блокировки: access exclusive, share row/update exclusive. Access exclusive может быть оправдана если таблица маленькая. При удалении столбца сначала удаляем все связанные индексы, потом уже сам столбец. Создание столбца требует access exclusive, но на очень короткий промежуток времени. CREATE/DROP INDEX CONCURRENTLY. 
ACID представляет 4 свойства:
A = atomicity (атомарность) - транзакции
C = consistency (консистентность или целостность) - дебит сходится с кредитом
I = isolation (изоляция) - параллельные транзакции как последовательные
D = durability (надежность) - если транзакция была применена, то она ни в коем случае не должна пропасть


ORM (объектно-реляционное отображение)
Технология связывает базы данных с концепциями объектно-ориентированных языков программирования, создавая «виртуальную объектную базу данных»
Идемпотентность миграций
Переключение бэков для работы с обновленной базой


Контейнеры и docker
Данные - bound mount, volume, tmpfs
Многоэтапные (multi-stage builds) сборки в Docker - нужны чтобы при компиляции не тащить мусор била
Уменьшение размера образа - специальные базовые образы, не использовать инструменты для дебага, минимизация слоев (это когда в ран сразу удаляем кэш к примеру)


Инструменты и практики оценки и мониторинга качества кода
Код ревью, статические анализаторы


Нормализация БД - выше


Unit-тесты и Интеграционные тесты
Юнит тесты, интеграционные тесты, Е2Е тестирование
Для маленького проекта возможно тестирование не нужно, для большого - обязательно (где потребуются доработки)
Стаб ничего не проверяет, а лишь имитирует заданное состояние. А мок – это объект, у которого есть ожидания
Покрытие тестами - плохая величина, но легко измеримая, лучше - сколько людей пишут тесты, какое количество багов приводя к написанию тестов
Пирамида тестирования - классический паттерн, надо индивидуально к каждому проекту подходить
Антипаттерны:
1. Модульные тесты без интеграционных
2. Интеграционные тесты без модульных
3. Неправильный тип тестов
4. Тестирование не той функциональности
5. Тестирование внутренней реализации
6. Чрезмерное внимание покрытию тестами
7. Ненадёжные или медленные тесты
8. Запуск тестов вручную
9. Недостаточное внимание коду теста
10. Отказ писать тесты для новых багов из продакшна
11. Отношение к TDD как к религии
12. Написание тестов без предварительного чтения документации
13. Плохое отношение к тестированию по незнанию


Диагностика работы сервиса
Обнаружение проблем на уровне приложения, ОС, железа


Процессы CI/CD
Continuous delivery (непрерывная доставка) - быстрая выкатка на прод
Continuous deployment(непрерывное развёртываение) - на прод без девопса
Continuous integration (непрерывная интеграция) - быстрая доставка в центральный репозиторий
Git Flow (мастер, девелоп, фичи), GitHub Flow (мастер, фичи, немедленная выкатка на прод), GitLab Flow (11 правил), One Flow
Vault


Безопасное программирование
Никогда не доверяйте входным данным от пользователя
Не изобретайте велосипед
Не доверяйте разработчикам
Пишите НАДЁЖНЫЙ код
Пишите тесты


Профилирование и трассировка обработки запросов
Jaeger, Sentry, timeit, python-profiling, etc.


Декомпозиция реализации фичи по архитектуре Точки


Выделение и реализация общекомандных библиотек


Жизненный цикл API сервиса
Идемпотентность АПИ - ключ идемпотентности
REST - jsonRPC: рост проще, много фич типа кэширования гет-запросов, но в то же время надо держать это в уме, джейсонэрписи сложнее, но поддерживает батч-запросы, единая точка входа, проще дебажить ошибки, но при батч-запросах возникают сложности при балансировке


Многопоточность приложения и асинхронное взаимодействие
Параллельность и конкурентность






gitlab-ci.yml

variables:
  KUBERNETES_CPU_LIMIT: 4
  KUBERNETES_MEMORY_LIMIT: 4Gi
  GITLAB_TOKEN: ""
  DOCKER_AUTH_CONFIG: ""
  KUBECTL_STAGE_TOKEN: ""
  KUBECTL_PROD_TOKEN: ""
  IMAGE: "hr-it/one-backend"
  SERVICE: "hr-one"
  APPLICATION: "backend"
  HELM_CHART_VERSION: "5.x"

stages:
  - version
  - build
  - quality
  - deploy

semantic-release:
  stage: version
  tags:
    - k8s
    - stage
  only:
    - master
  image: registry.tochka-tech.com/oci_semantic-release/semantic-release:latest
  variables:
    REPOSITORY: "$CI_SERVER_PROTOCOL://gitlab-ci-token:$GITLAB_TOKEN@$CI_SERVER_HOST:$CI_SERVER_PORT/$CI_PROJECT_PATH.git"
  before_script:
    - git remote set-url origin $REPOSITORY
  script:
    - semantic-release --debug

kaniko:
  stage: build
  tags:
    - k8s
    - stage
  except:
    - tags
  image: registry.tech.bank24.int/hr-it/kaniko:latest
  variables:
    REGISTRY: "registry.tech.bank24.int"
  before_script:
    - export VERSION="$(git describe --tags --always | sed -E 's/^v([0-9]+\.[0-9]+\.[0-9]+)/\1/')"
    - mkdir -p ~/.docker
    - echo "$DOCKER_AUTH_CONFIG" > ~/.docker/config.json
  script:
    - envsubst < .quality-template.env > .quality.env
    - echo -n $VERSION > src/VERSION
    - /kaniko/executor
      --cache=true
      --cache-copy-layers
      --context=$CI_PROJECT_DIR
      --destination=$REGISTRY/$IMAGE:$VERSION
  artifacts:
    reports:
      dotenv: .quality.env

quality:
  stage: quality
  tags:
    - k8s
    - stage
  except:
    - tags
  image: $REGISTRY/$IMAGE:$VERSION

  services:
    - name: registry.tochka-tech.com/proxy_docker-io/library/postgres:11
      alias: postgres
    - name: registry.tochka-tech.com/proxy_docker-io/library/rabbitmq:3.7.17-management-alpine
      alias: rabbitmq
    - name: registry.tochka-tech.com/proxy_docker-io/minio/minio:latest
      alias: minio
      command: [ "server", "/data" ]
  variables:
    POSTGRES_DB: "one"
    POSTGRES_USER: "one"
    POSTGRES_PASSWORD: "one"
    RABBITMQ_DEFAULT_USER: "one"
    RABBITMQ_DEFAULT_PASS: "one"
    MINIO_ACCESS_KEY: "one"
    MINIO_SECRET_KEY: "onepassword"
    APP_DB_HOST: "postgres"
    APP_RABBITMQ_HOST: "rabbitmq"
    APP_AWS_S3_ENDPOINT_URL: "http://minio:9000"
  script:
    - ./scripts/lint
    - ./scripts/test
  coverage: '/^TOTAL.+?(\d+\%)$/'

.deploy:
  tags:
    - k8s
    - stage
  image: registry.tochka-tech.com/oci_helm-builder/helm-builder:latest
  environment:
    name: "$ENVIRONMENT"
  variables:
    ENVIRONMENT: ""
    DEPLOY_TOKEN: ""
  before_script:
    - export VERSION="$(git describe --tags --always | sed -E 's/^v([0-9]+\.[0-9]+\.[0-9]+)/\1/')"
    - kubectl config set-credentials deployer --token="$DEPLOY_TOKEN"
    - kubectl config set-context deploy --cluster="$ENVIRONMENT" --user=deployer --namespace="$SERVICE"
    - kubectl config use-context deploy
    - helm repo update
    - envsubst < values-template.yml > values.yml
    - cat values.yml
  script:
    - helm -n "$SERVICE" upgrade -i --atomic --version="$HELM_CHART_VERSION" -f values.yml "$APPLICATION" devexp/hell --debug

.deploy-stage:
  extends: .deploy
  variables:
    ENVIRONMENT: "stage"
    DEPLOY_TOKEN: "$KUBECTL_STAGE_TOKEN"

.deploy-prod:
  extends: .deploy
  tags:
    - k8s
    - prod
  variables:
    KUBERNETES_CPU_LIMIT: 2
    KUBERNETES_MEMORY_LIMIT: 2Gi
    ENVIRONMENT: "prod"
    DEPLOY_TOKEN: "$KUBECTL_PROD_TOKEN"

deploy-stage:
  extends: .deploy-stage
  stage: deploy
  only:
    - master

deploy-stage-manual:
  extends: .deploy-stage
  stage: deploy
  when: manual
  except:
    - tags
    - master

deploy-prod:
  extends: .deploy-prod
  stage: deploy
  when: manual
  only:
    - master



values-template.yml

serviceName: "$SERVICE"
chartVersion: "$HELM_CHART_VERSION"
deploymentType: single
applications:
  backend:
    parameters:
      whiteIPs: default
    ports:
    - port: 80
      protocol: http
      ingress: vpn
    replicas: 2
    vaultSecrets:
      mount: /var/run/secrets/app
      secrets:
        - vaultPath: backend
    initContainers:
      migrate:
        image: registry.tech.bank24.int/hr-it/one-backend
        imageTag: "$VERSION"
        imagePullPolicy: Always
        args: [ "python", "manage.py", "migrate", "--lock" ]
        resources:
          limits: { memory: "256Mi", cpu: "1.1" }
          requests: { memory: "64Mi", cpu: "0.22" }
      collectstatic:
        image: registry.tech.bank24.int/hr-it/one-backend
        imageTag: "$VERSION"
        imagePullPolicy: Always
        args: [ "python", "manage.py", "collectstatic", "--noinput" ]
        resources:
          limits: { memory: "256Mi", cpu: "1.1" }
          requests: { memory: "64Mi", cpu: "0.22" }
        volumes:
          emptydirs:
          - name: static
            mountpath: /static
    containers:
      app:
        image: registry.tech.bank24.int/hr-it/one-backend
        imageTag: "$VERSION"
        args: [ "gunicorn", "--config", "gunicorn_config.py", "config.wsgi" ]
        resources:
          limits: { memory: "512Mi", cpu: "1" }
          requests: { memory: "256Mi", cpu: "0.2" }
        livenessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
      nginx:
        image: registry.tech.bank24.int/hr-it/nginx-k8s
        imageTag: 1.19.4-alpine
        resources:
          limits: { memory: "32Mi", cpu: "0.1" }
          requests: { memory: "16Mi", cpu: "0.02" }
        volumes:
          emptydirs:
          - name: static
            mountpath: /static
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
  esbworker:
    replicas: 1
    strategy:
      type: Recreate
    vaultSecrets:
      mount: /var/run/secrets/app
      secrets:
        - vaultPath: backend
    containers:
      app:
        image: registry.tech.bank24.int/hr-it/one-backend
        imageTag: "$VERSION"
        args: [ "python", "manage.py", "esbworker" ]
        resources:
          limits: { memory: "512Mi", cpu: "1" }
          requests: { memory: "256Mi", cpu: "0.4" }
        livenessProbe:
          exec:
            command: [ "./entrypoint.sh", "python", "esbworker_healthcheck.py" ]
          initialDelaySeconds: 300
          periodSeconds: 30
          timeoutSeconds: 5
  buslistener:
    replicas: 1
    strategy:
      type: Recreate
    vaultSecrets:
      mount: /var/run/secrets/app
      secrets:
        - vaultPath: backend
    containers:
      app:
        image: registry.tech.bank24.int/hr-it/one-backend
        imageTag: "$VERSION"
        args: [ "python", "manage.py", "bus_listener" ]
        resources:
          limits: { memory: "512Mi", cpu: "1" }
          requests: { memory: "256Mi", cpu: "0.2" }
  bussender:
    replicas: 1
    strategy:
      type: Recreate
    vaultSecrets:
      mount: /var/run/secrets/app
      secrets:
        - vaultPath: backend
    containers:
      app:
        image: registry.tech.bank24.int/hr-it/one-backend
        imageTag: "$VERSION"
        args: [ "python", "manage.py", "bus_sender" ]
        resources:
          limits: { memory: "128Mi", cpu: "1" }
          requests: { memory: "128Mi", cpu: "0.2" }
  celery:
    parameters:
      whiteIPs: default
    replicas: 1
    strategy:
      type: Recreate
    vaultSecrets:
      mount: /var/run/secrets/app
      secrets:
        - vaultPath: backend
    containers:
      app:
        image: registry.tech.bank24.int/hr-it/one-backend
        imageTag: "$VERSION"
        args: [ "./celery_worker.sh" ]
        resources:
          limits: { memory: "1024Mi", cpu: "1.2" }
          requests: { memory: "512Mi", cpu: "0.6" }
        livenessProbe:
          exec:
            command: [ "./entrypoint.sh", "./celery_healthcheck.sh" ]
          initialDelaySeconds: 30
          periodSeconds: 5
          timeoutSeconds: 5
  celery-beat:
    replicas: 1
    strategy:
      type: Recreate
    vaultSecrets:
      mount: /var/run/secrets/app
      secrets:
        - vaultPath: backend
    containers:
      app:
        image: registry.tech.bank24.int/hr-it/one-backend
        imageTag: "$VERSION"
        args: [ "celery", "-A", "config", "beat", "-l", "info", "--scheduler", "config.scheduler:S3Scheduler" ]
        resources:
          limits: { memory: "256Mi", cpu: "1.1" }
          requests: { memory: "192Mi", cpu: "0.22" }
        livenessProbe:
          exec:
            command: [ "./entrypoint.sh", "python", "celery_beat_healthcheck.py" ]
          initialDelaySeconds: 30
          periodSeconds: 30
          timeoutSeconds: 5
  metrics:
    ports:
      - port: 8080
        protocol: tcp
        monitoring:
          enabled: true
    replicas: 1
    strategy:
      type: Recreate
    vaultSecrets:
      mount: /var/run/secrets/app
      secrets:
        - vaultPath: backend
    containers:
      app:
        image: registry.tech.bank24.int/hr-it/one-backend
        imageTag: "$VERSION"
        args: [ "python", "manage.py", "metrics" ]
        resources:
          limits: { memory: "128Mi", cpu: "0.55" }
          requests: { memory: "128Mi", cpu: "0.11" }



docker-compose.yml

version: "3.7"

services:
  broker:
    image: rabbitmq:3.7.17-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: "filesync"
      RABBITMQ_DEFAULT_PASS: "filesync"
  s3:
    image: minio/minio
    command: "server /data"
    ports:
      - "9000:9000"
    environment:
      MINIO_ACCESS_KEY: "filesync"
      MINIO_SECRET_KEY: "filesync"
  smb:
    image: dperson/samba
    ports:
      - "139:139"
      - "445:445"
    volumes:
      - ./tests/files/smb:/smb-files
    environment:
      USER: "filesync;filesync"
      WORKGROUP: "TEST"
      SHARE: "files;/smb-files;yes;yes"



Dockerfile

FROM registry.tech.bank24.int/hr-it/python:3.10

ENV POETRY_VIRTUALENVS_CREATE=0

ENV PYTHONPATH=/app

WORKDIR /app

ENTRYPOINT [ "/app/entrypoint.sh" ]

COPY pyproject.toml poetry.lock ./

RUN pip install -U pip && poetry install && rm -rf /root/.cache/*

COPY . .

CMD [ "python", "-V" ]



setup.cfg

[isort]
line_length = 120
force_single_line = 1
skip = venv

[mypy]
python_version = 3.10
strict = True
ignore_missing_imports = True
no_implicit_optional = True
strict_equality = True
warn_redundant_casts = True
warn_unused_configs = True
warn_unused_ignores = True
warn_unreachable = True
exclude = venv

[tool:pytest]
addopts = --cov=app




entrypoint.sh


#!/usr/bin/env bash

set -e

if [[ -d /var/run/secrets/app ]]; then
  . load-env /var/run/secrets/app
fi

exec "$@"




'''