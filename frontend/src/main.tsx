import React, { useState, useEffect, type FormEvent } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';
const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
type Institution={id:string;name:string;code:string};
type Competency={id:string;code:string;title:string;description:string;level:string};
async function api(path:string, token:string, institutionId?:string, options:RequestInit={}) {
 const headers:Record<string,string>={'Content-Type':'application/json',...((options.headers||{}) as Record<string,string>)};
 if(token) headers.Authorization=`Bearer ${token}`;
 if(institutionId) headers['X-Institution-Id']=institutionId;
 const res=await fetch(BASE+path,{...options,headers});
 if(!res.ok){ let detail=`HTTP ${res.status}`; try {const body=await res.json();detail=typeof body.detail==='string'?body.detail:detail;}catch{} throw Error(detail); }
 return res.json();
}
function App(){
 const [token,setToken]=useState(''); const [email,setEmail]=useState(''); const [password,setPassword]=useState('');
 const [institutions,setInstitutions]=useState<Institution[]>([]);const [institution,setInstitution]=useState('');
 const [competencies,setCompetencies]=useState<Competency[]>([]);const [code,setCode]=useState(''); const [title,setTitle]=useState('');
 const [error,setError]=useState('');const [loading,setLoading]=useState(false);
 useEffect(()=>{if(!token)return;api('/v1/institutions',token).then((items:Institution[])=>{setInstitutions(items);setInstitution(items[0]?.id||'');}).catch(e=>setError(e.message))},[token]);
 useEffect(()=>{if(!token||!institution)return;api('/v1/competencies',token,institution).then(setCompetencies).catch(e=>setError(e.message))},[token,institution]);
 async function login(e:FormEvent){e.preventDefault();setError('');setLoading(true);try{const data=await api('/v1/auth/login','',undefined,{method:'POST',body:JSON.stringify({email,password})});setToken(data.access_token);setPassword('');}catch(e){setError((e as Error).message)}finally{setLoading(false)}}
 async function add(e:FormEvent){e.preventDefault();setError('');setLoading(true);try{await api('/v1/competencies',token,institution,{method:'POST',body:JSON.stringify({code,title})});setCode('');setTitle('');setCompetencies(await api('/v1/competencies',token,institution));}catch(e){setError((e as Error).message)}finally{setLoading(false)}}
 return <main className="shell"><header><div className="brand">SIVEFOC <span>MASTER BUILDER</span></div><span className="status">Prototipo técnico · v0.2</span></header><section className="hero"><p className="eyebrow">Sistema de formación por competencias</p><h1>Gestión académica trazable y centrada en evidencias</h1><p>Primer núcleo funcional de demostración. No representa una plataforma autorizada ni validada institucionalmente.</p></section>
 {error&&<div role="alert" className="error">{error}</div>}
 {!token?<section className="panel narrow"><h2>Iniciar sesión</h2><p>Utiliza la cuenta de demostración que configuraste localmente.</p><form onSubmit={login}><label>Correo electrónico<input type="email" value={email} onChange={e=>setEmail(e.target.value)} required/></label><label>Contraseña<input type="password" value={password} onChange={e=>setPassword(e.target.value)} required/></label><button disabled={loading}>Entrar</button></form></section>:<><div className="toolbar"><label>Institución<select value={institution} onChange={e=>setInstitution(e.target.value)}>{institutions.map(i=><option key={i.id} value={i.id}>{i.name}</option>)}</select></label><button className="secondary" onClick={()=>{setToken('');setInstitutions([]);setCompetencies([]);setError('')}}>Salir</button></div><div className="cols"><section className="panel"><h2>Competencias registradas</h2>{competencies.length===0?<p>No hay competencias en esta institución.</p>:<ul>{competencies.map(c=><li key={c.id}><strong>{c.code}</strong> · {c.title}</li>)}</ul>}</section><section className="panel"><h2>Nueva competencia</h2><p>Requiere rol administrador o docente.</p><form onSubmit={add}><label>Código<input value={code} onChange={e=>setCode(e.target.value)} required minLength={2} maxLength={40}/></label><label>Nombre<input value={title} onChange={e=>setTitle(e.target.value)} required minLength={3} maxLength={200}/></label><button disabled={loading||!institution}>Guardar competencia</button></form></section></div></>}
 <footer>Arquitectura inicial SIVEFOC · La información de demostración no constituye información oficial.</footer></main>;
}
createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
