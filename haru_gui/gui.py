import sys
import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose2D
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGraphicsScene, QGraphicsView, QGraphicsRectItem, QLabel
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPen
import threading


class BoolPublisherNode(Node):
    def __init__(self):
        super().__init__("bool_publisher")

        self.publishers_dict = {
            "START": self.create_publisher(Bool, "start", 10),
            "RESET": self.create_publisher(Bool, "reset", 10),
            "CALIB": self.create_publisher(Bool, "calib", 10),
            "CLOSED": self.create_publisher(Bool, "closed", 10),
        }

        self.pose_subscription = self.create_subscription(
            Pose2D, "/pose", self.pose_callback, 10
        )

        self.pose = Pose2D()
        self.get_logger().info("BoolPublisherNode has started.")

        # パラメタの宣言
        self.declare_parameter('field_color', 'red')

        # パラメタの取得
        self.field_color = self.get_parameter('field_color').get_parameter_value().string_value

        # 取得したパラメタの表示
        self.get_logger().info(f'field_color: {self.field_color}')

    def publish_true(self, topic_name):
        if topic_name in self.publishers_dict:
            msg = Bool()
            msg.data = True
            self.publishers_dict[topic_name].publish(msg)
            self.get_logger().info(f"Published True to {topic_name}")

    def pose_callback(self, msg):
        self.pose = msg


class PoseVisualizer(QGraphicsView):
    def __init__(self, ros_node, field_color):
        super().__init__()

        self.ros_node = ros_node
        self.field_color = field_color
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setFixedSize(448, 896)  # 560 * 0.8, 1120 * 0.8

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scene.setSceneRect(0, 0, 448, 896)  # 560 * 0.8, 1120 * 0.8

        # 長方形を描画
        self.boundary_rect = QGraphicsRectItem(24, 48, 392, 784)  # (x, y, width, height) 30 * 0.8, 60 * 0.8, 490 * 0.8, 980 * 0.8
        self.boundary_rect.setBrush(QColor('transparent'))
        self.boundary_rect.setPen(QColor('black'))
        self.scene.addItem(self.boundary_rect)

        # デカルト座標をピクセル座標に変換する関数
        def to_pixel_coords(x, y):
            x_pixel = 24 + (x / 3.5) * 392
            y_pixel = 832 - (y / 7) * 784
            return x_pixel, y_pixel
        
        # デカルト座標を x=1.75 で反転させる関数
        def reflect_x(x):
            return 2 * 1.75 - x

        if self.field_color == "blue":
            # デカルト座標の(0.9,1.5)と(0.9,5.5)を結ぶ線分を描画
            x1, y1 = to_pixel_coords(0.9, 1.5)
            x2, y2 = to_pixel_coords(0.9, 5.5)
            line1 = self.scene.addLine(x1, y1, x2, y2, QPen(QColor('black')))

            # デカルト座標の(2.95,1.5)と(2.95,5.5)を結ぶ線分を描画
            x3, y3 = to_pixel_coords(2.95, 1.5)
            x4, y4 = to_pixel_coords(2.95, 5.5)
            line2 = self.scene.addLine(x3, y3, x4, y4, QPen(QColor('black')))

            # デカルト座標の(0.9,1.5)と(1.9,1.5)を結ぶ線分を描画
            x5, y5 = to_pixel_coords(0.9, 1.5)
            x6, y6 = to_pixel_coords(1.9, 1.5)
            line3 = self.scene.addLine(x5, y5, x6, y6, QPen(QColor('black')))

            # デカルト座標の(0.9,3.5)と(1.9,3.5)を結ぶ線分を描画
            x7, y7 = to_pixel_coords(0.9, 3.5)
            x8, y8 = to_pixel_coords(1.9, 3.5)
            line4 = self.scene.addLine(x7, y7, x8, y8, QPen(QColor('black')))

            # デカルト座標の(0.9,5.5)と(1.9,5.5)を結ぶ線分を描画
            x9, y9 = to_pixel_coords(0.9, 5.5)
            x10, y10 = to_pixel_coords(1.9, 5.5)
            line5 = self.scene.addLine(x9, y9, x10, y10, QPen(QColor('black')))

            # デカルト座標の(2.95,2.5)と(1.95,2.5)を結ぶ線分を描画
            x11, y11 = to_pixel_coords(2.95, 2.5)
            x12, y12 = to_pixel_coords(1.95, 2.5)
            line6 = self.scene.addLine(x11, y11, x12, y12, QPen(QColor('black')))

            # デカルト座標の(2.95,4.5)と(1.95,4.5)を結ぶ線分を描画
            x13, y13 = to_pixel_coords(2.95, 4.5)
            x14, y14 = to_pixel_coords(1.95, 4.5)
            line7 = self.scene.addLine(x13, y13, x14, y14, QPen(QColor('black')))

            # デカルト座標の(3.5,3.0)と(2.95,3.0)を結ぶ線分を描画
            x15, y15 = to_pixel_coords(3.5, 3.0)
            x16, y16 = to_pixel_coords(2.95, 3.0)
            line8 = self.scene.addLine(x15, y15, x16, y16, QPen(QColor('black')))
        
        else:
            # デカルト座標の(0.9,1.5)と(0.9,5.5)を結ぶ線分を描画
            x1, y1 = to_pixel_coords(reflect_x(0.9), 1.5)
            x2, y2 = to_pixel_coords(reflect_x(0.9), 5.5)
            line1 = self.scene.addLine(x1, y1, x2, y2, QPen(QColor('black')))

            # デカルト座標の(2.95,1.5)と(2.95,5.5)を結ぶ線分を描画
            x3, y3 = to_pixel_coords(reflect_x(2.95), 1.5)
            x4, y4 = to_pixel_coords(reflect_x(2.95), 5.5)
            line2 = self.scene.addLine(x3, y3, x4, y4, QPen(QColor('black')))

            # デカルト座標の(0.9,1.5)と(1.9,1.5)を結ぶ線分を描画
            x5, y5 = to_pixel_coords(reflect_x(0.9), 1.5)
            x6, y6 = to_pixel_coords(reflect_x(1.9), 1.5)
            line3 = self.scene.addLine(x5, y5, x6, y6, QPen(QColor('black')))

            # デカルト座標の(0.9,3.5)と(1.9,3.5)を結ぶ線分を描画
            x7, y7 = to_pixel_coords(reflect_x(0.9), 3.5)
            x8, y8 = to_pixel_coords(reflect_x(1.9), 3.5)
            line4 = self.scene.addLine(x7, y7, x8, y8, QPen(QColor('black')))

            # デカルト座標の(0.9,5.5)と(1.9,5.5)を結ぶ線分を描画
            x9, y9 = to_pixel_coords(reflect_x(0.9), 5.5)
            x10, y10 = to_pixel_coords(reflect_x(1.9), 5.5)
            line5 = self.scene.addLine(x9, y9, x10, y10, QPen(QColor('black')))

            # デカルト座標の(2.95,2.5)と(1.95,2.5)を結ぶ線分を描画
            x11, y11 = to_pixel_coords(reflect_x(2.95), 2.5)
            x12, y12 = to_pixel_coords(reflect_x(1.95), 2.5)
            line6 = self.scene.addLine(x11, y11, x12, y12, QPen(QColor('black')))

            # デカルト座標の(2.95,4.5)と(1.95,4.5)を結ぶ線分を描画
            x13, y13 = to_pixel_coords(reflect_x(2.95), 4.5)
            x14, y14 = to_pixel_coords(reflect_x(1.95), 4.5)
            line7 = self.scene.addLine(x13, y13, x14, y14, QPen(QColor('black')))

            # デカルト座標の(3.5,3.0)と(2.95,3.0)を結ぶ線分を描画
            x15, y15 = to_pixel_coords(reflect_x(3.5), 3.0)
            x16, y16 = to_pixel_coords(reflect_x(2.95), 3.0)
            line8 = self.scene.addLine(x15, y15, x16, y16, QPen(QColor('black')))


        self.pose_rect = QGraphicsRectItem(-24, -24, 48, 48)  # -30 * 0.8, -30 * 0.8, 60 * 0.8, 60 * 0.8
        self.pose_rect.setBrush(QColor('blue'))
        self.scene.addItem(self.pose_rect)

        self.pose_label = QLabel(self)
        self.pose_label.setStyleSheet("font-size: 16px; color: black;")
        self.pose_label.setGeometry(8, 8, 160, 40)  # 10 * 0.8, 10 * 0.8, 200 * 0.8, 50 * 0.8
        self.scene.addWidget(self.pose_label)

    def update_pose(self):
        pose = self.ros_node.pose
        if self.field_color == "red":
            x_pixel = (pose.x + 3.5) * 112 + 24  # 140 * 0.8, 30 * 0.8
        else:
            x_pixel = pose.x * 112 + 24  # 140 * 0.8, 30 * 0.8
        y_pixel = (7 - pose.y) * 112 + 48  # 140 * 0.8, 60 * 0.8
        theta_deg = math.degrees(-pose.theta)

        self.pose_rect.setPos(x_pixel, y_pixel)
        self.pose_rect.setRotation(theta_deg)

        self.pose_label.setText(f"x: {pose.x:.2f}, y: {pose.y:.2f}, theta: {pose.theta*180/math.pi:.2f}")


