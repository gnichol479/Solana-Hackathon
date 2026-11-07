import {test} from 'node:test';
import assert from 'node:assert/strict';

const previousAccountApi=process.env.VITE_ACCOUNT_API_BASE_URL;
process.env.VITE_ACCOUNT_API_BASE_URL='http://account';
const {accountRequest}=await import('./api.js?csrf-test');
if(previousAccountApi===undefined)delete process.env.VITE_ACCOUNT_API_BASE_URL;
else process.env.VITE_ACCOUNT_API_BASE_URL=previousAccountApi;

function response(status,data){return {ok:status<400,json:async()=>data};}

test('refreshes a stale account CSRF token and retries a mutating request once',async()=>{
  const calls=[];
  const originalFetch=globalThis.fetch;
  let reportAttempts=0;
  globalThis.fetch=async(url,options)=>{
    calls.push({url,options});
    if(url.endsWith('/api/auth/login'))return response(200,{csrf:'stale',user:{id:'user-1',email:'test@example.com'}});
    if(url.endsWith('/api/reports')&&options.method==='POST'&&reportAttempts++===0)return response(403,{detail:'Invalid CSRF token.'});
    if(url.endsWith('/api/auth/me'))return response(200,{csrf:'fresh',user:{id:'user-1',email:'test@example.com'}});
    if(url.endsWith('/api/reports')&&options.method==='POST')return response(200,{ok:true});
    throw new Error(`Unexpected request: ${options.method} ${url}`);
  };
  try{
    await accountRequest('/api/auth/login',{method:'POST',body:{email:'test@example.com',password:'password'}});
    assert.deepEqual(await accountRequest('/api/reports',{method:'POST',body:{report:{risk_level:'needs_verification'}}}),{ok:true});
    assert.equal(calls.length,4);
    assert.equal(calls[1].options.headers['X-CSRF-Token'],'stale');
    assert.equal(calls[2].url,'http://account/api/auth/me');
    assert.equal(calls[3].options.headers['X-CSRF-Token'],'fresh');
  }finally{globalThis.fetch=originalFetch;}
});
