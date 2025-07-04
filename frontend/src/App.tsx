import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Debiaser from './pages/Debiaser';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/debiaser" element={<Debiaser />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
