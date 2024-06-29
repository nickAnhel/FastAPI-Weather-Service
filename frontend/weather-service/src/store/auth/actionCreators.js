import api from "../../api";
import {
  loginStart,
  loginSucess,
  loginFailure,
  logoutSuccess,
  loadProfileStart,
  loadProfileSucess,
  loadProfileFailure,
} from "./authReducer";


export const registerUser =
  (username, email, password) =>
    async (dispatch) => {
      try {
        const res = await api.auth.register(username, email, password)
        dispatch(loginUser(username, password));
      } catch (e) {
        console.error(e)
      }
    }


export const loginUser =
  (username, password) =>
    async (dispatch) => {
      try {
        dispatch(loginStart())

        const res = await api.auth.login(username, password)

        dispatch(loginSucess(res.access_token))
        dispatch(getProfile(res.access_token))

        

      } catch (e) {
        console.error(e)

        dispatch(loginFailure(e.message))
      }
    }

export const getProfile = (accessToken) =>
  async (dispatch) => {
    try {
      dispatch(loadProfileStart())

      const res = await api.auth.getProfile(accessToken)

      dispatch(loadProfileSucess(res))

    } catch (e) {
      console.error(e)

      dispatch(loadProfileFailure(e.message))
    }
  }


export const logoutUser = () => (dispatch) => {
  try {
    dispatch(logoutSuccess());

  } catch (e) {
    console.error(e)
  }
}