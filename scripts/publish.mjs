import {execFileSync} from 'node:child_process';
import {mkdtemp,readdir,rm,cp} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
const root=resolve(import.meta.dirname,'..');
const run=(command,args,cwd=root)=>execFileSync(command,args,{cwd,stdio:'inherit'});
// Validate and build before changing the published branch.
run(process.execPath,['--test','tests/catalog.test.mjs']);
run('python3',['-m','unittest','discover','-s','tests','-v'],join(root,'examples/mvc-python'));
run(process.execPath,['scripts/build.mjs']);
const remote=execFileSync('git',['remote','get-url','origin'],{cwd:root,encoding:'utf8'}).trim();
const temporary=await mkdtemp(join(tmpdir(),'system-atlas-pages-'));
try {
  const checkout=join(temporary,'site');
  run('git',['clone','--single-branch','--branch','gh-pages',remote,checkout]);
  for(const name of await readdir(checkout))if(name!=='.git')await rm(join(checkout,name),{recursive:true,force:true});
  for(const name of await readdir(join(root,'dist')))await cp(join(root,'dist',name),join(checkout,name),{recursive:true});
  run('git',['add','--all'],checkout);
  const changes=execFileSync('git',['diff','--cached','--name-only'],{cwd:checkout,encoding:'utf8'}).trim();
  if(changes){
    run('git',['commit','-m','Update published System Atlas'],checkout);
    run('git',['push','origin','gh-pages'],checkout);
    console.log('Arquivos enviados. O GitHub Pages publicará a branch gh-pages.');
  }else console.log('A branch publicada já contém estes arquivos.');
}finally{await rm(temporary,{recursive:true,force:true});}
