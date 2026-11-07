import {test} from 'node:test';
import assert from 'node:assert/strict';
import {demoReport,examples,validateReport,explorerLink} from './report.js';
test('demo never fabricates chain evidence or recipient verification',()=>{for(const text of Object.values(examples)){const r=demoReport(text);assert.equal(r.demo,true);assert.equal(r.solana_analysis.performed,false);assert.equal(r.solana_analysis.transaction_count,null);assert.equal(r.payment_details.recipient,null);validateReport(r);}});
test('suspicious example includes actionable signals',()=>{const r=demoReport(examples.invoice);assert.equal(r.risk_level,'suspicious');assert.ok(r.indicators.some(i=>i.type==='payment_change'));assert.equal(demoReport(examples.routine).risk_level,'needs_verification');});
test('malformed backend reports fail clearly',()=>{for(const data of [null,{}, {risk_level:'safe',summary:'safe',indicators:[]},{risk_level:'suspicious',summary:'x',indicators:[null]}])assert.throws(()=>validateReport(data));});
test('explorer links reject unsafe values and preserve network',()=>{assert.equal(explorerLink('javascript:alert(1)','devnet'),null);assert.equal(explorerLink('11111111111111111111111111111111','evil'),null);assert.equal(explorerLink('11111111111111111111111111111111','devnet'),'https://explorer.solana.com/address/11111111111111111111111111111111?cluster=devnet');});
