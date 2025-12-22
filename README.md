# Домашнее задание №4
## Инфраструктурные паттерны (Работа с Helm'ом)

### Вариант 1 (С КОДОМ)

#### Сделать простейший RESTful CRUD по созданию, удалению, просмотру и обновлению пользователей.

#### Пример API - https://app.swaggerhub.com/apis/otus55/users/1.0.0


#### Добавить базу данных для приложения.

#### Конфигурация приложения должна хранится в Configmaps.

#### Доступы к БД должны храниться в Secrets.

#### Первоначальные миграции должны быть оформлены в качестве Job-ы, если это требуется.

#### Ingress-ы должны также вести на url arch.homework/ (как и в прошлом задании)

#### Добавить шаблонизацию приложения в helm чартах


### КАК РАЗВЕРНУТЬ
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

#### Далее предполагается, что мы находимся в папке с приложением
#### Также предполагается, что контроллер nginx с прошлого ДЗ из кластера никуда не делся
#### Сборку докер-образа также не описываю - образ залит на dockerhub

#### "Внешняя" поставка секрета в кластер
```
kubectl apply -f ./secret/secret.yaml
```

#### Также закидываем в кластер configmap (она нужна для начальной миграции)
```
kubectl apply -f ./kuber/users_configmap.yaml
```

#### Устанавливаем БД в кластер. Пароль для пользователя будет взят из секрета
```
helm install users-postgresql -f ./postgre/db-values.yaml oci://registry-1.docker.io/bitnamicharts/postgresql
Дождаться установки БД
```

#### Запускаем начальную миграцию
```
kubectl apply -f ./kuber/job-migr.yaml
```

#### Проверяем успех миграции
```
kubectl get job
Job-а с именем run-migrations должна быть в статусе "Complete" - ждем этот статус
```

#### Применяем манифесты для деплоя приложухи
```
kubectl apply -f ./kuber/app-deploy/
```

#### Включаем (и не закрываем терминал)
```
minikube tunnel
```

#### Проверяем health-check (в новом окне терминала)
```
curl http://arch.homework/health/
curl http://arch.homework/health
```

#### Запускаем тест-коллекцию (корректно сработает только при первом запуске с чистой БД, т.к. ID пользователей генерируются автоинкрементом)
```
newman run ./postman/hw4_collection.json
```


### КАК УДАЛИТЬ
#### Сносим ingress, service, deployment
```
kubectl delete ingress users-ingress
kubectl delete service users-service
kubectl delete deployment users-app 
```

#### Сносим configmap и secret
```
kubectl delete configmap users-config
kubectl delete secret users-db-secret
```

#### Сносим Job-у миграций
```
kubectl delete job run-migrations
```

#### Сносим БД (ВАЖНО: после удаления остаются PVC и PV, их надо тоже грохнуть)
```
helm uninstall users-postgresql 
```

#### Сносим PVC, оставшиеся от БД
```
kubectl delete pvc -l app.kubernetes.io/name=postgresql,app.kubernetes.io/instance=users-postgresql
```

#### Сносим PV, оставшиеся от БД (если reclaimPolicy: Retain)
```
kubectl get pv
Смотрим вывод, узнаем <имя PV> (к сожалению, меток у него не будет - я проверил)
kubectl delete pv <имя PV>
```

#### Готово!