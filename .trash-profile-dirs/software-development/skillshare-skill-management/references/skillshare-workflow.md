# Skillshare multipart assembly and Hermes sync

## Observed working recipe

1. Write the main skill content to:
   `~/.config/skillshare/skills/<skill-name>/SKILL.md`
2. Write each supporting file under its requested relative path, for example:
   `~/.config/skillshare/skills/<skill-name>/reference/<file>.md`
3. Run `skillshare sync`. If it reports `config not found`, run `skillshare init` first.
4. Run `skillshare target list`. If it reports no configured targets, add Hermes:
   `skillshare target add hermes ~/.hermes/skills`
5. Run `skillshare sync` again.
6. Verify by reading files from `~/.hermes/skills/<skill-name>/`.

## Important distinction

The skillshare source directory and Hermes target are different directories. A successful write to the source is not an installed Hermes skill until a sync completes successfully with at least one configured target.

## Installation fallback

The `runkids/skillshare` project is distributed as a Go binary. It is not the npm registry package `skillshare`. If the official shell installer cannot use sudo interactively, download the matching release archive and install the binary to `~/.local/bin/skillshare`, then verify with `skillshare version`.
