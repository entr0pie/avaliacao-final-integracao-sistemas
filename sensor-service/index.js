const express = require('express');
const redis = require('redis');
const axios = require("axios");

const URL_EVENTS_SERVICE = 'http://localhost:5000/'

const app = express();
app.use(express.json());

const client = redis.createClient({
    host: "127.0.0.1",
    port: 6379,
});

client.on("error", (err) => console.error("Redis Error:", err));

(async () => {
    await client.connect();
})();

function getSensorData() {
    return [
        { temperature: 100, pressure: 1 },
        { temperature: 25, pressure: 2 },
        { temperature: 30, pressure: 3 },
        { temperature: 50, pressure: 4 },
        { temperature: 10, pressure: 5 },
    ]
}

app.get('/sensor-data', async (req, res) => {
    const sensorDataCache = JSON.parse(await client.get('sensor-data'));
    if (sensorDataCache) return res.send(sensorDataCache);

    const sensorData = getSensorData();
    await client.set('sensor-data', JSON.stringify(sensorData));
    
    return res.send(sensorData);
});

app.post('/alert', async (req, res) => {
    const { id, description } = req.body;
    const response = (await axios.post(URL_EVENTS_SERVICE + '/events', { id, description })).data;

    return res.send(response);
});

app.listen(3000, () => console.log('http://localhost:3000/'));