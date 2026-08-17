import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("genomeExplorer", {
  desktop: true,
  chooseBundle: () => ipcRenderer.invoke("genome:choose-bundle"),
  onChooseBundleRequested: (callback: () => void) => {
    ipcRenderer.on("genome:choose-bundle-requested", callback);
  },
  quit: () => ipcRenderer.invoke("app:quit"),
});
