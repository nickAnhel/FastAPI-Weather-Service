import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import './Header.css'


function Header() {
    const isLoggedIn = useSelector(
        (state) => !!state.auth.authData.accessToken
    )

    return (
        <>
            <div className="header">
                <div className='logo'><Link to="/">Weather Service</Link></div>
                <div className='navbar'>
                    {isLoggedIn ? <Link to="/profile">Profile</Link> : <Link to="/login">Login</Link>}

                </div>
            </div>
        </>
    )
}

export default Header