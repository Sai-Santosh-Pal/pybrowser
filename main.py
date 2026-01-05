import sys
import json
import tkinter as tk
from tkinter import ttk
from cefpython3 import cefpython as cef

BOOKMARKS_FILE = "bookmarks.json"
HISTORY_FILE = "history.json"
HOME_URL = "https://www.google.com"


class BrowserTab:
    def __init__(self, parent, url):
        self.frame = tk.Frame(parent)
        self.browser = cef.CreateBrowserSync(
            window_info=cef.WindowInfo(self.frame.winfo_id()),
            url=url
        )


class Browser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Chromium Browser")
        self.geometry("1200x800")

        self.toolbar = tk.Frame(self)
        self.toolbar.pack(fill="x")

        self.url = tk.Entry(self.toolbar)
        self.url.pack(side="left", fill="x", expand=True)
        self.url.bind("<Return>", self.go)

        tk.Button(self.toolbar, text="Back", command=self.back).pack(side="left")
        tk.Button(self.toolbar, text="Forward", command=self.forward).pack(side="left")
        tk.Button(self.toolbar, text="Reload", command=self.reload).pack(side="left")
        tk.Button(self.toolbar, text="Stop", command=self.stop).pack(side="left")
        tk.Button(self.toolbar, text="Home", command=self.home).pack(side="left")
        tk.Button(self.toolbar, text="New Tab", command=self.new_tab).pack(side="left")
        tk.Button(self.toolbar, text="Bookmark", command=self.bookmark).pack(side="left")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        self.new_tab(HOME_URL)
        self.after(10, cef.MessageLoopWork)

    def current_browser(self):
        tab = self.tabs.nametowidget(self.tabs.select())
        return tab.browser

    def new_tab(self, url=HOME_URL):
        tab = BrowserTab(self.tabs, url)
        self.tabs.add(tab.frame, text="Tab")
        self.tabs.select(tab.frame)
        self.url.delete(0, tk.END)
        self.url.insert(0, url)

    def go(self, _=None):
        u = self.url.get()
        if not u.startswith("http"):
            u = "https://" + u
        self.current_browser().LoadUrl(u)
        self.record(u)

    def home(self):
        self.current_browser().LoadUrl(HOME_URL)

    def back(self):
        self.current_browser().GoBack()

    def forward(self):
        self.current_browser().GoForward()

    def reload(self):
        self.current_browser().Reload()

    def stop(self):
        self.current_browser().StopLoad()

    def bookmark(self):
        try:
            b = json.load(open(BOOKMARKS_FILE))
        except:
            b = []
        u = self.url.get()
        if u not in b:
            b.append(u)
            json.dump(b, open(BOOKMARKS_FILE, "w"))

    def record(self, url):
        try:
            h = json.load(open(HISTORY_FILE))
        except:
            h = []
        h.append(url)
        h = h[-1000:]
        json.dump(h, open(HISTORY_FILE, "w"))


if __name__ == "__main__":
    cef.Initialize()
    app = Browser()
    app.mainloop()
    cef.Shutdown()        except:
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
