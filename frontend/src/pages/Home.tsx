export default function Home() {
  return (
    <div className="bg-white">
      <div className="flex w-screen h-24 items-center p-8"> 
        <a className="justify-left flex space-x-8 w-max items-center" href="/"><img src="https://carlos.emory.edu/themes/custom/zurbcarlos/logo.svg" alt="Emory Michael C. Carlos Museum Logo" className="h-12" /></a>
        
        <div className="justify-right space-x-2 ml-auto w-max items-center flex text-[18px]">
          <a className=" hover:bg-gray-300 p-4 rounded-md transition-colors duration-300" href="/debiaser">Debiaser</a>
          <a className=" hover:bg-gray-300 p-4 rounded-md transition-colors duration-300" href="/login">Login</a>
          <a className=" hover:bg-gray-300 p-4 rounded-md transition-colors duration-300" href="/signup">Signup</a>
        </div>
      </div>

      <div className="w-screen h-screen flex items-center justify-center bg-black">
        <h1 className="text-white text-4xl font-bold">Welcome to the Carlos App</h1>
      </div>
      <p className="text-gray-700 text-lg">This is the home page.</p>
    </div>
  );
}