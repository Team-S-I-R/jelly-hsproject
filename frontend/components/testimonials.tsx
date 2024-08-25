import { cn } from "@/lib/utils";
import { StarFilledIcon } from "@radix-ui/react-icons";
import Link from "next/link";

export const Highlight = ({
	children,
	className,
}: {
	children: React.ReactNode;
	className?: string;
}) => {
	return (
		<span
			className={cn(
				"p-1 py-0.5 font-bold dark:text-purple-600",
				className
			)}
		>
			{children}
		</span>
	);
};

export interface TestimonialCardProps {
	name: string;
	role: string;
	description: React.ReactNode;
	className?: string;
	[key: string]: any;
}

export const TestimonialCard = ({
	description,
	name,
	role,
	className,
	 // Capture the rest of the props
	}: TestimonialCardProps) => (
		<div
			className={cn(
				"flex w-72 shrink-0 cursor-pointer snap-center snap-always flex-col justify-between rounded-xl p-4 shadow-xl shadow-black/[0.1] lg:min-w-96",
				" border border-neutral-200 bg-white/[0.8]",
				"dark:bg-transparent dark:[border:1px_solid_rgba(255,255,255,.1)] dark:[box-shadow:0_-20px_80px_-20px_#ffffff1f_inset]",
				className
			)}
		>
		<div className="select-none font-normal text-neutral-700 dark:text-neutral-400">
			{description}
		</div>

		<div className="select-none">
			<div className="flex flex-row py-1">
				<StarFilledIcon className="size-4 text-yellow-500" />
				<StarFilledIcon className="size-4 text-yellow-500" />
				<StarFilledIcon className="size-4 text-yellow-500" />
				<StarFilledIcon className="size-4 text-yellow-500" />
				<StarFilledIcon className="size-4 text-yellow-500" />
			</div>
			<p className="font-medium text-neutral-500">{name}</p>
			<p className="text-sm font-normal text-neutral-400">{role}</p>
		</div>
	</div>
);

// TODO: REPLACE WITH REAL PEOPLE DATA
const testimonials = [
	{
		name: "Alex Rivera",
		role: "CTO at InnovateTech",
		description: (
			<p>
				The AI-driven analytics from #QuantumInsights have revolutionized our
				product development cycle.
				<Highlight>
					Insights are now more accurate and faster than ever.
				</Highlight>{" "}
				A game-changer for tech companies.
			</p>
		),
	},
	{
		name: "Samantha Lee",
		role: "Marketing Director at NextGen Solutions",
		description: (
			<p>
				Implementing #AIStream&lsquo;s customer prediction model has drastically
				improved our targeting strategy.
				<Highlight>Seeing a 50% increase in conversion rates!</Highlight> Highly
				recommend their solutions.
			</p>
		),
	},
	{
		name: "Raj Patel",
		role: "Founder & CEO at StartUp Grid",
		description: (
			<p>
				As a startup, we need to move fast and stay ahead. #CodeAI&lsquo;s automated
				coding assistant helps us do just that.
				<Highlight>Our development speed has doubled.</Highlight> Essential tool
				for any startup.
			</p>
		),
	},
	{
		name: "Emily Chen",
		role: "Product Manager at Digital Wave",
		description: (
			<p>
				#VoiceGen&lsquo;s AI-driven voice synthesis has made creating global products
				a breeze.
				<Highlight>Localization is now seamless and efficient.</Highlight> A
				must-have for global product teams.
			</p>
		),
	},
	{
		name: "Michael Brown",
		role: "Data Scientist at FinTech Innovations",
		description: (
			<p>
				Leveraging #DataCrunch&lsquo;s AI for our financial models has given us an
				edge in predictive accuracy.
				<Highlight>
					Our investment strategies are now powered by real-time data analytics.
				</Highlight>{" "}
				Transformative for the finance industry.
			</p>
		),
	},
];

export function Testimonials() {
	return (
		<section className="w-full" id="testimonials">
			<div className="py-14 w-full">
				<div className="mx-auto md:container w-full ">
					<h2 className="text-center text-xl font-semibold text-white">WHAT CUSTOMERS ARE SAYING</h2>
					<h4 className="text-center text-base font-semibold text-wrap from-inherit text-white pt-5">
						Join thousands of ambitious people from all over the world making jellies with Jelly Up!
					</h4>
					<div className="flex place-content-center p-8 gap-5 w-full h-max">
						{/* <button className="w-[150px] p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg">Generate</button> */}
						
						<Link href="/gallery">
							<button className="w-[150px] hover:bg-gradient-to-r hover:from-indigo-500 hover:to-purple-400 hover:scale-105 p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg">Explore</button>
						</Link>
					</div>
					<div className="relative  mt-6 max-w-[100vw] overflow-hidden">
						<div
							className={cn(
								"flex  flex-row place-items-s place-content-start gap-6 overflow-x-auto py-14",
								"[-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
							)}
						>
							{testimonials.map((card, idx) => (
							// <div className="size-72 bg-red-500 shrink-0 md:h-60 md:min-w-96"></div>
								<TestimonialCard {...card} key={idx} />
							))}
							<div className="size-72 shrink-0 md:h-60 md:min-w-96"></div>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}
