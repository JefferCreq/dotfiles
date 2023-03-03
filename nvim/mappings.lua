local M = {}

M.comment = {

   -- toggle comment in both modes
   n = {
      ["<C-_>"] = {
        function()
          require("Comment.api").toggle.linewise.current()
        end,

         "蘒  toggle comment",
      },
   },

   v = {
      ["<C-_>"] = {
        "<ESC><cmd>lua require('Comment.api').toggle.linewise(vim.fn.visualmode())<CR>",
         "蘒  toggle comment",
      },
   },
}

return M
