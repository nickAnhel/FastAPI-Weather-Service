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
import { store } from ".."
import { isTokenExpired } from "../../utils/jwt";


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

        dispatch(loginSucess({
          accessToken: res.access_token,
          refreshToken: res.refresh_token,
        }))

        dispatch(getProfile())

      } catch (e) {
        console.error(e)

        dispatch(loginFailure(e.message))
      }
    }

export const getProfile = () =>
  async (dispatch) => {
    try {
      dispatch(loadProfileStart())

      const accessToken = await dispatch(getAccessToken())
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


let refreshTokenRequest = null

export const getAccessToken =
  () =>
    async (dispatch) => {
      try {
        const accessToken = store.getState().auth.authData.accessToken
        const refreshToken = store.getState().auth.authData.refreshToken

        if (!accessToken || isTokenExpired(accessToken)) {
          if (refreshTokenRequest === null) {
            refreshTokenRequest = api.auth.refreshToken(refreshToken)
          }

          const res = await refreshTokenRequest
          refreshTokenRequest = null

          dispatch(loginSucess({
            accessToken: res.access_token,
            refreshToken: refreshToken,
          }))

          return res.access_token
        }

        return accessToken
      } catch (e) {
        console.error(e)
        return null;
      }
    }