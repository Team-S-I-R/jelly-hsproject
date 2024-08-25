"use client";

import React from "react";
import { BackgroundGradientAnimation } from "../components/ui/background-gradient-animations";
import { motion } from "framer-motion";
import { Input } from "@/components/ui/input";
import { useFormState, useFormStatus } from "react-dom";
import { submitFormResponse } from "./actions";
import { useToast } from "@/components/ui/use-toast";
import { ConfettiButton } from "@/components/magicui/confetti";
import { Testimonials } from "@/components/testimonials";
import { WobbleCardGrid } from "@/components/wobble-grid";
import Header from "./header";

export default function Home() {
	const { toast } = useToast();

	type FormState = {
		message: string;
	};

	const formAction = async (
		prevState: FormState,
		formData: FormData
	): Promise<FormState> => {
		await submitFormResponse(formData, formState)
			.then(() => {
				toast({
					title: "✅ Thanks for your Interest!",
					description: "You have been successfully added to the wait-list.",
					itemID: "success",
				});
			})
			.catch((error) => {
				toast({
					title: "❌ Error",
					description: `An unexpected error has occurred: ${error}`,
					itemID: "error",
				});
			});
		return { message: "Submission successful!" };
	};

	const [formState, action] = useFormState(formAction, {
		message: "",
	});

	return (
		<>
			<Header />
			<main className="no-scrollbar bg-transparent w-screen h-screen overflow-y-scroll">
				<div className="absolute z-[-1] w-full h-full">
					<BackgroundGradientAnimation className="w-full h-full"/>
				</div>
				<div className="w-full h-[20%]"></div>
				<div className="flex flex-col w-full  gap-4 h-max">
					

					<div className="w-full h-max flex flex-col place-items-center place-content-center">
						{/* Jelly Title */}
						<div className="w-1/2 h-max z-50 inset-0 flex flex-col place-items-center place-content-center justify-center text-white font-bold px-4 pointer-events-none text-3xl text-center md:text-4xl lg:text-7xl">
							<div className="w-max h-max flex flex-col gap-3">
								<p className="bg-clip-text text-transparent drop-shadow-2xl bg-gradient-to-b from-white to-white/70 p-2 select-none">
									Jelly Up!
								</p>
								<p className="text-[15px] select-none">
									The Fastest Way to Post Brilliant Video Chats.
								</p>
							</div>
						</div>	
					</div>

					{/* Testimonials */}
					<motion.div className="w-full relative z-10 my-4 h-max">
						<motion.div
							initial={{ opacity: 0, y: 20 }}
							animate={{ opacity: 1, y: 0 }}
							transition={{ duration: 1.7 }}
							className="w-full"
						>
							<Testimonials />
						</motion.div>
					</motion.div>

					<div className="w-full h-[80%] px-8 flex flex-col place-items-center place-content-center">
						
						{/* WobbleCardGrid */}
						<motion.div className="w-full my-4 flex flex-col gap-2 place-items-center">
							<motion.div
								initial={{ opacity: 0, y: 20 }}
								animate={{ opacity: 1, y: 0 }}
								transition={{ duration: 1.7 }}
							>
								<WobbleCardGrid/>
							</motion.div>
						</motion.div>

					</div>


					{/* JellyUp WaitList Form */}
					{/* <motion.div className="w-1/2 relative z-10 my-4  flex flex-col gap-2 place-items-center">
							<motion.form
								initial={{ opacity: 0, y: 20 }}
								animate={{ opacity: 1, y: 0 }}
								transition={{ duration: 1.7 }}
								action={action}
								className=" w-full flex flex-col gap-2"
							>
								<div className="p-[3px] relative">
									<div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
									<Input
										className="px-8 py-2 bg-black rounded-[6px] relative group transition duration-200 text-white"
										type="email"
										name="Email"
										autoFocus
										placeholder="Email"
									/>
								</div>
								<div className="p-[3px] relative">
									<div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
									<Input
										className="px-8 py-2 bg-black rounded-[6px] relative group transition duration-200 text-white"
										type="text"
										name="Name"
										placeholder="Name"
									/>
								</div>
								<ConfettiButton>Submit 🎉</ConfettiButton>
							</motion.form>
							<motion.p
								initial={{ opacity: 0 }}
								animate={{ opacity: 1 }}
								transition={{ duration: 2.4 }}
								className="p-2 select-none text-[12px] text-white"
							>
								Join the Waitlist!
							</motion.p>
					</motion.div> */}

				</div>
			</main>
		</>
	);
}
