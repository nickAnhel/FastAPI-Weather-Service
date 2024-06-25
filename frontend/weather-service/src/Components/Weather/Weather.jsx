import "./Weather.css"

function Weather() {
    const getWeather = () => {
        const city = document.querySelector("input").value;
        fetch(`http://localhost:8080/weather?city=${city}`)
            .then(response => response.json())
            .then(data => {
                // console.log(data);
                document.querySelector(".weather-data").innerHTML = JSON.stringify(data, null, 4);
            })
    }


    return (
        <>
            <div className="weather">
                <input type="text" placeholder="City" />
                <button onClick={getWeather}>Get Weather</button>
            </div>
            <div className="weather-data"></div>
        </>
    )
}

export default Weather