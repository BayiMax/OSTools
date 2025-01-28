import os
import subprocess
import sys

import psutil  # 导入 psutil 用于查询系统进程
from PyQt5.QtCore import QSize, QFile, QTextStream
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QMessageBox, QStatusBar

# 定义软件及其路径，按钮文本，说明，图标路径
geek = ["Tools\\geek.exe", "geek", "简易清理卸载", "corefile\\icon\\icon.png"]
rufus318 = ["Tools\\rufus-3.18.exe", "rufus-3.18", "系统U盘制作", "corefile\\to\\icon2.png"]
SpaceSniffer = ["Tools\\SpaceSniffer.exe", "SpaceSniffer", "磁盘空间分析", "corefile\\to\\icon3.png"]
snipaste = ["Tools\\snipaste\\Snipaste.exe", "Snipaste", "截图工具", "corefile\\to\\icon1.png"]
Translations = ["Tools\\Tu.exe", "Translations", "软件卸载、注册表清理、系统修改记录", "corefile\\to\\icon5.png"]
AID64 = ["Tools\\AID64.exe", "AID64", "懂？", "corefile\\to\\icon4.png"]
Debug = True

# 自定义exe文件路径、按钮文本、说明和图标路径
exe_data = [geek, rufus318, SpaceSniffer, snipaste, Translations, AID64]


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('白白的垃圾箱')
        self.setGeometry(100, 100, 400, 600)  # 默认大小，稍后会进行居中处理
        self.setWindowIcon(QIcon('corefile\\icon\\头像1.png'))  # 设置窗口的图标

        self.background_image = QPixmap('corefile\\background\\Furina1.jpg')  # 设置背景图片

        # 加载CSS文件
        self.load_stylesheet()

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

    def load_stylesheet(self):
        """加载外部CSS文件"""
        css_file = QFile('style.css')  # 读取CSS文件
        if css_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(css_file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)  # 应用样式表

    def custom_exe_files(self):
        # 获取当前工作目录
        current_path = os.getcwd()
        if Debug:
            print(current_path)

        # 创建按钮来启动自定义的.exe文件
        for exe in exe_data:
            exe_path = os.path.join(current_path, exe[0])
            exe_label = exe[1]
            description = exe[2]  # 鼠标悬浮时显示的说明
            exe_icon = exe[3]

            button = QPushButton(exe_label, self)
            button.clicked.connect(lambda checked, exe=exe_path: self.open_software(exe))

            button.setFixedSize(100, 100)  # 设置按钮大小为50x50
            # 设置按钮图标
            if os.path.exists(exe_icon):
                icon = QIcon(exe_icon)
                button.setIcon(icon)  # 设置按钮图标
                button.setIconSize(QSize(50, 50))  # 设置图标大小，使其适配按钮
            else:
                # 如果图标路径无效，设置一个默认图标
                button.setIcon(QIcon())  # 设置一个空图标
                button.setIconSize(QSize(50, 50))  # 默认图标大小

            # 设置按钮透明背景并保持文本与图标
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: black;  /* 按钮文本颜色 */
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 50);  /* 鼠标悬停时背景颜色 */
                }
            """)

            button.setToolTip(description)
            # 设置鼠标悬浮显示时，更新状态栏的文本
            button.enterEvent = lambda event, label=description: self.show_status_message(label)
            button.leaveEvent = self.clear_status_message
            self.layout.addWidget(button)

    def open_software(self, exe_file):
        """启动选中的.exe文件"""
        # 检查软件是否已经在运行
        if self.is_software_running(exe_file):
            self.show_error_message(f"{exe_file} 已经在运行!")  # 如果软件已运行，弹窗提示
        else:
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

    def is_software_running(self, exe_file):
        """检查软件是否已运行"""
        # 提取进程名称（文件名）
        exe_name = os.path.basename(exe_file)
        # 遍历当前所有的进程，查看是否已运行该程序
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if exe_name.lower() in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

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

    def paintEvent(self, event):
        """重载 paintEvent 来绘制背景图"""
        painter = QPainter(self)
        # 让背景图片适应窗口大小
        painter.drawPixmap(0, 0, self.width(), self.height(), self.background_image)
        super().paintEvent(event)  # 确保不影响其他绘制操作


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
