#!/bin/sh

echo "для пользователя без персональных рекомендаций"
./test_service.py -c
status=$?
[ $status -eq 0 ] || exit $status
printf "\n"

echo "для пользователя с персональными рекомендациями, но без онлайн-истории"
./test_service.py -r
status=$?
[ $status -eq 0 ] || exit $status
printf "\n"

echo "для пользователя с персональными рекомендациями и онлайн-историей"
./test_service.py -r -t 27071448
status=$?
[ $status -eq 0 ] || exit $status
./test_service.py -r
status=$?
[ $status -eq 0 ] || exit $status
printf "\n"
