# SAJ Inverter (Local) – Home Assistant Custom Integration  

[![HACS badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/sfazzy/SAJInverter)
![HA min version](https://img.shields.io/badge/HA%20version-2023.7%2B-blue)
![IoT class](https://img.shields.io/badge/IoT%20class-Local--Polling-brightgreen)

> **Live‑poll every SAJ solar inverter that hosts  
> `english_main.htm`, `param.js` and `real_time_data.xml`  
> on its built‑in web server (no cloud, no login).**

---

## ✨ Features

* **Automatic discovery of all metrics** – the integration reads the inverter’s
  own `param.js` to map every XML `<value>` to a friendly sensor  
  (voltage, current, grid power, today energy, inverter state, …).  
* **One‑minute polling** (configurable) – values appear as normal
  Home‑Assistant sensors you can graph, automate, or feed into the
  **Energy Dashboard** (kWh sensors are flagged `total_increasing`).
* **Zero cloud & zero credentials** – talks directly to the inverter over HTTP.
* **HACS‑ready** – easy install & updates.

---

## 📥 Installation

### Option A  – HACS (recommended)

1. **HACS → Integrations → “⋮” → Custom repositories**  
   *URL:* `https://github.com/sfazzy/SAJInverter`  
   *Category:* **Integration**  
2. Click **“Install”**.  
3. **Restart Home‑Assistant**.

### Option B  – Manual

```text
config/
└─ custom_components/
   └─ saj_inverter/
      ├─ __init__.py
      ├─ api.py
      ├─ const.py
      ├─ coordinator.py
      ├─ sensor.py
      └─ manifest.json
```
Download / clone the repo and copy the folder above.

Restart Home‑Assistant.

🔧 Configuration
Method	Steps
UI (preferred)	

1. Settings → Devices & Services → “Add Integration” → SAJ Inverter (Local).
2. Enter the inverter’s IP address (192.168.XXX.XXX in the default install) and click Submit.

YAML
(if you disabled config_flow in manifest.json)	
yaml<br>
```text
saj_inverter:
  host: 192.168.XXX.XXX # your inverter’s IP
  scan_interval: 60 # optional, seconds
```
Tip: if you don’t know the IP, check your router’s DHCP table or run a
network scan (arp -a, Fing, etc.).
<br>
<br>
🖥️ Entities created
<br>
sensor.voltage_pv1, sensor.current_pv11, sensor.grid_total_power,
sensor.energy_today, sensor.inverter_state, etc.

Exact names depend on what your param.js lists; every ID found there
(e.g. v-pv1, p-ac) becomes a sensor.
<br>
<br>

⚙️ Advanced options
scan_interval	60 s	Polling interval.
debug_logging	off	
Add to YAML if you want on:
logger: → logs: → custom_components.saj_inverter: debug
<br>
<br>
🆘 Troubleshooting
Symptom	Fix:
No entities after adding integration	Settings → System → Logs – enable debug (see above).
Check the inverter IP, that port 80 is reachable, and that param.js & real_time_data.xml load in a browser.
Log shows Length mismatch	Your inverter firmware added/removed values. Open an issue – include your param.js and real_time_data.xml.
HACS says “Repository structure for master is not compliant”	Your repo must contain custom_components/saj_inverter/manifest.json. See the Installation → Manual section for layout.
<br>
<br>
🤝 Contributing
PRs & issues welcome!

Typical contributions: 
Special‑case friendly names, units or icons for additional IDs.
Support for extra endpoints (day_trend.xml, month_trend.xml, …).
Code review & refactor (async best‑practices, config‑flow enhancements).
<br>
<br>
📜 License
Open Source - given to you by SfazzY
<br>(Original SAJ HTML/JS belongs to its respective owner; this repo merely interfaces with it.)
<br>
<br>
🙏 Acknowledgements
Inspired by the reverse‑engineering work of the Home‑Assistant community and Mucho Mas wine.
Thanks to each tester who shared inverter logs & feedback.
