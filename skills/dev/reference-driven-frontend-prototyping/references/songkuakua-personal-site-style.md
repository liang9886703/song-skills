# songkuakua.com Style Reference

Use when 松垮垮 asks for a personal-site/frontend visual direction or says to reference his own site.

Source: `http://songkuakua.com`.

Observed reusable cues:

- Site title: `松垮垮`.
- Self-hosted fonts discovered from CSS:
  - `/assets/fonts/FuturaLT-CondensedLightObl.4b439b3e.otf`
  - `/assets/fonts/together.0f413845.ttf`
- Light theme token cluster from CSS:
  - `--bodyBg: #f3d2c1`
  - `--mainBg: #fef6e4`
  - `--sidebarBg: rgba(254,246,228,0.73)`
  - `--blurBg: rgba(174,222,252,0.2)`
  - `--customBlockBg: #8bd3dd`
  - `--textColor: #172c66`
  - `--textLightenColor: #f582ae`
  - `--borderColor: rgba(0,23,88,0.49)`
  - `--codeBg: rgba(139,212,221,0.13)`
  - `--codeColor: #12c1e4`
  - `--buttonsColor: rgba(245,130,174,0.71)`
  - `--rightMenuColor: rgba(254,246,228,0.73)`
- Glassmorphism utility:
  ```css
  .blur {
    -webkit-backdrop-filter: saturate(200%) blur(20px);
    backdrop-filter: saturate(200%) blur(20px);
  }
  ```

Workflow note: when using this site as a visual reference, actively fetch its HTML/CSS and download/reuse the embedded font files if the prototype needs a closer match. Do not rely only on third-party reference sites when the user has provided this as his own style baseline.
