
# adb tcpip 6666
# adb connect 172.18.90.47:6666



# 输出 ui 树 
adb shell uiautomator dump /sdcard/ui123.xml
# 输出 ui 树 去到 test 文件夹下面 test.下面的版本不加参数就是可以直接输出到bash的路径
adb pull sdcard/ui123.xml 
# 格式化xml文件
xmllint --format --recover ui123.xml > ui.xml
# echo $phone


key="text"
param="朋友圈"

temp= cat ui.xml | grep $param | awk -F "text=$param" '{print $1}'  | awk -F "bounds=" '{print $2}' |  awk -F "/>" '{print $1}' > test.txt 
echo $temp
# # "[918,60][941,91]"
param1=$(cat test.txt | grep '\[' )
readarray -d ] -t strarr <<< "$param1"

# echo ${strarr[1]}
param_x1=$(echo ${strarr[0]} |  awk -F '[' '{print $2}'  | awk -F ',' '{print $1}')
param_y1=$(echo ${strarr[0]} | awk -F ',' '{print $2}' ) 
param_x2=$(echo ${strarr[1]} | awk -F "[" '{print $2}'  | awk -F ',' '{print $1}')
param_y2=$(echo ${strarr[1]} | awk -F ','  '{print $2}' ) 
param_x=$(($param_x2/2+$param_x1/2))
param_y=$(($param_y2/2+$param_y1/2))

adb shell input tap $param_x $param_y


echo $param_x1
echo $param_y1
echo $param_x2
echo $param_y2