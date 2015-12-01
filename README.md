Programmatic access to the NHTSA New Car Assessment Program (NCAP) - http://www.nhtsa.gov/webapi/Default.aspx?SafetyRatings/API/5.

`nhtsa.py` will download vehicle data for all vehicles available through the NCAP API into the file `vehicles.json`.

Interruptions (e.g. `CTRL-C`) are handled by caching API results in a file and using cached results when resumed.

### Instructions
```
> pip install requests
> python nhtsa.py
```

Then wait...

### Known Bugs
Some Models are invalid to use in a URL and no advice is given on how to correctly format the request, e.g. the Volvo "XC90 (T5/T6)". This results in a 404 errors and some missing data.