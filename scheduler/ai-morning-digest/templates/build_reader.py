from pathlib import Path
import json,re
root=Path(__file__).parent
base=json.loads((root/'articles.json').read_text())
history=json.loads((root/'history.json').read_text()) if (root/'history.json').exists() else []
projects=json.loads((root/'projects.json').read_text()) if (root/'projects.json').exists() else {'projects':[],'categories':[]}
css=(root/'reader.css').read_text();js=(root/'reader.js').read_text();utils=(root/'reader-utils.js').read_text()
# Function declarations are hoisted. Keep the root data placeholders in the reusable shell.
shell=(root/'structure.html').read_text().replace('/*CSS*/',css).replace('/*SCRIPT*/',js+'\n'+utils)
(root/'shell.html').write_text(shell)
page=shell.replace('/*DATA*/{}',json.dumps(base,ensure_ascii=False).replace('</','<\\/')).replace('/*HISTORY*/[]',json.dumps(history,ensure_ascii=False).replace('</','<\\/'))
page=page.replace('/*PROJECTS*/{ \"projects\":[], \"categories\":[] }',json.dumps(projects,ensure_ascii=False).replace('</','<\\/'))
(root/'dist').mkdir(exist_ok=True);(root/'dist/index.html').write_text(page)
if (root/'projects.json').exists(): (root/'dist/projects.html').write_text(page)
(root/'check.js').write_text(re.search(r'<script>(.*?)</script>',page,re.S).group(1))
print('Built',len(history)+1,'editions,',sum(len(d['articles']) for d in history)+len(base['articles']),'articles')
