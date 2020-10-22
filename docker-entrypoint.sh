docker run -t -p 9000:9000 --name minio1 \
	-e "MINIO_ACCESS_KEY=testkey" \
	-e "MINIO_SECRET_KEY=testsecret" \
	-v /home/dev/mdata:/data \
	 minio/minio server /data



