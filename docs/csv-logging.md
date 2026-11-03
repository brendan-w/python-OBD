# Example: log RPM and speed to CSV

This example queries engine RPM and vehicle speed once per second and appends each reading to a CSV file for later review in a spreadsheet. It uses only the public API from the README: `obd.OBD()`, `obd.commands.RPM`, `obd.commands.SPEED`, `connection.query()`, and the Pint unit values on `response.value`.

```python
import csv
import time
import obd

connection = obd.OBD()

if not connection.is_connected():
    raise SystemExit("Could not connect to the vehicle. Check the adapter and try again.")

with open("drive_log.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["timestamp", "rpm", "speed_kph"])
    for _ in range(60):
        rpm = connection.query(obd.commands.RPM)
        speed = connection.query(obd.commands.SPEED)
        if rpm.is_null() or speed.is_null():
            time.sleep(1)
            continue
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), round(rpm.value.magnitude), round(speed.value.to("kph").magnitude, 1)])
        time.sleep(1)
```

## Notes

- Support varies by car. Before relying on a command, check it first with `connection.has_command(cmd)`.
- `response.value` carries Pint units, so `.to("kph")` or `.to("mph")` converts cleanly.
- Run this only while stationary or with a passenger operating the laptop, never while driving.
