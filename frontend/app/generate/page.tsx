'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Player, Script } from "liqvid";
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

            const data = await response.blob(); // Assuming response is a file (e.g., transcript)
            const url = URL.createObjectURL(data);

            // You can handle the response file here, e.g., show a download link
            const a = document.createElement('a');
            a.href = url;
            a.download = 'transcript.txt'; // Adjust the filename based on your backend's response
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
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
            <div className="w-full h-full flex items-center justify-center">
                <div className="w-1/2 h-full flex flex-col gap-4 place-items-center place-content-center">
                    <p>Test Gen</p>
                    <input 
                        type="file" 
                        accept="video/*" 
                        ref={fileInputRef} 
                        onChange={handleFileChange} 
                        className="w-max bg-blue-300"
                    />
                    <button className="p-[3px]" onClick={uploadVideo}>Generate</button>
                    {/* <button className="p-[3px]" onClick={callJelly}>Generate</button> */}
                </div>

                <div className='w-1/2 h-full flex place-items-center place-content-center '>
                    {script && (
                        <Player script={script}>
                            <Intro/>
                            <Plan/>
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