'use client';

import React, { useState, useRef } from 'react';

export default function GenClientComponent() {
    // const [videoFile, setVideoFile] = useState<File | null>(null);
    // const fileInputRef = useRef<HTMLInputElement>(null);

    // // Function to handle file input change
    // const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    //     const file = event.target.files ? event.target.files[0] : null;
    //     if (file) {
    //         setVideoFile(file);
    //     }
    // };

    // // Function to upload the video file to the backend
    // const uploadVideo = async () => {
    //     if (!videoFile) {
    //         alert('Please select a video file.');
    //         return;
    //     }

    //     const formData = new FormData();
    //     formData.append('file', videoFile);

    //     try {
    //         console.log('Uploading video file');
    //         const response = await fetch(`${process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : 'https://vercel-globetrotters-be-deployment.vercel.app'}/upload`, {
    //         // const response = await fetch('/upload', {
    //             method: 'POST',
    //             body: formData,
    //         });

    //         if (!response.ok) {
    //             throw new Error('Failed to upload video');
    //         }

    //         const data = await response.blob(); // Assuming response is a file (e.g., transcript)
    //         const url = URL.createObjectURL(data);

    //         // You can handle the response file here, e.g., show a download link
    //         const a = document.createElement('a');
    //         a.href = url;
    //         a.download = 'transcript.txt'; // Adjust the filename based on your backend's response
    //         document.body.appendChild(a);
    //         a.click();
    //         document.body.removeChild(a);
    //     } catch (error) {
    //         console.error('Error uploading video file:', error);
    //     }
    // };

    // const callJelly = async () => {
    //     try {
    //         console.log('Calling createJelly API');
    //         const response = await fetch('/api/createJelly', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json; charset=utf-8',
    //             },
    //             body: JSON.stringify({}),
    //         });
    //         const data = await response.json();
    //         console.log('API response:', data);
    //         return data;
    //     } catch (error) {
    //         console.error('Error calling createJelly API:', error);
    //         throw error;
    //     }
    // }

    // return (
    //     <>
    //         <div className="w-screen h-screen flex items-center justify-center">
    //             <div className="w-full h-full flex flex-col gap-4 items-center justify-center">
    //                 <p>Test Gen</p>
    //                 <input 
    //                     type="file" 
    //                     accept="video/*" 
    //                     ref={fileInputRef} 
    //                     onChange={handleFileChange} 
    //                     className="mb-4"
    //                 />
    //                 <button className="p-[3px]" onClick={uploadVideo}>Upload and Generate</button>
    //                 {/* <button className="p-[3px]" onClick={callJelly}>Generate</button> */}
    //             </div>
    //         </div>
    //     </>
    // );
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [videoSrc, setVideoSrc] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const videoRef = useRef<HTMLVideoElement>(null);
    
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setSelectedFile(file);
            const fileURL = URL.createObjectURL(file);
            setVideoSrc(fileURL);
        }
    };
    
    const handleUpload = async () => {
        if (!selectedFile) return;

        setIsLoading(true);
    
        const formData = new FormData();
        formData.append('file', selectedFile);
    
        try {
            const response = await fetch(`${process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : 'https://vercel-globetrotters-be-deployment.vercel.app'}/upload`, {
            method: 'POST',
                body: formData,
            });
    
            const blob = await response.blob();
            console.log('Blob:', blob);
            const url = URL.createObjectURL(blob);
            console.log('URL:', url);
            setVideoSrc(url);
            console.log('Video src:', videoSrc);

            setIsLoading(false);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };
    
    const handleCustomizeEffect = (effectType: string) => {
        // Placeholder function to send customization data to the backend
        console.log(`Applying effect: ${effectType}`);
    };
    
    return (
        <div className="w-screen h-screen flex flex-col items-center justify-center gap-4">
            <input type="file" accept="video/*" onChange={handleFileChange} />
            {videoSrc && (
                <>
                    <video ref={videoRef} controls src={videoSrc} className="max-w-full max-h-[400px]" />
                    <div className="flex gap-2 mt-4">
                        <button onClick={() => handleCustomizeEffect('grayscale')}>Grayscale</button>
                        <button onClick={() => handleCustomizeEffect('sepia')}>Sepia</button>
                        <button onClick={() => handleCustomizeEffect('invert')}>Invert</button>
                    </div>
                    {isLoading && <p>Loading...</p>}
                    <button onClick={handleUpload} className="mt-4">Upload & Apply Effects</button>
                </>
            )}
        </div>
    );

}

// const VideoEditor: React.FC = () => {
// };


