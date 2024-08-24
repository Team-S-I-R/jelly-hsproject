'use client'

export default function GenClientComponent() {
    
    const callJelly = async () => {
        try {
            const response = await fetch('/api/createJelly', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json; charset=utf-8',
                },
                body: JSON.stringify({}),
            });
            const data = await response.json();
            console.log(data);
            return data;
        } catch (error) {
            console.error('Error calling createJelly API:', error);
            throw error;
        }
    }

    return (
    <>
        <div className="w-screen h-screen flex place-items-center place-content-center">
            <div className="w-full h-full flex flex-col gap-4 place-items-center place-content-center">
                <p> Test Gen </p>
                <div>
                    <button className="p-[3px] " onClick={callJelly}>Generate</button>
                </div>
            </div>

        </div>
    </>
    )
}