ARRAY_NAME=()
ARRAY_NAME+=(*.sh)


count=1
echo ${ARRAY_NAME[0]} 

for i in "${ARRAY_NAME[@]}"; do 
    # > 是 强制覆写
    # >> 是 在尾部添加
    #  $(date +%Y%m%d%H%M%S) 对应着年 月 日 时分秒
    echo "$i $(date +%Y%m%d%H%M%S) $count " >> output.txt; 
    ((count++))
done