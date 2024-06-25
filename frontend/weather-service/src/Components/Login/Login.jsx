import { useState } from "react"
import "./Login.css"

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const loginUser = (e) => {
        e.preventDefault();
        // console.log(username, password);

    }

    return (
        <>
            <div className="login">
                <h1>Login</h1>

                <form onSubmit={loginUser}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        required
                    />
                    <button type="submit">Log in</button>
                    <p style={{"margin": 0}}>
                        Don't have an account? <a href="/register">Sign up</a>
                    </p>
                </form>
            </div>
        </>
    )
}

export default Login