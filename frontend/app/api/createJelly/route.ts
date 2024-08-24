import { NextRequest } from "next/server";


interface JellyResponse {
    talkId: string;
    url: string;
    shortUrl: {
      slug: string;
      short: string;
    };
  }

  const jellyKey = process.env.JELLY_API_KEY as string;
  

  import { NextResponse } from "next/server";

//   test prod
  export async function POST(req: NextRequest): Promise<NextResponse> {
    const apiUrl = 'https://www.jellyjelly.com/api/ti/start_jelly';
    
    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Authorization': `Bearer ${jellyKey}`,
        },
        // Since we're not specifying privacy, we can send an empty body
        body: JSON.stringify({}),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data: JellyResponse = await response.json();
      console.log(data);
      return NextResponse.json(data);
    } catch (error) {
      console.error('Error creating jelly:', error);
      return NextResponse.json({ error: 'Failed to create jelly' }, { status: 500 });
    }
  }