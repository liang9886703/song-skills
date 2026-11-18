"""Standard-library smoke tests; no network or third-party project execution."""
import json,re,shutil,subprocess,tempfile,unittest
from pathlib import Path
T=Path(__file__).resolve().parents[1]/'templates'
class ReaderBuild(unittest.TestCase):
 def build(self,project=False):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);r=Path(tmp.name)
  for name in ['build_reader.py','reader.css','reader.js','reader-utils.js','structure.html']:
   shutil.copy2(T/name,r/name)
  base={'date':'2026-11-18','title':'Fixture','site_url':'https://example.com','articles':[{'id':'a','title':'Test </script>','source':'Fixture','lead':'hello','sections':[{'title':'Body','paragraphs':['a < b & c']}],'links':[]}]}
  if project: base['project_library_url']='https://example.com/projects.html#projects'
  (r/'articles.json').write_text(json.dumps(base));(r/'history.json').write_text(json.dumps([dict(base,date='2026-11-17')]))
  if project:(r/'projects.json').write_text(json.dumps({'projects':[],'categories':[]}))
  subprocess.run(['python',str(r/'build_reader.py')],check=True,capture_output=True)
  subprocess.run(['node','--check',str(r/'check.js')],check=True,capture_output=True)
  return r
 def test_daily(self):
  r=self.build();s=(r/'dist/index.html').read_text();self.assertEqual(len(re.findall(r'</script>',s)),1);self.assertIn('Test <\\/script>',s);self.assertFalse((r/'dist/projects.html').exists());self.assertIn('2026-11-17',s)
 def test_projects(self):
  r=self.build(True);self.assertEqual((r/'dist/index.html').read_bytes(),(r/'dist/projects.html').read_bytes());self.assertIn('https://example.com/projects.html#projects',(r/'dist/index.html').read_text())
 def test_shell(self):
  expected=(T/'structure.html').read_text().replace('/*CSS*/',(T/'reader.css').read_text()).replace('/*SCRIPT*/',(T/'reader.js').read_text()+'\n'+(T/'reader-utils.js').read_text())
  self.assertEqual((T/'reader-shell.html').read_text(),expected)
 def test_project_navigation(self):
  js=(T/'reader.js').read_text()
  url_line=js.splitlines()[1]
  start=js.index("document.querySelector('#projectsView').hidden")
  end=js.index("document.querySelector('#readView').onclick",start)
  handler=js[start:end]
  for url,count,path,hidden,destination in [('',0,'/',True,''),('javascript:alert(1)',0,'/',True,''),('https://example.com/projects.html#projects',0,'/',False,'https://example.com/projects.html#projects'),('',1,'/projects.html',False,'#projects')]:
   setup='const BASE='+json.dumps({'project_library_url':url})+';const PROJECTS={projects:'+json.dumps([{}]*count)+'};const b={};const document={querySelector:()=>b};const location='+json.dumps({'pathname':path,'hash':'','href':''})+';'
   script=setup+url_line+handler+'if(!b.hidden)b.onclick();console.log(JSON.stringify([b.hidden,location.href||location.hash]));'
   result=json.loads(subprocess.check_output(['node','-e',script],text=True))
   self.assertEqual(result,[hidden,destination])
  self.assertIn('#projectsView[hidden]{display:none}',(T/'reader.css').read_text())
 def test_no_embedded_deployment(self):
  s='\n'.join(p.read_text() for p in T.iterdir() if p.is_file())
  for marker in ['appgprj_','/workspace/','/home/','docs.google.com/document/d/']:
   self.assertNotIn(marker,s)
if __name__=='__main__':unittest.main()
