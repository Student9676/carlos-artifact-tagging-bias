import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Debiaser from './pages/Debiaser';
import Results from './pages/Results';
import Login from './pages/Login';
import Signup from './pages/Signup';

import './index.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/debiaser" element={<Debiaser />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
