# Домашнее задание №3
## Основы работы с Kubernetes

### Вариант 1 (С КОДОМ)

#### Шаг 1. Создать минимальный сервис, который
1. отвечает на порту 8000
2. имеет http-метод GET /health/

GET /health/
RESPONSE: {"status": "OK"}

#### Шаг 2. Cобрать локально образ приложения в докер.
- Запушить образ в dockerhub

#### Шаг 3. Написать манифесты для деплоя в k8s для этого сервиса.

- Манифесты должны описывать сущности: Deployment, Service, Ingress.
- В Deployment могут быть указаны Liveness, Readiness пробы.
- Количество реплик должно быть не меньше 2. Image контейнера должен быть указан с Dockerhub.
- Хост в ингрессе должен быть arch.homework. В итоге после применения манифестов GET запрос на http://arch.homework/health должен отдавать {“status”: “OK”}.

#### Шаг 4. На выходе предоставить
- ссылку на github c манифестами (в виде pull request). Манифесты должны лежать в одной директории, так чтобы можно было их все применить одной командой kubectl apply -f .
- url, по которому можно будет получить ответ от сервиса (либо тест в postmanе).

###### Задание со звездой:
В Ingress-е должно быть правило, которое форвардит все запросы с /otusapp/{student name}/* на сервис с rewrite-ом пути. Где {student name} - это имя студента.
Например: curl arch.homework/otusapp/aeugene/health -> рерайт пути на arch.homework/health

### Как запустить
#### Шаги 1 и 2 выполнены в рамках предыдущего ДЗ
#### в /etc/hosts прописываем
```
127.0.0.1 arch.homework 
```

#### Запускаем docker
```
любым вариантом, у меня docker desktop с виртуализацией VT-d
```

#### Запускаем minikube
```
minikube start --driver=docker
```

#### Переходим в папку nginx
```
cd ./nginx
```

#### Ставим контроллер Nginx
```
kubectl create namespace m
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx/
helm repo update
helm install nginx ingress-nginx/ingress-nginx --namespace m -f nginx_ingress.yaml
```

#### Переходим в папку манифестов деплоя
```
cd ../"deploy yamls"
```

#### Применяем все манифесты
```
kubectl apply -f .
```

#### Открываем второй экземпляр консоли, вводим команду И НЕ ЗАКРЫВАЕМ
```
minikube tunnel
```

#### Проверяем базу
```
curl http://arch.homework/health/
curl http://arch.homework/health
```
#### С Rewrite'ом
```
curl arch.homework/otusapp/aeugene/health
curl arch.homework/otusapp/aeugene/health/
```