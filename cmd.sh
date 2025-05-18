docker compose --env-file .env.dev --file compose.dev.yml up -d --build

docker compose --env-file .env.dev --file compose.dev.yml down #-v

#
sudo apt-get install unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc


#
# DOCKER BACKUP
#

docker run --rm --mount source=multishopp2_media_volume,target=/data -v $(pwd):/backup busybox tar -czvf /backup/mediafile.tar.gz /data
docker run --rm --mount source=multishopp2_msql-data,target=/data -v $(pwd):/backup busybox tar -czvf /backup/msqldata.tar.gz /data

scp al3x@emprender-radix.com:/home/al3x/mediafile.tar.gz ./
scp al3x@emprender-radix.com:/home/al3x/msqldata.tar.gz ./

#
# DOCKER RESTORE
#
cd ~ && docker run --rm --mount source=multishopp2_media_volume,target=/data -v $(pwd):/backup busybox tar -xzvf /backup/mediafile.tar.gz -C / && cd multishopp2 && docker compose exec backend bash

docker run --rm --mount source=multishopp2_msql-data,target=/var/opt/mssql -v $(pwd):/backup busybox tar -xzvf /backup/msqldata.tar.gz -C /

