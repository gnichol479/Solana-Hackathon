export const API=(import.meta.env.VITE_API_BASE_URL||'').replace(/\/$/,'');
let csrf=null;
export async function request(path,{method='GET',body}={}) {
 if(!API)throw new Error('Account services are not connected yet. Your team must deploy the backend and configure its address.');
 const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),30000);
 try{const res=await fetch(API+path,{method,credentials:'include',headers:{'Content-Type':'application/json',...(csrf?{'X-CSRF-Token':csrf}:{})},body:body?JSON.stringify(body):undefined,signal:controller.signal});const data=await res.json();if(!res.ok)throw new Error(typeof data.detail==='string'?data.detail:'The service could not complete this request.');if(data.csrf)csrf=data.csrf;return data;}catch(e){if(e.name==='AbortError')throw new Error('The service timed out. Please try again.');if(e.message==='Failed to fetch')throw new Error('Cannot reach the backend. Check the service and connection.');throw e;}finally{clearTimeout(timeout);}
}
