##  adb

```sh
无线连接必须先有线连接
--1. 手机上开发者选项和USB调试 模拟点击打开
--2. adb.zip 解压后，添加这个环境到环境变量
--3. 有线连上后
--3.1 adb devices // 输出现在连接的设备，有限连接后 才有设备。这个时候 会输出 xxxxxx（反正不是空值）
--3.2 手机上设置中状态信息 找到手机ipv4的地址
--3.3 adb tcpip 6666 //电脑端开启新的端口，这个时候可以拔掉有线连接
--3.4 adb connect 172.18.90.4:6666 //（手机网段 在步骤3.2 找到的）
--3.5 这时候就可以写shell脚本了
--3.6 在git bash 就可以 运行脚本 sh xxxxxxxxx.sh


我的shell 脚本如下

echo "请Input你想沟通的人数"
read n
count=1
while ((count<=n))
do  
    # 点击沟通列表,这里的指针位置要自己打开无障碍去查
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
```

