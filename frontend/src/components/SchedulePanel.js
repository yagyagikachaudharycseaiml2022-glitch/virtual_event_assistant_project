import React, { useEffect, useState } from 'react';
import axios from 'axios';
import dayjs from 'dayjs';

export default function SchedulePanel({ venueId, apiBase }){
  const [events, setEvents] = useState([]);

  useEffect(()=>{
    async function load(){
      try{
        const res = await axios.get(`${apiBase}/events/${venueId}`);
        setEvents(res.data || []);
      }catch(e){
        setEvents([
          { hall_id: 'Hall No-5', title: 'AI Summit', start_time: '2025-10-09T10:00:00' },
          { hall_id: 'Hall No-3', title: 'Robotics Demo', start_time: '2025-10-09T11:30:00' },
        ]);
      }
    }
    load();
  },[venueId, apiBase]);

  return (
    <div className='space-y-2'>
      {events.map((ev,i)=>(
        <div key={i} className='p-3 bg-white rounded-md shadow-sm flex justify-between items-center'>
          <div>
            <div className='font-semibold'>{ev.title}</div>
            <div className='text-xs text-slate-400'>{ev.hall_id}</div>
          </div>
          <div className='text-xs text-slate-500'>{dayjs(ev.start_time).format('HH:mm')}</div>
        </div>
      ))}
    </div>
  );
}
