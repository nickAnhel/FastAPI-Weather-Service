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
        // .then(response => response.json())
        // .then(data => {
        //     // console.log(data);
        //     return data
        // })

    // console.log(await response.json())

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