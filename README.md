# <h1>network programming ZMQ opdracht</h1>
<h2>requirements</h2>
<p>
  <ul>
    <li>python 3.X</li>
    <li>zmq library</li>
  </ul> 
</p>

<h2>how to use?</h2>
<p>you will be asked 3 questions:
  <ul>
  <li>youre name and the location (spacebar delimited)</li>
  <li>the information you want to know (weather description and temperature are always included so you dont need to ask for it) <b>also space delimited</b></li>
  <li>in what units do you want youre forecast metric, scientific or imperial</li>
</ul> 
  after hitting enter the server will return either an error or the requested information
</p>

<h2>the commands</h2>
<p><h3>the possible info you can request for:</h3>
<ul>
  <li>observation_time</li>
  <li>weather_code</li>
  <li>wind_speed</li>
  <li>wind_degree</li>
  <li>wind_dir</li>
  <li>pressure</li>
  <li>precip</li>
  <li>humidity</li>
  <li>cloudcover</li>
  <li>youre name and the location (spacebar delimited)</li>
  <li>feelslike</li>
  <li>uv_index</li>
  <li>visibility</li>
  <li>is_day</li>
</ul>
<h3>the unit</h3>
<ul>
  <li>m for metric (°C)</li>
  <li>f for imperial (°F)</li>
  <li>s for scientific (kelvin)</li>
</ul>
</p>
<h2>example</h2>
<p> example of a succes and a failure</p>
<img src="https://github.com/hamza-outa/NP_ZMQ/blob/main/example.PNG?raw=true">
