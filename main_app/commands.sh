# build
#flet build web

# moves build files out of repo
rm -rf ../../b
mv build ../../b

# commit branch main
ga -u
gc -m "updates"

# checkout branch gh-pages-2
git checkout gh-pages-2

# copy build files
cd ..
rm -rf *
cp -R ../b/web/* .

# remove line from index.html
head -n 14 index.html > tmp.html
tail -n+16 index.html >> tmp.html
mv -f tmp.html index.html

# commit and push gh-pages-2
ga -u
gc -m "updates"
git push

# return to main
git checkout main
cd main_app
