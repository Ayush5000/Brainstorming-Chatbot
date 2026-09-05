const { app, BrowserWindow } = require("electron");
const fs = require("fs");
const path = require("path");

if (require("electron-squirrel-startup")) {
  app.quit();
}

if (process.platform === "win32") {
  app.setAppUserModelId("com.squirrel.BrainstormAI.BrainstormAI");
}

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,

    title: "Brainstorm AI",

    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  if (!app.isPackaged) {
    const localBuild = path.join(__dirname, "../frontend/dist/index.html");

    if (fs.existsSync(localBuild)) {
      mainWindow.loadFile(localBuild);
    } else {
      mainWindow.loadURL("http://localhost:5173");
    }
  } else {
    // Production / installed EXE
    mainWindow.loadFile(
      path.join(process.resourcesPath, "dist", "index.html")
    );
  }

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});