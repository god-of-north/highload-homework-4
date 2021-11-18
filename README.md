# Homework #4 for Highload:Projector

## Installation

```
git clone https://github.com/god-of-north/highload-homework-4.git
cd highload-homework-4 
docker-compose build
install_db.bat
```

## Running tests

```
docker-compose up -d
siege_test.bat
```

## Description

Project has the following endpoints:

Simple page, no DB connection
http://localhost:1337/

Simple caching
http://localhost:1337/dummy_cache

Propabalistic cache algorithm 
http://localhost:1337/cache_test

Requst to DB without caching
http://localhost:1337/hard_query

Propabalistic cache algorithm with fail resistance
http://localhost:1337/cache_test_retry

Simple caching, no data returns
http://localhost:1337/dummy_cache_nodata


## Testing results


**Concurrency 10**

```
      Endpiont     ,  Trans,  Elap Time,  Data Trans,  Resp Time,  Trans Rate,  Throughput,  Concurrent,    OKAY,   Failed
/                  ,   1171,      59.48,           0,       0.01,       19.69,        0.00,        0.10,    1171,       0
/dummy_cache       ,   1102,      59.89,         102,       0.01,       18.40,        1.70,        0.24,    1102,       0
/cache_test        ,   1176,      59.90,         108,       0.02,       19.63,        1.80,        0.32,    1176,       0
/cache_test_retry  ,   1124,      59.90,         104,       0.02,       18.76,        1.74,        0.30,    1124,       0
/hard_query        ,    967,      59.90,          89,       0.11,       16.14,        1.49,        1.85,     967,       0
/dummy_cache_nodata,   1208,      59.27,           0,       0.01,       20.38,        0.00,        0.28,    1208,       0
urls.txt           ,    128,       9.02,           7,       0.09,       14.19,        0.78,        1.32,     128,       0
```

**Concurrency 25**

```
/                  ,   2910,      59.94,           0,       0.01,       48.54,        0.00,        0.26,    2910,       0
/dummy_cache       ,   2885,      59.94,         267,       0.02,       48.14,        4.45,        0.84,    2885,       0
/cache_test        ,   2909,      59.91,         269,       0.02,       48.55,        4.49,        0.91,    2909,       0
/cache_test_retry  ,   2875,      59.93,         266,       0.02,       47.97,        4.44,        0.93,    2875,       0
/hard_query        ,   1919,      59.92,         177,       0.27,       32.02,        2.95,        8.66,    1919,       0
/dummy_cache_nodata,   2911,      59.94,           0,       0.01,       48.57,        0.00,        0.50,    2911,       0
urls.txt           ,    471,       9.90,          29,       0.08,       47.60,        2.93,        3.98,     471,       0
```

**Concurrency 50**

```
/                  ,   5772,      59.95,           0,       0.01,       96.28,        0.00,        0.61,    5772,       0
/dummy_cache       ,   5750,      59.90,         532,       0.02,       95.99,        8.88,        2.03,    5750,       0
/cache_test        ,   4686,      59.92,         434,       0.13,       78.20,        7.24,       10.18,    4686,       0
/cache_test_retry  ,   5771,      59.93,         534,       0.02,       96.30,        8.91,        2.37,    5771,       0
/hard_query        ,   2098,      59.82,         194,       0.90,       35.07,        3.24,       31.73,    2098,       0
/dummy_cache_nodata,   5828,      59.92,           0,       0.01,       97.25,        0.00,        1.06,    5830,       0
urls.txt           ,    813,       9.73,          49,       0.08,       83.54,        5.03,        6.84,     813,       0
```

**Concurrency 100**

