const env=import.meta.env||{};
const runtimeEnv=typeof process==='object'&&process?.env?process.env:{};
export const API=(env.VITE_API_BASE_URL||runtimeEnv.VITE_API_BASE_URL||'').replace(/\/$/,'');
export const ACCOUNT_API=(env.VITE_ACCOUNT_API_BASE_URL||runtimeEnv.VITE_ACCOUNT_API_BASE_URL||'').replace(/\/$/,'');
let accountCsrf=null;

async function send(base,path,{method='GET',body}={},service){
 if(!base)throw new Error(`${service} is not connected yet. Configure its API origin first.`);
 const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),30000);
 try{const res=await fetch(base+path,{method,credentials:'include',headers:{'Content-Type':'application/json',...(service==='account service'&&accountCsrf?{'X-CSRF-Token':accountCsrf}:{})},body:body?JSON.stringify(body):undefined,signal:controller.signal});const data=await res.json();if(!res.ok)throw new Error(typeof data.detail==='string'?data.detail:'The service could not complete this request.');if(service==='account service'&&data.csrf)accountCsrf=data.csrf;return data;}catch(e){if(e.name==='AbortError')throw new Error('The service timed out. Please try again.');if(e.message==='Failed to fetch')throw new Error('Cannot reach the service. Check that it is running.');throw e;}finally{clearTimeout(timeout);}
}

function isAccountPath(path){return path.startsWith('/api/auth')||path==='/api/reports'||path.startsWith('/api/reports/');}
export function request(path,options={}){return isAccountPath(path)?accountRequest(path,options):send(API,path,options,'analysis service');}
export async function accountRequest(path,options={}){
 try{return await send(ACCOUNT_API,path,options,'account service');}
 catch(error){
  const method=options.method||'GET';
  if(method!=='GET'&&error.message==='Invalid CSRF token.'){
   accountCsrf=null;
   await send(ACCOUNT_API,'/api/auth/me',{},'account service');
   return send(ACCOUNT_API,path,options,'account service');
  }
  throw error;
 }
}
