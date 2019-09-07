docker run --name ub-mariadb -e MYSQL_ROOT_PASSWORD=qwer1234@ -d mariadb

#docker build . -t ubonexnl
#docker run -it -d --name ubonex_nl -p 80:80 --link ub-mariadb:ub-mariadb ubonexnl

docker run -it -d -e UBONEX_ENV='prod_nl' --name ubonex_nl_new -p 8001:80 -v /home/root/work/dockerubonex/app_nl:/home/docker/code/app  --link ub-mariadb:ub-mariadb ubonex
docker run -it -d -e UBONEX_ENV='prod_de' --name ubonex_de -p 8002:80 -v /home/root/work/dockerubonex/app_de:/home/docker/code/app  --link ub-mariadb:ub-mariadb ubonex

docker run --name myadmin -d --link ub-mariadb:db -p 8080:80 phpmyadmin/phpmyadmin

## backup db data
CREATE DATABASE ubonex CHARACTER SET utf8 COLLATE utf8_general_ci;

mysql_container_name=ub-mariadb
mysql_user=root
mysql_password=qwer1234@
mysql_db_name=ubonex

docker exec  -t ${mysql_container_name} /usr/bin/mysqldump -u ${mysql_user} --password=${mysql_password} ${mysql_db_name} > ${mysql_db_name}.`date +%d-%m-%Y"_"%H_%M_%S`.sql

# Restore
cat backup.sql | docker exec -t ${mysql_container_name} /usr/bin/mysql -u ${mysql_user} --password=${mysql_password} ${mysql_db_name}

### DOCKER NETWORKING
#create network
docker network create -d bridge NETWORK_NAME
# create mariadb
docker run --name ub-mariadb -e MYSQL_ROOT_PASSWORD=qwer1234@ -d mariadb
# add this container to our network
docker network connect NETWORK_NAME CONTAINER_NAME
# check network
docker network inspect NETWORK_NAME