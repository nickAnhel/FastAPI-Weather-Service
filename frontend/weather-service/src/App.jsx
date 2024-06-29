import './App.css'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'

import Header from './Components/Header/Header'
import Login from './Components/Login/Login'
import Register from './Components/Register/Register'
import Weather from './Components/Weather/Weather'
import Profile from './Components/Profile/Profile'


function App() {
  const isLoggedIn = useSelector(
    (state) => !!state.auth.authData.accessToken
  )

  return (
    <>
      <Header />

      <Routes>
        <Route path="/" element={<Weather />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/profile"
          element={isLoggedIn ? <Profile /> : <Navigate to="/login" />} />
      </Routes>
    </>
  )
}

export default App
