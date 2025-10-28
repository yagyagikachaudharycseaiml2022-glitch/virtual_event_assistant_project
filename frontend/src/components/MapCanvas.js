import React, { useEffect, useRef } from 'react';

export default function MapCanvas({ blueprint, path }){
  const canvasRef = useRef();

  useEffect(()=>{
    const canvas = canvasRef.current;
    if(!canvas || !blueprint) return;
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
    ctx.clearRect(0,0,canvas.width,canvas.height);

    const nodes = blueprint.nodes || [];
    const edges = blueprint.edges || [];

    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 2;
    edges.forEach(e=>{
      const a = nodes.find(n=>n.id===e.from||n.id===e.source);
      const b = nodes.find(n=>n.id===e.to||n.id===e.target);
      if(a && b){ ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke(); }
    });

    if(path && path.length){
      ctx.beginPath();
      ctx.strokeStyle = 'orange';
      ctx.lineWidth = 4;
      path.forEach((p, idx)=>{
        const pid = p.id || p;
        const node = nodes.find(n=>n.id===pid || n.id===(p.label || p.id));
        if(node){
          if(idx===0) ctx.moveTo(node.x, node.y); else ctx.lineTo(node.x, node.y);
        }
      });
      ctx.stroke();
    }

    nodes.forEach(n=>{
      ctx.beginPath();
      ctx.fillStyle = '#fff';
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 2;
      ctx.arc(n.x, n.y, 8, 0, Math.PI*2);
      ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#0f172a';
      ctx.font = '12px sans-serif';
      ctx.fillText(n.id, n.x + 10, n.y + 4);
    });

  }, [blueprint, path]);

  return (
    <div className='w-full h-96 bg-slate-50 rounded-lg p-2'>
      <canvas ref={canvasRef} style={{width:'100%', height:'100%'}} />
    </div>
  );
}
