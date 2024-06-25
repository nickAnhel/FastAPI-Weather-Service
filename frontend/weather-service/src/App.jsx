import './App.css'
import { Routes, Route } from 'react-router-dom'
import Header from './Components/Header/Header'
import Login from './Components/Login/Login'
import Register from './Components/Register/Register'
import Weather from './Components/Weather/Weather'


function App() {
  return (
    <>
      <Header />

      <Routes>
        <Route path="/" element={<Weather />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </>
  )
}

export default App
