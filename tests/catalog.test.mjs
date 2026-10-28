import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,readdir} from 'node:fs/promises';
import {searchEntries,loadList,escapeHTML,validateCatalog} from '../lib.js';
const folder=new URL('../data/',import.meta.url);
const files=(await readdir(folder)).filter(f=>f.endsWith('.json')&&f!=='catalog.json');
const entries=(await Promise.all(files.map(f=>readFile(new URL(f,folder),'utf8').then(JSON.parse)))).flat();
test('Todo guia tem identificador único, contexto, decisões, etapas, exemplo e fontes HTTPS',()=>assert.deepEqual(validateCatalog(entries),[]));
test('Busca ignora acentos e caixa e combina palavras',()=>{const items=[{name:'Arquitetura Hexagonal',organization:'Engenharia',summary:'Portas e adaptadores',tags:['aplicação'],category:'architecture',level:'Intermediário'}];assert.equal(searchEntries(items,'APLICACAO hexagonal').length,1);assert.equal(searchEntries(items,'hexagonal',{category:'pattern'}).length,0);assert.equal(searchEntries(items,'hexagonal',{level:'Avançado'}).length,0);});
test('Dados locais corrompidos ou IDs antigos não quebram o progresso',()=>{const valid=new Set(['a','b']);for(const value of ['null','{}','{invalid'])assert.equal(loadList({getItem:()=>value},'key',valid).size,0);assert.deepEqual([...loadList({getItem:()=>JSON.stringify(['a','a','unknown',3])},'key',valid)],['a']);});
test('Textos e exemplos não executam HTML no navegador',()=>assert.equal(escapeHTML('<script>"&\'</script>'),'&lt;script&gt;&quot;&amp;&#39;&lt;/script&gt;'));
test('Cloud exige provedor conhecido',()=>{const guide=structuredClone(entries[0]);guide.category='cloud';guide.provider='invalid';assert.ok(validateCatalog([guide]).some(e=>e.includes('provedor inválido')));});

test('Catálogo de backend tem mais de 100 guias e todas as referências internas resolvidas',()=>{
 assert.ok(entries.length>100);
 const ids=new Set(entries.map(e=>e.id));
 for(const e of entries){
  assert.ok(['foundation','pattern','architecture','cloud'].includes(e.category));
  for(const related of e.related||[])assert.ok(ids.has(related),`${e.id} -> ${related}`);
 }
 for(const provider of ['aws','azure','gcp'])assert.ok(entries.filter(e=>e.provider===provider).length>=6);
});
