# これは何
春ロボ2025用のコントローラー兼状態監視web gui
# 使い方
```
ip a
```
これでipアドレスを確認する  
haru_gui/src/App.tsxにある
```
const ros = new ROSLIB.Ros({
  url: "ws://[ROSを走らせるPCのローカルIP]:9090",
});
```
[ROSを走らせるPCのローカルIP]に先程確認したipを入れる
```
実行方法
```
cd [haru_guiのディレクトリ]
npm run dev
```
別ターミナルで
```
sudo apt install -y ros-humble-rosbridge-suite
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

