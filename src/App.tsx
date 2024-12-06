import { useEffect, useState } from "react";
import "./App.css";
import ROSLIB from "roslib";
import nipplejs from "nipplejs";

// ROSの設定
const ros = new ROSLIB.Ros({
  url: "ws://192.168.10.123:9090", // WebSocketのURL
});

// Twistトピック設定
const cmdVelTopic = new ROSLIB.Topic({
  ros: ros,
  name: "/cmd_vel",
  messageType: "geometry_msgs/Twist",
});

function App() {
  const [maxSpeed, setMaxSpeed] = useState(5); // 最大速度の状態を管理

  useEffect(() => {
    // Nipple.jsを初期化
    const joystickContainer = document.getElementById("joystick");
    const manager = nipplejs.create({
      zone: joystickContainer,
      mode: "static",
      position: { left: "50%", top: "50%" },
      color: "blue",
    });

    manager.on("move", (evt, data) => {
      if (data.distance) {
        const scaledSpeed = (maxSpeed / 5) * data.distance; // スピードをスケーリング
        const angleRad = data.angle.radian;

        // ジョイスティック操作によるTwistメッセージの作成
        const twist = new ROSLIB.Message({
          linear: {
            x: 0.1 * scaledSpeed * Math.cos(angleRad),
            y: 0.1 * scaledSpeed * Math.sin(angleRad),
            z: 0,
          },
          angular: {
            x: 0,
            y: 0,
            z: 0,
          },
        });

        cmdVelTopic.publish(twist); // メッセージを送信
      }
    });

    manager.on("end", () => {
      // 停止信号を送信
      const twist = new ROSLIB.Message({
        linear: { x: 0, y: 0, z: 0 },
        angular: { x: 0, y: 0, z: 0 },
      });
      cmdVelTopic.publish(twist);
    });

    return () => {
      manager.destroy();
    };
  }, [maxSpeed]); // maxSpeedが変更されたら再設定

  return (
    <div
      style={{
        textAlign: "center",
        marginTop: "20px",
        userSelect: "none",
        touchAction: "none",
        WebkitTouchCallout: "none",
      }}
    >
      <div
        style={{
          width: "200px",
          margin: "0 auto",
          position: "relative",
        }}
      >
        {/* スライダーをジョイスティックの上部に配置 */}
        <div style={{ marginBottom: "10px" }}>
          <label>
            <strong>Max Speed: {maxSpeed}</strong>
          </label>
          <br />
          <input
            type="range"
            min="1"
            max="3"
            step="0.05"
            value={maxSpeed}
            onChange={(e) => setMaxSpeed(parseFloat(e.target.value))}
            style={{
              width: "100%",
              appearance: "none",
              height: "8px",
              backgroundColor: "#ccc",
              borderRadius: "4px",
              outline: "none",
              cursor: "pointer",
            }}
          />
          <style>
            {`
              input[type="range"]::-webkit-slider-thumb {
                appearance: none;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background: #007bff;
                cursor: pointer;
              }
              input[type="range"]::-moz-range-thumb {
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background: #007bff;
                cursor: pointer;
              }
              input[type="range"]::-ms-thumb {
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background: #007bff;
                cursor: pointer;
              }
            `}
          </style>
        </div>
        {/* ジョイスティックエリア */}
        <div
          id="joystick"
          style={{
            width: "200px",
            height: "200px",
            border: "1px solid black",
            borderRadius: "50%",
            position: "relative",
            userSelect: "none",
            touchAction: "none",
            WebkitTouchCallout: "none",
          }}
        ></div>
      </div>
    </div>
  );
}

export default App;
