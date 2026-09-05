module.exports = {
  packagerConfig: {
    name: "brainstorm-ai",
    executableName: "brainstorm-ai",
    extraResource: ["../frontend/dist"]
  },

  rebuildConfig: {},

  makers: [
    {
      name: "@electron-forge/maker-squirrel",
      config: {
        name: "BrainstormAI",
        setupExe: "Brainstorm AI Setup.exe",
        title: "Brainstorm AI",
        description: "Brainstorm AI Desktop Application"
      }
    }
  ]
};