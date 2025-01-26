import os
import subprocess
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QMessageBox, QStatusBar

# 定义软件及其路径，按钮文本，说明，图标路径
geek = ["Some_Tools\\geek.exe", "geek", "软件清理卸载", "core_file/icon/icon.png"]
rufus318 = ["Some_Tools\\rufus-3.18.exe", "rufus-3.18", "系统U盘制作", "path\\to\\icon2.png"]
SpaceSniffer = ["Some_Tools\\SpaceSniffer.exe", "SpaceSniffer", "磁盘空间分析", "path\\to\\icon3.png"]
AID64 = ["Some_Tools\\AID64.exe", "AID64", "懂？", "path\\to\\icon4.png"]
Debug = True


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('白白的垃圾箱')
        self.setGeometry(100, 100, 800, 600)  # 默认大小，稍后会进行居中处理
        self.setWindowIcon(QIcon('core_file/icon/头像1.png'))  # 设置窗口的图标

        # 创建布局
        self.layout = QVBoxLayout()

        # 设置布局
        self.setLayout(self.layout)
        # 创建 QWidget 用于显示
        widget = QWidget(self)
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        # 添加状态栏
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # 调用居中函数
        self.center()

        # 自定义exe文件路径及按钮
        self.custom_exe_files()

    def center(self):
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen().availableGeometry()  # 获取屏幕大小
        window = self.frameGeometry()  # 获取窗口的几何形状
        # 将窗口设置为居中显示
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)  # 使用 move(x, y) 来设置窗口位置

    def custom_exe_files(self):
        # 获取当前工作目录
        current_path = os.getcwd()
        if Debug:
            print(current_path)

        # 自定义exe文件路径、按钮文本、说明和图标路径
        exe_data = [geek, rufus318, SpaceSniffer, AID64]

        # 创建按钮来启动自定义的.exe文件
        for exe in exe_data:
            exe_path = os.path.join(current_path, exe[0])
            exe_label = exe[1]
            description = exe[2]  # 鼠标悬浮时显示的说明
            exe_icon = exe[3]

            button = QPushButton(exe_label, self)
            button.clicked.connect(lambda checked, exe=exe_path: self.open_software(exe))

            button.setFixedSize(200, 50)  # 设置按钮大小为50x50
            # 设置按钮图标
            if os.path.exists(exe_icon):
                icon = QIcon(exe_icon)
                button.setIcon(icon)  # 设置按钮图标
                button.setIconSize(QSize(50, 50))  # 设置图标大小，使其适配按钮
            else:
                # 如果图标路径无效，设置一个默认图标
                button.setIcon(QIcon())  # 设置一个空图标
                button.setIconSize(QSize(50, 50))  # 默认图标大小

            button.setToolTip(description)
            # 设置鼠标悬浮显示时，更新状态栏的文本
            button.enterEvent = lambda event, label=description: self.show_status_message(label)
            button.leaveEvent = self.clear_status_message
            self.layout.addWidget(button)

    def open_software(self, exe_file):
        """启动选中的.exe文件"""
        if os.path.exists(exe_file):  # 如果exe文件存在
            try:
                subprocess.run([exe_file], check=True)  # 启动.exe文件
            except subprocess.CalledProcessError as e:
                self.show_error_message(f"运行 {exe_file} 时发生错误: {e}")  # 弹窗显示错误
            except FileNotFoundError:
                self.show_error_message(f"文件未找到: {exe_file}")  # 弹窗显示文件未找到
            except Exception as e:
                self.show_error_message(f"启动程序时发生未知错误: {e}")  # 弹窗显示未知错误
        else:
            self.show_error_message(f"指定的.exe文件不存在: {exe_file}")  # 弹窗提示文件不存在

    def show_status_message(self, message):
        """鼠标悬停时更新状态栏文本"""
        self.status_bar.showMessage(message)

    def clear_status_message(self, event):
        """鼠标离开按钮时清除状态栏文本"""
        self.status_bar.clearMessage()

    def show_error_message(self, message):
        """显示错误消息的弹窗"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)  # 设置为错误类型图标
        msg_box.setWindowTitle("出错了捏~(￣▽￣)~*")  # 弹窗标题
        msg_box.setText(message)  # 设置错误消息内容
        msg_box.setStandardButtons(QMessageBox.Ok)  # 显示确定按钮
        msg_box.exec_()  # 弹出对话框并等待用户操作


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
