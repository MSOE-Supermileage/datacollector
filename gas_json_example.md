# gas car output example 
(over tcp/ip on adb)

# units
| key | description | data type |
| --- | ----------- | --------- |
| speed | miles per hour | double |
| oxy | air / fuel ratio, in a percentage | double
| temp | temperature, in fahrenheit | double |
| time | unix time in milliseconds since January 1st, 1970 | long |

# example
```
{
    speed: 45.0, 
    oxy: 79.0, 
    temp: 100.0, 
    time: 1453572832
}
```

