import{u as y,h as f}from"./query-results-DX3PRUWY.js";import{d as v,l as n,o as i,c as d,g as s,w as l,a as o,f as w,F as b,e as a,h as g}from"./index-Bzw5iiEC.js";const k={key:1},B=v({__name:"ResultsSummaryView",setup(F){const u=y().annotations,c=n(()=>u.map(e=>e.depth_meters??NaN).filter(e=>!isNaN(e))),p=n(()=>{const e=f(c.value);return{series:[{name:"Depth",data:e.map(t=>t.count)}],options:{dataLabels:{enabled:!0},plotOptions:{bar:{horizontal:!0}},xaxis:{categories:e.map(t=>`${t.min.toFixed(0)}-${t.max.toFixed(0)}m`),lines:{show:!0},title:{text:"Count"}},yaxis:{lines:{show:!0},title:{text:"Depth (m)"}},tooltip:{enabled:!1}}}}),r=n(()=>({series:[{name:"T-S",data:u.filter(t=>t.temperature_celsius&&t.salinity).map(t=>[t.salinity,t.temperature_celsius])}],options:{grid:{xaxis:{lines:{show:!0},type:"numeric"},yaxis:{lines:{show:!0}}},xaxis:{lines:{show:!0},max:35.5,min:32.5,labels:{formatter:t=>t.toFixed(1)},tickAmount:10,title:{text:"Salinity (psu)"}},yaxis:{min:0,max:24,labels:{formatter:t=>t.toFixed(1)},lines:{show:!0},tickAmount:10,title:{text:"Temperature (C)"}},tooltip:{enabled:!1,x:{formatter:t=>t.toFixed(1)},y:{formatter:t=>t.toFixed(1)}}}}));return(e,t)=>{const x=a("router-link"),h=a("v-col"),_=a("v-row"),m=a("apexchart");return i(),d(b,null,[s(_,null,{default:l(()=>[s(h,null,{default:l(()=>[s(x,{to:"/results-table-view"},{default:l(()=>t[0]||(t[0]=[g("Back to results table")])),_:1})]),_:1})]),_:1}),o("div",null,[t[1]||(t[1]=o("h2",null,"Depth Histogram",-1)),s(m,{series:p.value.series,options:p.value.options,type:"bar",height:"700"},null,8,["series","options"])]),o("div",null,[t[2]||(t[2]=o("h2",null,"T-S Diagram",-1)),r.value.series[0].data.length>0?(i(),w(m,{key:0,series:r.value.series,options:r.value.options,type:"scatter",height:"700"},null,8,["series","options"])):(i(),d("div",k,"No data. To view this plot, return temperature and salinity data in your query"))])],64)}}});export{B as default};