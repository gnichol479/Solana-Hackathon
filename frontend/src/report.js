import {extractPayment,inspectURLs} from './payment.js';
export const examples = {
  solanaSuspicious: 'URGENT: send 100 USDC on Solana to 11111111111111111111111111111111 immediately. Do not contact the project manager; the account will be closed today if payment is late.',
  solanaMedium: 'Please send 50 USDC on Solana to 11111111111111111111111111111111 for this month’s invoice. Confirm the details with our accounting contact before paying.',
  solanaNotSuspicious: 'Routine Solana settlement record for this month. Wallet 11111111111111111111111111111111 is listed for reference; no payment or wallet action is requested in this notice.',
  traditionalSuspicious: 'URGENT: our payment details have changed. Wire the outstanding $2,500 USD balance today to avoid service suspension. Do not call our accounting office; they are unavailable.',
  traditionalMedium: 'Please review the $300 USD invoice and confirm the updated bank details with our existing accounting contact before submitting payment.',
  traditionalNotSuspicious: 'Hello, attached is the monthly invoice for $300 USD. Please review it and contact our accounting team using the phone number in your existing records to confirm payment details.'
};
export const exampleGroups = [
  {label:'Solana',options:[{key:'solanaSuspicious',label:'Suspicious'},{key:'solanaMedium',label:'Medium suspicious'},{key:'solanaNotSuspicious',label:'Not suspicious'}]},
  {label:'Other payment',options:[{key:'traditionalSuspicious',label:'Suspicious'},{key:'traditionalMedium',label:'Medium suspicious'},{key:'traditionalNotSuspicious',label:'Not suspicious'}]}
];
export function demoReport(text) {
  const urgent = text.match(/urgent|today|immediately|suspension/i)?.[0];
  const changed = text.match(/details have changed|new account|(?:new|changed|updated|different)\s+(?:bank|payment|account|wire)\s+(?:details|instructions|account)?/i)?.[0];
  const discouraged = text.match(/do not (call|contact)/i)?.[0];
  const crypto = text.match(/\b(?:pay|send|transfer)\b.{0,60}\b(?:crypto|cryptocurrency|bitcoin|btc|ethereum|eth|solana|usdc)\b/i)?.[0];
  const sensitive = text.match(/seed phrase|private key|password|one[- ]time code|2fa code/i)?.[0];
  const solana = /solana|USDC|SOL\b/i.test(text);
  const indicators = [
    ...(urgent ? [{type:'urgency',severity:'warning',phrase:urgent,message:'The request uses language that may create pressure to pay quickly.',action:'Pause and confirm the deadline through an established contact.'}] : []),
    ...(changed ? [{type:'payment_change',severity:'warning',phrase:changed,message:'The request mentions a change to payment instructions.',action:'Confirm the new details using contact information you already trust.'}] : []),
    ...(discouraged ? [{type:'verification_discouraged',severity:'warning',phrase:discouraged,message:'The request discourages independent contact.',action:'Use a previously known contact to verify the instructions.'}] : []),
    ...(crypto ? [{type:'crypto_payment',severity:'warning',phrase:crypto,message:'The request asks for cryptocurrency, which may be difficult to reverse.',action:'Verify the request independently before sending any funds.'}] : []),
    ...(sensitive ? [{type:'sensitive_information',severity:'warning',phrase:sensitive,message:'The request mentions sensitive access information. Check whether someone is asking you to disclose it.',action:'Never share seed phrases, private keys, passwords, or one-time codes with a payment requester.'}] : []),
    {type:'unverified_recipient',severity:'info',message:'Recipient identity and payment details have not been independently verified.'}
  ];
  const extracted=extractPayment(text);
  for(const link of inspectURLs(extracted.urls))for(const warning of link.warnings)indicators.push({type:'url_structure',severity:'warning',phrase:link.raw,message:warning,action:'Check the destination through the business’s independently established website.'});
  const warningCount=indicators.filter(i=>i.severity==='warning').length;
  const risk_level=warningCount>=2?'suspicious':warningCount===1?'needs_verification':'no_major_warnings_detected';
  const summary=warningCount>=2?'Several warning signs were detected. Independently verify the recipient before paying.':warningCount===1?'One warning sign was detected. Verify the recipient and payment instructions independently.':'No major warning pattern was detected by these local checks. This is not proof the payment is safe.';
  return {analysis_id:'local-'+Date.now(),payment_type:solana?'solana':'traditional',risk_level,summary,indicators,extracted,payment_details:{amount:extracted.amount,currency:extracted.currency,recipient:null},solana_analysis:{performed:false,network:null,wallet_address:null,transaction_count:null,known_scam_reports:null},demo:true};
}
export function validateReport(data) {
  if (!data || !['suspicious','needs_verification','no_major_warnings_detected'].includes(data.risk_level) || typeof data.summary !== 'string' || !Array.isArray(data.indicators) || data.indicators.some(i=>!i || typeof i.message!=='string')) throw new Error('The server returned an unsupported report format. Please ask your backend teammate to check the shared API contract.');
  return {
    ...data,
    indicators:data.indicators.map(indicator=>({...indicator,type:indicator.type||indicator.code||indicator.category||'finding',severity:indicator.severity==='critical'?'high':indicator.severity,phrase:indicator.phrase??indicator.evidence??null,action:indicator.action??indicator.next_action??null})),
    solana_analysis:data.solana_analysis?{...data.solana_analysis,transaction_count:data.solana_analysis.transaction_count??data.solana_analysis.recent_transaction_count??null,known_scam_reports:data.solana_analysis.known_scam_reports??null}:data.solana_analysis,
  };
}
export function explorerLink(address, network) {
  if (typeof address!=='string' || !/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(address)) return null;
  if (!['mainnet-beta','devnet','testnet'].includes(network)) return null;
  return `https://explorer.solana.com/address/${encodeURIComponent(address)}${network==='mainnet-beta'?'':`?cluster=${network}`}`;
}
