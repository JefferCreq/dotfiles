local M = {}

M.plugins = {
  options = {
      lspconfig = {
         setup_lspconf = "custom.plugins.lspconfig",
      },
   },

  override = {
      ["nvim-treesitter/nvim-treesitter"] = {
        ensure_installed = {
          "html",
          "css",
          "python",
          "c",
          "cpp",
          "bash",
          "go",
          "lua",
          "markdown",
          "java",
       },
     }
   },

  user = require "custom.plugins",

}

M.ui = {
  -- theme = "catppuccin",
  transparency = true,
}

M.mappings = require "custom.mappings"

return M