```
/                  ,  11625,      59.94,           0,       0.01,      193.93,        0.00,        1.64,   11625,       0
/dummy_cache       ,  10859,      59.92,        1006,       0.05,      181.22,       16.79,        8.72,   10859,      12
/cache_test        ,  10569,      59.92,         979,       0.06,      176.40,       16.34,       10.91,   10569,       2
/cache_test_retry  ,  11096,      59.94,        1027,       0.03,      185.12,       17.13,        6.06,   11096,       0
/hard_query        ,   1052,      31.25,          97,       1.73,       33.66,        3.10,       58.32,    1052,    1034
/dummy_cache_nodata,  10847,      59.54,           0,       0.04,      182.18,        0.00,        6.91,   10847,      17
urls.txt           ,   1067,       9.90,          65,       0.32,      107.82,        6.57,       34.99,    1067,      49
```

**Grouped by endpoint**

```
      Endpiont     ,  Trans,  Elap Time,  Data Trans,  Resp Time,  Trans Rate,  Throughput,  Concurrent,    OKAY,   Failed
/                  ,   1171,      59.48,           0,       0.01,       19.69,        0.00,        0.10,    1171,       0
/                  ,   2910,      59.94,           0,       0.01,       48.54,        0.00,        0.26,    2910,       0
/                  ,   5772,      59.95,           0,       0.01,       96.28,        0.00,        0.61,    5772,       0
/                  ,  11625,      59.94,           0,       0.01,      193.93,        0.00,        1.64,   11625,       0

/dummy_cache       ,   1102,      59.89,         102,       0.01,       18.40,        1.70,        0.24,    1102,       0
/dummy_cache       ,   2885,      59.94,         267,       0.02,       48.14,        4.45,        0.84,    2885,       0
/dummy_cache       ,   5750,      59.90,         532,       0.02,       95.99,        8.88,        2.03,    5750,       0
/dummy_cache       ,  10859,      59.92,        1006,       0.05,      181.22,       16.79,        8.72,   10859,      12

/cache_test        ,   1176,      59.90,         108,       0.02,       19.63,        1.80,        0.32,    1176,       0
/cache_test        ,   2909,      59.91,         269,       0.02,       48.55,        4.49,        0.91,    2909,       0
/cache_test        ,   4686,      59.92,         434,       0.13,       78.20,        7.24,       10.18,    4686,       0
/cache_test        ,  10569,      59.92,         979,       0.06,      176.40,       16.34,       10.91,   10569,       2

/cache_test_retry  ,   1124,      59.90,         104,       0.02,       18.76,        1.74,        0.30,    1124,       0
/cache_test_retry  ,   2875,      59.93,         266,       0.02,       47.97,        4.44,        0.93,    2875,       0
/cache_test_retry  ,   5771,      59.93,         534,       0.02,       96.30,        8.91,        2.37,    5771,       0
/cache_test_retry  ,  11096,      59.94,        1027,       0.03,      185.12,       17.13,        6.06,   11096,       0

/hard_query        ,    967,      59.90,          89,       0.11,       16.14,        1.49,        1.85,     967,       0
/hard_query        ,   1919,      59.92,         177,       0.27,       32.02,        2.95,        8.66,    1919,       0
/hard_query        ,   2098,      59.82,         194,       0.90,       35.07,        3.24,       31.73,    2098,       0
/hard_query        ,   1052,      31.25,          97,       1.73,       33.66,        3.10,       58.32,    1052,    1034

/dummy_cache_nodata,   1208,      59.27,           0,       0.01,       20.38,        0.00,        0.28,    1208,       0
/dummy_cache_nodata,   2911,      59.94,           0,       0.01,       48.57,        0.00,        0.50,    2911,       0
/dummy_cache_nodata,   5828,      59.92,           0,       0.01,       97.25,        0.00,        1.06,    5830,       0
/dummy_cache_nodata,  10847,      59.54,           0,       0.04,      182.18,        0.00,        6.91,   10847,      17

urls.txt           ,    128,       9.02,           7,       0.09,       14.19,        0.78,        1.32,     128,       0
urls.txt           ,    471,       9.90,          29,       0.08,       47.60,        2.93,        3.98,     471,       0
urls.txt           ,    813,       9.73,          49,       0.08,       83.54,        5.03,        6.84,     813,       0
urls.txt           ,   1067,       9.90,          65,       0.32,      107.82,        6.57,       34.99,    1067,      49
```

