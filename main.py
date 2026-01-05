# Auto-install required packages before imports
import sys
import subprocess

def ensure(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

ensure("PyQt5")
ensure("PyQtWebEngine")

# ===================== Browser Code =====================

import json
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction,
    QLineEdit, QTabWidget, QFileDialog, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

BOOKMARKS_FILE = "bookmarks.json"
HISTORY_FILE = "history.json"
HOME_URL = "https://www.google.com"


class BrowserTab(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.urlChanged.connect(self.record_history)

    def record_history(self, url):
        try:
            history = json.load(open(HISTORY_FILE))
        except:
            history = []
        history.append(url.toString())
        history = history[-500:]
        json.dump(history, open(HISTORY_FILE, "w"))


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Browser")
        self.resize(1200, 800)

        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.downloadRequested.connect(self.handle_download)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.setCentralWidget(self.tabs)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)

        self.search_bar = QLineEdit()
        self.search_bar.returnPressed.connect(self.search)

        self.add_actions()
        self.new_tab(QUrl(HOME_URL))

    def add_actions(self):
        def btn(name, fn):
            a = QAction(name, self)
            a.triggered.connect(fn)
            self.toolbar.addAction(a)

        btn("Back", lambda: self.current().back())
        btn("Forward", lambda: self.current().forward())
        btn("Refresh", lambda: self.current().reload())
        btn("Stop", lambda: self.current().stop())
        btn("Home", lambda: self.current().setUrl(QUrl(HOME_URL)))
        btn("New Tab", lambda: self.new_tab(QUrl(HOME_URL)))
        btn("Bookmark", self.bookmark)

        self.toolbar.addWidget(self.url_bar)
        self.toolbar.addWidget(self.search_bar)

    def new_tab(self, url):
        tab = BrowserTab()
        tab.setUrl(url)
        i = self.tabs.addTab(tab, "New")
        self.tabs.setCurrentIndex(i)
        tab.titleChanged.connect(lambda t, tab=tab: self.tabs.setTabText(self.tabs.indexOf(tab), t))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def current(self):
        return self.tabs.currentWidget()

    def navigate(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.current().setUrl(QUrl(url))

    def update_url_bar(self):
        self.url_bar.setText(self.current().url().toString())

    def search(self):
        q = self.search_bar.text()
        self.current().setUrl(QUrl(f"https://www.google.com/search?q={q}"))

    def bookmark(self):
        try:
            data = json.load(open(BOOKMARKS_FILE))
        except:
            data = []
        url = self.current().url().toString()
        if url not in data:
            data.append(url)
            json.dump(data, open(BOOKMARKS_FILE, "w"))

    def handle_download(self, d):
        path, _ = QFileDialog.getSaveFileName(self, "Save", d.path())
        if path:
            d.setPath(path)
            d.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Browser().show()
    sys.exit(app.exec_())
