#Step Before Installation
Please add api key into the function getSearchResult and getOntologyBuildURL in searcher.py from backend code

# Installation Step
1. Docker is needed to be installed: https://docs.docker.com/get-docker/
1.2 (For Linux system user) Docker Compose is also needed to be installed: https://docs.docker.com/compose/install/
2. Open CLI console and navigate to these project:
```
cd <path to this project>
```
3. Navigate into the fyp project (where a “docker-compose.yml” file is found):
```
cd ./fyp
```
4. Enter the follow command (if do not work, please follow instruction at step 4: https://docs.docker.com/compose/gettingstarted/):
```
docker compose up -d
```
5. Go to http://localhost:3000/ or http://127.0.0.1:3000/ in web browser to use the app

6. Type the following to shutdown system:
```
docker compose down
```

#Instruction
1. To search keyword, just type it in the search bar and click on the search icon
2. List of sub-domain specific knowledge of keyword searched would be return
3. User choose the sub-domain specific knowledge they want to search and click search
4. Search Result return to user after a long searching time
5. User may click on "Search More" button at each sub-domain specific knowledge search result to search for that keyword

#Ontology
- User may edit the ontology tree at: <path to this project>/fyp/BackEnd/src/ontology/allConcept.owl
- While editing ontology tree, user may have reference to json file which saved statistic information of each newly added keyword at: <path to this project>/fyp/BackEnd/src/ontology/ref/