## README
It can be execute in two different ways (with and without):

Run a `docker-compose` via `docker compose up --build`

Also, you can run with the default file database (`sqlite`) and execute every service:

```
python -m venv venv && source venv/bin/activate
pip install -r labhouse/requeriments.txt
```

Run database migrations:

```
python manage.py makemigrations
python manage.py migrate --settings=labhouse.settings
 ```


In `/labhouse` folder:
 - `celery -A labhouse worker -l INFO`
 - `docker run -d -p 6379:6379 redis`
 - webservice via : `python manager.py server`


This second method is the best one for test purposes

## Deliverables
- Download the offline model with `python download_model.py` (modify the flag with_float if you uses gpu config to enable floats)
- For checking the ML, go to the `infra` folder.
- For checking the results: `http://localhost` or `http://0.0.0.0:8000`

The webservice and its REST API is implemented in the `app_labhouse` folder.

for running tests

```
source venv/bin/activate
python manager test core/
python manager test
```

## Design

- It applies a clean architecture where it is splitted the domain entities from a specific framework. For this
reason the core module has  `usecases` that it includes the main pipelines. In our case, we only have one use case
(very easy) then it is one function. This structure permits to be flexible and isolate responsabilites, it is open for improvements
- In the `core` project we have `Adapters` is typical pattern for clean architecture to keep uncoupled the domain entities
 and infrastructure modules.
- To apply the celery queue, It is necessary share volumes to save temporal files. The other option should be the serialization of data
and send in batches, but it seemed more complicated and more memory consuming.
- Tests for django modules were discarded... It makes sense because most of the code is the application of django patterns, that they are well
tested, apply tests in these patterns are out of context.. This idea is subjective, but for PoC can be enough
- It was introduced some first steps in good practices like `logging` that it permits to add more logs or `gitactions `that it provides the
first CIs configuration.
- The docker compose config is near a real product, it uses `gunicorn` and a `nginx` that it permits to keep being stateless and scalable
- To keep being near a real product, I added a postgres db for docker-compose deployment.
- To apply environment variable for the docker configuration, it open the door for different environment like production, testing, etc...
- Related with ML, it is applied two different approaches, one with APIS, the other one with our model (a petrained one). I did this because
in a real case you want to apply external libraries for a fast iteration but start implementing your model for future iterations. In fact,
the idea is to reuse this model with some finetuning techniques, all includes some framework lie `Airflow` or `Kubeflow` , to apply refinements. In this
case, it was not done, it seemed out of the problem scope... All these things would mean, crawling, scraping, cleaning data, redesign the NN...
- Both models are using Stable Diffusion XL
- The API is from `stability.AI` that it consumes credits (I charged 10 euros)... Please take care about this. I harcoded the value in the `settings` file
for easier the testing. Also it can be passed as another with the compose file.
- In the last moment, with a lack of ideas... I added a pix2pix network to add nicolas cage faces in the photos
