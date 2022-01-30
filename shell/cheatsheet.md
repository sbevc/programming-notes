#### Execute shell command for every line in file:
```shell
# option 1
while read line; do
  echo $line | sed 's/foo/bar'; echo "original: $line";
done <path/to/file

# option 2
cat path/to/file | while read line; do echo $line; done

# option 3
for line in $(cat path/to/file); do echo line; done
```

#### Find with perms, group and user info
```shell
find /target/dir -name filename -printf %M" "%g" "%u" "%P\\n
```


## AWS
```shell
# List s3 directories
aws s3 ls s3://my-bucket
```

```shell
# awk
kubectl get pods | awk '/senbroker-worker/ {print $1}'

kubectl get pods | awk '/senbroker-worker/ {print $1}' | xargs -t -I{} kubectl logs {} -c senbroker-worker
```


## K8s
```shell
# Logs from multiple pods based on tag
kubectl logs --selector app.kubernetes.io/name=senbroker-worker --container senbroker-worker

# Copy file from remote pod
kubectl cp sentinel-mainstack-venus-sentinel-redis-6f87dfbfc7-nhxmj:/root/redis/download.rdb /tmp/downloads/download.rdb
```


diff <(ll /ghds/ivd/flowcentral/**/bip_config.json | grep -v ^l | awk '{print $8 $9}' | sed 's|/bip_config.json||') <(ls /ghds/ivd/flowcentral/**/cleanup.finished | grep -v ^l | awk '{print $8 $9}' | sed 's|/cleanup.finished||') |grep '<'|sed 's|< ||'