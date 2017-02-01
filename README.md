Programmatic access to the NHTSA New Car Assessment Program (NCAP) - http://www.nhtsa.gov/webapi/Default.aspx?SafetyRatings/API/5.

Interruptions (e.g. `CTRL-C`) are handled by caching API results in a file and using cached results when resumed.

### Instructions
```
> pip install requests
> python safety_ratings.py
# results in safety_ratings.json
> python vpic.py
# results in vpic_models.json
```

Then wait...

### Known Bugs
Some Models are invalid to use in a URL and no advice is given on how to correctly format the request, e.g. the Volvo "XC90 (T5/T6)". This results in a 404 errors and some missing data.