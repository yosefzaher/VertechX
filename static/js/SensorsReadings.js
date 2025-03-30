document.addEventListener("DOMContentLoaded", function() {
    const ctxTemperature = document.getElementById('temperatureChart').getContext('2d');
    const ctxHumidity = document.getElementById('humidityChart').getContext('2d');
    const ctxPH1 = document.getElementById('phChart1').getContext('2d');
    const ctxPH2 = document.getElementById('phChart2').getContext('2d');

    function createChart(ctx, label, yAxisLabel, borderColor, backgroundColor) {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: label,
                    borderColor: borderColor,
                    backgroundColor: backgroundColor,
                    data: [],
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${label}: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    x: { title: { display: true, text: 'Time' } },
                    y: { title: { display: true, text: yAxisLabel } }
                }
            }
        });
    }

    const temperatureChart = createChart(ctxTemperature, 'Temperature (°C)', 'Temperature (°C)', '#ff6384', 'rgba(255, 99, 132, 0.2)');
    const humidityChart = createChart(ctxHumidity, 'Humidity (%)', 'Humidity (%)', '#36a2eb', 'rgba(54, 162, 235, 0.2)');
    const phChart1 = createChart(ctxPH1, 'pH1 Level', 'pH1 Level', '#4bc0c0', 'rgba(75, 192, 192, 0.2)');
    const phChart2 = createChart(ctxPH2, 'pH2 Level', 'pH2 Level', '#4bc0c0', 'rgba(75, 192, 192, 0.2)');

    function updateChart(chart, label, value) {
        if (typeof value !== 'number' || isNaN(value)) {
            console.warn(`Invalid value for chart update: ${value}`);
            return;
        }

        if (chart.data.labels.length >= 15) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }
        chart.data.labels.push(label);
        chart.data.datasets[0].data.push(value);
        chart.update();
    }

    let isFetching = false;

    async function fetchSensorData() {
        if (isFetching) return;
        isFetching = true;

        try {
            const response = await axios.get('http://127.0.0.1:8000/api/sensors');
            const data = response.data;

            document.getElementById('temperature').textContent = data.temperature + ' °C';
            document.getElementById('humidity').textContent = data.humidity + '%';
            document.getElementById('ph1').textContent = data.ph1;
            document.getElementById('ph2').textContent = data.ph2;

            const timeLabel = new Date().toLocaleTimeString();

            updateChart(temperatureChart, timeLabel, data.temperature);
            updateChart(humidityChart, timeLabel, data.humidity);
            updateChart(phChart1, timeLabel, data.ph1);
            updateChart(phChart2, timeLabel, data.ph2);
        } catch (error) {
            console.error('Error fetching sensor data:', error);
        } finally {
            isFetching = false;
        }
    }

    fetchSensorData();
    setInterval(fetchSensorData, 4000);
});