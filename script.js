// Initialize Leaflet map (Insert this part here)
const map = L.map('map').setView([20, 77], 5); // Center of India

// Load and display tile layers (Insert this part here)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Function to fetch and display weather
async function getWeather() {
    const city = document.getElementById('city-input').value.trim();
    
    if (city === '') {
        alert('Please enter a city');
        return;
    }

    const WEATHER_API_KEY = 'adbbf33300084696a36f6f151a2efe5b'; // Use your valid key
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${WEATHER_API_KEY}&units=metric`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.cod === 200) {
            let weatherEmoji = '';
            const weatherDescription = data.weather[0].description.toLowerCase();

            if (weatherDescription.includes('cloud')) {
                weatherEmoji = '☁️';
            } else if (weatherDescription.includes('clear')) {
                weatherEmoji = '☀️';
            } else if (weatherDescription.includes('rain')) {
                weatherEmoji = '🌧️';
            } else if (weatherDescription.includes('snow')) {
                weatherEmoji = '❄️';
            } else if (weatherDescription.includes('thunderstorm')) {
                weatherEmoji = '⛈️';
            } else {
                weatherEmoji = '🌈';
            }

            const weatherResultDiv = document.getElementById('weather-result');
            weatherResultDiv.innerHTML = `
                <p>Weather in ${data.name}, ${data.sys.country}: ${weatherEmoji}</p>
                <p>Temperature: ${data.main.temp} °C 🌡️</p>
                <p>Weather: ${data.weather[0].description}</p>
                <p>Humidity: ${data.main.humidity}% 💧</p>
            `;
        } else {
            alert('City not found. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching weather data:', error);
        alert('Failed to fetch weather data.');
    }
}

// Function to get coordinates from location (same as before)
async function getCoordinates(location) {
    const url = `https://api.opencagedata.com/geocode/v1/json?q=${encodeURIComponent(location)}&key=YOUR_API_KEY`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.results.length > 0) {
            const latitude = data.results[0].geometry.lat;
            const longitude = data.results[0].geometry.lng;
            console.log('Coordinates:', latitude, longitude);
            return { latitude, longitude };
        } else {
            throw new Error('Location not found');
        }
    } catch (error) {
        console.error('Error fetching coordinates:', error);
        return null;
    }
}

// Earthquake, Flood, Tsunami, Tornado Prediction Functions
// These functions can be defined here, as per your earlier code.

document.getElementById('get-weather-btn').addEventListener('click', function() {
    const city = document.getElementById('city-input').value.trim();
    if (city === '') {
        alert('Please enter a city name.');
        return;
    }
    getWeather();
});
