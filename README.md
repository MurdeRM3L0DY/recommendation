# recommendation

A simple movie recommendation mvp app

At the risk of stating the obvious, this is a toy, *NOT PRODUCTION READY* software

## requirements
- docker
- make

## setup
-   ```bash
    make loaddata # load the pregenerated data
    make up # start docker services
    ```

- navigate to `localhost:8000/api/docs` to try out the APIs

-   ```bash
    make down # stop docker services
    ```
