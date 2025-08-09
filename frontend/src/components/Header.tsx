export default function Header() {
  return (
    <div className="flex w-full h-24 items-center px-10 mt-4"> 
      <div className="flex w-full items-center bg-white bg-opacity-10 backdrop-blur-md rounded-full p-4 shadow-lg border border-white border-opacity-20 px-10">
        <a className="justify-left flex space-x-8 w-max items-center" href="/"><img src="/src/assets/carlos-logo-white.png" alt="Emory Michael C. Carlos Museum Logo" className="h-12" /></a>
        
        <div className="justify-right ml-auto w-max items-center flex text-[18px] text-white space-x-6">
          <a className="relative rounded-md transition-all duration-300 hover:after:w-full after:content-[''] after:absolute after:bottom-0 after:left-0 after:h-0.5 after:w-0 after:bg-white after:transition-all after:duration-300" href="/debiaser">Debiaser</a>
          <a className="relative rounded-md transition-all duration-300 hover:after:w-full after:content-[''] after:absolute after:bottom-0 after:left-0 after:h-0.5 after:w-0 after:bg-white after:transition-all after:duration-300" href="/login">Login</a>
          <a className="relative rounded-md transition-all duration-300 hover:after:w-full after:content-[''] after:absolute after:bottom-0 after:left-0 after:h-0.5 after:w-0 after:bg-white after:transition-all after:duration-300" href="/signup">Signup</a>
        </div>
      </div>
    </div>
  );
}
