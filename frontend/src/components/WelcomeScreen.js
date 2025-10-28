import React from 'react';

export default function WelcomeScreen(){
  return (
    <div className='w-full max-w-2xl bg-white/80 rounded-3xl p-8 shadow-2xl flex items-center justify-center flex-col'>
      <div className='animate-fade-in text-center'>
        <h1 className='text-4xl font-extrabold text-sky-700 mb-3'>✨ Welcome to</h1>
        <h2 className='text-3xl font-bold'>Virtual Event Assistant</h2>
        <p className='text-slate-500 mt-3'>Your indoor navigation & event guide</p>
      </div>
    </div>
  );
}
