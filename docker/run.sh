#! /bin/bash

. ~/.py-env/bin/activate

case $TARGET in
  1.0)
    ./generate-all.sh $LANGS
    ;;
  clean)
    make clean
    ;;
  *)
    make $FORMATS
    ;;
esac
