import { revalidatePath } from 'next/cache';
import GalleryClientComponent from './page';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Define the structure of a Video object
type Video = {
    url: string; // URL of the video
  };

async function fetchAllUrls() {
  try {
    const result: Video[] = await prisma.$queryRaw<Video[]>`
      SELECT * FROM fetch_all_urls();
    `;
    console.log('Fetched URLs:', result);
    return result;
  } catch (error) {
    console.error('Error fetching URLs:', error);
    throw new Error('Internal Server Error');
  } finally {
    await prisma.$disconnect();
  }
}


export default async function GenServerComponent() {    

    const videoUrls = await fetchAllUrls();

    revalidatePath('/gallery');

    return (
        <>
            <GalleryClientComponent videos={videoUrls} />
        </>
    );
}
