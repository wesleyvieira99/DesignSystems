export const normalize = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
export const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function searchEntries(entries, query = '', filters = {}) {
  const words = normalize(query).trim().split(/\s+/).filter(Boolean);
  return entries.filter(e => (!filters.category || e.category === filters.category) && (!filters.level || e.level === filters.level) && (!filters.provider || e.provider === filters.provider) && (!filters.kind || e.kind === filters.kind) && words.every(w => normalize([e.name,e.organization,e.summary,...e.tags].join(' ')).includes(w)));
}
export function loadList(storage, key, knownIds) {
  try { const value = JSON.parse(storage.getItem(key) || '[]'); return new Set(Array.isArray(value) ? value.filter(id => typeof id === 'string' && knownIds.has(id)) : []); } catch { return new Set(); }
}
export function validateCatalog(entries) {
  const errors = [], ids = new Set();
  if (!Array.isArray(entries)) return ['O catálogo precisa ser uma lista.'];
  for (const e of entries) {
    if (!e.id || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(e.id) || ids.has(e.id)) errors.push(`ID inválido ou duplicado: ${e.id}`);
    ids.add(e.id);
    for (const field of ['name','category','kind','organization','level','summary','overview']) if (typeof e[field] !== 'string' || !e[field].trim()) errors.push(`${e.id}: ${field} ausente`);
    if (!['pattern','architecture','cloud','foundation'].includes(e.category)) errors.push(`${e.id}: categoria inválida`);
    if (!['Fundamentos','Intermediário','Avançado'].includes(e.level)) errors.push(`${e.id}: nível inválido`);
    for (const [field,min] of [['tags',1],['when',2],['benefits',2],['tradeoffs',2],['avoid',1],['steps',4],['sources',1]]) if (!Array.isArray(e[field]) || e[field].length < min) errors.push(`${e.id}: ${field} incompleto`);
    for (const s of e.steps || []) if (!s.title || !s.detail) errors.push(`${e.id}: etapa incompleta`);
    for (const s of e.sources || []) {try {if(new URL(s.url).protocol !== 'https:') errors.push(`${e.id}: fonte insegura`);} catch {errors.push(`${e.id}: URL inválida`);}}
    if (!e.example?.code || !e.example?.language || !e.example?.explanation) errors.push(`${e.id}: exemplo incompleto`);
    if (e.category === 'cloud' && !['aws','azure','gcp'].includes(e.provider)) errors.push(`${e.id}: provedor inválido`);
    {
      if (!e.blueprint?.nodes?.length || !e.blueprint?.edges?.length) errors.push(`${e.id}: blueprint ausente`);
      const nodes = e.blueprint?.nodes || [], nodeIds = new Set(nodes.map(n => n.id));
      if (nodeIds.size !== nodes.length || nodes.length < 3 || nodes.length > 6) errors.push(`${e.id}: peças inválidas`);
      for (const n of nodes) if (!n.id || !n.label || !n.technology || !n.role || !n.detail) errors.push(`${e.id}: peça incompleta`);
      for (const edge of e.blueprint?.edges || []) if (!nodeIds.has(edge.from) || !nodeIds.has(edge.to) || !edge.label) errors.push(`${e.id}: conexão inválida`);
      if (e.category !== 'pattern') for (const field of ['prerequisites','validation','failureModes']) if (!Array.isArray(e[field]) || e[field].length < 2) errors.push(`${e.id}: ${field} incompleto`);
    }

  }
  return errors;
}
