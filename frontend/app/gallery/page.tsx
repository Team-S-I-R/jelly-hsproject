
// Define the structure of a Video object
import BlurFade from "@/components/magicui/blur-fade";
import Sidebar from "../sidebar";

type Video = {
  url: string; // URL of the video
};

interface GalleryClientComponentProps {
  videos: Video[]; // Array of Video objects
}

export default function GalleryClientComponent({ videos }: GalleryClientComponentProps) {
  // Function to calculate dynamic width and height
  const calculateDimensions = (index: number) => {
    const baseWidth = 400;
    const baseHeight = 300;
    const width = baseWidth + (index % 3) * 50; // Example dynamic width calculation
    const height = baseHeight + (index % 3) * 50; // Example dynamic height calculation
    return { width, height };
  };

  return (
    <>
      <div className="w-screen h-screen overflow-y-scroll">
        <div className="w-full h-full flex p-2 gap-6 place-items-start">
         
         <Sidebar />

          <div className="w-full h-full flex flex-col p-4 place-items-start">
              {/* <h1 className="text-5xl bg-clip-text text-transparent drop-shadow-2xl bg-gradient-to-b from-white to-white/70 p-2 select-none">
                Gallery
              </h1> */}
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 p-4">
              {videos?.map((video, index) => {
                const { width, height } = calculateDimensions(index);
                return (
                  <BlurFade className="overflow-hidden rounded-lg" key={index} delay={0.25 + index * 0.10} inView>
                    <div
                      style={{ width: `${width}px`, height: `${height}px` }}
                    >
                      <video muted autoPlay loop className="w-full h-full object-cover">
                        <source src={video.url} type="video/mp4" />
                        Your browser does not support the video tag.
                      </video>
                    </div>
                  </BlurFade>
                );
              })}
              </div>
            </div>

        </div>
      </div>
    </>
  );
}
