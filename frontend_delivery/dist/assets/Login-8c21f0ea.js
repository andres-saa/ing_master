import{_ as k}from"./logo-c69ae777.js";import{_ as h,u as S,b as p,C as I,O as T,r as n,o as C,c as U,a as r,e,F as V,y as B,z as E,U as P,Q as W}from"./index-147646d1.js";const m=l=>(B("data-v-579633b0"),l=l(),E(),l),j={class:"flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden"},A={class:"flex flex-column align-items-center justify-content-center"},F={style:{"border-radius":"2rem",border:"3px solid var(--primary-color)"}},L={class:"w-full surface py-6 px-2 sm:px-5"},O=m(()=>e("div",{class:"text-center mb-5"},[e("img",{src:k,alt:"Image",height:"50",class:"mb-3"}),e("div",{style:{color:"black"},class:"text-balck text-3xl font-medium mb-3"},"Bienvenido, Admin!"),e("span",{class:"text-600 text-white font-medium"},"Inicia sesion para continuar")],-1)),R=m(()=>e("label",{for:"email1",class:"block text-900 text-xl font-medium mb-2"},"Usuario",-1)),$=m(()=>e("label",{for:"password1",class:"block text-900 font-medium text-xl mb-2"},"Contrasena",-1)),D=m(()=>e("div",{class:"flex align-items-center justify-content-between mb-5 gap-5"},[e("div",{class:"flex align-items-center"})],-1)),M={__name:"Login",setup(l){const _=S(),c=p(""),i=p(""),d=I(),f=T();let a=null;const v=async()=>{try{if(!c.value||!i.value){d.add({severity:"error",summary:"Campos vacíos",detail:"Por favor, completa todos los campos",life:3e3});return}const t=new FormData;t.append("username",c.value),t.append("password",i.value);const o=await fetch(`${P}/token`,{method:"POST",body:t});if(o.ok){const s=await o.json();localStorage.setItem("accessToken",s.access_token),localStorage.setItem("siteId",s.site_id),b(s.site_id),_.setSite(s),f.push("/"),d.add({severity:"success",summary:"Bienvenido",detail:"",life:3e3})}else console.error("Error de inicio de sesión:",o.statusText),d.add({severity:"error",summary:"Usuario o contraseña incorrectos",detail:"",life:3e3})}catch(t){console.error("Error al enviar la solicitud:",t),d.add({severity:"error",summary:"Error en la solicitud",detail:"Por favor, intenta de nuevo más tarde",life:3e3})}};function b(t){a=new WebSocket(`wss://${W}/ws/${t}`),a.onopen=()=>console.log("WebSocket connected"),a.onmessage=o=>console.log("Message received:",o.data),a.onclose=()=>console.log("WebSocket disconnected"),a.onerror=o=>console.error("WebSocket error:",o)}return(t,o)=>{const s=n("Toast"),x=n("InputText"),g=n("Password"),y=n("Button"),w=n("AppConfig");return C(),U(V,null,[r(s),e("div",j,[e("div",A,[e("div",F,[e("div",L,[O,e("div",null,[R,r(x,{id:"email1",type:"text",placeholder:"Usuario",class:"w-full md:w-30rem mb-5",style:{padding:"1rem"},modelValue:c.value,"onUpdate:modelValue":o[0]||(o[0]=u=>c.value=u)},null,8,["modelValue"]),$,r(g,{id:"password1",modelValue:i.value,"onUpdate:modelValue":o[1]||(o[1]=u=>i.value=u),placeholder:"contrasena",toggleMask:!0,class:"w-full mb-3",inputClass:"w-full",inputStyle:{padding:"1rem"}},null,8,["modelValue"]),D,r(y,{label:"Iniciar Sesion",class:"w-full p-3 text-xl button-send",style:{border:"none","background-color":"var(--primary-color)"},onClick:v})])])])])]),r(w,{simple:""})],64)}}},K=h(M,[["__scopeId","data-v-579633b0"]]);export{K as default};
