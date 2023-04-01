
# https://developer.android.com/studio/command-line/adb?hl=zh-cn#notlisted

# width=1080

# height=2340
# adb shell wm size 获取屏幕宽高   
#  172.18.89.179 
# adb connect 172.18.89.179:6666


echo "请输入你想沟通的人数"
read n
count=1
while ((count<=n))
do  
    # 点击沟通列表
    adb shell input tap 460 450
    sleep 2
    # 点击最下面的立即沟通
    adb shell input tap 530 2200 
    sleep 2
    adb shell input keyevent BACK
    sleep 2
    adb shell input keyevent BACK
    sleep 2
    adb shell input swipe 960 950 960 600
    echo "当前沟通了: $count 人"
    ((count++))
    sleep 2
done



# 点击列表的一项
# adb shell input tap 460 450
# sleep 2
# adb shell input tap 530 2200 
# sleep 2
# adb shell input keyevent BACK
# sleep 2
# adb shell input keyevent BACK
# sleep 2
# adb shell input swipe 960 950 960 600


# 指定设备控制：
# adb devices    // 172.18.89.179:6666      device
# adb -s 172.18.89.179:6666 shell input keyevent BACK

# 输入
# adb shell input text test123456

# 常按
# adb shell input swipe 300 300 300 300 500



# 打开网页
# adb shell am start -a android.intent.action.VIEW -d  http://google.com

# 输出 ui 树 
# adb shell uiautomator dump sdcard/ui123.xml
# 输出 ui 树 去到 test 文件夹下面 test.下面的版本不加参数就是可以直接输出到bash的路径
# adb pull sdcard/ui123.xml 

# 确定
 
# 设置滑动时间 50 就是滑动时间
# adb shell input swipe 960 950 960 600 50

# adb shell uiautomator dump sdcard/ui123.xml
# adb pull sdcard/ui123.xml 
# value=`cat ui123.xml`
# echo "$value"


# 关联数组 declare -A ARRAY_NAME


# 索引数组 declare -a ARRAY_NAME
# declare -a example_array=( "Welcome" "To" "Yiibai" )  



# 1.数组声明 名称=(元素 元素 元素) =左右赋值的时候不用加空格
# "" 变成 变量 , '' 全部不是变量都是字符串
# ARRAY_NAME=("element_1st" "element_2nd" "element_3th")

# 2.打印元素
# 2.1 打印所有 元素
# echo ${ARRAY_NAME[@]}
# 2.2 打印单个元素
# echo ${ARRAY_NAME[0]}
# 2.3 循环打印
# for i in "${ARRAY_NAME[@]}"; do 
# echo "$i"; 
# done

# 2.4 数组长度
# for i in "${!ARRAY_NAME[@]}"; 
# do 
# echo "${ARRAY_NAME[i]},${#ARRAY_NAME[@]}";  
# done

# 数组添加
# ARRAY_NAME+=("last")
# echo "${ARRAY_NAME[@]}==2"

# 3. 比较
# echo ${ARRAY_NAME[0]}==2
# echo $(($ARRAY_NAME[0]==element_1st))

# 3.5 筛选文件 index 开头
# str=`ls  |egrep "^index"`
# echo "$str"

# 4.工具
# grep 过滤行 
# cat ui123.xml | grep '<node'   | awk -F "text=" '{print $2}'  | awk -F "resource-id=" '{print $1}'

# 5.拆分数组 根据,来拆
# str="aaa,bbb,ccc,ddd"
# readarray -d , -t strarr <<< "$str"
# echo   "${strarr[@]}"











# echo $result

# resultVector=`ls |egrep "1"`
# str= cat test.txt | egrep "\w"  
# str= cat ui123.xml |sed 's#<node #^<node #g' | tr ^ '\n' |grep '"确定“'
# echo $str


# grep "車" index.txt | awk {'print $2" - "$3'} 



# test(){
#     echo "这是我的参数：$1"
#     ls > ls.txt
#     echo `cat ls.txt`
#     return 
# }
# test "param"

# a=ls

#  awk 过滤列  像是$2就是第二个空格
# cat ./ui123.xml | grep '<catalpaflat>' | awk -F '>' '{print $2}' | awk -F '<' '{print $1}'















# getCoordinateByAttribution()
# {

# #这里我们定义了一个instance，它的灵感是来自UiAutomator中的同名操作．意思是在当前页面下，有n个一模一样的属性，我们不好区分时，使用instance来指出我们需要点击的是第一个还是第n个属性．默认点击第一个．
# instance=""
# instance=${instance:=$2}
# instance=${instance:=1}

# uiautomator dump
# #这里借助了busybox工具，至于什么是busybox工具以及如何安装，此处暂不讲，读者可以先行百度，若有困难，再说．
# #这里借助grep命令，来过滤出我们需要点击的属性，个人认为此方法比UiAutomator这个工具本身要方便一些．UiAutomator本身做了很多的区别，比如text，descrption，resourceId等等．
# temp=`cat /mnt/sdcard/window_dump.xml|busybox sed 's/>/\n/g'|busybox grep "$1"|busybox sed -n {$2}p`
# temp=`echo ${temp%]\"*}`
# temp=`echo $temp|busybox awk '{print $NF}'`

# #此处我们作一个判断，如果temp的值不等空串的话，我们认为找到了我们需要查找的属性，并作进一步的处理
# if busybox test ! "$temp" == ""
# then
# temp=`echo ${temp/bounds=/}`
# temp=`echo $temp| busybox sed 's/"//g'| busybox sed 's/\[//g'| busybox sed 's/\]/\n/g'`
# p1=`echo $temp|busybox awk '{print $1}'`
# p2=`echo $temp|busybox awk '{print $2}'`
# #定义四个变量，用例存储找到的属性的四个坐标值
# p1x=`echo ${p1%,*}`
# p1y=`echo ${p1#*,}`
# p2x=`echo ${p2%,*}`
# p2y=`echo ${p2#*,}`

# let centerX=$p1x/2+$p2x/2
# let centerY=$p1y/2+$p2y/2
# else
# #这里是查找属性失败时的动作
# echo `date +%m-%d-%H-%M-%S` getCoordinateByAttribution $1 failed >> /mnt/sdcard/log.txt
# #screencap是android自带的可以抓图的命令，这里加上了时间而已
# screencap -p /mnt/sdcard/"`date +%m-%d-%H-%M-%S`".png
# fi
# }

# cat ui123.xml | getCoordinateByAttribution "text" 1