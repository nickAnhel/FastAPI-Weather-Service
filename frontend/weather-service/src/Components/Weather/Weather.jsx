import "./Weather.css"

function Weather() {
    const getWeather = () => {
        let city = document.querySelector("input").value;
        city  = city ? city : "Moscow";

        fetch(`http://localhost:8080/weather/?city=${city}`)
            .then(response => response.json())
            .then(data => {
                // console.log(data);
                // document.querySelector(".weather-data").innerHTML = JSON.stringify(data, null, 4);
                try {
                    document.querySelector(".weather-data").innerHTML =
                        `<strong>${data.city}</strong>: ${Math.round(+data.temperature.value)}°C, ${data.description}`;
                } catch (e) {
                    console.log(e);
                    document.querySelector(".weather-data").innerHTML = "City not found";
                }
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