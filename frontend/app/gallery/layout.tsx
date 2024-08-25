import { revalidatePath } from 'next/cache';
import GalleryClientComponent from './page';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function fetchAllUrls(): Promise<string[]> {
    try {
        const result = await prisma.$queryRaw<{ url: string | null }[]>`
            SELECT url FROM fetch_all_urls();
        `;
        console.log('Fetched URLs:', result);
        return result
            .map(item => item.url)
            .filter((url): url is string => url !== null);
    } catch (error) {
        console.error('Error fetching URLs:', error);
        throw new Error('Internal Server Error');
    } finally {
        await prisma.$disconnect();
    }
}

export default async function GalleryPage() {    
    const urls = await fetchAllUrls();
    
    revalidatePath('/gallery');

    return <GalleryClientComponent initialVideos={urls.map(url => ({ url }))} />;
}