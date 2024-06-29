import { useState } from "react"
import { useAppDispatch } from "../../store";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../../store/auth/actionCreators";
import "./Login.css"


function Login() {
    const dispatch = useAppDispatch();
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const loginUserHandler = (e) => {
        e.preventDefault();
        // console.log(username, password);
        dispatch(loginUser(username, password))
            .then(() => navigate("/"));
        // navigate("/profile")

    }

    return (
        <>
            <div className="login">
                <h1>Login</h1>

                <form onSubmit={loginUserHandler}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button type="submit">Log in</button>
                    <p style={{ "margin": 0 }}>
                        Don't have an account? <a href="/register">Sign up</a>
                    </p>
                </form>
            </div>
        </>
    )
}

export default Login