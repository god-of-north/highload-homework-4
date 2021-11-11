@echo off

echo ************************************************
echo *    Testing simple page, no DB connection     *
echo ************************************************
C:\siege-windows\siege -c10  -t60s -q http://localhost:1337/
C:\siege-windows\siege -c25  -t60s -q http://localhost:1337/
C:\siege-windows\siege -c50  -t60s -q http://localhost:1337/
C:\siege-windows\siege -c100 -t60s -q http://localhost:1337/

echo ************************************************
echo *            Testing simple caching            *
echo ************************************************
C:\siege-windows\siege -c10  -t60s -q http://localhost:1337/dummy_cache
C:\siege-windows\siege -c25  -t60s -q http://localhost:1337/dummy_cache
C:\siege-windows\siege -c50  -t60s -q http://localhost:1337/dummy_cache
C:\siege-windows\siege -c100 -t60s -q http://localhost:1337/dummy_cache

echo ************************************************
echo *         Testing propabalistic cache          *
echo ************************************************
C:\siege-windows\siege -c10  -t60s -q http://localhost:1337/cache_test
C:\siege-windows\siege -c25  -t60s -q http://localhost:1337/cache_test
C:\siege-windows\siege -c50  -t60s -q http://localhost:1337/cache_test
C:\siege-windows\siege -c100 -t60s -q http://localhost:1337/cache_test

echo ************************************************
echo * Testing propabalistic cache with fail resist *
echo ************************************************
C:\siege-windows\siege -c10  -t60s -q http://localhost:1337/cache_test_retry
C:\siege-windows\siege -c25  -t60s -q http://localhost:1337/cache_test_retry
C:\siege-windows\siege -c50  -t60s -q http://localhost:1337/cache_test_retry
C:\siege-windows\siege -c100 -t60s -q http://localhost:1337/cache_test_retry

echo ************************************************
echo *          Testing DB without cache            *
echo ************************************************
C:\siege-windows\siege -c10  -t60s -q http://localhost:1337/hard_query
C:\siege-windows\siege -c25  -t60s -q http://localhost:1337/hard_query
C:\siege-windows\siege -c50  -t60s -q http://localhost:1337/hard_query
C:\siege-windows\siege -c100 -t60s -q http://localhost:1337/hard_query

echo ************************************************
echo *   Testing simple caching, no data returns    *
echo ************************************************
C:\siege-windows\siege -c10  -t60s -q http://localhost:1337/dummy_cache_nodata
C:\siege-windows\siege -c25  -t60s -q http://localhost:1337/dummy_cache_nodata
C:\siege-windows\siege -c50  -t60s -q http://localhost:1337/dummy_cache_nodata
C:\siege-windows\siege -c100 -t60s -q http://localhost:1337/dummy_cache_nodata

echo ************************************************
echo *              Testing all pages               *
echo ************************************************
C:\siege-windows\siege -c10  -t10s -q -f urls.txt
C:\siege-windows\siege -c25  -t10s -q -f urls.txt
C:\siege-windows\siege -c50  -t10s -q -f urls.txt
C:\siege-windows\siege -c100 -t10s -q -f urls.txt

rem C:\siege-windows\siege -H 'Content-Type: application/json' -c 10 -r 10 'http://localhost:1337/add_film POST {"title":"Star Wars: A New Hope","description":"Princess Leia gets abducted by the insidious Darth Vader. Luke Skywalker then teams up with a Jedi Knight, a pilot and two droids to free her and to save the galaxy from the violent Galactic Empire.","release_year":1997,"rating":"PG","language_id":1}' 
