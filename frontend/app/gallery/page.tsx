
// Define the structure of a Video object
type Video = {
  url: string; // URL of the video
};

interface GalleryClientComponentProps {
  videos: Video[]; // Array of Video objects
}

export default function GalleryClientComponent({ videos }: GalleryClientComponentProps) {
  return (
    <>
      <div className="w-screen h-screen overflow-y-scroll">
        <div className="w-full h-full flex flex-col">
          <h1>Gallery</h1>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 p-4">
            {videos?.map((video, index) => (
              <div key={index} className="video-item bg-red-500 w-full h-[500px] overflow-hidden rounded-md flex items-center justify-center">
                <video className="w-full h-full object-cover">
                  <source src={video.url} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}