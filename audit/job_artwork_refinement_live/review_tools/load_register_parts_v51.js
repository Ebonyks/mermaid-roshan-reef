async function loadVerifiedRegisterV51(){
 const ceiling=4*1024*1024,decoder=new TextDecoder('utf-8',{fatal:true});
 const hash=async bytes=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),x=>x.toString(16).padStart(2,'0')).join('');
 const read=async path=>{const response=await fetch(path,{cache:'no-store'});if(!response.ok)throw Error('Register file unavailable: '+path);const declared=Number(response.headers.get('content-length'));if(declared>ceiling)throw Error('Register JSON exceeds the existing 4MiB ceiling');const bytes=await response.arrayBuffer();if(bytes.byteLength>ceiling)throw Error('Register JSON exceeds the existing 4MiB ceiling');return{bytes,data:JSON.parse(decoder.decode(bytes))}};
 const loaded=await read('ALL_ITEMS.json'),root=loaded.data;
 if(!root||!Array.isArray(root.items))throw Error('Invalid root register');
 const parts=root.item_shards||[],seen=new Set(),items=[...root.items];
 if(!Array.isArray(parts)||parts.length>12)throw Error('Invalid register part list');
 for(const p of parts){
  if(!p||typeof p.path!=='string'||!/^[A-Za-z0-9][A-Za-z0-9_.-]*\.json$/.test(p.path)||p.path==='ALL_ITEMS.json'||seen.has(p.path))throw Error('Unsafe or repeated register part path');seen.add(p.path);
  if(!Number.isInteger(p.bytes)||p.bytes<=0||p.bytes>ceiling||!Number.isInteger(p.items)||p.items<=0||p.items>100000||typeof p.sha256!=='string'||!/^[0-9a-f]{64}$/.test(p.sha256))throw Error('Invalid register part descriptor');
  const part=await read(p.path);
  if(part.bytes.byteLength!==p.bytes||await hash(part.bytes)!==p.sha256)throw Error('Register part byte/hash mismatch');
  if(!part.data||!Array.isArray(part.data.items)||part.data.items.length!==p.items)throw Error('Register part item-count mismatch');items.push(...part.data.items);
 }
 const ids=new Set();for(const q of items){if(!q||typeof q.id!=='string'||!q.id||typeof q.path!=='string'||ids.has(q.id))throw Error('Invalid or duplicate register item identity/path');ids.add(q.id)}
 if(root.counts?.registered_items!==items.length)throw Error('Assembled register count mismatch');
 root.items=items;root.verified_root_sha256=await hash(loaded.bytes);return root;
}
