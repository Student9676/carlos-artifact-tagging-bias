export default function Home() {
  return (
    <div className="bg-white">
      <div className="flex w-screen h-24 items-center pl-10 pr-10"> 
        <a className="justify-left flex space-x-8 w-max items-center" href="/"><img src="https://carlos.emory.edu/themes/custom/zurbcarlos/logo.svg" alt="Emory Michael C. Carlos Museum Logo" className="h-12" /></a>
        
        <div className="justify-right space-x-2 ml-auto w-max items-center flex text-[18px]">
          <a className="hover:bg-gray-300 p-4 rounded-md transition-colors duration-300" href="/debiaser">Debiaser</a>
          <a className="hover:bg-gray-300 p-4 rounded-md transition-colors duration-300" href="/login">Login</a>
          <a className="hover:bg-gray-300 p-4 rounded-md transition-colors duration-300" href="/signup">Signup</a>
        </div>
      </div>

      <div>
        <img src="https://www.skyweaver.net/images/media/wallpapers/wallpaper2.jpg" alt="Carlos Museum Hero Image" className="w-full h-3xs fill" />
        <div className="w-full absolute top-0 left-0 text-center mt-10">
          <h2 className="text-4xl font-bold text-red-500 text-center">
            TailwindCSS + React
          </h2>
          <button className="mt-10 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Test Button
          </button>
        </div>
      </div>
      <div className="text-center mb-10">
      </div>
      <h1 className="text-4xl font-bold text-center">Welcome to the Home Page</h1>

      <p className="text-gray-700 text-lg">This is the home page.</p>
    </div>
  );
}

