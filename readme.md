git fetch (récupérer les versions des branches en remote)
git branch (toujours être sur dev)
git checkout -b nom-branche (création d'une branche + se placer dessus)
faire les modifs
git add .
git commit -m "commentaire"
git push -u origin nom-branche
ensuite, créer une merge request sur gitlab
afin de mettre à jour le termina laprès la MR approuvée (donc la brance a été merge dans dev) :
git pull origin dev