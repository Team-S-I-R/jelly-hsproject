'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Player, Script, Controls } from "liqvid";
import { BackgroundGradientAnimation } from "../../components/ui/background-gradient-animations";


export default function GenClientComponent() {
    const [videoFile, setVideoFile] = useState<File | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [videoUrl, setVideoUrl] = useState<string>('/testvid.mp4'); // Reference the file directly

    // Function to handle file input change
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files ? event.target.files[0] : null;
        if (file) {
            setVideoFile(file);
        }
    };

    // Function to upload the video file to the backend
    const uploadVideo = async () => {
        if (!videoFile) {
            alert('Please select a video file.');
            return;
        }
        const formData = new FormData();
        formData.append('file', videoFile);

        try {
            console.log('Uploading video file');
            const response = await fetch(`${process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : 'https://vercel-globetrotters-be-deployment.vercel.app'}/main`, {
            // const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to upload video');
            }

            const data = await response.json(); // Assuming response is a file (e.g., transcript)
            setVideoUrl(data.url);

        } catch (error) {
            console.error('Error uploading video file:', error);
        }
    };

    const callJelly = async () => {
        try {
            console.log('Calling createJelly API');
            const response = await fetch('/api/createJelly', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json; charset=utf-8',
                },
                body: JSON.stringify({}),
            });
            const data = await response.json();
            console.log('API response:', data);
            return data;
        } catch (error) {
            console.error('Error calling createJelly API:', error);
            throw error;
        }
    }      

    type Marker = [string, string | number];

    const markers: Marker[] = [
        ["intro/", "0:01.5"],
        ["intro/world", "0:01.5"],
        ["plan/", "0:01"],
        ["plan/1", "0:01"],
        ["plan/2", "0:01"],
        ["plan/3", "0:01"]
    ];

    const [script, setScript] = useState<Script | null>(null);

    // ALL OF THE REACT STUFF THAT NEEDS TO HAPPEN WILL HAPPEN FIRST
    useEffect(() => {
        // AND THEN THE PLAYER WILL TRY TO RENDER
        setScript(new Script(markers));
    }, []);


    function Intro() {
        return (
            <section data-during="intro/">
                <h1>Hello <span data-from-first="intro/world">World!</span></h1>
            </section>
        );
    }
    
    function Plan() {
        return (
            <section data-during="plan/">
                <h2>The Plan</h2>
                <ol>
                    <li data-from-first="plan/1">Make interactive videos</li>
                    <li data-from-first="plan/2">???</li>
                    <li data-from-first="plan/3">Profit!</li>
                </ol>
            </section>
        );
    }


    return (
        <>
            <BackgroundGradientAnimation className="flex flex-col place-items-center place-content-center h-full w-full"/>
            <div className="w-screen h-screen flex items-center justify-center">
                <div className="w-1/2 h-full flex flex-col gap-4 place-items-center place-content-center">
                    <input 
                        type="file" 
                        accept="video/*" 
                        ref={fileInputRef} 
                        onChange={handleFileChange} 
                        className="w-max p-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <button className="p-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition duration-300" onClick={uploadVideo}>Generate</button>
                </div>

                <div className='w-[50%] h-[100%] flex place-items-center place-content-center '>
                    {script && (
                        <Player  className='' script={script}>
                           <video src={videoUrl}></video>
                        </Player>
                    )}
                </div>
            </div>
        </>
    );
}


// waitlist

// record yourself and see your video
// generate

// mapped videos in the database
// explore page