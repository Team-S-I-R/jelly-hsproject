import { revalidatePath } from 'next/cache';
import GalleryClientComponent from './gallery';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Define the structure of a Video object
type Video = {
    url: string;
};

async function fetchAllUrls(): Promise<Video[]> {
    try {
        const result = await prisma.$queryRaw<{ url: string | null }[]>`
            SELECT url FROM fetch_all_urls();
        `;
        console.log('Fetched URLs:', result);
        return result.map(item => ({ url: item.url || '' }));
    } catch (error) {
        console.error('Error fetching URLs:', error);
        throw new Error('Internal Server Error');
    } finally {
        await prisma.$disconnect();
    }
}

export default async function GalleryPage() {    
    const videos = await fetchAllUrls();
    
    revalidatePath('/gallery');

    return <GalleryClientComponent initialVideos={videos} />;
}