import {extractPayment,inspectURLs} from './payment.js';
export const examples = {
  invoice: 'Hi, following up on invoice INV-2048 for $2,500 USD. Our bank details have changed. Please send the outstanding balance to the new account today to avoid service suspension. Do not call our accounting office; they are unavailable.',
  solana: 'Please send 100 USDC on Solana to the wallet address we will provide separately. This payment is for your design project deposit.',
  routine: 'Hello, attached is the monthly invoice for $300 USD. Please review it and contact our accounting team using the phone number in your existing records to confirm payment details.'
};
export function demoReport(text) {
  const urgent = text.match(/urgent|today|immediately|suspension/i)?.[0];
  const changed = text.match(/details have changed|new account/i)?.[0];
  const discouraged = text.match(/do not (call|contact)/i)?.[0];
  const sensitive = text.match(/seed phrase|private key|password|one[- ]time code|2fa code/i)?.[0];
  const solana = /solana|USDC|SOL\b/i.test(text);
  const indicators = [
    ...(urgent ? [{type:'urgency',severity:'warning',phrase:urgent,message:'The request uses language that may create pressure to pay quickly.',action:'Pause and confirm the deadline through an established contact.'}] : []),
    ...(changed ? [{type:'payment_change',severity:'warning',phrase:changed,message:'The request mentions a change to payment instructions.',action:'Confirm the new details using contact information you already trust.'}] : []),
    ...(discouraged ? [{type:'verification_discouraged',severity:'warning',phrase:discouraged,message:'The request discourages independent contact.',action:'Use a previously known contact to verify the instructions.'}] : []),
    ...(sensitive ? [{type:'sensitive_information',severity:'warning',phrase:sensitive,message:'The request mentions sensitive access information. Check whether someone is asking you to disclose it.',action:'Never share seed phrases, private keys, passwords, or one-time codes with a payment requester.'}] : []),
    {type:'unverified_recipient',severity:'info',message:'Recipient identity and payment details have not been independently verified.'}
  ];
  const extracted=extractPayment(text);
  for(const link of inspectURLs(extracted.urls))for(const warning of link.warnings)indicators.push({type:'url_structure',severity:'warning',phrase:link.raw,message:warning,action:'Check the destination through the business’s independently established website.'});
  const suspicious=indicators.some(i=>i.severity==='warning');
  return {analysis_id:'local-'+Date.now(),payment_type:solana?'solana':'traditional',risk_level:suspicious?'suspicious':'needs_verification',summary:suspicious?'Local checks found payment instructions or link structures that deserve a closer look.':'This request does not establish who will receive the payment. Verify the recipient independently.',indicators,extracted,payment_details:{amount:extracted.amount,currency:extracted.currency,recipient:null},solana_analysis:{performed:false,network:null,wallet_address:null,transaction_count:null,known_scam_reports:null},demo:true};
}
export function validateReport(data) {
  if (!data || !['suspicious','needs_verification','no_major_warnings_detected'].includes(data.risk_level) || typeof data.summary !== 'string' || !Array.isArray(data.indicators) || data.indicators.some(i=>!i || typeof i.message!=='string')) throw new Error('The server returned an unsupported report format. Please ask your backend teammate to check the shared API contract.');
  return {
    ...data,
    indicators:data.indicators.map(indicator=>({...indicator,type:indicator.type||indicator.code||indicator.category||'finding'})),
    solana_analysis:data.solana_analysis?{...data.solana_analysis,transaction_count:data.solana_analysis.transaction_count??data.solana_analysis.recent_transaction_count??null,known_scam_reports:data.solana_analysis.known_scam_reports??null}:data.solana_analysis,
  };
}
export function explorerLink(address, network) {
  if (typeof address!=='string' || !/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(address)) return null;
  if (!['mainnet-beta','devnet','testnet'].includes(network)) return null;
  return `https://explorer.solana.com/address/${encodeURIComponent(address)}${network==='mainnet-beta'?'':`?cluster=${network}`}`;
}
