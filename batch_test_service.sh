#!/bin/sh

echo "для пользователя без персональных рекомендаций"
./test_service.py -c
printf "\n"

echo "для пользователя с персональными рекомендациями, но без онлайн-истории"
./test_service.py -r
printf "\n"

echo "для пользователя с персональными рекомендациями и онлайн-историей"
./test_service.py -r -t 27071448
./test_service.py -r
printf "\n"
