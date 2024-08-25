"use client";

import { House, Globe, Sparkles, User, Settings, Images } from "lucide-react";
import Link from "next/link";

export default function Sidebar() {
	return (
		<>
			<div className="z-10 text-white justify-between flex-col p-9 place-items-start w-full hidden sm:flex sm:max-w-[50px] md:max-w-[100px] lg:max-w-[200px] h-full">
				<p className="text-xl">Jelly Up!</p>
				<div className="flex flex-col gap-4">
					<div className="flex gap-5">
						<House />
						<Link href="/" className="hidden lg:flex">
							Home
						</Link>
					</div>

					<div className="flex gap-5">
						<Sparkles />
						<Link href="/generate" className="hidden lg:flex">
							Generate
						</Link>
					</div>

					<div className="flex gap-5">
						<Images />
						<Link href="/gallery" className="hidden lg:flex">
							Gallery
						</Link>
					</div>
				</div>
			</div>

			<div className="z-10 text-white p-9 place-items-center w-full flex sm:hidden h-[50px] absolute bottom-0 left-0">
				<p className="text-xl">Jelly</p>
			</div>
		</>
	);
}
