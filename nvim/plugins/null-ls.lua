local present, null_ls = pcall(require, "null-ls")

if not present then
	return
end

local b = null_ls.builtins

local sources = {

	-- b.formatting.prettierd.with { filetypes = { "html", "markdown", "css" } },
	-- b.formatting.deno_fmt,

	-- Lua
	b.formatting.stylua,
	-- b.diagnostics.luacheck.with { extra_args = { "--global vim" } },

	-- Shell
	-- b.formatting.shfmt,
	-- b.diagnostics.shellcheck.with { diagnostics_format = "#{m} [#{c}]" },

	-- Python
	b.formatting.autopep8,
	b.diagnostics.pylint,

	-- Cpp
	b.formatting.clang_format,

	-- Java
	b.formatting.google_java_format,
}

null_ls.setup({
	debug = true,
	sources = sources,
})
