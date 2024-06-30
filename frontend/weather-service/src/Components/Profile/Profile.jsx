import { useSelector } from 'react-redux'
import { useAppDispatch } from "../../store";
import { logoutUser, getProfile } from '../../store/auth/actionCreators'
import "./Profile.css"


function Profile() {
    const dispatch = useAppDispatch();

    const profileData = useSelector(
        (state) => state.auth.profileData.profile
    )

    const logoutUserHandler = () => {
        dispatch(logoutUser());
    }

    return (
        <>
            <div className="profile">
                <h1>Profile</h1>
                <table>
                    <tbody>
                        <tr>
                            <td>Username</td>
                            <td>{profileData.username}</td>
                        </tr>
                        <tr>
                            <td>Email</td>
                            <td>{profileData.email}</td>
                        </tr>
                    </tbody>
                </table>
                <button onClick={logoutUserHandler}>Logout</button>
                {/* <button onClick={() => dispatch(getProfile())}>Update profile</button> */}
            </div>
        </>
    )
}

export default Profile