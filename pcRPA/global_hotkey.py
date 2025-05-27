import threading
from pynput import keyboard
import time

class GlobalHotkey:
    def __init__(self):
        self.listener = None
        self.callbacks = {}
        self.is_running = False
        self._lock = threading.Lock()
    
    def register_hotkey(self, key, callback):
        """注册热键回调"""
        with self._lock:
            self.callbacks[key] = callback
    
    def unregister_hotkey(self, key):
        """取消注册热键"""
        with self._lock:
            if key in self.callbacks:
                del self.callbacks[key]
    
    def start(self):
        """启动全局热键监听"""
        if self.is_running:
            return
            
        self.is_running = True
        self.listener = keyboard.Listener(on_press=self._on_key_press)
        self.listener.start()
        print("全局热键监听已启动")
    
    def stop(self):
        """停止全局热键监听"""
        if not self.is_running:
            return
            
        self.is_running = False
        if self.listener:
            self.listener.stop()
            self.listener = None
        print("全局热键监听已停止")
    
    def _on_key_press(self, key):
        """按键事件处理"""
        if not self.is_running:
            return
            
        with self._lock:
            if key in self.callbacks:
                try:
                    self.callbacks[key]()
                except Exception as e:
                    print(f"热键回调执行出错: {e}")

# 全局热键管理器实例
global_hotkey_manager = GlobalHotkey() 