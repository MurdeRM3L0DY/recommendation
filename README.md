# recommendation

A simple movie recommendation mvp app

At the risk of stating the obvious, this is a toy, *NOT PRODUCTION READY* software

## requirements
- docker
- make

## setup
- start docker services:
```bash
make up
 ```
- in another terminal:
```bash
make migrate # initialize database
make loaddata # load the pregenerated data
```
- navigate to `localhost:8000/api/docs` to try out the APIs

- stop docker services
```bash
make down
```
