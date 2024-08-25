"use client";
import Image from "next/image";
import React from "react";
import { WobbleCard } from "@/components/wobble-card";


export function WobbleCardGrid() {
	return (
		<div className="grid grid-cols-1 lg:grid-cols-3 gap-4 max-w-7xl mx-auto w-full">
			<WobbleCard
				containerClassName="col-span-1 lg:col-span-2 h-full bg-purple-900 min-h-[500px] lg:min-h-[300px]"
				className="h-full"
			>
				<div className="max-w-xs">
					<h2 className="text-left text-balance text-base md:text-xl lg:text-3xl font-semibold tracking-[-0.015em] text-white">
						Transcribing captions has never been easier
					</h2>
					<p className="mt-4 text-left text-base/6 text-neutral-200">
                        Our essential transcribing tool allows you to add captions 
                        to your videos with ease. Why spend hours transcribing when
                        you can do it in seconds? 😌
					</p>
				</div>
			</WobbleCard>
			<WobbleCard containerClassName="col-span-1 min-h-[300px]">
				<h2 className="max-w-80 text-left text-balance text-base md:text-xl lg:text-3xl font-semibold tracking-[-0.015em] text-white">
                    Gallery of our latest work
				</h2>
				<p className="mt-4 max-w-[26rem] text-left text-base/6 text-neutral-200">
️                   Check out our latest work through a gallery of transcribed videos.
				</p>
			</WobbleCard>
			<WobbleCard containerClassName="col-span-1 lg:col-span-3 ... min-h-[500px] lg:min-h-[600px] xl:min-h-[300px]">
				<div className="max-w-sm">
					<h2 className="max-w-sm md:max-w-lg text-left text-balance text-base md:text-xl lg:text-3xl font-semibold tracking-[-0.015em] text-white">
						We make it look easy, when it&lsquo;s not
					</h2>
					<p className="mt-4 max-w-[26rem] text-left text-base/6 text-neutral-200">
						Our product is so easy to use, you&lsquo;ll wonder how you ever lived without using it.
					</p>
				</div>
			</WobbleCard>
            <WobbleCard containerClassName="col-span-1 lg:col-span-2 bg-blue-900 min-h-[500px] lg:min-h-[600px] xl:min-h-[300px]">
				<div className="max-w-sm">
					<h2 className="max-w-sm md:max-w-lg  text-left text-balance text-base md:text-xl lg:text-3xl font-semibold tracking-[-0.015em] text-white">
						Signup for blazing-fast cutting-edge state of the art Gippity AI
						wrapper today!
					</h2>
					<p className="mt-4 max-w-[26rem] text-left  text-base/6 text-neutral-200">
						With over 100,000 mothly active bot users, Gippity AI is the most
						popular AI platform for developers.
					</p>
				</div>
			</WobbleCard>
		</div>
	);
}
