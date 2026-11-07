import jsQR from 'jsqr';
import {validateImage,parseSolanaQR} from './payment';
export async function scanImage(file,progress) {
 validateImage(file);progress('Reading image…');
 const bitmap=await createImageBitmap(file);
 if(bitmap.width*bitmap.height>20000000){bitmap.close();throw new Error('This image is too large to process. Resize it to under 20 megapixels.');}
 const canvas=document.createElement('canvas');const ratio=Math.min(1,2500/Math.max(bitmap.width,bitmap.height));canvas.width=Math.round(bitmap.width*ratio);canvas.height=Math.round(bitmap.height*ratio);
 const context=canvas.getContext('2d',{willReadFrequently:true});context.drawImage(bitmap,0,0,canvas.width,canvas.height);bitmap.close();
 const pixels=context.getImageData(0,0,canvas.width,canvas.height);const code=jsQR(pixels.data,pixels.width,pixels.height,{inversionAttempts:'attemptBoth'});
 let qr=null;let qrError=null;if(code){try{qr=parseSolanaQR(code.data);}catch(e){qrError=e.message;qr={kind:'invalid',raw:code.data};}}
 progress('Starting text recognition…');const {createWorker}=await import('tesseract.js');let worker;
 try{worker=await createWorker('eng',1,{workerPath:new URL('/ocr/worker.min.js',location.origin).href,corePath:new URL('/ocr/core',location.origin).href,langPath:new URL('/ocr/lang',location.origin).href,workerBlobURL:false,cacheMethod:'none',logger:m=>{if(m.status)progress(`${m.status}${Number.isFinite(m.progress)?` · ${Math.round(m.progress*100)}%`:''}`);}});const result=await worker.recognize(canvas);return {text:result.data.text.trim(),confidence:Math.round(result.data.confidence),qr,qrError};}
 catch(e){if(qr)return {text:'',confidence:null,qr,qrError,ocrError:'Text recognition was unavailable. The QR was decoded; review its content below.'};throw new Error('Text recognition could not finish. Try a clearer image or paste the text instead.');}
 finally{if(worker)await worker.terminate();canvas.width=0;canvas.height=0;}
}
