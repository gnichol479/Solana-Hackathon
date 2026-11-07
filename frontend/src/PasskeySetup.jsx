import React,{useState} from 'react';
import {Fingerprint,ScanFace,ArrowRight,Check,LoaderCircle,ShieldCheck} from 'lucide-react';
import {ACCOUNT_API,request} from './api';

export default function PasskeySetup({user,navigate}) {
 const [busy,setBusy]=useState(false),[error,setError]=useState(''),[complete,setComplete]=useState(false);
 const supported=Boolean(window.PublicKeyCredential&&navigator.credentials&&window.isSecureContext);
 async function enroll(){
  if(!user||busy||complete)return;
  setBusy(true);setError('');
  try{
   const {startRegistration}=await import('@simplewebauthn/browser');
   const options=await request('/api/auth/passkeys/register/options',{method:'POST',body:{}});
   const credential=await startRegistration({optionsJSON:options.options});
   await request('/api/auth/passkeys/register/verify',{method:'POST',body:{challenge_id:options.challenge_id,credential}});
   setComplete(true);
  }catch(e){setError(e.name==='NotAllowedError'?'Setup was canceled or your device could not complete it. You can try again or set it up later.':e.name==='InvalidStateError'?'This device already has a passkey for your account. You can continue to your workspace.':e.message);}
  finally{setBusy(false);}
 }
 return <div className="passkey-onboarding"><div className="onboarding-steps" aria-label="Account setup progress"><span className={user?'done':''}>{user?<Check size={13}/>:<span>1</span>}Create account</span><i/><span className="current"><span>2</span>Device sign-in</span><i/><span><span>3</span>Workspace</span></div><section className="panel passkey-setup-card" aria-labelledby="passkey-setup-title"><div className="setup-illustration">{complete?<ShieldCheck size={48}/>:<ScanFace size={48}/>}</div><div className="eyebrow">{complete?'READY FOR YOUR NEXT SIGN-IN':'MAKE YOUR NEXT SIGN-IN EASIER'}</div><h1 id="passkey-setup-title">{complete?'Your passkey is ready.':'Set up Face ID or a passkey.'}</h1><p className="setup-description">{complete?'Your device passkey has been verified and linked to your Bait account.':'Use your device’s built-in security for a faster sign-in next time.'}</p><div className="setup-explainer"><Fingerprint size={22}/><p>Your device chooses the available method: Face ID, Touch ID, Windows Hello, a security key, or a device PIN. Bait never receives your face or fingerprint data.</p></div>{!ACCOUNT_API&&<div className="demo-notice"><span>Account services are not connected yet. This step becomes available after your account is successfully created on the backend.</span></div>}{!user&&ACCOUNT_API&&<div className="demo-notice"><span>Sign in or create an account before registering a device passkey.</span></div>}{!supported&&<p className="subtle">Passkeys are unavailable in this browser. Try a compatible browser on HTTPS, or set this up later.</p>}{error&&<div className="error" role="alert">{error}</div>}{complete?<><div className="success" role="status"><Check size={17}/>Passkey registered successfully</div><button className="primary full" onClick={()=>navigate('analyze')}>Continue to workspace <ArrowRight size={17}/></button></>:<><button className="primary full" disabled={busy||!user||!supported||!ACCOUNT_API} onClick={enroll}>{busy?<LoaderCircle className="spin" size={18}/>:<Fingerprint size={19}/>} {busy?'Waiting for your device…':'Set up device sign-in'}</button>{!user?<button className="secondary full" onClick={()=>navigate('account')}>Go to sign in / create account <ArrowRight size={16}/></button>:<button className="text-button setup-later" disabled={busy} onClick={()=>navigate('analyze')}>Set up later <ArrowRight size={15}/></button>}</>}<p className="setup-footnote">No camera scan or facial image upload is required. Your device handles authentication.</p></section></div>;
}
