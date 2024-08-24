'use client'

import Image from "next/image";
import { BackgroundGradientAnimation } from "../components/ui/background-gradient-animations";
import { motion } from "framer-motion";
import { Input } from "@/frontend/ui/input";
import { useFormState, useFormStatus } from 'react-dom'
import { submitFormResponse } from './actions'
import { useToast } from "@/frontend/ui/use-toast";
import Header from "./header";

export default function Home() {
  
  const { toast } = useToast()

  const SubmitButton = () => {
      
      const status = useFormStatus()

      if (status.pending !== true) {
          return (
            <>            
              <motion.button
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1.9 }}
              className='p-[3px] relative' type="submit">
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
                <div className="px-8 py-2  bg-black rounded-[6px]  relative group transition duration-200 text-white hover:bg-transparent">
                  Submit
                </div>
              </motion.button>
            </>
          )
      }

      if (status.pending === true) {
          return (
          <>
              <motion.button
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1.9 }}
              className='p-[3px] relative' type="submit">
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
                <div className="px-8 py-2  bg-black rounded-[6px]  relative group transition duration-200 text-white hover:bg-transparent">
                  Submitting...
                </div>
              </motion.button>
          </>
          )
      }

  }

  type FormState = {
      message: string;
  };

  const formAction = async (prevState: FormState, formData: FormData): Promise<FormState> => {
      await submitFormResponse(formData, formState);
      console.log('Form submitted successfully!');
      toast({ title: '✅ Thanks for your Interest!', description: 'You have been added to the waitlist.', itemID: 'success' });
      return { message: 'Submission successful!' };
  };

  const [formState, action] = useFormState(formAction, {
      message: '',
  });


  return (
    <>
      <Header />

      <main className="no-scrollbar w-screen h-screen overflow-y-scroll">
        <div className="w-full h-full flex flex-col place-items-center place-content-center">
          <BackgroundGradientAnimation className="flex flex-col place-items-center place-content-center h-full w-full">
            <div className="w-1/2 h-max z-50 inset-0 flex flex-col place-items-center place-content-center justify-center text-white font-bold px-4 pointer-events-none text-3xl text-center md:text-4xl lg:text-7xl">
              {/* Jelly + subtext */}
              <div className="w-max h-max flex flex-col gap-3">
                  <p className="bg-clip-text text-transparent drop-shadow-2xl bg-gradient-to-b from-white to-white/70">
                    Jelly
                  </p>
                  <p className="text-[15px]">
                    The fastest way to post brilliant video chats! 
                    {/* We use AI to generate stylish clips for all your socials, so you do no work. It's podcasting, reinvented. */}
                  </p>  
              </div>
            </div>
            <motion.div className="w-1/2 relative z-10 my-4  flex flex-col gap-2 place-items-center">
              <motion.form 
              initial={{opacity: 0, y: 20}}
              animate={{opacity: 1, y: 0}}
              transition={{duration: 1.7}}
              action={action} className=' w-full flex flex-col gap-2'>
                  <div className='p-[3px] relative'>
                    <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
                    <Input className="px-8 py-2 bg-black rounded-[6px] relative group transition duration-200 text-white" type='email' name='Email' autoFocus placeholder="Email" />
                  </div>
                  <div className='p-[3px] relative'>
                    <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
                    <Input className="px-8 py-2 bg-black rounded-[6px] relative group transition duration-200 text-white" type='text' name='Name' placeholder="Name" />
                  </div>
                  <SubmitButton />
              </motion.form> 
              <motion.p 
              initial={{opacity: 0}}
              animate={{opacity: 1}}
              transition={{duration: 2.4}}
              className='p-2 select-none text-[12px] text-white'>Join the wait list!</motion.p>
            </motion.div>
          </BackgroundGradientAnimation> 
          <div>
          </div>       
        </div>
      </main>
      </>
  );
}
