import './Header.css'


function Header() {
    return (
        <>
            <div className="header">
                <div className='logo'><a href="/">Weather Service</a></div>
                <div className='navbar'>
                    <a href="/login">Login</a>
                </div>
            </div>
        </>
    )
}

export default Header