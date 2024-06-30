import Endpoints from "../endpoints";


export const register = async (username, email, password) => {
    const response = await fetch(Endpoints.BASE + Endpoints.AUTH.REGISTER, {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "username": username,
            "email": email,
            "password": password,
        }),
    })
    return await response.json()
}

export const login = async (username, password) => {
    const response = await fetch(Endpoints.BASE + Endpoints.AUTH.LOGIN, {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${username}&password=${password}`,
    })

    return await response.json()
}

export const getProfile = async (accessToken) => {
    const response = await fetch(Endpoints.BASE + Endpoints.AUTH.PROFILE, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${accessToken}`,
        },
    })
    return await response.json()
}


export const refreshToken = async (refreshToken) => {
    const response = await fetch(Endpoints.BASE + Endpoints.AUTH.REFRESH, {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${refreshToken}`,
        },
    })
    return await response.json()
}