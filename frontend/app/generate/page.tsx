'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Player, Script, Controls } from "liqvid";
import { BackgroundGradientAnimation } from "../../components/ui/background-gradient-animations";
import Sidebar from '../sidebar';
import { motion } from 'framer-motion';


export default function GenClientComponent() {
    const [videoFile, setVideoFile] = useState<File | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [videoUrl, setVideoUrl] = useState<string>('/testvid.mp4'); // Reference the file directly
    const [isLoading, setIsLoading] = useState(false);

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

        setIsLoading(true);

        const formData = new FormData();
        formData.append('file', videoFile);

        try {
            console.log('Uploading video file');
            const response = await fetch(`${process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : 'https://jelly-hackathon-hs.fly.dev/'}/main`, {
            // const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to upload video');
            }

            const data = await response.json(); // Assuming response is a file (e.g., transcript)
            setVideoUrl(data.url);

            setIsLoading(false);

        } catch (error) {
            console.error('Error uploading video file:', error);
        }
    };

    // this connects to the jelly api....but there were many issues after connection like videos not even being created
    // able to record. Also we were able to actually save the video even if we were able to record.
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


    
    
    
    const VideoRecorder = () => {
                
        const [permission, setPermission] = useState(false);
        const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
        const [audio, setAudio] = useState<Blob | null>(null);
        const mediaRecorder = useRef<MediaRecorder | null>(null);
        const liveVideoFeed = useRef<HTMLVideoElement | null>(null);
        const [recordingStatus, setRecordingStatus] = useState("inactive");
        const [stream, setStream] = useState<MediaStream | null>(null);
        const [videoChunks, setVideoChunks] = useState<Blob[]>([]); // Explicitly type as Blob[]
        const [recordedVideo, setRecordedVideo] = useState<string | null>(null);

        const mimeType = "video/webm";

        const toggleCamera = async () => {
            if (permission) {
                // Turn off the camera
                stream?.getTracks().forEach(track => track.stop());
                setPermission(false);
                setStream(null);
            } else {
                // Turn on the camera
                if ("MediaRecorder" in window) {
                    try {
                        const streamData = await navigator.mediaDevices.getUserMedia({
                            audio: true,
                            video: true,
                        });
                        setPermission(true);
                        setStream(streamData);
                        if (liveVideoFeed.current) {
                            liveVideoFeed.current.srcObject = streamData;
                        }
                    } catch (err : any) {
                        alert(err.message);
                    }
                } else {
                    alert("The MediaRecorder API is not supported in your browser.");
                }
            }
        };

        const getMicrophonePermission = async () => {
            if ("MediaRecorder" in window) {
                try {
                    const streamData = await navigator.mediaDevices.getUserMedia({
                        audio: true,
                        video: false,
                    });
                    setPermission(true);
                    setStream(streamData);
                } catch (err : any) {
                    alert(err.message);
                }
            } else {
                alert("The MediaRecorder API is not supported in your browser.");
            }
        };
    
        const getCameraPermission = async () => {
            setRecordedVideo(null);
            if ("MediaRecorder" in window) {
                try {
                    const videoConstraints = {
                        audio: false,
                        video: true,
                    };
                    const audioConstraints = { audio: true };
                    // create audio and video streams separately
                    const audioStream = await navigator.mediaDevices.getUserMedia(
                        audioConstraints
                    );
                    const videoStream = await navigator.mediaDevices.getUserMedia(
                        videoConstraints
                    );
                    setPermission(true);
                    //combine both audio and video streams
                    const combinedStream = new MediaStream([
                        ...videoStream.getVideoTracks(),
                        ...audioStream.getAudioTracks(),
                    ]);
                    setStream(combinedStream);
                    if (liveVideoFeed.current) {
                        liveVideoFeed.current.srcObject = combinedStream;
                    }
                } catch (err : any) {
                    alert(err.message);
                }
            } else {
                alert("The MediaRecorder API is not supported in your browser.");
            }
        };

        const startRecording = async () => {
            if (!stream) {
                alert("No media stream available.");
                return;
            }
            setRecordingStatus("recording");
            const media = new MediaRecorder(stream, { mimeType });
            mediaRecorder.current = media;
            mediaRecorder.current.start();
            let localVideoChunks: Blob[] = [];
            mediaRecorder.current.ondataavailable = (event) => {
                if (typeof event.data === "undefined") return;
                if (event.data.size === 0) return;
                localVideoChunks.push(event.data);
            };
            setVideoChunks(localVideoChunks);
        };
    
        const stopRecording = () => {
            if (!mediaRecorder.current) {
                alert("No media recorder available.");
                return;
            }
            setPermission(false);
            setRecordingStatus("inactive");
            mediaRecorder.current.stop();
            mediaRecorder.current.onstop = () => {
                const videoBlob = new Blob(videoChunks, { type: mimeType });
                const videoUrl = URL.createObjectURL(videoBlob);
                setRecordedVideo(videoUrl);
                setVideoChunks([]);
            };
        };

        return (
            <div className='w-full flex flex-col justify-between place-items-center place-content-center h-full p-4'>
                <h2>Video Recorder</h2>
                <main>
                    <div className="audio-controls">
                        {!permission ? (
                            <button onClick={getCameraPermission} type="button">
                                Get Camera
                                </button>                       
                        ) : null}
                        {permission && recordingStatus === "inactive" ? (
                            <button onClick={startRecording} type="button">
                                Start Recording
                            </button>
                        ) : null}
                        {recordingStatus === "recording" ? (
                            <button onClick={stopRecording} type="button">
                                Stop Recording
                            </button>
                        ) : null}
                    </div>
                    {permission && (
                        <video ref={liveVideoFeed} autoPlay muted className="w-full h-auto mt-4"></video>
                    )}
                </main>
                <div></div>
            </div>
        );
    };



    return (
        <>
            <BackgroundGradientAnimation className="flex flex-col place-items-center place-content-center h-full w-full"/>
            <div className="w-screen h-screen flex items-center justify-center">
                
                <Sidebar/>

                <div className="w-1/2 py-[4%] h-full flex flex-col gap-4 place-items-center place-content-center">
                    
                    <VideoRecorder/>

                    <input 
                        type="file" 
                        accept="video/*" 
                        ref={fileInputRef} 
                        onChange={handleFileChange} 
                        className="w-max p-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                       
                    {isLoading === false && (
                            <>
                            <motion.button 
                            initial={{ opacity: 0, y: 50 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5 }}
                            className="p-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition duration-300" onClick={uploadVideo}>Generate</motion.button>
                            </>
                    )}

                    {isLoading === true && (
                        <>
                        <motion.button 
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="p-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition duration-300" onClick={uploadVideo}>Generating Video....</motion.button>
                        </>
                    )}

                </div>

                <div className='w-[50%] h-[100%] flex place-items-center place-content-center '>
                    {script && (
                        <video autoPlay muted src={videoUrl}></video>
                        // <Player  className='' script={script}>
                        // </Player>
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