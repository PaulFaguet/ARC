Process DevOps :
Si modificiation sur l'application streamlit (github) :
vérifier qu'on soit bien sur dev (git branch ou git checkout dev)
git fetch (récupérer les versions des branches en remote) ou git pull github dev
git checkout -b nom-branche (création d'une branche + se placer dessus)
faire les modifs
git add .
git commit -m "commentaire"
git push -u github branche
ensuite, créer une merge request sur gitlab
afin de mettre à jour le termina laprès la MR approuvée (donc la brance a été merge dans dev) :
git pull origin dev

Si modification sur GitLab : 
pareil sauf que github devient origin 


--> Mettre l'application sur un DNS axess genre adcom-arc.axess.fr ?