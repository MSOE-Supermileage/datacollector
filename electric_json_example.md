# electric car output example 
(over tcp/ip on adb)

# units
| key | description | data type |
| --- | ----------- | --------- |
| speed | miles per hour | double |
| joules | estimate total energy consumed in joules | double |
| time | unix time in milliseconds since January 1st, 1970 | long |

# example
```
{
    speed: 45.0, 
    joules: 190.0, 
    time: 1453572832
}
```

