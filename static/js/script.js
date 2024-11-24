fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        const geolocation = data.data;

        // Populate location data
        document.getElementById('city').textContent = geolocation.City || 'N/A';
        document.getElementById('region').textContent = geolocation.Region || 'N/A';
        document.getElementById('country').textContent = geolocation.Country || 'N/A';
        document.getElementById('local-time').textContent = geolocation.LocalTime || 'N/A';

        // Populate coordinates
        document.getElementById('latitude').textContent = geolocation.Latitude || 'N/A';
        document.getElementById('longitude').textContent = geolocation.Longitude || 'N/A';

        // Populate weather data
        const weather = geolocation.Weather || {};
        document.getElementById('temperature').textContent = `${weather.Temperature || 'N/A'} °C`;
        document.getElementById('weather').textContent = weather.Weather || 'N/A';
        document.getElementById('humidity').textContent = `${weather.Humidity || 'N/A'}%`;
        document.getElementById('wind').textContent = `${weather["Wind Speed"] || 'N/A'} m/s`;
        document.getElementById('sunrise').textContent = weather.Sunrise || 'N/A';
        document.getElementById('sunset').textContent = weather.Sunset || 'N/A';

        // Populate pollution data
        const aqi = geolocation.Pollution?.AQI || 'N/A';
        document.getElementById('aqi').textContent = `${aqi} (1=Good, 5=Hazardous)`;
        const pollutants = geolocation.Pollution?.Pollutants || {};
        const pollutantsList = Object.entries(pollutants)
            .map(([key, value]) => `<li>${key}: ${value}</li>`)
            .join('');
        document.getElementById('pollutants').innerHTML = `<ul>${pollutantsList}</ul>`;

        // Render AQI chart
        if (aqi !== 'N/A') {
            const ctx = document.getElementById('aqiChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Good', 'Moderate', 'Unhealthy for Sensitive', 'Unhealthy', 'Very Unhealthy', 'Hazardous'],
                    datasets: [{
                        label: 'AQI Level',
                        data: [
                            aqi == 1 ? 1 : 0,
                            aqi == 2 ? 1 : 0,
                            aqi == 3 ? 1 : 0,
                            aqi == 4 ? 1 : 0,
                            aqi == 5 ? 1 : 0,
                        ],
                        backgroundColor: ['#00e400', '#ffff00', '#ff7e00', '#ff0000', '#8f3f97', '#7e0023'],
                        hoverOffset: 10,
                    }]
                },
                options: {
                    plugins: {
                        legend: { position: 'bottom' }
                    },
                    animation: {
                        animateScale: true,
                        animateRotate: true
                    },
                    responsive: true
                }
            });
        }

        // Populate forecast table
        const forecastData = geolocation.Forecast || [];
        const forecastTableBody = document.querySelector('#forecast tbody');
        forecastData.forEach(item => {
            const row = forecastTableBody.insertRow();
            row.innerHTML = `<td>${item.DateTime}</td><td>${item.Temperature} °C</td><td>${item.Weather}</td>`;
        });
        
        // Display weather news
        const newsContainer = document.getElementById('news-container');
        const newsArticles = geolocation.News || [];
        if (newsArticles.length > 0 && !newsArticles[0].Error) {
            newsContainer.innerHTML = newsArticles
                .map(article => `
                    <div class="news-card">
                        <a href="${article.url}" class="news-title" target="_blank">${article.title}</a>
                        <div class="news-source">Source: ${article.source}</div>
                        <a href="${article.url}" class="read-more" target="_blank">Read More</a>
                    </div>
                `)
                .join('');
        } else {
            newsContainer.innerHTML = `<p>No news available at the moment.</p>`;
        }
        
        // Display recommendations
        const recommendationsList = document.getElementById('recommendations-list');
        const recommendations = geolocation.Recommendations || [];
        if (recommendations.length > 0) {
            recommendationsList.innerHTML = recommendations
                .map(rec => `<li>${rec}</li>`)
                .join('');
        } else {
            recommendationsList.innerHTML = `<li>No specific recommendations at the moment. Enjoy your day!</li>`;
        }
    })
    .catch(error => console.error('Error fetching data:', error));
