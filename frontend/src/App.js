import React, { useEffect, useState } from 'react';
import WelcomeScreen from './components/WelcomeScreen';
import AIAssistant from './components/AIAssistant';
import MapCanvas from './components/MapCanvas';
import SchedulePanel from './components/SchedulePanel';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

export default function App(){
  const [showWelcome, setShowWelcome] = useState(true);
  const [blueprint, setBlueprint] = useState(null);
  const [venueId] = useState('miet-meerut');
  const [selectedPath, setSelectedPath] = useState(null);

  useEffect(()=>{ const t=setTimeout(()=>setShowWelcome(false), 2200); return ()=>clearTimeout(t); }, []);

  useEffect(()=>{
    async function load(){
      try{
        const res = await fetch(`/data/venues/${venueId}.json`);
        if(res.ok){ const bp = await res.json(); setBlueprint(bp); return; }
      }catch(e){}
      try{ const r2 = await axios.get(`${API_BASE}/venues/${venueId}`); setBlueprint(r2.data); }catch(e){
        setBlueprint({
          venue_name: 'MIET (sample)',
          nodes:[{id:'Main Gate',x:80,y:80},{id:'Library',x:300,y:160},{id:'Lecture Hall 2',x:300,y:320},{id:'Hostel',x:80,y:360}],
          edges:[{from:'Main Gate',to:'Library',distance:200},{from:'Library',to:'Lecture Hall 2',distance:160},{from:'Lecture Hall 2',to:'Hostel',distance:200}]
        });
      }
    }
    load();
  },[venueId]);

  async function handleNavigationQuery(text){
    const res = await axios.post(`${API_BASE}/navigate`, { venue_id: venueId, text });
    setSelectedPath(res.data.path || res.data);
    return res.data;
  }

  return (
    <div className='min-h-screen bg-gradient-to-br from-sky-100 via-indigo-100 to-pink-50 flex items-center justify-center p-6'>
      {showWelcome ? (
        <WelcomeScreen />
      ) : (
        <div className='w-full max-w-6xl grid lg:grid-cols-12 gap-6'>
          <div className='lg:col-span-7 bg-white rounded-2xl shadow-xl p-6 flex flex-col'>
            <div className='flex items-center justify-between mb-4'>
              <div>
                <h1 className='text-2xl font-bold text-sky-700'>Virtual Event Assistant</h1>
                <p className='text-sm text-slate-500'>Ask where to go — by voice or text</p>
              </div>
              <div className='text-sm text-slate-400'>Venue: <strong>{blueprint?.venue_name || venueId}</strong></div>
            </div>

            <div className='flex gap-4 mb-4'>
              <AIAssistant onNavigate={handleNavigationQuery} />
            </div>

            <div className='flex-1'>
              <MapCanvas blueprint={blueprint} path={selectedPath} />
            </div>
          </div>

          <div className='lg:col-span-5 flex flex-col gap-4'>
            <div className='bg-white rounded-2xl shadow-xl p-4'>
              <h2 className='font-semibold mb-2'>Today's Schedule</h2>
              <SchedulePanel venueId={venueId} apiBase={API_BASE} />
            </div>

            <div className='bg-white rounded-2xl shadow-xl p-4'>
              <h2 className='font-semibold mb-2'>Assistant Logs</h2>
              <p className='text-xs text-slate-500'>Responses from AI and navigation are shown on the map and as chat bubbles.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
