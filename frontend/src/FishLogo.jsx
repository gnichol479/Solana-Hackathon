import React from 'react';

export default function FishLogo({className=''}) {
  return <svg className={className} viewBox="0 0 32 32" fill="none" aria-hidden="true">
    <path d="M9 16 3 10v12l6-6Zm0 0c4.4-6.4 11.3-8 18.5-4.4L30 16l-2.5 4.4C20.3 24 13.4 22.4 9 16Z" fill="currentColor"/>
    <circle cx="23" cy="14" r="1.25" fill="#172a20"/>
  </svg>;
}
