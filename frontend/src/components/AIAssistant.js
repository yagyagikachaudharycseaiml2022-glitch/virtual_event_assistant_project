import React, { useState } from 'react';

export default function AIAssistant({ onNavigate }){
  const [text, setText] = useState('');
  const [listening, setListening] = useState(false);
  const [history, setHistory] = useState([]);

  let recognition = null;
  if(typeof window !== 'undefined' && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)){
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
  }

  function startListening(){
    if(!recognition) return alert('Speech recognition not supported (use Chrome).');
    setListening(true);
    recognition.start();
    recognition.onresult = (e) => {
      const t = e.results[0][0].transcript;
      setText(t);
      handleSend(t);
    };
    recognition.onerror = (e) => { console.error(e); setListening(false); };
    recognition.onend = () => setListening(false);
  }

  async function handleSend(overrideText){
    const q = overrideText ?? text;
    if(!q) return;
    setHistory(h => [...h, { who: 'user', text: q }]);
    setText('');
    try{
      const res = await onNavigate(q);
      const answer = (res && res.path) ? `Route: ${res.path.map(p=>p.label||p.id).join(' → ')}` : 'No path found.';
      setHistory(h => [...h, { who: 'assistant', text: answer }]);
    }catch(e){
      setHistory(h => [...h, { who: 'assistant', text: 'Error: ' + (e?.response?.data?.detail || e.message) }]);
    }
  }

  return (
    <div className='flex-1'>
      <div className='bg-white rounded-lg p-3 shadow-sm'>
        <div className='flex gap-2'>
          <input value={text} onChange={e=>setText(e.target.value)} placeholder="Say: I'm at Gate 3, take me to Hall 5" className='flex-1 border border-slate-200 rounded-md px-3 py-2' />
          <button onClick={()=> startListening()} className={`px-4 py-2 rounded-md ${listening ? 'bg-rose-500 text-white' : 'bg-amber-400 text-white'}`}>🎤</button>
          <button onClick={()=>handleSend()} className='px-4 py-2 bg-sky-600 text-white rounded-md'>Navigate</button>
        </div>

        <div className='mt-3 space-y-1 max-h-36 overflow-auto'>
          {history.slice().reverse().map((m,i)=>(
            <div key={i} className={`text-sm ${m.who==='user' ? 'text-right' : 'text-left'}`}>
              <div className={`inline-block px-3 py-1 rounded ${m.who==='user' ? 'bg-indigo-100 text-indigo-900' : 'bg-slate-100 text-slate-800'}`}>{m.text}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
