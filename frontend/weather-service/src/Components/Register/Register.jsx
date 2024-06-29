import { useState } from "react"
import { useNavigate } from "react-router-dom";
import { useAppDispatch } from "../../store";
import { registerUser } from "../../store/auth/actionCreators";
import "./Register.css"


function Register() {
    const dispatch = useAppDispatch();
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const registerUserHandler = (e) => {
        e.preventDefault();
        dispatch(registerUser(username, email, password))
            .then(() => navigate("/"));
    }

    return (
        <>
            <div className="register">
                <h1>Sign Up</h1>

                <form onSubmit={registerUserHandler}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        required
                    />
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
                    <button type="submit">Sign Up</button>
                </form>
            </div>
        </>
    )
}

export default Register