# WeChat reader fallback notes

## Provider behavior observed

- `curl https://r.jina.ai/<wechat-url>` can return an HTML/Markdown CAPTCHA shell such as `环境异常` rather than article text. Treat this as a read failure.
- Exa MCP may expose `web_search_exa` and `web_fetch_exa`; inspect `mcporter list <server>` before calling. Older examples may mention `crawling_exa`, which is not necessarily registered.
- Exact searches of an opaque short-link ID can return unrelated repositories or articles. The token is useful only as a weak discovery hint.

## Verification checklist

Before naming a repository, confirm that the extracted article has at least one discriminating identifier:

- exact repository URL;
- project/repository name plus author or organization;
- distinctive code/package/module name;
- README wording that matches the article's project description;
- article backlink or citation.

If none is available, return a blocker-oriented answer and ask for title, opening text, or a screenshot. Avoid listing a long set of topical candidates.
