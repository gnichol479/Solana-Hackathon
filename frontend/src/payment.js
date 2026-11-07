import bs58 from 'bs58';

export function validWallet(value) {
  if (typeof value !== 'string' || value.length<32 || value.length>44) return false;
  try { return bs58.decode(value).length === 32; } catch { return false; }
}
export function normalizeWebsite(value) {
  try { const u=new URL(/^[a-z]+:\/\//i.test(value)?value:`https://${value}`);
    if(u.protocol!=='https:' || u.username || u.password || u.port || !u.hostname.includes('.') || /^(localhost|127\.|0\.)/i.test(u.hostname)) throw Error();
    return {url:u.origin,domain:u.hostname.toLowerCase().replace(/^www\./,'')};
  } catch {throw new Error('Enter a public HTTPS website without a username, password, or custom port.');}
}
export const demoMerchant = Object.freeze({name:'Northstar Design — fictional demo',domain:'northstar-design.example',wallet:'So11111111111111111111111111111111111111112',evidence:'Synthetic hackathon fixture. This reserved .example domain and address association do not identify a real merchant.',date:'2026-11-06',demo:true});
export const alternateWallet='11111111111111111111111111111111';
export function compareRecipient({business,website,wallet,demo=false}) {
  if(!validWallet(wallet))throw new Error('The recipient must be a valid base58-encoded 32-byte Solana address.');
  const {domain}=normalizeWebsite(website);
  const base={checked_at:new Date().toISOString(),requested_wallet:wallet,domain,business,status:'unverified',demo:false,source:null,expected_wallet:null,explanation:'No independently authenticated merchant record is available. A supplied website or valid address does not prove ownership.'};
  if(demo && domain===demoMerchant.domain && business.trim().toLowerCase()==='northstar design')return {...base,demo:true,status:wallet===demoMerchant.wallet?'verified_match':'address_mismatch',expected_wallet:demoMerchant.wallet,source:demoMerchant.evidence,verified_at:demoMerchant.date,explanation:wallet===demoMerchant.wallet?'The address matches the fictional demo registry. This is a simulated merchant association, not verified real-world identity.':'The requested address differs from the fictional demo registry. For a real request, confirm the intended recipient independently.'};
  return base;
}
export function parseSolanaQR(raw) {
  if(typeof raw!=='string'||raw.length>20000)throw new Error('QR content is too large.');
  if(!/^solana:/i.test(raw))return {kind:'unknown',raw,warning:'Unrecognized QR format. Content is shown as text; no link has been opened.'};
  const tail=raw.slice(7);if(/^https?%3a|^https?:/i.test(tail))return {kind:'transaction_request',raw,warning:'Solana transaction-request URL detected. It has not been fetched or executed.'};
  const [recipient,query='']=tail.split('?');if(!validWallet(recipient))throw new Error('The Solana QR contains an invalid recipient address.');
  const params=new URLSearchParams(query);const known=['amount','spl-token','reference','label','message','memo'];
  for(const key of known.filter(k=>k!=='reference'))if(params.getAll(key).length>1)throw new Error(`Duplicate ${key} in payment QR.`);
  const amount=params.get('amount');if(amount!==null && (!/^(0|[1-9]\d*)(\.\d+)?$/.test(amount)||amount.length>40))throw new Error('The QR payment amount is invalid.');
  const mint=params.get('spl-token');if(mint!==null&&!validWallet(mint))throw new Error('The token mint address is invalid.');
  if(!mint&&amount?.split('.')[1]?.length>9)throw new Error('A SOL amount cannot have more than nine decimal places.');
  const references=params.getAll('reference');if(references.some(r=>!validWallet(r)))throw new Error('A QR reference address is invalid.');
  return {kind:'solana_transfer',raw,recipient,amount,token_mint:mint,token:mint?'SPL token (mint supplied)':'SOL',network:'Solana (cluster not specified by QR)',references,label:params.get('label'),message:params.get('message'),memo:params.get('memo')};
}
export function extractPayment(text) {
  const match=text.match(/\b(\d+(?:,\d{3})*(?:\.\d+)?)\s*(USDC|USDT|USD|EUR|GBP|SOL)\b/i)||text.match(/([$€£])\s*(\d+(?:,\d{3})*(?:\.\d+)?)/);
  const amount=match?(match[1].match(/^[$€£]$/)?match[2]:match[1]).replaceAll(',',''):null;
  const currency=match?({$:'USD','€':'EUR','£':'GBP'}[match[1]]||match[2].toUpperCase()):null;
  const candidates=text.match(/\b[1-9A-HJ-NP-Za-km-z]{32,44}\b/g)||[];
  const wallet=candidates.find(validWallet)||null;
  const purpose=text.match(/(?:payment is for|payment for|for your|purpose:)\s+([^.!\n]+)/i)?.[1]?.trim().replace(/^your\s+/i,'')||null;
  const deadline=text.match(/\b(?:by|before|due on|deadline:)\s+([^.!\n]{1,70})/i)?.[1]?.trim()||(/\btoday\b/i.test(text)?'Today (as written; date unverified)':null);
  const urls=(text.match(/https?:\/\/[^\s<>"']+/gi)||[]).map(u=>u.replace(/[).,;]+$/,''));
  return {amount,currency,network:/\bsolana\b/i.test(text)?'Solana':null,wallet,recipient:text.match(/(?:recipient|payee):\s*([^\n,;.]+)/i)?.[1]?.trim()||null,company:text.match(/(?:company|business):\s*([^\n,;.]+)/i)?.[1]?.trim()||null,purpose,deadline,urls,reference:text.match(/\b(?:INV-[\w-]+|reference:\s*[\w-]+)/i)?.[0]||null};
}
export function inspectURLs(urls) {
 return urls.map(raw=>{try{const u=new URL(raw);const warnings=[];if(u.protocol!=='https:')warnings.push('The link does not use HTTPS.');if(u.username||u.password)warnings.push('Embedded credentials can hide the actual destination.');if(u.hostname.startsWith('xn--')||u.hostname.includes('.xn--'))warnings.push('Internationalized domain: check its exact spelling.');if(/^\d{1,3}(\.\d{1,3}){3}$/.test(u.hostname))warnings.push('The destination uses an IP address rather than a business domain.');for(const [brand,official] of [['paypal','paypal.com'],['solana','solana.com'],['coinbase','coinbase.com']])if(u.hostname.includes(brand)&&u.hostname!==official&&!u.hostname.endsWith('.'+official))warnings.push(`Contains “${brand}” but is outside ${official}. This may indicate impersonation.`);if(u.hostname.split('.').length>4)warnings.push('Several subdomain levels can obscure the actual domain.');for(const brand of domainTypos(u.hostname))warnings.push(`The domain resembles ${brand} with a one-character spelling change. Verify it independently.`);return {raw,host:u.hostname,warnings,checked:'Local URL structure only. No reputation service or website fetch was performed.'};}catch{return {raw,warnings:['The URL could not be parsed.'],checked:'Not checked'};}});
}
// Deliberately limited brand similarity check; no domain is classified as safe.
export function domainTypos(host) {
  function distance(a,b){let row=Array.from({length:b.length+1},(_,i)=>i);for(let i=1;i<=a.length;i++){const next=[i];for(let j=1;j<=b.length;j++)next[j]=Math.min(next[j-1]+1,row[j]+1,row[j-1]+(a[i-1]===b[j-1]?0:1));row=next;}return row[b.length];}
  const labels=host.split('.').slice(0,-1);
  return ['paypal','solana','coinbase'].filter(brand=>!host.endsWith('.'+brand+'.com')&&host!==brand+'.com'&&labels.some(label=>label!==brand&&Math.abs(label.length-brand.length)<=1&&distance(label,brand)===1));
}
export function validateImage(file){if(!file||!['image/png','image/jpeg','image/webp'].includes(file.type))throw new Error('Choose a PNG, JPG, JPEG, or WEBP image.');if(!file.size||file.size>10*1024*1024)throw new Error('Choose a nonempty image up to 10 MB.');}