class BoolPublisherGUI(QWidget):
    def __init__(self, ros_node):
        super().__init__()
        self.ros_node = ros_node

        self.setWindowTitle("Bool Publisher & Pose Viewer")

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        exit_button = QPushButton("Exit", self)
        exit_button.setStyleSheet("min-width: 64px; min-height: 32px;")  # 80 * 0.8, 40 * 0.8
        exit_button.clicked.connect(self.close_application)
        left_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        button_layout = QGridLayout()
        self.buttons = {
            "START": "START",
            "RESET": "RESET",
            "CALIB": "CALIB",
            "CLOSED": "CLOSED",
        }

        button_style = """
        QPushButton {
            border: 2px solid #8f8f91;
            border-radius: 80px;  # 100 * 0.8
            background-color: #f0f0f0;
            min-width: 160px;  # 200 * 0.8
            min-height: 160px;  # 200 * 0.8
            max-width: 160px;  # 200 * 0.8
            max-height: 160px;  # 200 * 0.8
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        """

        positions = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for position, (button_text, topic) in zip(positions, self.buttons.items()):
            button = QPushButton(button_text, self)
            button.setStyleSheet(button_style)
            button.clicked.connect(lambda checked, t=topic: self.ros_node.publish_true(t))
            button_layout.addWidget(button, *position)

        button_container = QWidget()
        button_container.setLayout(button_layout)
        button_container.setFixedSize(800, 800)  # 1000 * 0.8

        left_layout.addWidget(button_container, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.pose_viewer = PoseVisualizer(ros_node, self.ros_node.field_color)

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.pose_viewer)

        self.setLayout(main_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.pose_viewer.update_pose)
        self.timer.start(10)

    def close_application(self):
        self.close()


def ros_spin(node):
    rclpy.spin(node)


def main():
    app = QApplication(sys.argv)
    rclpy.init()
    node = BoolPublisherNode()
    gui = BoolPublisherGUI(node)
    gui.show()

    ros_thread = threading.Thread(target=ros_spin, args=(node,), daemon=True)
    ros_thread.start()

    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
